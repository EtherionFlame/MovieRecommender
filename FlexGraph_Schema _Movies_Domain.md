# FlexGraph Schema - Movies Domain

## Node Types

### Movie
- tmdb_id (integer, unique)
- title (string)
- release_year (integer)
- rating (float)
- budget (integer, USD, nullable)
- revenue (integer, USD, nullable)
- overview (text)
- poster_url (string, nullable)

### Person
- tmdb_id (integer, unique)
- name (string)
- birth_year (integer, nullable)
- profile_url (string, nullable)

### Genre
- name (string, unique) - "Action", "Drama", etc.

## Relationship Types

### ACTED_IN
From: Person → Movie
Properties:
- character (string) - role name like "Tony Stark"
- order (integer) - billing position (1 = lead, 2 = supporting, etc.)

### DIRECTED
From: Person → Movie
Properties: None

### IN_GENRE
From: Movie → Genre
Properties:
- is_primary (boolean) - true for main genre, false for secondary