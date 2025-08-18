from pypsexec.client import Client
from logger import logger
from kasse import windows_credentials


async def windows_pos(ip_host: str, executable: str, arguments: str) -> str:
    try:
        client = Client(ip_host,
                        username=windows_credentials["login"],
                        password=windows_credentials["password"],
                        encrypt=False
                        )

        client.connect()
        client.create_service()
        stdout, stderr, rc = client.run_executable(executable, arguments=arguments)

        await logger(f"Pypsexec return code: {rc}")

        if stdout:
            return stdout.decode('ISO-8859-1')
        if stderr:
            return stderr.decode('ISO-8859-1')

    except Exception as error:
        await logger(f"Error pypexec: {error}")

    finally:
        client.remove_service()
        client.disconnect()
