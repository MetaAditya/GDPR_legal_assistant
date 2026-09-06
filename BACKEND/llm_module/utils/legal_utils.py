from langchain_openai import ChatOpenAI
import json, re
from settings import env_settings
import psycopg2
import ollama
import numpy as np
from langchain.agents import create_agent
from langchain.messages import AIMessageChunk, HumanMessage, SystemMessage
import feedparser
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain.agents.middleware import PIIMiddleware
from guardrails.guardrails import ProfanityMiddleware, PromptInjectionMiddleware
from langchain_core.messages import AIMessage
from langchain.tools import tool
from llm_module.utils.agent_tools import document_generation_tool
from typing import AsyncGenerator
import asyncio
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


ollama_client = ollama.Client(
    host="http://host.docker.internal:11434"
)
#############################Tools ################3

@tool
def tool_compliance_document_generator()->None:
    """
        Generate a formal GDPR compliance document.

        TRIGGER THIS TOOL when the user asks to:
        - generate a GDPR compliance document
        - create a GDPR compliance report
        - prepare a GDPR assessment
        - draft GDPR compliance documentation
        - produce a company GDPR compliance report
        - perform a comprehensive GDPR compliance assessment

        DO NOT TRIGGER THIS TOOL for:
        - general GDPR questions
        - explanations of individual GDPR Articles
        - questions about specific GDPR concepts
        - simple compliance advice
        - questions that do not request a formal compliance document
    """

    tool_obj=document_generation_tool( )


    tool_obj.document_data_generator()

    return None
#################################


class Legal_Assistant_respond():

    def __init__(self):

        dbname=env_settings.PG_DB
        user=env_settings.PG_USER
        password=env_settings.PG_PASSWORD
        host=env_settings.PG_HOST
        port=env_settings.PG_PORT
    

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

        ##LLM based settings
        self.api_key = (
            env_settings.API_KEY
            .get_secret_value()
        )
        self.model=env_settings.model

        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            streaming=True,
            temperature=0.9
        )

        self.llm_non_stream=ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                streaming=False,
                verbose=True
            )


        

    def get_news(self, topic: str, max_items: int = 5):
        feed_url = f"https://news.google.com/rss/search?q={topic}&hl=en&gl=US&ceid=US:en"
        feed = feedparser.parse(feed_url)

        results = []
        for entry in feed.entries[:max_items]:
            results.append({
                "title": entry.title,
                "summary": entry.summary,
                "link": entry.link
            })
        return {"topic": topic, "headlines": results}



    def search_top_matches(self, query: str, table_name="legal_nodes", top_limit=2):
        """
        Retrieve the top most similar sentences from Postgres using cosine similarity (<=>).
        """
        # Get embedding for the query
        emb = ollama_client.embed(
            model="mxbai-embed-large",
            input=query
        ).embeddings[0]

        emb_str = ",".join(str(x) for x in emb)

        # Run similarity search
        self.cur.execute(
            f"""
            SELECT sentence, embedding <=> (ARRAY[{emb_str}]::vector) AS distance
            FROM {table_name}
            ORDER BY embedding <=> (ARRAY[{emb_str}]::vector)
            LIMIT {top_limit};
            """
        )

        results = self.cur.fetchall()

        sentence_str=""

        for sent, sim in results:
            sentence_str=f"{sentence_str}\n{sent}"

        return sentence_str



    def search_with_threshold(self, query: str, table_name="legal_nodes", threshold: float = 0.8, top_k: int = 10):
        """
        Retrieve sentences with cosine similarity >= threshold.
        Default threshold = 0.8 (80%).
        """
        # Get embedding for the query
        emb = ollama_client.embed(
            model="mxbai-embed-large",
            input=query
        ).embeddings[0]

        # Convert Python list to Postgres array string
        emb_str = ",".join(str(x) for x in emb)

        # Query top_k results ordered by distance
        self.cur.execute(
            f"""
            SELECT sentence, embedding <=> (ARRAY[{emb_str}]::vector) AS distance
            FROM {table_name}
            ORDER BY embedding <=> (ARRAY[{emb_str}]::vector)
            LIMIT {top_k};
            """
        )

        rows = self.cur.fetchall()

        # Convert distance → similarity and filter by threshold
        results = []
        for sentence, distance in rows:
            similarity = 1 - distance
            if similarity >= threshold:
                results.append((sentence, similarity))

        return results


    def extract_entities_with_chatopenai(self,text: str, prompt_file: str) -> dict:
        """
        Extracts legal entities from text using ChatOpenAI guided by a prompt stored in a markdown file.

        Parameters:
            text (str): The legal or regulatory text to analyze.
            prompt_file (str): Path to the markdown file containing the enhanced prompt.
            model (str): OpenAI model to use (default: gpt-4o-mini).

        Returns:
            dict: A dictionary of extracted entities with their categories.
        """

        # Load the enhanced prompt from markdown file
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_content = f.read()

        api_key = (
                env_settings.API_KEY
                .get_secret_value()
            )
        model=env_settings.model

        # Initialize ChatOpenAI client
        llm = ChatOpenAI(model=model, 
                        api_key=api_key,

                        temperature=0)

        # Construct messages
        messages = [
            ("system", "You are a legal entity extraction assistant. "
                    "Follow the instructions in the provided prompt carefully. "
                    "Output must be structured JSON with entity type and extracted value."),
            ("user", f"{prompt_content}\n\nNow extract entities from the following text:\n{text}")
        ]

        # Call the model
        response = llm.invoke(messages)

        # Parse response
        result_text = response.content
        try:
            result = json.loads(result_text)
        except Exception:
            result = {"raw_output": result_text}

        return result


    def cosine_similarity(self,a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def find_relevant_nodes(self, entities_list: list, top_k=1):
        matches = {}

        # Step 1: Fetch all stored embeddings for list2
        self.cur.execute("SELECT sentence, embedding::text FROM node_embeddings;")
        rows = self.cur.fetchall()
        nodes_list = [row[0] for row in rows]
        
        

        node_embeddings = []
        for sentence, emb_text in rows:
            emb = [float(x) for x in emb_text.strip("[]").split(",")]
            node_embeddings.append((sentence, emb))

        node_embeddings=[node[1] for node in node_embeddings]

        

        # Step 2: For each item in list1, compute embedding and compare
        for phrase in entities_list:
            
            emb1 = ollama_client.embed(model="mxbai-embed-large", input=phrase).embeddings[0]
            
            sims = [self.cosine_similarity(emb1, emb2) for emb2 in node_embeddings]
            best_indices = np.argsort(sims)[::-1][:top_k]

            matches[phrase] = [(nodes_list[i], sims[i]) for i in best_indices]


        matches_values= [
            tup[0]   # take the first element of each tuple
            for key, val_list in matches.items()
            for tup in val_list
        ]
        return matches_values
    


    def get_connected_nodes_with_relationships(self, node_values, nodes_table="nodes", rel_table="relationships"):
        """
        Given a list of node IDs, fetch all connected nodes (both directions)
        along with the relationship type and properties. Then return their id + properties.
        """
        connected_ids = set(node_values)
        relationships = []

        # Step 1: Collect relationships for each node
        for node_id in node_values:
            self.cur.execute(
                f"""
                SELECT source_id, target_id, type, properties
                FROM {rel_table}
                WHERE source_id = %s OR target_id = %s;
                """,
                (node_id, node_id)
            )
            rows = self.cur.fetchall()
            for src, tgt, rel_type, rel_props in rows:
                connected_ids.add(src)
                connected_ids.add(tgt)
                relationships.append({
                    "source_id": src,
                    "target_id": tgt,
                    "type": rel_type,
                    "properties": rel_props
                })

        # Step 2: Fetch node details for all collected IDs
        connected_ids = list(connected_ids)
        
        self.cur.execute(
            f"""
            SELECT id, properties
            FROM {nodes_table}
            WHERE id = ANY(%s);
            """,
            (connected_ids,)
        )
        node_rows = self.cur.fetchall()

        nodes = [{"id": nid, "properties": props} for nid, props in node_rows]

        
        graph_data_str="TOPICS:\n"

        for nd in nodes:
            graph_data_str=f"{graph_data_str}\nTopic:{nd.get("id", "")}\nProperties:{nd.get("properties", "")}\n"

        graph_data_str=graph_data_str.replace("\\n", "")
        
        relationships_str="RELATIONSHIPS:\n"

        for rel in relationships:
            relationships_str=f"{relationships_str}{rel.get("source_id", "")} → {rel.get("type", "")} → {rel.get("target_id", "")}\n"

        final_graph_str=f"{graph_data_str}\n{relationships_str}"

        return final_graph_str




        

    def llm_generate_response_with_system_prompt(self, prompt_file_path:str, input_query:str)-> str:

        
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
    

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=input_query),
        ]

        response = self.llm_non_stream.invoke(messages)
        
        return response.content

        





if __name__ == "__main__":
    pass

