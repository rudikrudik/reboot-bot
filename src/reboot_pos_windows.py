from pypsexec.client import Client
from kasse import windows_credentials

username = windows_credentials["login"]
password = windows_credentials["password"]


async def windows_pos(ip_host: str, executable: str, arguments: str) -> str:
    connect = Client(ip_host, username=username, password=password, encrypt=False)
    connect.connect()

    try:
        connect.create_service()
        result = connect.run_executable(executable, arguments=arguments)
    finally:
        connect.remove_service()
        connect.disconnect()

    if result[0]:
        return result[0].decode('ISO-8859-1')
    if result[1]:
        return result[1].decode('ISO-8859-1')
