
pytest-network-endpoints
========================

Pytest plugin for defining remote network nodes.
This plugin introduces **--networkfile** option and session scoped **endpoints** fixture which will contain automatically generated and configured clients for given type.

Predefined types avaiable:

+----------------+-------------------------------------------------+-------------------------------+
| yaml type key  | endpoint class                                  | comment                       |
+================+=================================================+===============================+
| .ssh           | pytest_network_endpoints.ssh.SshEndpoint        | wrapper for paramiko          |
+----------------+-------------------------------------------------+-------------------------------+
| .tunnel        | pytest_network_endpoints.tunnel.TunnelEndpoint  | wrapper for sshtunnel         |
+----------------+-------------------------------------------------+-------------------------------+
| .snmp          | pytest_network_endpoints.snmp.SnmpEndpoint      | wrapper for easysnmp          |
+----------------+-------------------------------------------------+-------------------------------+
| .winrm         | pytest_network_endpoints.winrm.WinrmEndpoint    | wrapper for pywinrm, winrmcp  |
+----------------+-------------------------------------------------+-------------------------------+

install
=======

.. code-block:: shell

   pip install pytest-network-endpoints

easysnmp may require additional binary packages on your system: https://easysnmp.readthedocs.io/en/latest/#installation

usage
=====

.. code-block:: shell

   pytest --networkfile=example.yml

example.yml
^^^^^^^^^^^

.. code-block:: yaml

   - name: host-1
     type: .ssh
     ssh_params:
       hostname: 192.0.2.13
       port: 2222
       username: root
       key_filename: config/id_ecdsa
       allow_agent: False

test_example.py
^^^^^^^^^^^^^^^

.. code-block:: python

   def test_ssh_server(endpoints):
       assert "root" in endpoints["host-1"].cmd("whoami")

test_smart.py
^^^^^^^^^^^^^

.. code-block:: python

   import pytest_network_endpoints.ssh.SshEndpoint

   @pytest.fixture
   def host1(endpoints) -> SshEndpoint:
       return devices["host-1"]

   def test_ssh_server(host1: SshEndpoint):
       assert "root" in host1.cmd("whoami")

please see `test <test>`_ directory for more usage examples

standalone
==========

This package can be used without pytest

.. code-block:: python

   from pytest_network_endpoints.plugin import create_endpoints_from_networkfile
   endpoints = create_endpoints_from_networkfile('path/to/networkfile.yml')
