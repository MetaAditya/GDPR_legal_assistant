from langchain.tools import tool
from langchain.agents import create_agent
from openai import OpenAI
from llm_module.utils.legal_utils import Legal_Assistant_respond
import re, json
from settings import env_settings
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import (
    PIIMiddleware,
    HumanInTheLoopMiddleware,
    SummarizationMiddleware,
    ModelCallLimitMiddleware,
    ModelRetryMiddleware,
)
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from guardrails.guardrails import (
    ProfanityMiddleware,
    PromptInjectionMiddleware,
    JailbreakMiddleware,
)
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from typing import AsyncGenerator
import asyncio
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from typing import *
from llm_module.utils.user_document_chat import (
    user_compliance_verifier,
    risk_analyzer,
    retrieve_top_chunks,
    download_tool,
)
from dataclasses import dataclass
import traceback
import time
from pathlib import Path
import uuid
from langchain_core.runnables import RunnableConfig
import logging

import os



from concurrent.futures import ThreadPoolExecutor, TimeoutError


#############################

api_key = env_settings.API_KEY.get_secret_value()

guardrail_llm = ChatOpenAI(
    model=env_settings.model,
    api_key=api_key,
).with_config({"run_name": "guardrail_llm"})


llm = ChatOpenAI(
    model=env_settings.model,
    api_key=api_key,
    streaming=True,
).with_config({"run_name": "main_llm"})


@dataclass
class UserContext:
    user_id: str


phone_pattern = re.compile(r"\b\d{10}\b")


def phone_detector(text: str):
    return list(phone_pattern.finditer(text))


def your_read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    print(f"Reading email with ID: {email_id}")
    return f"Email content for ID: {email_id}"


def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    print(f"Sending email to {recipient} with subject '{subject}' and body '{body}'")
    return f"Email sent to {recipient} with subject '{subject}'"


############################


# 1. Make the core execution logic an async function
async def _execute_web_search_logic(query: str, question_id: str) -> str:
    """Internal async function that handles the heavy lifting."""
    
    
    client = OpenAI(api_key=api_key)
    print("*********** WEB SEARCH TRIGGERED******************")
    
    response = client.responses.create(
        model="gpt-5", tools=[{"type": "web_search"}], input=query
    )

    extracted_text = (
        response.output_text if hasattr(response, "output_text") else str(response)
    )
    timestamp = int(asyncio.get_event_loop().time())

    tool_content=response.model_dump() if hasattr(response, "model_dump") else str(response)

    response_data = {
        "tool":"web_search",
        "tool_query": query,
        "tool_content": tool_content.splitlines(),
        "timestamp": timestamp,
        "question_id": question_id,
    }

    file_path = Path("/app/responses") / f"{timestamp}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)

    return extracted_text


# 2. Make the main LangChain tool async using the async definition
@tool(
    "web_search",
    description="""    
        Search the live web for current GDPR and data-protection information.
        Use when the user asks about recent GDPR developments, EDPB guidance,
        regulatory enforcement, fines, court decisions, or other information
        that may have changed since the internal knowledge base was created.
    """,
)
async def gpdr_web_search(query: str, config: RunnableConfig) -> str:
    question_id = config.get("metadata", {}).get("question_id")

    try:
        # Enforce the strict 10-second timeout limit asynchronously
        return await asyncio.wait_for(
            _execute_web_search_logic(query, question_id), 
            timeout=10.0
        )

    # 3. This block will now trigger exactly at 10.0 seconds without waiting for the sleep to finish
    except asyncio.TimeoutError:
        logging.error(f"❌ Web search timed out after 10 seconds for query: {query}")
        
        # Plain text instructions force the LLM to output a human-readable notice to your frontend
        error_msg = (
            "SYSTEM NOTICE: The web search tool timed out after 10 seconds. "
            "Please explicitly inform the user on the frontend that the live web search timed out, "
            "and answer their question using your default internal GDPR knowledge base instead."
        )
        return error_msg

    except Exception as e:
        logging.error(f"⚠️ Error during web search execution: {str(e)}")
        traceback.print_exc()
        error_payload = {
            "status": "error",
            "error": str(e),
            "message": "Web search failed execution completely.",
        }
        return json.dumps(error_payload)


#####################
@tool(
    "data_retriever",
    description="""    
    Retrieve relevant legal information from the internal GDPR knowledge base.

    The tool performs two complementary retrieval strategies:
    1. Semantic retrieval to identify relevant legal content based on the
       meaning of the user's query.
    2. Entity- and relationship-based retrieval from the GDPR knowledge graph
       to identify relevant entities, relationships, and connected legal
       concepts.

    Use this tool for questions involving GDPR Articles, Recitals, principles,
    obligations, rights, lawful bases, definitions, compliance requirements,
    and relationships between legal concepts.

    Input:
        input_query: A natural-language legal question or information request.

    Output:
        Relevant GDPR legal context retrieved through semantic and
        graph-based/entity-aware retrieval.
              """,
)
def data_retriever(input_query: str, config: RunnableConfig) -> str:
    print("*********** DATA RETRIEVER TRIGGERED******************")
    try:
        question_id = config.get("metadata", {}).get("question_id")
        legal_obj = Legal_Assistant_respond()

        # Normalize the query
        normalize_query_prompt_path = "./prompt_library/query_normalization.md"

        refined_query = legal_obj.llm_generate_response_with_system_prompt(
            normalize_query_prompt_path, input_query
        )

        refined_query = re.sub(r"```(?:json)?\n?|\n?```", "", refined_query)

        refined_query = json.loads(refined_query)

        normalized_query = refined_query.get("query_string", "")

        ## Extract the entities
        entity_prompt_file_path = "./prompt_library/entity_extractor.md"

        entities = legal_obj.extract_entities_with_chatopenai(
            normalized_query, entity_prompt_file_path
        )

        # If entites are not extracted then fetch the similar statements from corpus and then extract the entities
        if len(entities) == 0:
            worst_match = legal_obj.search_top_matches(normalized_query, "legal_nodes")

            entities = legal_obj.extract_entities_with_chatopenai(
                worst_match, entity_prompt_file_path
            )

            if len(entities) == 0:
                return "Inadequate Query, please enter the proper query\n\n"

        entity_list = [entity.get("value", "") for entity in entities]

        ## Find the most relevant nodes
        matches = legal_obj.find_relevant_nodes(entity_list, top_k=1)
        # print("Matches", matches)

        # Geth the nodes and their properties
        graph_data_str = legal_obj.get_connected_nodes_with_relationships(matches)

        # Get the semantic data
        semantic_str = "SEMANTIC DATA:"

        matches = legal_obj.search_with_threshold(normalized_query, threshold=0.7)

        for sent, sim in matches:
            semantic_str = f"{semantic_str}\n{sent}\n"

        input_user_prompt = f"{graph_data_str}\n{semantic_str}"

        timestamp = int(time.time())
        response_data = {
            "tool": "data_retriever",
            "tool_query": input_query,
            "tool_content": input_user_prompt.splitlines(),
            "timestamp": timestamp,
            "question_id": question_id,
        }
        file_path = Path("/app/responses") / f"{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        print(f"🔥 RESPONSE SAVED: {file_path}", flush=True)

        return input_user_prompt
    except Exception as e:
        logging.error(f"Error during data retrieval: {str(e)}")
        traceback.print_exc()
        error_payload = {
            "status": "error",
            "error": str(e),
            "message": "Data retrieval failed. Continue without retrieved data if possible.",
        }

        return json.dumps(error_payload)

@tool(
    "compliance_verifier",
    description="""    
    Verify and assess GDPR compliance by comparing the user's query or
    described situation against the legal context retrieved from the
    internal GDPR knowledge base.

    The tool analyzes the retrieved GDPR requirements and determines whether
    the situation described in the user's query is compliant, partially
    compliant, non-compliant, or cannot be determined from the available
    evidence.

    Perform:
    - Requirement-to-situation comparison
    - Compliance verification
    - Identification of compliance gaps
    - Risk analysis and risk severity assessment
    - Evidence-based reasoning for the assessment

    Input:
        input_query: The original user question or description of the
        organization's situation.

        retrieved_data: Relevant GDPR requirements and legal context
        retrieved by the data_retriever tool.

    Output:
        A compliance assessment containing the verification result,
        identified gaps, risk analysis, and reasoning based on the
        retrieved legal context.
              """,
)
def compliance_verifier(input_query: str, config: RunnableConfig) -> str:
    print("*********** COMPLIANCE VERIFIER TRIGGERED******************")
    try:
        question_id = config.get("metadata", {}).get("question_id")

        client = OpenAI(api_key=api_key)
        input_prompt = f"input_query:\n{input_query}"
        with open(
            "./prompt_library/compliance_verifier.md", "r", encoding="utf-8"
        ) as f:
            system_prompt = f.read()

        response = client.responses.create(
            model=env_settings.model, instructions=system_prompt, input=input_prompt
        )

        timestamp = int(time.time())
        response_data = {
            "tool": "compliance_verifier",
            "tool_query": input_query,
            "tool_content": response.output_text.splitlines(),
            "timestamp": timestamp,
            "question_id": question_id,
        }
        file_path = Path("/app/responses") / f"{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        print(f"🔥 RESPONSE SAVED: {file_path}", flush=True)

        return response.output_text
    except Exception as e:
        logging.error(f"Error during compliance verification: {str(e)}")
        traceback.print_exc()
        error_payload= {
            "status": "error",
            "error": str(e),
            "message": "Compliance verification failed. Continue without compliance assessment if possible.",
        }

        return json.dumps(error_payload)


@tool(
    "general_legal_researcher",
    description="""    
    Researches general legal questions that are not specifically related
    to GDPR.

    Use this tool when the user asks for general legal information,
    legal concepts, statutes, procedures, rights, obligations, or
    terminology.

    The tool must remain within the legal domain and should not answer
    non-legal questions.
              """,
)
def general_legal_researcher(input_query: str, config: RunnableConfig) -> str:
    print("*********** GENERAL LEGAL TRIGGERED******************")
    try:
        question_id = config.get("metadata", {}).get("question_id")

        client = OpenAI(api_key=api_key)

        with open("./prompt_library/general_layer.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        response = client.responses.create(
            model=env_settings.model, instructions=system_prompt, input=input_query
        )

        timestamp = int(time.time())
        response_data = {
            "tool": "general_legal_researcher",
            "tool_query": input_query,
            "tool_content": response.output_text.splitlines(),
            "timestamp": timestamp,
            "question_id": question_id,
        }
        file_path = Path("/app/responses") / f"{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        print(f"🔥 RESPONSE SAVED: {file_path}", flush=True)

        return response.output_text
    except Exception as e:
        logging.error(f"Error during general legal research: {str(e)}")
        traceback.print_exc()
        error_payload= {
            "status": "error",
            "error": str(e),
            "message": "General legal research failed. Continue without general legal information if possible.",
        }
        return json.dumps(error_payload)


#########################


async def query_processing_pipeline(
    input_query: str, user_id: str, chat_mode: str
) -> AsyncGenerator[str, None]:
    middleware_stream_names = [
        "PromptInjectionMiddleware.before_agent",
        "ProfanityMiddleware.before_agent",
    ]

    streaming_llm = llm.with_config(
        {"streaming": True, "callbacks": [StreamingStdOutCallbackHandler()]}
    )

    if chat_mode == "legal":
        main_agent_file = "main_agent.md"
        tools = [
            data_retriever,
            general_legal_researcher,
            gpdr_web_search,
            compliance_verifier,
        ]
        thread_id = user_id
        run_name = "legal_chat"
    elif chat_mode == "document":
        main_agent_file = "user_document_chat.md"
        tools = [
            data_retriever,
            gpdr_web_search,
            user_compliance_verifier,
            risk_analyzer,
            retrieve_top_chunks,
            download_tool,
        ]
        thread_id = f"{user_id}_dochat"
        run_name = "document_chat"
    else:
        main_agent_file = "main_agent.md"
        tools = [
            data_retriever,
            general_legal_researcher,
            gpdr_web_search,
            compliance_verifier,
        ]
        thread_id = user_id
        run_name = "legal_chat"

    with open(f"./prompt_library/{main_agent_file}", "r", encoding="utf-8") as f:
        main_system_prompt = f.read()

    try:
        DB_URI = f"postgresql://{env_settings.PG_USER}:{env_settings.PG_PASSWORD}@host.docker.internal:{env_settings.PG_PORT}/{env_settings.agent_memory_db}?sslmode=disable"
        async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
            await checkpointer.setup()  # Automatically creates tables in PostgreSQL
            agent = create_agent(
                model=streaming_llm,
                tools=tools,
                system_prompt=main_system_prompt,
                checkpointer=checkpointer,
                middleware=[
                    ProfanityMiddleware(guardrail_llm),
                    PromptInjectionMiddleware(guardrail_llm),
                    JailbreakMiddleware(guardrail_llm),
                    # Token Limiter
                    SummarizationMiddleware(
                        model=llm,
                        trigger=("tokens", 4000),
                        keep=("messages", 5),
                    ),
                    # Layer 2: PII protection (before and after model)
                    PIIMiddleware("email", strategy="redact", apply_to_input=True),
                    PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
                    PIIMiddleware(
                        "api_key",
                        detector=r"sk-[a-zA-Z0-9]{32}",
                        strategy="block",
                    ),
                    PIIMiddleware(
                        "phone_number",
                        detector=phone_detector,
                        strategy="mask",
                    ),
                ],
            )

            question_id = str(uuid.uuid4())
            thread_config = {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 50,
                "run_name": run_name,
                "tags": ["gdpr", "legal-assistant", "production"],
                "metadata": {
                    "user_id": user_id,
                    "chat_mode": chat_mode,
                    "question_id": question_id,
                },
            }
            context = UserContext(user_id=user_id)

            print("🔥 ABOUT TO START AGENT STREAM", flush=True)
            full_response = ""
            execution_steps = []
            async for event in agent.astream_events(
                {"messages": [{"role": "user", "content": input_query}]},
                config=thread_config,
                context=context,
                version="v2",
            ):
                # print(
                #     "🔥 EVENT RECEIVED:",
                #     event.get("event"),
                #     event.get("name"),
                #     flush=True,
                # )

                event_name = event["event"]
                event_name_id = event.get("name")

                # =========================================================
                # 3. NORMAL LLM STREAM
                # =========================================================

                if (
                    event_name == "on_chat_model_stream"
                    and event.get("name") != "guardrail_llm"
                ):
                    with open("model_stream_debug.txt", "a", encoding="utf-8") as f:
                        f.write("\n================ MODEL STREAM ================\n")
                        f.write(f"NAME: {event.get('name')}\n")
                        f.write(f"TAGS: {event.get('tags')}\n")
                        f.write(f"METADATA: {event.get('metadata')}\n")
                        f.write(f"PARENT IDS: {event.get('parent_ids')}\n")

                        chunk = event["data"]["chunk"]

                        f.write(f"CONTENT: {repr(chunk.content)}\n")
                        f.write(f"EVENT: {event}\n")

                        f.write("================================================\n\n")

                    metadata = event.get("metadata", {})

                    # Don't expose summarization middleware output
                    if metadata.get("lc_source") == "summarization":
                        continue

                    if metadata.get("langgraph_node") == "tools":
                        continue

                    chunk = event["data"]["chunk"]

                    # -----------------------------
                    # TOOL CALL DETECTED
                    # -----------------------------

                    if chunk.tool_calls:
                        for tool_call in chunk.tool_calls:
                            tool_name = tool_call.get("name")

                            if tool_name:
                                print("🔥 TOOL REQUESTED:", tool_name)

                                payload = json.dumps(
                                    {"type": "tool_start", "tool": tool_name}
                                )
                                execution_steps.append(
                                    {
                                        "type": "tool_call",
                                        "tool": tool_name,
                                        "timestamp": time.time(),
                                    }
                                )

                                yield f"data: {payload}\n\n"

                        continue

                    if isinstance(chunk.content, str) and chunk.content:
                        # Accumulate complete response
                        full_response += chunk.content
                        payload = json.dumps(
                            {"type": "token", "content": chunk.content}
                        )

                        yield f"data: {payload}\n\n"

                # =========================================================
                # 4. MIDDLEWARE GENERATED RESPONSE
                # =========================================================

                elif event_name == "on_chain_stream":
                    if event.get("name") in middleware_stream_names:
                        chunk_data = event.get("data", {}).get("chunk", {})

                        if chunk_data:
                            messages = chunk_data.get("messages", [])

                            for message in messages:
                                if message.content:
                                    payload = json.dumps(
                                        {
                                            "type": "guardrail",
                                            "content": message.content,
                                        }
                                    )

                                    yield f"data: {payload}\n\n"

            print("🔥 FULL RESPONSE:", full_response, flush=True)
            timestamp = int(time.time())
            response_data = {
                "input_query": input_query,
                "content": full_response.splitlines(),
                "timestamp": timestamp,
                "thread_id": thread_id,
                "user_id": user_id,
                "chat_mode": chat_mode,
                "question_id": question_id,
                "execution_steps": execution_steps,
            }
            file_path = Path("/app/responses") / f"{timestamp}.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(response_data, f, ensure_ascii=False, indent=4)

            print(f"🔥 RESPONSE SAVED: {file_path}", flush=True)

    except Exception as e:
        print("🔥 PIPELINE ERROR:", repr(e), flush=True)
        traceback.print_exc()

        payload = json.dumps({"type": "error", "content": str(e)})

        yield f"data: {payload}\n\n"


#######################


# async def main():
#     async for output in query_processing_pipeline("Hello"):
#         pass


# if __name__ == "__main__":
#     asyncio.run(main())
