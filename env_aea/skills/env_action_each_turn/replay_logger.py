import os
from datetime import datetime
import json

# from packages.gdp8.skills.env_action_each_turn.environment import SimulationState


class ReplayLogger:
    """ Responsible for logging simulation state, for later
        visualisation. """

    def __init__(self, filename=None):
        self._filename = filename
        self._file = None
        self._folder = "logs"

    def initialize(self, simulation_state):
        self._open_file()
        self._dump_json(simulation_state.get_header_object())

    def log_state(self, simulation_state):
        self._dump_json(simulation_state.serialize_current())

    def close(self):
        self._file.close()

    def __del__(self):
        if self._file and not self._file.closed:
            self.close()

    def _open_file(self):
        if self._filename is None:
            filename = datetime.now().strftime(
                "logs/simlog_%Y-%m-%d_%H.%M.%S.json")
        else:
            filename = self._filename
        if not os.path.exists(self._folder):
            os.mkdir(self._folder)
        self._file = open(filename, "w")

    def _dump_json(self, obj):
        json.dump(obj, self._file)
        self._file.write("\n")
