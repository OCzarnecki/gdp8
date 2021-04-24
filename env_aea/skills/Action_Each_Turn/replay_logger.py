from datetime import datetime
from environment import SimulationState
import json

class ReplayLogger:
    """ Responsible for logging simulation state, for later
        visualisation. """

    def initialize(self, simulation_state):
        self._open_file()
        self._dump_json(simulation_state.get_header_object())

    def log_state(self, simulation_state):
        self._dump_json(simulation_state.serialize_current())

    def close(self):
        self._file.close()

    def __del__(self):
        if self._file.is_open():
            self.close()

    def _open_file(self):
        filename = datetime.now().strftime(
                "logs/simlog_%Y-%m-%d_%H.%M.%S.json")
        self._file = open(filename, "w")

    def _dump_json(self, obj):
        json.dump(obj, self._file)
