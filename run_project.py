#! /usr/bin/python
# Start all agents using the MultiAgentManager
from aea.configurations.base import PublicId
from aea.manager import MultiAgentManager

def main():
    WORKING_DIR = "mam"
    manager = MultiAgentManager(WORKING_DIR)
    manager.start_manager()

    agent_aea_id = PublicId.from_str("gdp/agent_aea:0.1.0")
    env_aea_id = PublicId.from_str("gdp/env_aea:0.1.0")
    manager.add_project(agent_aea_id, local=True)
    manager.add_project(env_aea_id, local=True)

    manager.stop_manager

if __name__ == "__main__":
    main()
