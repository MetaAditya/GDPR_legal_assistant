import pymupdf
import json
import os
import ollama
import json
import math

ollama_client = ollama.Client(
    host="http://host.docker.internal:11434"
)

class document_class:
    def __init__(self):
        self.EMBEDDING_MODEL = "mxbai-embed-large"
        self.EMBEDDING_DIMENSIONS = 1024

    def extract_pdf_text(self, pdf_path: str) -> str:
        text = []

        doc = pymupdf.open(pdf_path)

        for page in doc:
            text.append(page.get_text())

        doc.close()

        return "\n".join(text)

    def create_document_json(self, text: str, json_path: str = "./user_docs/document.json"):
        if not text or not text.strip():
            raise ValueError("Input text is empty.")

        # -----------------------------------------
        # 1. Delete existing JSON file
        # -----------------------------------------

        if os.path.exists(json_path):
            os.remove(json_path)

        # -----------------------------------------
        # 2. Split into exactly 4 chunks
        # -----------------------------------------

        chunks = self.split_into_four_chunks(text)

        documents = []

        # -----------------------------------------
        # 3. Generate embeddings
        # -----------------------------------------

        for index, chunk in enumerate(chunks, start=1):
            response = ollama_client.embed(model=self.EMBEDDING_MODEL, input=chunk)

            embedding = response["embeddings"][0]

            # Make sure embedding dimension is correct
            if len(embedding) != self.EMBEDDING_DIMENSIONS:
                raise ValueError(
                    f"Expected {self.EMBEDDING_DIMENSIONS} dimensions, got {len(embedding)}"
                )

            documents.append(
                {"chunk_id": index, "content": chunk, "embedding": embedding}
            )

        # -----------------------------------------
        # 4. Create JSON
        # -----------------------------------------

        data = {
            "embedding_model": self.EMBEDDING_MODEL,
            "embedding_dimensions": self.EMBEDDING_DIMENSIONS,
            "chunks": documents,
        }

        # -----------------------------------------
        # 5. Write JSON
        # -----------------------------------------

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        print(f"Created: {json_path}")
        print("Number of chunks:", len(documents))

        return data

    def split_into_four_chunks(self, text: str):
        text = text.strip()

        total_length = len(text)

        chunks = []

        start = 0

        for i in range(4):
            if i == 3:
                end = total_length
            else:
                end = round((i + 1) * total_length / 4)

            chunk = text[start:end].strip()

            chunks.append(chunk)

            start = end

        return chunks




    def user_doc_ingestion_pipeline(self,file_name:str="company_draft.pdf",user_id:str=""):

        if not user_id:
            raise ValueError("No User Given")

        if user_id:
            user_id=user_id.replace("-", "_")            
        
        pdf_text = self.extract_pdf_text(f"./uploads/{file_name}")

        
        self.create_document_json( pdf_text,json_path= f"./user_docs/{user_id}.json")

        return 
   
    


if __name__ == "__main__":
  doc_obj = document_class()
  input_query="""This information is associated with the customer's account where the customer"""
  kk=doc_obj.retrieve_top_chunks(query=input_query,user_id="")
  print(kk)

 
