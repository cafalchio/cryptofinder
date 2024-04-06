from app import app
from threading import Thread
from app.scheduler import start_scheduler


if __name__ == "__main__":
    scheduler_thread = Thread(target=start_scheduler)
    scheduler_thread.start()
    app.run(debug=True)
