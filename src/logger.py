import aiofiles
from datetime import datetime


async def logger(text: str) -> None:
    current_date = datetime.now()
    print(f"{current_date} => {text}", flush=True)

    async with aiofiles.open("log.txt", "+a", encoding="utf-8") as aio_file:
        await aio_file.write(f"{current_date} => {text}\n")
