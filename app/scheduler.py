import time
from datetime import datetime
import requests
from utils import run_compare_coins


def get_gmt_hour():
    """Fetches the current hour in GMT from an API."""
    response = requests.get("http://worldtimeapi.org/api/timezone/Etc/GMT")
    if response.status_code == 200:
        current_time = response.json()['datetime']
        gmt_hour = datetime.fromisoformat(current_time).hour
        return gmt_hour
    else:
        print("Failed to fetch the time from the API.")
        return None


def job_that_runs_daily():
    """Fetches and compares coin data, then updates logs and new coins found."""
    print("Running scheduled job...")
    run_compare_coins()  # Utilize the function from utils.py


def check_and_schedule():
    """Checks the current GMT hour and schedules the job if it matches the target hour, otherwise sleeps."""
    gmt_hour = get_gmt_hour()
    target_hour = 7  # Target hour in GMT

    if gmt_hour is not None:
        if gmt_hour == target_hour:
            print(f"It's {target_hour}:00 GMT, running the job...")
            job_that_runs_daily()
            # After running the job, sleep until past the target hour to avoid re-runs.
            # Sleep until the next hour.
            time.sleep((60 - datetime.utcnow().minute) * 60)
        else:
            # Calculate sleep time to wake up shortly before the target hour.
            hours_until_target = (target_hour - gmt_hour - 1) % 24
            sleep_time = hours_until_target * 3600 + \
                (60 - datetime.utcnow().minute) * 60
            print(
                f"Sleeping for {sleep_time} seconds until it's close to the target hour.")
            time.sleep(sleep_time)


def start_scheduler():
    while True:
        check_and_schedule()
