import icmplib
from logger import logger


async def ping(host_ip: str) -> bool:
    try:
        result = await icmplib.async_ping(host_ip, count=2)
        return result.is_alive

    except icmplib.exceptions.ICMPLibError as e:
        await logger(f"Error icmplib: {e}")
