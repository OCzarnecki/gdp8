import json


class AddressMapping:
    """Provides id<->address mapping, based on a static mapping
       file."""

    def __init__(self, mapping_path, agent_count):
        self._mapping_path = mapping_path
        self._agent_count = agent_count

    def load(self):
        with open(self._mapping_path, "r") as file:
            self.mapping = json.load(file)
        self._addresses = [None] * (self._agent_count + 1)
        self._address_to_id = {}
        for agent_id_str in self.mapping:
            agent_id = int(agent_id_str)
            if agent_id <= self._agent_count:
                address = self.mapping[agent_id_str]
                self._addresses[agent_id] = address
                self._address_to_id[address] = agent_id

    def get_address_from_id(self, agent_id):
        return self._addresses[agent_id]

    def get_id_from_address(self, address):
        return self._address_to_id[address]
