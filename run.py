from app.app import create_app
from app.config_app import DATABASE


flask_app = create_app()


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=True, port=10000)
