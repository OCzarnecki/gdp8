import os
from pathlib import Path
from aea.manager import MultiAgentManager

WORKING_DIR = "mam"

manager = MultiAgentManager(WORKING_DIR)
manager.start_manager()

from aea.configurations.base import PublicId

weather_station_id = PublicId.from_str("gdp8/env_aea:0.1.0")
weather_client_id = PublicId.from_str("fetchai/weather_client:0.28.0")
manager.add_project(weather_station_id)
manager.add_project(weather_client_id)
weather_station_name = weather_station_id.name
weather_client_name = weather_client_id.name

agent_overrides = {
    "private_key_paths": {"fetchai": "fetchai_private_key.txt"},
    "connection_private_key_paths": {"fetchai": "fetchai_connection_private_key.txt"}
}

p2p_public_id = PublicId.from_str("fetchai/p2p_libp2p:0.21.0")
soef_public_id = PublicId.from_str("fetchai/soef:0.22.0")

component_overrides = [{
    **p2p_public_id.json,
    "type": "connection",
    "cert_requests": [{
      "identifier": "acn",
      "ledger_id": "fetchai",
      "not_after": '2022-01-01',
      "not_before": '2021-01-01',
      "public_key": "fetchai",
      "message_format": "{public_key}",
      "save_path": "conn_cert.txt"
    }]
}, {
    **soef_public_id.json,
    "type": "connection",
    "config": {
        "token_storage_path": "soef_token.txt"
    }
}]
manager.add_agent(weather_station_id, component_overrides=component_overrides, agent_overrides=agent_overrides)

agent_overrides = {
    "private_key_paths": {"fetchai": "fetchai_private_key.txt"},
    "connection_private_key_paths": {"fetchai": "fetchai_connection_private_key.txt"}
}
component_overrides = [{
    **p2p_public_id.json,
    "type": "connection",
    "config": {
        "delegate_uri": "127.0.0.1:11001",
        "entry_peers": ['/dns4/127.0.0.1/tcp/9000/p2p/16Uiu2HAkzgZYyk25XjAhmgXcdMbahrHYi18uuAzHuxPn1KkdmLRw'],
        "local_uri": "127.0.0.1:9001",
        "public_uri": "127.0.0.1:9001",
    },
    "cert_requests": [{
      "identifier": "acn",
      "ledger_id": "fetchai",
      "not_after": '2022-01-01',
      "not_before": '2021-01-01',
      "public_key": "fetchai",
      "message_format": "{public_key}",
      "save_path": "conn_cert.txt"
    }]
}, {
    **soef_public_id.json,
    "type": "connection",
    "config": {
        "token_storage_path": "soef_token.txt"
    }
}]

manager.add_agent(weather_client_id, component_overrides=component_overrides, agent_overrides=agent_overrides)

FET_PRIVATE_KEY_STATION = b"72d3149f5689f0749eaec5ebf6dba5deeb1e89b93ae1c58c71fd43dfaa231e87"
FET_PRIVATE_KEY_PATH_STATION = Path(manager.data_dir, weather_station_name, "fetchai_private_key.txt").absolute()
FET_PRIVATE_KEY_PATH_STATION.write_bytes(FET_PRIVATE_KEY_STATION)

FET_CONNECTION_PRIVATE_KEY_STATION = b"bf529acb2546e13615ef6004c48e393f0638a5dc0c4979631a9a4bc554079f6f"
FET_CONNECTION_PRIVATE_KEY_PATH_STATION = Path(manager.data_dir, weather_station_name, "fetchai_connection_private_key.txt").absolute()
FET_CONNECTION_PRIVATE_KEY_PATH_STATION.write_bytes(FET_CONNECTION_PRIVATE_KEY_STATION)

FET_PRIVATE_KEY_CLIENT = b"589839ae54b71b8754a7fe96b52045364077c28705a1806b74441debcae16e0a"
FET_PRIVATE_KEY_PATH_CLIENT = Path(manager.data_dir, weather_client_name, "fetchai_private_key.txt").absolute()
FET_PRIVATE_KEY_PATH_CLIENT.write_bytes(FET_PRIVATE_KEY_CLIENT)

FET_CONNECTION_PRIVATE_KEY_CLIENT = b"c9b38eff57f678f5ab5304447997351edb08eceb883267fa4ad849074bec07e4"
FET_CONNECTION_PRIVATE_KEY_PATH_CLIENT = Path(manager.data_dir, weather_client_name, "fetchai_connection_private_key.txt").absolute()
FET_CONNECTION_PRIVATE_KEY_PATH_CLIENT.write_bytes(FET_CONNECTION_PRIVATE_KEY_CLIENT)

import time

manager.start_agent(weather_station_id.name)

# wait for ~10 seconds for peer node to go live
time.sleep(10.0)

manager.start_agent(weather_client_id.name)

time.sleep(5.0)

manager.stop_all_agents()

manager.stop_manager()