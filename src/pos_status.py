from ping import ping
import asyncio
from reboot_pos_linux import linux_pos
from reboot_pos_windows import windows_pos
from logger import logger


async def ping_status(ip_host: str, count: int) -> bool:
    count_for_ping = 0

    while True:
        if count_for_ping == count:
            return False

        if not await ping(ip_host):
            return True

        await asyncio.sleep(1)
        count_for_ping += 1


async def reboot_status(ip_host: str, count: int) -> bool:
    count_for_reboot = 0

    while True:
        if count_for_reboot == count:
            return False

        if await ping(ip_host):
            return True

        await asyncio.sleep(1)
        count_for_reboot += 1


async def pos_program_status(ip_host: str, count: int, system: str) -> bool:
    count_for_program_process = 0

    while True:
        if count_for_program_process == count:
            return False

        if system == "linux":
            try:
                result = await linux_pos(ip_host, "/usr/local/bin/cash status")
                if result.find("YES") != -1:
                    return True
            except BaseException as error:
                await logger(f"Ошибка получения данных о кассовой системе linux: {error}")
                return False

        else:
            try:
                result = await windows_pos(ip_host, "tasklist", '/FI "IMAGENAME eq SCOTAppU.exe"')
                if result.find("SCOTAppU.exe") != -1:
                    return True
            except BaseException as error:
                await logger(f"Ошибка получения данных о кассовой системе windows: {error}")

        count_for_program_process += 1
        await asyncio.sleep(1)
