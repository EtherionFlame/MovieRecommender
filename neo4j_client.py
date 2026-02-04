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
def create_acted_in_relationship(session, person_tmdb_id, movie_tmdb_id, character, order):
    """
    Create ACTED_IN relationship between Person and Movie nodes

    Args:
        session: Active Neo4j session
        person_tmdb_id (int): TMDB ID of the actor
        movie_tmdb_id (int): TMDB ID of the movie
        character (str): Character/role name
        order (int): Billing order (0 = lead actor)

    Returns:
        bool: True if successful, False if error occurred
    """
    
    try:
        logger.debug(f"Creating ACTED_IN relationship: {person_tmdb_id} -> {movie_tmdb_id} on character {character}")
        if not movie_tmdb_id:
            logger.error("Cannot find movie node: No Id")
            return False
        if not person_tmdb_id:
            logger.error("Cannot find person node: No Id")
            return False
        parameters = {
            'person_id' : person_tmdb_id,
            'movie_id' : movie_tmdb_id,
            'character' : character,
            'order' : order
        }
        query = """
        MATCH (p:Person {tmdb_id: $person_id})
        MATCH (m:Movie {tmdb_id: $movie_id})
        MERGE (p)-[r:ACTED_IN]->(m)
        SET r.character = $character, r.order = $order
        """
        session.run(query, parameters)
        logger.info(f"Created ACTED_IN: Person {person_tmdb_id} -> Movie {movie_tmdb_id}")

        return True
    
    except Exception as e:
        logger.error(f"Failed to create ACTED_IN Relationship: {e}")
        return False
def create_directed_relationship(session, person_tmdb_id, movie_tmdb_id):
    """
    Create Directed relationship between Person and Movie nodes

    Args:
        session: Active Neo4j session
        person_tmdb_id (int): TMDB ID of the director
        movie_tmdb_id (int): TMDB ID of the movie


    Returns:
        bool: True if successful, False if error occurred
    """
    
    try:
        logger.debug(f"Creating Directed relationship: {person_tmdb_id} -> {movie_tmdb_id}")
        if not movie_tmdb_id:
            logger.error("Cannot find movie node: No Id")
            return False
        if not person_tmdb_id:
            logger.error("Cannot find person node: No Id")
            return False
        parameters = {
            'person_id' : person_tmdb_id,
            'movie_id' : movie_tmdb_id,
        }
        query = """
        MATCH (p:Person {tmdb_id: $person_id})
        MATCH (m:Movie {tmdb_id: $movie_id})
        MERGE (p)-[r:DIRECTED]->(m)
        """
        session.run(query, parameters)
        logger.info(f"Created Directed: Person {person_tmdb_id} -> Movie {movie_tmdb_id}")

        return True
    
    except Exception as e:
        logger.error(f"Failed to create Directed Relationship: {e}")
        return False
    
def create_in_genre_relationship(session, movie_tmdb_id, genre_name, is_primary=False):
    """
    Create IN_GENRE relationship between Movie and Genre nodes
    
    Args:
        session: Active Neo4j session
        movie_tmdb_id (int): TMDB ID of the movie
        genre_name (str): Name of the genre (e.g., 'Drama', 'Action')
        is_primary (bool): True if this is the primary/main genre
    
    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        logger.debug(f"Creating IN_Genre relationship: {genre_name} -> {movie_tmdb_id}")
        if not movie_tmdb_id:
            logger.error("Cannot find movie node: No Id")
            return False
        if not genre_name:
            logger.error("Cannot find Genre node: No Id")
            return False
        parameters = {
            'genre_name' : genre_name,
            'movie_id' : movie_tmdb_id,
            'is_primary': is_primary
        }
        query = """
        MATCH (m:Movie {tmdb_id: $movie_id})
        MATCH (g:Genre {name: $genre_name})
        MERGE (m)-[r:IN_GENRE]->(g)
        SET r.is_primary = $is_primary
        """
        session.run(query, parameters)
        logger.info(f"Created IN_GENRE: Movie {movie_tmdb_id} -> Genre {genre_name}")

        return True
    
    except Exception as e:
        logger.error(f"Failed to create IN_GENRE Relationship: {e}")
        return False

def create_produced_by_relationship(session, studio_id, movie_tmdb_id):
    """
    Create PRODUCED_BY relationship between Movie and Studio nodes
    
    Args:
        session: Active Neo4j session
        movie_tmdb_id (int): TMDB ID of the movie
        studio_id (int): Studio ID from TMDB
    
    Returns:
        bool: True if successful, False if error occurred
    """
    
    try:
        logger.debug(f"Creating PRODUCED_BY relationship: {studio_id} -> {movie_tmdb_id}")
        if not movie_tmdb_id:
            logger.error("Cannot find movie node: No Id")
            return False
        if not studio_id:
            logger.error("Cannot find studio node: No Id")
            return False
        parameters = {
            'studio_id' : studio_id,
            'movie_id' : movie_tmdb_id,
        }
        query = """
        MATCH (m:Movie {tmdb_id: $movie_id})
        MATCH (s:Studio {id: $studio_id})
        MERGE (m)-[r:PRODUCED_BY]->(s)
        """
        session.run(query, parameters)
        logger.info(f"Created PRODUCED_BY: Studio {studio_id} -> Movie {movie_tmdb_id}")

        return True
    
    except Exception as e:
        logger.error(f"Failed to create Produced_By Relationship: {e}")
        return False


if __name__ == "__main__":
    """
    Code to test node creation functions


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
    """

    print("\n--- Testing Relationship ---")
    driver = get_driver()

    with driver.session() as session:
        """# Create David Fincher node FIRST (if it doesn't exist)
        print("Creating David Fincher node...")
        fincher_data = {
            'tmdb_id': 7467,
            'name': 'David Fincher',
            'profile_url': 'https://example.com/fincher.jpg'
        }
        success = create_person_node(session, fincher_data)
        print(f"David Fincher node: {success}")
        
        # Now create the relationship
        print("\nCreating DIRECTED relationship...")
        success = create_directed_relationship(
            session,
            person_tmdb_id=7467,
            movie_tmdb_id=550
        )
        print(f"DIRECTED relationship: {success}")
        drama_genre = {'name': 'Drama'}
        create_genre_node(session, drama_genre)

        # Then create the relationship
        success = create_in_genre_relationship(
            session,
            movie_tmdb_id=550,
            genre_name='Drama',
            is_primary=True
        )
        print(f"IN_GENRE relationship: {success}")"""
        print("\n--- Testing IN_GENRE Relationship ---")

        # Create Drama genre first
        drama_genre = {'name': 'Drama'}
        create_genre_node(session, drama_genre)

        # Create relationship
        success = create_in_genre_relationship(
            session,
            movie_tmdb_id=550,
            genre_name='Drama',
            is_primary=True
        )
        print(f"IN_GENRE relationship: {success}")
    driver.close()