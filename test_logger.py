#test_logger.py
from logger import setup_logger, log_failed_movie

logger = setup_logger(__name__)

# Test different log levels
logger.debug("This is a DEBUG message - only in file")
logger.info("This is an INFO message - console and file")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")

# Test failed movie logging
log_failed_movie(12345, "API rate limit exceeded")
log_failed_movie(67890, "Network timeout")

logger.info("Check logs/ folder for ingest.log")
logger.info("Check data/ folder for failed_movies.txt")