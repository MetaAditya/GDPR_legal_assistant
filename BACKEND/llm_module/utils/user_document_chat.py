from langchain.tools import tool
import math, json, os, re, ollama, time
from langchain.agents import create_agent
from openai import OpenAI
from settings import env_settings
from llm_module.utils.legal_utils import document_generation_tool
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass
from langchain_core.tools import tool
from weasyprint import HTML
from langchain_core.runnables import RunnableConfig
from pathlib import Path
##################################
ollama_client = ollama.Client(
    host="http://host.docker.internal:11434"
)

api_key = (
            env_settings.API_KEY
            .get_secret_value()
        )

@dataclass
class UserContext:
    user_id: str


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    """

    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    magnitude1 = math.sqrt(sum(a * a for a in vec1))

    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


@tool(
    "retrieve_top_chunks",
    description="""
    Retrieve the most semantically relevant sections or chunks from the
    user's uploaded document based on the user's query.

    This tool is used to obtain factual context about the organization's
    data processing activities, policies, systems, and practices as
    described in the uploaded document.

    The tool performs semantic similarity-based retrieval and returns the
    top relevant chunks of the document.

    Use this tool when the user's question relates to information that may
    be contained in the uploaded document.

    Examples of information that may be retrieved include:

    - Personal data collected
    - Data processing activities
    - Data retention periods
    - Customer profiling
    - Automated decision-making
    - Marketing activities
    - Data sharing
    - Third-party processors
    - International data transfers
    - Security controls
    - Employee access
    - Data subject rights
    - Privacy policies
    - Organizational practices

    Input:
        input_query:
            The user's question or description of the situation.
            The query is used to identify the most relevant portions of
            the uploaded document.

    Output:
        The most relevant document chunks, including their textual
        content and, where available, relevant metadata.

    IMPORTANT:

    - Retrieve information based on semantic relevance to the query.
    - Do not generate or infer information that is not present in the
      uploaded document.
    - The retrieved chunks represent organizational facts and should be
      treated as factual evidence.
    - If relevant information cannot be found in the document, return an
      appropriate indication that sufficient document evidence is
      unavailable.
    """,
)
def retrieve_top_chunks(
    query: str,
    runtime: ToolRuntime[UserContext],
    json_path: str = "./user_docs/document.json",
    top_k: int = 4,
    # user_id: str = "",
):
    # -----------------------------------------
    # 1. Load JSON
    # -----------------------------------------
    try:
        
        EMBEDDING_MODEL = "mxbai-embed-large"
        user_id = runtime.context.user_id

        if user_id:
            user_id = user_id.replace("-", "_")
        json_path = f"./user_docs/{user_id}.json"

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        chunks = data["chunks"]

        # -----------------------------------------
        # 2. Create query embedding
        # -----------------------------------------

        response = ollama_client.embed(model=EMBEDDING_MODEL, input=query)

        query_embedding = response["embeddings"][0]

        # -----------------------------------------
        # 3. Calculate similarity
        # -----------------------------------------

        results = []

        for chunk in chunks:
            similarity = cosine_similarity(query_embedding, chunk["embedding"])

            results.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"],
                    "similarity": similarity,
                }
            )

        # -----------------------------------------
        # 4. Sort by similarity
        # -----------------------------------------

        results.sort(key=lambda x: x["similarity"], reverse=True)

        # -----------------------------------------
        # 5. Return top K
        # -----------------------------------------

        results = results[:top_k]
        chunk_str = ""
        for result in results:
            chunk_str = chunk_str + result.get("content") + "\n\n"

        return chunk_str
    except Exception as e:
        print(f"EXception--------------------------{str(e)}")
        error_payload = {
            "status": "error",
            "error": str(e),
            "message": "Document chunk retrieval failed. Continue without document context if possible.",
        }
        return json.dumps(error_payload)


#############
@tool(
    "risk_analyzer",
    description="""
    Analyze GDPR-related privacy and data protection risks based on the
    user's query, applicable GDPR legal context, and relevant organizational
    document context.

    The tool identifies potential risks arising from the organization's
    data processing activities and evaluates their potential impact on
    data subjects and the organization.

    The main agent must provide three inputs:

    1. input_query:
       The original user question or description of the organization's
       data processing situation.

    2. legal_context:
       Relevant GDPR legal requirements and legal context retrieved by
       the data_retriever tool.

    3. document_context:
       Relevant organizational facts retrieved from the user's uploaded
       document by the retrieve_top_chunks tool.

    Perform:

    - Identification of privacy and data protection risks
    - Identification of affected data subjects
    - Identification of potential harm to data subjects
    - Assessment of likelihood of the risk occurring
    - Assessment of potential impact or severity
    - Overall risk severity classification
    - Identification of contributing factors
    - Evidence-based explanation of each identified risk
    - Recommended risk mitigation measures

    Risk severity should be classified as:

    - Low
    - Medium
    - High
    - Critical

    IMPORTANT:

    Base the risk assessment on the provided legal_context and
    document_context.

    Do not invent organizational facts.

    Do not assume that a practice exists unless it is supported by the
    document_context or input_query.

    Distinguish between:
    - Facts about the organization
    - GDPR legal requirements
    - Risk conclusions
    - Recommended mitigations

    Input:
        input_query:
            The original user question or description of the
            organization's situation.

        legal_context:
            Relevant GDPR requirements retrieved by data_retriever.

        document_context:
            Relevant organizational information retrieved by
            retrieve_top_chunks.

    Output:

        A risk assessment containing:

        - Identified risks
        - Affected data subjects
        - Potential harm
        - Likelihood
        - Impact
        - Overall risk severity
        - Contributing factors
        - Risk reasoning
        - Recommended mitigation measures
    """,
)
def risk_analyzer(
    input_query: str,
    legal_context: str,
    document_context: str,
    config: RunnableConfig
) -> str:
    print("*********** RISK ANALYZER TRIGGERED ******************")
    try:

        client = OpenAI(api_key=api_key)

        input_prompt = f"""
                    input_query:
                    {input_query}

                    ========================
                    GDPR LEGAL CONTEXT
                    ========================

                    {legal_context}

                    ========================
                    ORGANIZATIONAL DOCUMENT CONTEXT
                    ========================

                    {document_context}
                """

        with open("./prompt_library/risk_analysis.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        response = client.responses.create(
            model=env_settings.model, instructions=system_prompt, input=input_prompt
        )

        question_id = config.get("metadata", {}).get("question_id")
        timestamp = int(time.time())
        response_data = {
            "tool": "risk_analyzer",
            "tool_query": input_query,
            "tool_content": response.output_text.splitlines(),
            "timestamp": timestamp,
            "question_id": question_id,
        }
        file_path = Path("/app/responses") / f"{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        return response.output_text
    except Exception as e:
        print(f"Exception in risk_analyzer: {str(e)}")
        error_payload = {
            "status": "error",
            "error": str(e),
            "message": "Risk analysis failed. Continue without risk assessment if possible.",
        }
        return json.dumps(error_payload)


@tool(
    "user_compliance_verifier",
    description="""
    Verify and assess GDPR compliance by comparing the user's described
    situation against the applicable GDPR legal context and the relevant
    organizational information retrieved from the user's uploaded document.

    The tool receives three inputs:

    1. input_query:
       The original user question or description of the organization's
       situation.

    2. legal_context:
       Relevant GDPR requirements and legal context retrieved by the
       data_retriever tool.

    3. document_context:
       Relevant organizational facts retrieved by the
       retrieve_top_chunks tool.

    The tool must compare the organization's actual or described practices
    against the applicable GDPR requirements.

    Determine whether the situation is:

    - Compliant
    - Partially compliant
    - Non-compliant
    - Cannot be determined from the available evidence

    Perform:

    - Requirement-to-situation comparison
    - Compliance verification
    - Identification of compliance gaps
    - Identification of relevant GDPR principles or obligations
    - Evidence-based reasoning
    - Identification of potential concerns
    - Recommendations for remediation where appropriate

    IMPORTANT:

    The legal_context comes from the GDPR legal knowledge base.

    The document_context comes from the user's uploaded organizational
    document.

    Do not invent organizational facts.

    Do not invent GDPR requirements.

    Clearly distinguish between:
    - Organizational facts
    - GDPR requirements
    - Compliance findings
    - Assumptions or limitations
    - Recommendations

    Input:
        input_query:
            The original user question or description of the
            organization's situation.

        legal_context:
            Relevant GDPR requirements and legal context retrieved by
            data_retriever.

        document_context:
            Relevant organizational information retrieved by
            retrieve_top_chunks.

    Output:
        A compliance assessment containing:

        - Compliance status
        - Applicable GDPR requirements
        - Relevant organizational facts
        - Compliance gaps
        - Evidence-based reasoning
        - Limitations or missing information
        - Recommended remediation actions
    """,
)
def user_compliance_verifier(
    input_query: str,
    legal_context: str,
    document_context: str,
    config: RunnableConfig
) -> str:
    print("*********** USER COMPLIANCE VERIFIER TRIGGERED******************")

    try:

        client = OpenAI(api_key=api_key)

        input_prompt = f"""
                    input_query:
                    {input_query}

                    ========================
                    GDPR LEGAL CONTEXT
                    ========================

                    {legal_context}

                    ========================
                    ORGANIZATIONAL DOCUMENT CONTEXT
                    ========================

                    {document_context}
                    """

        with open("./prompt_library/compliance_verifier.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        response = client.responses.create(
            model=env_settings.model, instructions=system_prompt, input=input_prompt
        )

        question_id = config.get("metadata", {}).get("question_id")
        timestamp = int(time.time())
        response_data = {
            "tool": "user_compliance_verifier",
            "tool_query": input_query,
            "tool_content": response.output_text.splitlines(),
            "timestamp": timestamp,
            "question_id": question_id,
        }
        file_path = Path("/app/responses") / f"{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        return response.output_text
    except Exception as e:
        print(f"Exception in user_compliance_verifier: {str(e)}")
        error_payload = {
            "status": "error",
            "error": str(e),
            "message": "Compliance verification failed. Continue without compliance assessment if possible.",
        }
        return json.dumps(error_payload)


@tool(
    "download_tool",
    description="""
    Create a downloadable PDF document from HTML content generated by the
    main agent.

    The main agent is responsible for deciding what content should be
    downloaded and generating the complete HTML document.

    This tool only converts the supplied HTML content into a PDF and saves it
    to the configured download directory.

    Input:
        html_content: Complete HTML document generated by the main agent.

    Output:
        A result indicating whether the PDF was successfully created and
        the download endpoint that can be used by the frontend.
    """,
)
def download_tool(html_content: str) -> str:
    
    print("*********** DOWNLOAD TOOL TRIGGERED ******************")
    print(html_content)

    if not html_content or not html_content.strip():
        return "ERROR: html_content is empty."

    download_dir = "./downloads"

    os.makedirs(download_dir, exist_ok=True)

    pdf_path = os.path.join(download_dir, "download.pdf")

    try:
        HTML(string=html_content).write_pdf(pdf_path)

        if not os.path.exists(pdf_path):
            return "ERROR: PDF was not created."

        return """
            {
                "status": "success",
                "filename": "download.pdf",
                "download_url": "/download"
            }
            """

    except Exception as e:
        print("PDF generation error:", e)

    
        error_payload = {
            "status": "error",
            "error": str(e),
            "message": "Download failed.",
        }
        return json.dumps(error_payload)