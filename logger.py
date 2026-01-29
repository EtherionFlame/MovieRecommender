import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='Flexgraph-Movie'):
    """
    Set up logger with console and file handlers

    Args:
        name: Logger name (use __name__ from calling module)
    
    Returns:
        logging.logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    formatter=logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S'
        )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    file_handler = RotatingFileHandler(
        'logs/ingest.log',
        maxBytes=5*1024*1024,   #5MB
        backupCount=3 #keep 3 old log files
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def log_failed_movie(movie_id, error_message):
    """
    Log a failed movie ID to file for retry later
    
    Args:
        movie_id: TMDB movie ID that failed
        error_message: Why it failed

    """

# TODO: Append to failed_movies.txt
# with open('data/failed_movies.txt', 'a') as f:
#     f.write(f"{movie_id}|{error_message}\n")
