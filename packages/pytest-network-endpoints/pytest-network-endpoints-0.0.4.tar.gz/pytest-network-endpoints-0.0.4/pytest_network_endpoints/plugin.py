from importlib import import_module
import pytest
import yaml
from typing import List

VERSION = "0.0.4"

# pytest fixtures


def pytest_addoption(parser):
    parser.addoption("--networkfile", type=str)


@pytest.fixture(scope="session")
def endpoints(request):
    network_file_path = request.config.getoption("--networkfile")
    if network_file_path:
        return create_endpoints_from_networkfile(network_file_path)
    else:
        return {}


# internals (eg. for standalone use outside pytest)


def create_endpoints_from_networkfile(network_file_path: str) -> dict:
    endpoints = {}
    with open(network_file_path) as network_file:
        network = yaml.full_load(network_file)
    for definition in network:
        if "name" in definition:
            endpoints[definition["name"]] = create_endpoint(definition)
    return endpoints


def get_endpoint_module_and_class(devtype: str) -> List[str]:
    # '.ssh' -> ['pytest_network_endpoints.ssh', 'SshEndpoint']
    # 'custom.my' -> ['custom.my', 'MyEndpoint']
    module_name_chunks = devtype.split(".")
    module_name_chunks[-1] = module_name_chunks[-1].split("-")[0]
    module_name = ".".join(module_name_chunks)
    if module_name[0] == ".":
        module_name = "pytest_network_endpoints" + module_name
    class_name_chunks = devtype.split(".")[-1].split("-")
    class_name = "".join([s.title() for s in class_name_chunks]) + "Endpoint"
    return module_name, class_name


def create_endpoint(definition: dict):
    module_name, class_name = get_endpoint_module_and_class(definition["type"])
    devmodule = import_module(module_name)
    devclass = getattr(devmodule, class_name)
    return devclass(definition)
