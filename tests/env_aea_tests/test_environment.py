import unittest
import random

from env_aea.skills.env_action_each_turn.environment import Environment, SimulationState, OfferWaterCommand, ReceiveWaterCommand, MoveCommand

@unittest.skip("AEA interface changed. Must figure out how to provide name and skill_context")
class TestEnvironment(unittest.TestCase):
    """ Tests for the environment _model_. Tests for the SimulationState, which
        actually do the heavy lifting, can be found in TestSimulationState
        below. """

    def setUp(self):
        self.env_model = Environment(
                size_x = 10,
                size_y = 10,
                initial_oasis_water = 1000,
                oasis_count = 10,
                initial_agent_water = 100,
                agent_mining_speed = 20,
                agent_max_capacity = 150,
                agent_count = 10,
                name = None,
                skill_context = None
        )

    def test_update_simulation_advances_turn_number_by_1(self):
        turn_number = self.env_model.turn_number
        self.env_model.start_next_simulation_turn()
        self.assertEqual(turn_number + 1, self.env_model.turn_number)

class TestSimulationState(unittest.TestCase):
    """ Tests for SimulationState. This is where (we verify that) the magic
        happens (correctly). """

    def setUp(self):
        # Make test runs deterministic
        random.seed(42)

    def create_state_with_defaults(
            self,
            size_x = 10,
            size_y = 10,
            initial_oasis_water = 1000,
            oasis_count = 10,
            agent_count = 40,
            initial_agent_water = 100,
            agent_mining_speed = 20,
            agent_max_capacity = 150):
        return SimulationState(size_x, size_y, initial_oasis_water, oasis_count,
                agent_count, initial_agent_water, agent_mining_speed,
                agent_max_capacity)

    def create_agent_pair(self, initial_water, max_capacity = 1000):
        # Two adjacent agents, without any oases
        state = self.create_state_with_defaults(
                size_x = 2,
                size_y = 1,
                oasis_count = 0,
                agent_count = 2,
                initial_agent_water = initial_water,
                agent_max_capacity = max_capacity
            )
        return (state, state.get_agent_by_pos(0, 0), state.get_agent_by_pos(1, 0))

    def create_agent_triple(self, initial_water, max_capacity = 1000):
        # Two adjacent agents, without any oases
        state = self.create_state_with_defaults(
                size_x = 3,
                size_y = 1,
                oasis_count = 0,
                agent_count = 3,
                initial_agent_water = initial_water,
                agent_max_capacity = max_capacity
            )
        return (state,
                state.get_agent_by_pos(0, 0),
                state.get_agent_by_pos(1, 0),
                state.get_agent_by_pos(2, 0))


    def test_agent_moving_out_of_the_map(self):
        state = self.create_state_with_defaults(agent_count=1)
        agents = state.get_agents_alive()
        agent = agents[0]
        ##map has size 10x10

        agent.pos_x = 0
        agent.pos_y = 5
        agent.queue_command(MoveCommand("left"))
        state.update_simulation()
        self.assertEqual(10, agent.pos_x)

        agent.pos_x = 10
        agent.pos_y = 5
        agent.queue_command(MoveCommand("right"))
        state.update_simulation()
        self.assertEqual(0, agent.pos_x)

        agent.pos_x = 5
        agent.pos_y = 0
        agent.queue_command(MoveCommand("up"))
        state.update_simulation()
        self.assertEqual(10, agent.pos_y)

        agent.pos_x = 5
        agent.pos_y = 10
        agent.queue_command(MoveCommand("down"))
        state.update_simulation()
        self.assertEqual(0, agent.pos_y)

        
    
    def test_agent_moving_to_a_spot_already_taken(self):
        state = self.create_state_with_defaults(agent_count=2)
        agents = state.get_agents_alive()
        agents[0].pos_x = 5
        agents[0].pos_y = 5
        agents[1].pos_x = 4
        agents[1].pos_y = 5
        agents[1].queue_command(MoveCommand("right"))
        state.update_simulation()
        ##making sure the agent didn't move
        self.assertEqual(4, agents[1].pos_x)
        self.assertEqual(5, agents[1].pos_y)
    
    def test_agent_moving_correctly(self):
        state = self.create_state_with_defaults(agent_count=1)
        agents = state.get_agents_alive()
        agent=agents[0]
        agent.pos_x = 5
        agent.pos_y = 5
        agent.queue_command(MoveCommand("up"))
        state.update_simulation()
        self.assertEqual(5, agent.pos_x)
        self.assertEqual(4, agent.pos_y)
        
        agent.pos_x = 5
        agent.pos_y = 5
        agent.queue_command(MoveCommand("down"))
        state.update_simulation()
        self.assertEqual(5, agent.pos_x)
        self.assertEqual(6, agent.pos_y)

        agent.pos_x = 5
        agent.pos_y = 5
        agent.queue_command(MoveCommand("right"))
        state.update_simulation()
        self.assertEqual(6, agent.pos_x)
        self.assertEqual(5, agent.pos_y)

        agent.pos_x = 5
        agent.pos_y = 5
        agent.queue_command(MoveCommand("left"))
        state.update_simulation()
        self.assertEqual(4, agent.pos_x)
        self.assertEqual(5, agent.pos_y)

    def test_all_agents_are_initially_alive(self):
        agent_count = 30
        state = self.create_state_with_defaults(agent_count = agent_count)
        agents_alive = state.get_agents_alive()
        self.assertEqual(agent_count, len(agents_alive),
                "number of agents alive should match the initial agent count before the first turn")

    def test_agent_ids_are_set_correctly(self):
        state = self.create_state_with_defaults()
        agents = state.get_agents_alive() # initially, all agents are alive
        for agent in agents:
            agent_by_id = state.get_agent_by_id(agent.agent_id)
            self.assertIs(agent, agent_by_id,
                    "`agent -> id -> agent` should return to the same object")

    def test_agent_positions_are_set_correctly(self):
        state = self.create_state_with_defaults()
        agents = state.get_agents_alive() # initially, all agents are alive
        for agent in agents:
            agent_by_pos = state.get_agent_by_pos(agent.pos_x, agent.pos_y)
            self.assertIs(agent, agent_by_pos,
                    "`agent -> pos -> agent` should return to the same object")

    def test_agent_water_is_set_correctly(self):
        initial_water = 66
        state = self.create_state_with_defaults(initial_agent_water = initial_water)
        agents = state.get_agents_alive() # initially, all agents are alive
        for agent in agents:
            self.assertIs(initial_water, agent.water,
                    "initially, the water of each agent should match the initial water")

    def test_agents_consume_water_each_turn(self):
        state = self.create_state_with_defaults(oasis_count = 0, agent_count = 1)
        the_agent = state.get_agents_alive()[0]
        initial_water = the_agent.water
        state.update_simulation()
        self.assertEqual(initial_water - 1, the_agent.water, "an agent should consume 1 water per turn")

    def test_agent_dies_after_all_water_is_consumed(self):
        initial_water = 20
        state = self.create_state_with_defaults(
                oasis_count = 0,
                agent_count = 1,
                initial_agent_water = initial_water
            )
        the_agent = state.get_agents_alive()[0]
        for _ in range(initial_water):
            self.assertTrue(the_agent in state.get_agents_alive(),
                    "an agent should be alive as long as it has water")
            state.update_simulation()
        self.assertFalse(the_agent in state.get_agents_alive(),
                "an agent should be dead once its water is 0")

    def test_agent_mines_as_much_water_as_possible_each_turn(self):
        initial_oasis_water = 25
        initial_agent_water = 10
        agent_mining_speed = 10
        state = self.create_state_with_defaults(
                size_x = 1,
                size_y = 1,
                initial_oasis_water = initial_oasis_water,
                oasis_count = 1,
                agent_count = 1,
                initial_agent_water = initial_agent_water,
                agent_mining_speed = agent_mining_speed,
                agent_max_capacity = 1000)
        the_agent = state.get_agents_alive()[0]
        self.assertEqual(25, state.get_cell_water(0, 0))
        self.assertEqual(10, the_agent.water)
        state.update_simulation()
        self.assertEqual(15, state.get_cell_water(0, 0)) # 25 - 10
        self.assertEqual(19, the_agent.water) # 10 + 10 - 1
        state.update_simulation()
        self.assertEqual(5, state.get_cell_water(0, 0)) # 15 - 10
        self.assertEqual(28, the_agent.water) # 19 + 10 - 1
        state.update_simulation()
        self.assertEqual(0, state.get_cell_water(0, 0)) # 5 - 5
        self.assertEqual(32, the_agent.water) # 28 + 5 - 1

    def test_agent_wont_mine_beyond_its_capacity(self):
        agent_capacity = 100
        oasis_water = 500
        state = self.create_state_with_defaults(
                size_x = 1,
                size_y = 1,
                initial_oasis_water = oasis_water,
                oasis_count = 1,
                agent_count = 1,
                initial_agent_water = agent_capacity,
                agent_max_capacity = agent_capacity
            )
        the_agent = state.get_agents_alive()[0]
        self.assertEqual(500, state.get_cell_water(0, 0))
        self.assertEqual(100, the_agent.water)
        state.update_simulation()
        self.assertEqual(500, state.get_cell_water(0, 0))
        self.assertEqual(99, the_agent.water)
        # The order of mining vs. consuming is not specified. What matters is
        # that the max capacity of an agent isn't exceeded.

    def test_unambiguous_water_transfer(self):
        initial_water = 10
        (state, left_agent, right_agent) = self.create_agent_pair(initial_water)
        left_agent.queue_command(OfferWaterCommand(5))
        right_agent.queue_command(ReceiveWaterCommand(5))
        self.assertEqual(10, left_agent.water)
        self.assertEqual(10, right_agent.water)
        state.update_simulation()
        self.assertEqual(4, left_agent.water)
        self.assertEqual(14, right_agent.water)

    def test_agent_can_give_only_as_much_as_they_have(self):
        initial_water = 10
        (state, left_agent, right_agent) = self.create_agent_pair(initial_water)
        left_agent.queue_command(OfferWaterCommand(100))
        right_agent.queue_command(ReceiveWaterCommand(100))
        self.assertEqual(10, left_agent.water)
        self.assertEqual(10, right_agent.water)
        state.update_simulation()
        self.assertEqual(0, left_agent.water)
        self.assertEqual(19, right_agent.water)

    def test_agent_cannot_receive_more_than_requested(self):
        initial_water = 15
        (state, left_agent, right_agent) = self.create_agent_pair(initial_water)
        left_agent.queue_command(OfferWaterCommand(10))
        right_agent.queue_command(ReceiveWaterCommand(5))
        self.assertEqual(15, left_agent.water)
        self.assertEqual(15, right_agent.water)
        state.update_simulation()
        self.assertEqual(9, left_agent.water)
        self.assertEqual(19, right_agent.water)

    def test_agent_cannot_receive_beyond_capacity(self):
        initial_water = 15
        (state, left_agent, right_agent) = self.create_agent_pair(
                initial_water,
                max_capacity = 20)
        left_agent.queue_command(OfferWaterCommand(10))
        right_agent.queue_command(ReceiveWaterCommand(10))
        self.assertEqual(15, left_agent.water)
        self.assertEqual(15, right_agent.water)
        state.update_simulation()
        self.assertEqual(9, left_agent.water)
        self.assertEqual(19, right_agent.water)

    def test_agents_can_transfer_water_they_mine(self):
        initial_water = 5
        state = self.create_state_with_defaults(
                size_x = 2,
                size_y = 1,
                oasis_count = 2,
                agent_count = 2,
                initial_agent_water = initial_water,
                agent_mining_speed = 10
            )
        left_agent = state.get_agent_by_pos(0, 0)
        right_agent = state.get_agent_by_pos(1, 0)
        left_agent.queue_command(OfferWaterCommand(10))
        right_agent.queue_command(ReceiveWaterCommand(10))
        self.assertEqual(5, left_agent.water)
        self.assertEqual(5, right_agent.water)
        state.update_simulation()
        self.assertEqual(4, left_agent.water)       # 5 + 10 - 10 - 1
        self.assertEqual(24, right_agent.water)     # 5 + 10 + 10 - 1

    def test_no_water_is_transfered_if_agents_are_not_adjacent(self):
        initial_water = 10
        state = self.create_state_with_defaults(
                size_x = 3,
                size_y = 1,
                oasis_count = 0,
                agent_count = 2,
                initial_agent_water = initial_water
            )
        agents = state.get_agents_alive()
        # Overwrite random positions for test
        left_agent = agents[0]
        right_agent = agents[1]
        left_agent.x = 0
        right_agent.x = 2
        state._agent_grid[0][0] = left_agent
        state._agent_grid[1][0] = None
        state._agent_grid[2][0] = right_agent
        # Test
        left_agent.queue_command(OfferWaterCommand(10))
        right_agent.queue_command(ReceiveWaterCommand(10))
        self.assertEqual(10, left_agent.water)
        self.assertEqual(10, right_agent.water)
        state.update_simulation()
        self.assertEqual(9, left_agent.water)
        self.assertEqual(9, right_agent.water)

    def test_unambiguous_transfer_to_two_agents(self):
        initial_water = 20
        (state, left_agent, center_agent, right_agent) = self.create_agent_triple(initial_water)
        left_agent.queue_command(ReceiveWaterCommand(5))
        center_agent.queue_command(OfferWaterCommand(10))
        right_agent.queue_command(ReceiveWaterCommand(5))
        self.assertEqual(20, left_agent.water)
        self.assertEqual(20, center_agent.water)
        self.assertEqual(20, right_agent.water)
        state.update_simulation()
        self.assertEqual(24, left_agent.water)
        self.assertEqual(9, center_agent.water)
        self.assertEqual(24, right_agent.water)

    def test_unambiguous_transfer_from_two_agents(self):
        initial_water = 20
        (state, left_agent, center_agent, right_agent) = self.create_agent_triple(initial_water)
        left_agent.queue_command(OfferWaterCommand(5))
        center_agent.queue_command(ReceiveWaterCommand(10))
        right_agent.queue_command(OfferWaterCommand(5))
        self.assertEqual(20, left_agent.water)
        self.assertEqual(20, center_agent.water)
        self.assertEqual(20, right_agent.water)
        state.update_simulation()
        self.assertEqual(14, left_agent.water)
        self.assertEqual(29, center_agent.water)
        self.assertEqual(14, right_agent.water)

    def test_ambiguous_transfer(self):
        initial_water = 20
        (state, left_agent, center_agent, right_agent) = self.create_agent_triple(initial_water)
        left_agent.queue_command(ReceiveWaterCommand(10))
        center_agent.queue_command(OfferWaterCommand(5))
        right_agent.queue_command(ReceiveWaterCommand(10))
        self.assertEqual(20, left_agent.water)
        self.assertEqual(20, center_agent.water)
        self.assertEqual(20, right_agent.water)
        state.update_simulation()
        self.assertEqual(19 + 19 + 5, left_agent.water + right_agent.water)
        self.assertEqual(19 - 5, center_agent.water)

    def test_running_simulation_for_a_long_time(self):
        state = self.create_state_with_defaults()
        for _ in range(5000):
            state.update_simulation()


