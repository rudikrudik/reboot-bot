import time
from get_current_time import get_current_time
from get_current_version import get_current_version


while True:
    print(f"{get_current_version()} Current time is:", get_current_time(), flush=True)
    time.sleep(10)
    