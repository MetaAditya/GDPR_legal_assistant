import psycopg2
import re
from settings import env_settings
import ollama


class LegalVectorDB:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost",
            port=port
        )
        self.cur = self.conn.cursor()
        

    def create_table(self, table_name="legal_nodes", dim=1024):
        """
        Create a pgvector table for storing sentences + embeddings.
        """
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                sentence TEXT,
                embedding VECTOR({dim})
            );
        """)

        self.conn.commit()

    def _split_into_chunks(self, text: str, chunk_size=2):
        """
        Split text into chunks of N sentences (default 2).
        """
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        chunks = [
            " ".join(sentences[i:i+chunk_size])
            for i in range(0, len(sentences), chunk_size)
            if sentences[i:i+chunk_size]
        ]
        return chunks

    def insert_chunks(self, text: str, table_name="legal_nodes"):
        """
        Extract 2-sentence chunks from text, embed, and insert into Postgres.
        """
        
        chunks = self._split_into_chunks(text)
        
        for chunk in chunks:
            emb = ollama.embed(
            model='mxbai-embed-large',
            input=chunk
            ).embeddings[0]

            self.cur.execute(
                f"INSERT INTO {table_name} (sentence, embedding) VALUES (%s, %s)",
                (chunk, emb)
            )
        self.conn.commit()



    def insert_node_embeddings(self, nodes_list: list, table_name="node_embeddings"):
        """
        Extract 2-sentence chunks from text, embed, and insert into Postgres.
        """
       
        for node in nodes_list:
            emb = ollama.embed(
            model='mxbai-embed-large',
            input=node
            ).embeddings[0]

            self.cur.execute(
                f"INSERT INTO {table_name} (sentence, embedding) VALUES (%s, %s)",
                (node, emb)
            )
        self.conn.commit()



if __name__ == "__main__":

    # Example usage:
    db = LegalVectorDB(dbname=env_settings.PG_DB,
                        user=env_settings.PG_USER,
                        password=env_settings.PG_PASSWORD,
                        host=env_settings.PG_HOST,
                        port=env_settings.PG_PORT

                          )
    db.create_table(dim=1024)

    with open("GDPR_output.txt", "r", encoding="utf-8") as f:
        text_data = f.read()

    text_data = " ".join(text_data.split())
    text_data=text_data.lower()
    
    db.insert_chunks(text_data)

    # Create the embedding table for nodes too
    db.create_table(table_name="node_embeddings", dim=1024)
    db.cur.execute("""
    SELECT DISTINCT id 
    FROM nodes;
    """)

    rows = db.cur.fetchall()
    nodes_list = [row[0] for row in rows]

    db.insert_node_embeddings(nodes_list)

    





   