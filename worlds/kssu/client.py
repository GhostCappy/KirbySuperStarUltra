import logging
import time
import asyncio

from Utils import async_start
from NetUtils import ClientStatus
from typing import TYPE_CHECKING, Optional, Set, List, Dict
from .items import treasures, BASE_ID
from random import Random

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import data

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
    
# Game Address Offsets

# AP Address Offsets

    
    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.seed_verify = False
        self.received_deathlink = False
        self.location_name_to_id = None
    
    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        return True
    
    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "DataPackage":
            self.location_name_to_id = args["data"]["games"][self.game]["location_name_to_id"]
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.received_deathlink = True
                    
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        # Commented out so i dont have to see the error 
        '''
        try:
            if ctx.slot_data is None:
                return
            if self.location_name_to_id is None:
                if not self.datapackage_requested:
                    await ctx.send_msgs([{"cmd": "GetDataPackage", "games": [self.game]}])
                    self.datapackage_requested = True
                    logger.info("Awaiting datapackage...")
                return

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx, [
                    
                ]
            )
            
            # Return if save data not yet initialized, else it's 0xff, and that's bad
            # Also after booting the entire memory will be 0x00, which is also not good for receiving items
            if int.from_bytes(read_state[0]) == 0:
                return

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (self.received_offset, 2, self.ram_mem_domain),
                ]
            )

            received_in_sav = int.from_bytes(read_state[0], "little")
            
            for index in range(min(self.received_items_count, received_in_sav), len(ctx.items_received)):
                network_item = ctx.items_received[index]
                name = ctx.item_names.lookup_in_game(network_item.item)
                # temporary
                if name is None:
                    break
                self.received_items_count = index+1
                await asyncio.sleep(0.1)    
                
            # Check for location checks
            locations_to_send = set()

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [

                ]
            )
 '''


