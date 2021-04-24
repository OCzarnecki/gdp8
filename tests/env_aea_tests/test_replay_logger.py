import os
import unittest

from datetime import datetime

from env_aea.skills.Action_Each_Turn.environment import SimulationState
from env_aea.skills.Action_Each_Turn.replay_logger import ReplayLogger

class TestReplayLogger(unittest.TestCase):
    """ Tests for ReplayLogger """

    def setUp(self):
        self._filename = datetime.now().strftime(
                "testfile_simlog_%Y-%m-%d_%H.%M.%S.json")

    def tearDown(self):
        # Remove the testfile, if it exists
        try:
            os.remove(self._filename)
        except OSError:
            pass

    def test_logging(self):
        """ Test if simulation can be logged without error.
            Correctnes of log was tested manually, because
            testing serialization code is very tedious, and
            it's not worth it."""
        state = SimulationState(
                size_x = 1,
                size_y = 1,
                initial_oasis_water = 100,
                oasis_count = 0,
                agent_count = 1,
                initial_agent_water = 100,
                agent_mining_speed = 20,
                agent_max_capacity = 150
            )

        logger = ReplayLogger(self._filename)

        logger.initialize(state)
        logger.log_state(state)
        state.update_simulation()
        logger.log_state(state)
        logger.close()
