from graph_data import nodes, relationships
from settings import env_settings
import psycopg2
import json


class GraphDB:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost",
            port=port
        )
        self.cur = self.conn.cursor()

    def create_schema(self):
        """Create tables for nodes and relationships if they don't exist."""
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            properties JSONB
        );
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id SERIAL PRIMARY KEY,
                source_id TEXT NOT NULL,
                source_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                target_type TEXT NOT NULL,
                type TEXT NOT NULL,
                properties JSONB,
                FOREIGN KEY (source_id) REFERENCES nodes(id) ON DELETE CASCADE,
                FOREIGN KEY (target_id) REFERENCES nodes(id) ON DELETE CASCADE,
                UNIQUE (source_id, target_id, type)  
            );

        
        """)
        self.conn.commit()

    def add_node(self, node):
        """Insert or update a node."""
        node_id = node["id"].lower()
        node_type = node["type"].lower()
        properties = {k.lower(): v for k, v in node["properties"].items()}  # optional: lowercase keys
        self.cur.execute("""
            INSERT INTO nodes (id, type, properties)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET properties = EXCLUDED.properties;
        """, (node_id, node_type, json.dumps(properties)))
        self.conn.commit()

    def add_relationship(self, relationship):
        """Insert a relationship between nodes, ensuring both ends exist."""
        # Ensure source node exists

        source_id = relationship["source"]["id"].lower()
        source_type = relationship["source"]["type"].lower()
        target_id = relationship["target"]["id"].lower()
        target_type = relationship["target"]["type"].lower()
        rel_type = relationship["type"].lower()
        properties = {k.lower(): v for k, v in relationship.get("properties", {}).items()}

        self.cur.execute("SELECT id FROM nodes WHERE id = %s;", (relationship["source"]["id"].lower(),))
        if not self.cur.fetchone():
            raise ValueError(f"Source node '{relationship['source']['id'].lower()}' does not exist in nodes table.")

        # Ensure target node exists
        self.cur.execute("SELECT id FROM nodes WHERE id = %s;", (relationship["target"]["id"].lower(),))
        if not self.cur.fetchone():
            raise ValueError(f"Target node '{relationship['target']['id'].lower()}' does not exist in nodes table.")

        # Insert relationship
        self.cur.execute("""
            INSERT INTO relationships (source_id, source_type, target_id, target_type, type, properties)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id, target_id, type) DO UPDATE 
            SET properties = EXCLUDED.properties;
        """, (
            source_id,
            source_type,
            target_id,
            target_type,
            rel_type,
            json.dumps(properties)
        ))
        self.conn.commit()

    def get_relationships(self, node_id):
        """Fetch all relationships for a given node."""
        self.cur.execute("""
            SELECT r.type, r.source_id, r.target_id, r.properties
            FROM relationships r
            WHERE r.source_id = %s OR r.target_id = %s;
        """, (node_id, node_id))
        return self.cur.fetchall()


    def get_connected_nodes(self, node_id):
        """
        Fetch all nodes connected to the given node, both as source and target,
        along with the relationship type.
        """
        self.cur.execute("""
            SELECT DISTINCT 
                n.id, n.type, n.properties, r.type AS relationship_type
            FROM relationships r
            JOIN nodes n 
                ON (n.id = r.target_id AND r.source_id = %s)
                OR (n.id = r.source_id AND r.target_id = %s);
        """, (node_id.lower(), node_id.lower()))
        return self.cur.fetchall()


    def close(self):
        """Close the database connection."""
        self.cur.close()
        self.conn.close()








# This block only runs if you execute 'math_utils.py' directly
if __name__ == "__main__":
    import logging
    graph_db = GraphDB(
        dbname=env_settings.PG_DB,
        user=env_settings.PG_USER,
        password=env_settings.PG_PASSWORD,
        host=env_settings.PG_HOST,
        port=env_settings.PG_PORT
    )
    graph_db.create_schema()

    # # Insert nodes and relationships from the provided data
    for node in nodes:
        graph_db.add_node(node)

    logging.info("Nodes added successfully.")
    

    for rel in relationships:
        print(f"Relationship {rel}")
        graph_db.add_relationship(rel)

    logging.info("Relationships added successfully.")

    # Example query: get all relationships for a specific node
    node="Data Controller"
    relationships_for_node = graph_db.get_connected_nodes(node.lower())
    print("Connected nodes and relationship types:")
    for node_id, node_type, properties, rel_type in relationships_for_node:
        print(f"{node} {rel_type} {node_id}")
    graph_db.close()

