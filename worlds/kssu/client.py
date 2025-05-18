import logging
import time
import asyncio

from Utils import async_start
from NetUtils import ClientStatus
from typing import TYPE_CHECKING, Optional, Set, List, Dict
from .locations import location_lookup_by_name
from .items import treasures, item_lookup_by_id, BASE_ID
from random import Random

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    
# This is gunna take forever.
class KSSUClient(BizHawkClient):
    game = "Kirby Super Star Ultra"
    system = "NDS"
    patch_suffix = ".apkssu"
    local_checked_locations: Set[int]
    goal_flag: int
    ram_mem_domain = "Main RAM"
    goal_complete = False