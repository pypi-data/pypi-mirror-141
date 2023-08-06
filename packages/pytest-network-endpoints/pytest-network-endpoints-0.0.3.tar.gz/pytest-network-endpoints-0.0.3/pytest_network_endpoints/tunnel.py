import sshtunnel
import logging

log = logging.getLogger(__name__)


def definition_to_args(tunnel_params: dict):
    # just rewrite yaml keys to what library constructor wants:
    targs = tunnel_params.copy()
    # provide ssh_address_or_host argument
    if "ssh_address_ip" in targs:
        if "ssh_address_port" in targs:
            targs["ssh_address_or_host"] = (
                targs["ssh_address_ip"],
                targs["ssh_address_port"],
            )
        else:
            targs["ssh_address_or_host"] = targs("ssh_address_ip")
    targs.pop("ssh_address_ip", None)
    targs.pop("ssh_address_port", None)
    # provide remote_bind_address and local_bind_adderss arguments
    for prefix in ["remote_bind_", "local_bind_"]:
        if f"{prefix}ip" in targs:
            if f"{prefix}port" in targs:
                targs[f"{prefix}address"] = (
                    targs[f"{prefix}ip"],
                    targs[f"{prefix}port"],
                )
            else:
                targs[f"{prefix}address"] = targs[f"{prefix}ip"]
        targs.pop(f"{prefix}ip", None)
        targs.pop(f"{prefix}port", None)
    return targs


class TunnelEndpoint:
    def __init__(self, definition: dict):
        """Provide definition dictionary containing 'tunnel_params' which matches
        sshtunnel.SSHTunnelForwarder.__init__ arguments with exception of:
        ssh_address_or_host tuple, which is split to:
            ssh_address_ip, ssh_address_port in yaml
        remote_bind_address tuple, which is split to:
            remote_bind_ip, remote_bind_port in yaml
        local_bind_address tuple, which is split to:
            local_bind_ip, local_bind_port in yaml
        for all above: if port is missing the only ip will be used
        Example yaml definition:
          - name: private-server
            type: .tunnel
            tunnel_params:
              ssh_address_ip: 127.0.0.1
              ssh_address_port: 22
              ssh_username: user
              ssh_password: pa$$w0rd
              remote_bind_ip: 192.168.0.25
              remote_bind_port: 2222
        """
        self.definition = {"tunnel_params": {}}
        self.definition.update(definition)
        tunnel_args = definition_to_args(self.definition["tunnel_params"])
        self.forwarder = sshtunnel.SSHTunnelForwarder(**tunnel_args)

    def start(self):
        self.forwarder.start()
        return self.forwarder

    def stop(self):
        self.forwarder.stop()

    def __enter__(self):
        self.forwarder.start()
        return self.forwarder

    def __exit__(self, *args):
        self.forwarder.stop()
