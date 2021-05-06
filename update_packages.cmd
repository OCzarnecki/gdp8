rm -r packages/gdp8/skills/env_action_each_turn
cd env_aea
aea fingerprint skill gdp8/env_action_each_turn:0.1.0
aea --registry-path ../packages/ push --local skill gdp8/env_action_each_turn:0.1.0
cd ..

rm -r packages/gdp8/skills/agent_action_each_turn
cd Agent_aea
aea fingerprint skill gdp8/agent_action_each_turn:0.1.0
aea --registry-path ../packages/ push --local skill gdp8/agent_action_each_turn:0.1.0
cd ..
