import icmplib


async def ping(host_ip: str) -> bool:
    try:
        # Asynchronous ping to a single host
        result = await icmplib.async_ping(host_ip, count=2)
        return result.is_alive

    except icmplib.exceptions.ICMPLibError as e:
        print(f"Error: {e}")
