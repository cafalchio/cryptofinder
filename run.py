from app.app import create_app
from app.config_app import get_logger

PORT = 10000
DEBUG = False
HOST = "0.0.0.0"

logger = get_logger()
flask_app = create_app()

if __name__ == "__main__":
    bar = {"-" * 30}
    logger.info(f"{bar}\nRunning Server: {HOST}:{PORT} Debug: {DEBUG}\n{bar}")
    flask_app.run(host=HOST, debug=DEBUG, port=PORT)
