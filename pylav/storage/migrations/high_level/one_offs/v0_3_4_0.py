from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import Version

from pylav.constants.node import NODE_DEFAULT_SETTINGS
from pylav.constants.versions import VERSION_0_0_0, VERSION_0_3_4_0
from pylav.storage.migrations.logging import LOGGER

if TYPE_CHECKING:
    from pylav.core.client import Client


async def migration_v_0_3_4_0(client: Client, current_version: Version) -> None:
    if current_version >= VERSION_0_3_4_0 or current_version == VERSION_0_0_0:
        return

    LOGGER.info("Running %s migration", VERSION_0_3_4_0)
    config = client.node_db_manager.bundled_node_config()
    yaml_data = await config.fetch_yaml()
    if "soundgasm" not in yaml_data["plugins"]["dunctebot"]["sources"]:
        yaml_data["plugins"]["dunctebot"]["sources"]["soundgasm"] = True

    yaml_data["lavalink"]["plugins"] = NODE_DEFAULT_SETTINGS["lavalink"]["plugins"]
    await config.update_yaml(yaml_data)
    await client.lib_db_manager.update_bot_dv_version(VERSION_0_3_4_0)
