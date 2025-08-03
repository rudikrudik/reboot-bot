import time
from datetime import datetime


def get_current_time() -> str:
    return str(datetime.now())


def get_current_version() -> str:
    return "v1"


while True:
    print(f"{get_current_version()} Current time is:", get_current_time(), flush=True)
    time.sleep(10)
    