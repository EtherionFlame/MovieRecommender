from neo4j import GraphDatabase
from config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

def get_driver():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER,NEO4J_PASSWORD))
    return driver

def create_movie_node(???, ???):
    """
    Your docstring here
    """
    query="""
    MERGE (m:Movie {tmdb_id: $tmdb_id})
    SET m.title = $title,
        m.rating = $rating,
        m.release_year = $release_year
        m.budget
    """
    pass
if __name__ == "__main__":
    driver = get_driver()
    print("Driver created successfully!")
    driver.close()