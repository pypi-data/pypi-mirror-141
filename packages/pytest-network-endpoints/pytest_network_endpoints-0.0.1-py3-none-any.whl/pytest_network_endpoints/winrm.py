from winrmcp import client
import base64
from dataclasses import dataclass
from winrm import Session
from winrmcp import Client
import logging

log = logging.getLogger(__name__)


@dataclass
class RawCmdResponse:
    """Class representing command response"""

    std_out: bytes
    std_err: bytes
    status_code: int


class WinrmEndpoint:
    def __init__(self, definition: dict):
        """Provide definition dictionary containing keys:
        'winrm_target' and 'winrm_auth' matching winrm.Session.__init__() args
        Additionaly 'winrm_params' key may be passed which should match
        positional arguments for winrm.Protocol.__init__() arguments
        Example yaml definition:
          - name: Windows
            type: .winrm
            winrm_target: 127.0.0.1
            winrm_auth:
              - user
              - pa$$word
            winrm_params:
              service: HTTP
              keytab: None
              ca_trust_path: legacy_requests
              cert_pem: None
              cert_key_pem: None
              server_cert_validation: validate
        """
        self.definition = {"winrm_params": {}}
        self.definition.update(definition)

    def raw(self, cmd: str, **user_winrm_params) -> RawCmdResponse:
        """Runs a command in remote CMD.EXE shell. Returns RawCmdResponse"""
        winrm_params = {**self.definition["winrm_params"], **user_winrm_params}
        session = Session(
            self.definition["winrm_target"],
            tuple(self.definition["winrm_auth"]),
            **winrm_params,
        )
        log.debug(
            f"{self.definition['name']}({session.url}) "
            f"executing command: {cmd}"
        )
        rmr = session.run_cmd(cmd)
        response = RawCmdResponse(rmr.std_out, rmr.std_err, rmr.status_code)
        log.debug(
            f"{self.definition['name']}({session.url}) "
            f"command response: {response}"
        )
        return response

    def cmd(self, cmd: str, **user_winrm_params) -> str:
        """Runs a command in remote CMD.EXE shell.
        Returns string with concatenated STDOUT and STDERR"""
        response = self.raw(cmd, **user_winrm_params)
        return response.std_out.decode() + response.std_err.decode()

    def file_put(
        self, local_path: str, remote_path: str, **user_winrm_params
    ) -> None:
        """Copies the content of local file local_file to the remote machine
        as remote_file"""
        winrm_params = {**self.definition["winrm_params"], **user_winrm_params}
        client = Client(
            self.definition["winrm_target"],
            tuple(self.definition["winrm_auth"]),
            **winrm_params,
        )
        log.debug(
            f"put file from {local_path} to "
            f"{self.definition['name']}({client.url}):{remote_path}"
        )
        client.copy(local_path, remote_path)


# MONKEY PATCHING OF MALFUNCT LIBRARY FUNCTION


def patch_upload_chunks(shell, file_path: str, max_chunks: int, fileobj):

    chunk_size = ((8000 - len(file_path)) // 4) * 3

    if max_chunks == 0:
        max_chunks = 1

    for _ in range(max_chunks):
        chunk = fileobj.read(chunk_size)
        assert isinstance(chunk, bytes)
        assert len(chunk) <= chunk_size

        if len(chunk) == 0:
            return True  # means "done"

        chunk = base64.b64encode(chunk).decode("ascii")
        shell.check_cmd("echo", chunk, ">>", file_path)

    return False  # not yet done, just max_chunks exhausted


client.upload_chunks = patch_upload_chunks
