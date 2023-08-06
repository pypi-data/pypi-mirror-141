from dataclasses import dataclass
import paramiko
import logging

log = logging.getLogger(__name__)


@dataclass
class RawCmdResponse:
    """Class representing command response"""

    std_out: bytes
    std_err: bytes
    status_code: int


class SshEndpoint:
    def __init__(self, definition: dict):
        """Provide definition dictionary containing 'ssh_params' which matches
        paramiko.client.SSHClient.connect() arguments
        Example yaml definition:
          - name: raspberry
            type: .ssh
            ssh_params:
              hostname: 127.0.0.1
              port: 2222
              username: user
              password: pass
              compress: False
              banner_timeout: None
        """
        self.definition = {"ssh_params": {}}
        self.definition.update(definition)

    def raw(self, cmd: str, **user_ssh_params) -> RawCmdResponse:
        """Execute a command on the SSH server. Returns SshResponse"""
        ssh = self.__connect(**user_ssh_params)
        log.debug(f"{self.__dbg_info(ssh)} executing command: {cmd}")
        _, stdout, stderr = ssh.exec_command(cmd)
        response = RawCmdResponse(
            stdout.read(), stderr.read(), stdout.channel.recv_exit_status()
        )
        log.debug(f"{self.__dbg_info(ssh)} command output: {response}")
        ssh.close()
        return response

    def cmd(self, cmd: str, **user_ssh_params) -> str:
        """Execute a command on the SSH server.
        Returns string with concatenated STDOUT and STDERR"""
        response = self.raw(cmd, **user_ssh_params)
        return response.std_out.decode() + response.std_err.decode()

    def sftp_get(
        self, local_path: str, remote_path: str, **user_ssh_params
    ) -> None:
        """Copy a remote file (remote_path) from the SFTP server
        to the local host as local_path.
        Any exception raised by operations will be passed through"""
        sftp = self.__open_sftp(**user_ssh_params)
        log.debug(
            f"sftp get from {self.__dbg_info(sftp.get_channel())}"
            f":{remote_path} to {local_path}"
        )
        sftp.get(remote_path, local_path)
        sftp.close()

    def sftp_put(
        self, local_path: str, remote_path: str, **user_ssh_params
    ) -> None:
        """Copy a local file (local_path) to the SFTP server as remote_path.
        Any exception raised by operations will be passed through."""
        sftp = self.__open_sftp(**user_ssh_params)
        log.debug(
            f"sftp put from {local_path} to "
            f"{self.__dbg_info(sftp.get_channel())}:{remote_path}"
        )
        sftp.put(local_path, remote_path)
        sftp.close()

    def __dbg_info(self, channel: paramiko.channel.Channel) -> str:
        peer_data = str(channel.get_transport().getpeername())
        return self.definition["name"] + peer_data

    def __connect(self, **user_ssh_params):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_params = {**self.definition["ssh_params"], **user_ssh_params}
        ssh.connect(**ssh_params)
        return ssh

    def __open_sftp(self, **user_ssh_params):
        ssh = self.__connect(**user_ssh_params)
        sftp = ssh.open_sftp()
        return sftp
