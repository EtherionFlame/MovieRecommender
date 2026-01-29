from neo4j import GraphDatabase
from config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER,NEO4J_PASSWORD))

try:
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' AS message")
        record = result.single()
        print(record["message"])
finally:
    driver.close()