import paramiko
from logger import logger
from kasse import linux_credentials


async def linux_pos(ip_host: str, command: str) -> str:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_host,
                    username=linux_credentials["login"],
                    password=linux_credentials["password"],
                    port=linux_credentials["port"]
                    )

        _, stdout, stderr = ssh.exec_command(command)

        if stdout:
            return stdout.read().decode('utf-8')
        if stderr:
            return stderr.read().decode('utf-8')

    except paramiko.AuthenticationException:
        await logger("Authentication failed. Check your username and password/keys.")
    except paramiko.SSHException as e:
        await logger(f"SSH connection error: {e}")
    except Exception as e:
        await logger(f"An unexpected error occurred: {e}")
    finally:
        ssh.close()
