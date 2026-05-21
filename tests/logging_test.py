import os 
print (os.getcwd())

from src.logger import get_logger

if __name__ == "__main__":
    log = get_logger(__name__)
    log.info("Testing logger, if log file created, then test passed successfully.")