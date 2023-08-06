import pytest
import docker
from conftest import wait_socket_open
from pytest_network_endpoints.ssh import SshEndpoint
from pytest_network_endpoints.tunnel import TunnelEndpoint


@pytest.fixture(scope="module", autouse=True)
def start_tunnel_server(tunnel: TunnelEndpoint):
    client = docker.from_env()
    tunnel_server = client.containers.run(
        "localhost/alpine-tunneler", detach=True, network_mode="host"
    )
    ip = tunnel.definition["tunnel_params"]["ssh_address_ip"]
    port = tunnel.definition["tunnel_params"]["ssh_address_port"]
    wait_socket_open((ip, port))
    yield tunnel_server
    tunnel_server.kill()


@pytest.fixture(scope="function")
def tunnel_connection(tunnel: TunnelEndpoint):
    yield tunnel.start()
    tunnel.stop()


def test_tunnel_as_context_manager(tunnel: TunnelEndpoint, alice: SshEndpoint):
    with tunnel as t:
        ip, port = t.local_bind_address
        assert "alice" == alice.cmd("whoami", hostname=ip, port=port).strip()


def test_tunnel_as_yield_fixture(tunnel_connection, bob: SshEndpoint):
    ip, port = tunnel_connection.local_bind_address
    assert "bob" == bob.cmd("whoami", hostname=ip, port=port).strip()
