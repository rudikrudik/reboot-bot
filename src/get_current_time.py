from datetime import datetime


def get_current_time() -> str:
    return datetime.now().strftime("%Y %m %d %H:%M")


print(get_current_time())