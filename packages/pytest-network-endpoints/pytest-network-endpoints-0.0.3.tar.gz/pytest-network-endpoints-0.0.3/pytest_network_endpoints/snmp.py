from easysnmp import snmp_get, snmp_walk


class SnmpEndpoint(object):
    def __init__(self, definition):
        self.definition = {"snmp_params": {}}
        self.definition.update(definition)

    def get(self, oid, **user_params):
        params = {**self.definition["snmp_params"], **user_params}
        return snmp_get(oid, **params)

    def walk(self, oid, **user_params):
        params = {**self.definition["snmp_params"], **user_params}
        return snmp_walk(oid, **params)
