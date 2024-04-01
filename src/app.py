from flask import Flask
import logging


app = Flask(__name__)

# define logger https://medium.com/@briankworld/logging-in-flask-introduction-and-practical-example-d2eeac0078b0
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
app.logger.addHandler(handler)


@app.route('/')
def hello():
    return 'Hello, World!'


# soh pra acessar o log do site
@app.route('/log')
def log():
    logs = []
    try:
        with open("./app.log", "r") as f:
            for i, line in enumerate(f.readlines()):
                logs.append(f"<p>{i} - {line}</p>")
        return "".join(logs)
    except FileNotFoundError:
        return "log file not found"


if __name__ == '__main__':
    app.run()
