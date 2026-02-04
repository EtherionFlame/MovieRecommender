from neo4j import GraphDatabase
from config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER
from logger import setup_logger


logger = setup_logger(__name__)

def get_driver():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER,NEO4J_PASSWORD))
    return driver

def create_movie_node(session, movie_data):
    """
    Create or update a Movie node in Neo4j
    
    Args:
        session: Active Neo4j session
        movie_data (dict): Movie data from fetch_movie_details()
            Required keys: tmdb_id, title, release_year, rating
            Optional keys: budget, revenue, overview, poster_url
    
    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        logger.debug(f"Creating movie node from data: {movie_data.get('title')}")
        tmdb_id = movie_data.get('tmdb_id')
        if not tmdb_id:
            logger.error("Cannot create movie node: missing tmdb_id")
            return False
        title = movie_data.get('title')
        rating = movie_data.get('rating')
        release_year = movie_data.get('release_year')
        budget = movie_data.get('budget')  or 0
        revenue = movie_data.get('revenue') or 0
        overview = movie_data.get('overview')
        poster_url = movie_data.get('poster_url')
        parameters = {
            'tmdb_id': tmdb_id,
            'title': title,
            'rating':rating,
            'release_year':release_year,
            'budget':budget,
            'revenue':revenue,
            'overview':overview,
            'poster_url':poster_url
         }   
        query="""
        MERGE (m:Movie {tmdb_id: $tmdb_id})
        SET m.title = $title,
            m.rating = $rating,
            m.release_year = $release_year,
            m.budget = $budget,
            m.revenue = $revenue,
            m.overview = $overview,
            m.poster_url=$poster_url
        """
        session.run(query, parameters)

        logger.info(f"Successfully created movie node for '{title}' (ID: {tmdb_id})")

        return True
    except Exception as e:
        logger.error(f"Failed to create movie node: {e}")
        return False

def create_person_node(session, person_data):
    """
    Create or update a Person node in Neo4j
    
    Args:
        session: Active Neo4j session
        person_data (dict): Person data with keys: tmdb_id, name, profile_url
    
    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        logger.debug(f"Creating person node from data: {person_data.get('name')}")
        tmdb_id = person_data.get('tmdb_id')
        if not tmdb_id:
            logger.error("Cannot create movie node: missing tmdb_id")
            return False
        name = person_data.get('name')
        profile_url = person_data.get('profile_url')
        parameters = {
            'tmdb_id': tmdb_id,
            'name': name,
            'profile_url' : profile_url
        }
        query = """
        MERGE (p:Person{tmdb_id: $tmdb_id})
        SET p.name = $name,
            p.profile_url = $profile_url
        """
        session.run(query,parameters)
        logger.info(f"Successfully created person node for '{name}' (ID: {tmdb_id})")

        return True
    except Exception as e:
        logger.error(f"Failed to create Person node: {e}")
        return False
    
def create_genre_node(session, genre_data):
    """
    Create or update a Genre node in Neo4j
    
    Args:
        session: Active Neo4j session
        genre_data (dict): Genre data with keys: id, name
    
    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        logger.debug(f"Creating person node from data: {genre_data.get('name')}")
        name = genre_data.get('name')
        if not name:
            logger.error("Cannot create Genre node: missing name")
            return False
        parameters = {
            'name': name
        }
        query = """
        MERGE (g:Genre{name: $name})
        """
        session.run(query,parameters)
        logger.info(f"Successfully created Genre node for '{name}' (ID: {id})")

        return True
    except Exception as e:
        logger.error(f"Failed to create Genre node: {e}")
        return False

def create_studio_node(session, studio_data):
    """
    Create or update a Studio node in Neo4j
    
    Args:
        session: Active Neo4j session
        genre_data (dict): Studio data with keys: id, name
    
    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        logger.debug(f"Creating Studio node from data: {studio_data.get('name')}")
        id = studio_data.get('id')
        if not id:
            logger.error("Cannot create Studio node: No Id")
            return False
        name = studio_data.get('name')
        parameters = {
            'id':id,
            'name':name
        }
        query = """
        MERGE (s:Studio{id: $id})
        SET s.name = $name
        """
        session.run(query,parameters)
        logger.info(f"Successfully created studio node '{name}' (ID: {id})")

        return True
    except Exception as e:
        logger.error(f"Failed to create Studio node: {e}")
        return False

if __name__ == "__main__":
    
    test_movie = {
        'tmdb_id': 550,
        'title': 'Fight Club',
        'release_year': 1999,
        'rating': 8.4,
        'budget': 63000000,
        'revenue': 100853753,
        'overview': 'A test overview',
        'poster_url': 'https://test.jpg'
    }
    
    test_person = {
        'tmdb_id': 819,
        'name': 'Edward Norton',
        'profile_url': 'https://example.com/norton.jpg'
    }
    
    test_genre = {
        'name': 'Action'
    }
    
    test_studio = {
        'id': 711,
        'name': 'Fox 2000 Pictures'
    }
    
    driver = get_driver()
    
    with driver.session() as session:
        print("Testing movie node...")
        success = create_movie_node(session, test_movie)
        print(f"Movie: {success}")
        
        print("\nTesting person node...")
        success = create_person_node(session, test_person)
        print(f"Person: {success}")
        
        print("\nTesting genre node...")
        success = create_genre_node(session, test_genre)
        print(f"Genre: {success}")
        
        print("\nTesting studio node...")
        success = create_studio_node(session, test_studio)
        print(f"Studio: {success}")
    
    driver.close()
    print("\n✅ Check Neo4j Browser to verify!")