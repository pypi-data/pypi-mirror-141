import os
from time import time
from pytest_network_endpoints.ssh import SshEndpoint


def test_ssh_raw(root: SshEndpoint):
    raw = root.raw("hostname")
    assert 0 == raw.status_code
    assert isinstance(raw.std_err, bytes)
    assert isinstance(raw.std_out, bytes)


def test_ssh_cmd(root: SshEndpoint):
    assert "Alpine" in root.cmd("cat /etc/os-release")


def test_sftp_get(tmp_path, root: SshEndpoint):
    tmp_file_path = tmp_path / "downloaded"
    root.sftp_get(str(tmp_file_path), "/etc/os-release")
    assert os.path.isfile(tmp_file_path)


def test_sftp_put(tmp_path, root: SshEndpoint):
    tmp_file_path = tmp_path / "for_upload"
    remote_path = "/tmp/uploaded"
    file_content = f"Lorem ipsum dolor sit amet {time()}"
    with open(tmp_file_path, "w") as tmp_file:
        tmp_file.write(file_content)
    root.sftp_put(str(tmp_file_path), remote_path)
    assert file_content in root.cmd(f"cat {remote_path}")


def test_ssh_alice(alice: SshEndpoint):
    assert "alice" == alice.cmd("whoami").strip()


def test_ssh_bob(bob: SshEndpoint):
    assert "bob" == bob.cmd("whoami").strip()
