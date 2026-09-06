from weasyprint import HTML
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
from langchain_core.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup
import json
from jinja2 import Environment, FileSystemLoader
from langchain.tools import tool






# HTML(string=html_string).write_pdf("output.pdf")

class document_generation_tool():

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

        api_key = (
            env_settings.API_KEY
            .get_secret_value()
        )
        model=env_settings.model

        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            streaming=False,
            temperature=0.1
        )

    def extract_details_from_input(self, input_text:str=""):

        with open("compliance_input.txt", "r", encoding="utf-8") as f:
            html = f.read()


        soup = BeautifulSoup(html, "html.parser")

        result = {}

        for section in soup.find_all("section"):

            heading = section.find("h2")

            if not heading:
                continue

            # Remove numbering: "1. Executive Summary" -> "Executive Summary"
            title = heading.get_text(" ", strip=True)

            if "." in title:
                title = title.split(".", 1)[1].strip()

            # Extract all text except the heading
            content = section.find_all(["p", "li"])

            text = " ".join(
                element.get_text(" ", strip=True)
                for element in content
            )

            result[title] = text


        return result

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


    
    def document_data_generator(self):


        print("*************************DOCUMENT TOOL TRIGERRED*************************************")


        nodes_part_1=["gdpr", "data processor", "data controller", "data protection officer",
                      "guiding principles", "lawful Basis and limits to processing"]

        nodes_part_1=[node.lower() for node in nodes_part_1]

        nodes_part_2=["Processing Special Categories of Data", "Processing Data on Criminal Offences",
                      "Processing in the Context of Employment","Individual Rights of Data Subjects", "Data Protection Impact Assessment (DPIA)",
                      "Data Breach", 
                      ]

        nodes_part_2=[node.lower() for node in nodes_part_2]

        nodes_part_3=["Ensuring Compliance","Codes of Conduct","Binding Corporate Rules","Fines","The GDPR and the Public Sector","Public Authorities or Bodies",
                      "Independent Supervisory Authority","Guidelines on Compliance for Trade Unions","Practical Recommendations on Data Protection",


        ]
        nodes_part_3=[node.lower() for node in nodes_part_3]


        ###################
        graph_knowledge_base_part_1=f"GDPR Knowledge Base:\n{self.get_connected_nodes_with_relationships(nodes_part_1)}"
        graph_knowledge_base_part_2=f"GDPR Knowledge Base:\n{self.get_connected_nodes_with_relationships(nodes_part_2)}"
        graph_knowledge_base_part_3=f"GDPR Knowledge Base:\n{self.get_connected_nodes_with_relationships(nodes_part_3)}"

        
        ###################
        input_compliance_data=self.extract_details_from_input(input_text="")
  
        keys_to_extract=['Executive Summary','Company and GDPR Applicability', 'Data Processing Analysis', 'GDPR Principles and Legal Basis' ]
        input_compliance_data_part_1={k: input_compliance_data[k] for k in keys_to_extract if k in input_compliance_data}
        input_compliance_data_part_1 = "\n".join(f"{k}:\n{v}" for k, v in input_compliance_data_part_1.items())

        keys_to_extract=['Data Subject Rights', 'Third Parties and International Transfers', 'Security and Breach Management', 'DPIA / DPO / Governance']
        input_compliance_data_part_2={k: input_compliance_data[k] for k in keys_to_extract if k in input_compliance_data}
        input_compliance_data_part_2 = "\n".join(f"{k}:\n{v}" for k, v in input_compliance_data_part_2.items())

        keys_to_extract=['Retention and Deletion', 'Compliance Gap Analysis', 'Remediation Roadmap']
        input_compliance_data_part_3={k: input_compliance_data[k] for k in keys_to_extract if k in input_compliance_data}
        input_compliance_data_part_3 = "\n".join(f"{k}:\n{v}" for k, v in input_compliance_data_part_3.items())
                           

        with open("./prompt_library/document_generation_prompts/Docu_part1.md", "r", encoding="utf-8") as f:
            system_prompt_part_1 = f.read()     

        with open("./prompt_library/document_generation_prompts/Docu_part2.md", "r", encoding="utf-8") as f:
            system_prompt_part_2 = f.read() 

        with open("./prompt_library/document_generation_prompts/Docu_part3.md", "r", encoding="utf-8") as f:
            system_prompt_part_3 = f.read() 


        input_query_part_1=f"{graph_knowledge_base_part_1}\n{input_compliance_data_part_1}"
        input_query_part_2=f"{graph_knowledge_base_part_2}\n{input_compliance_data_part_2}"
        input_query_part_3=f"{graph_knowledge_base_part_3}\n{input_compliance_data_part_3}"

        output_dict={}


        for n in ['1', '2', '3']:

            input_query=eval(f"input_query_part_{n}")
            system_prompt=eval(f"system_prompt_part_{n}")

            # print(input_query)
            # print()


            agent = create_agent(
                model=self.llm,
                system_prompt=system_prompt,
        
            )
            # Simple call with a user query
            result = agent.invoke({
                "messages": [
                    {"role": "user", "content": input_query}
                ]
            })

            result=json.loads(result["messages"][-1].content)

            output_dict.update(result)

            print(f"--------------------Iter {n} DONE------------------")


        env = Environment(
            loader=FileSystemLoader(".")
        )

        template = env.get_template("prompt_library/document_generation_prompts/tool_template.html")

        html_document = template.render(data=output_dict)

        HTML(string=html_document).write_pdf("output.pdf")

        print("=================DOCUMENT GENERATED ==================")








if __name__ == "__main__":
    tool_obj=document_generation_tool( dbname=env_settings.PG_DB,
                    user=env_settings.PG_USER,
                    password=env_settings.PG_PASSWORD,
                    host=env_settings.PG_HOST,
                    port=env_settings.PG_PORT)
    tool_obj.document_data_generator()
