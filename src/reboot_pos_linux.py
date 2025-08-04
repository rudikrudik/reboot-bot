import paramiko

# Server details
username = 'tc'
password = '324012'
port = 22
command_reboot = "/usr/bin/sudo /sbin/reboot"
command_get_started_process = "/usr/local/bin/cash status"


async def linux_pos(ip_host: str, command: str) -> str:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_host, username=username, password=password, port=port)
        stdin, stdout, stderr = ssh.exec_command(command)
        # Read the output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if output:
            return output
        if error:
            return error

    except paramiko.AuthenticationException:
        print("Authentication failed. Check your username and password/keys.")
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the connection
        ssh.close()
