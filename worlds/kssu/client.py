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
    unlock_games = 0x05c174
    unlock_true_arena = 0x05C175
    ignore_game_notice = 0x05C176
    ignore_arena_notice = 0x05C177
    current_game = 0x05B6A5
    current_stage = 0x05B6A6
    current_screen = 0x05B6A7
    transition_state = 0x05B6A4
    kirby_lifes = 0x05B824
    kirby_hp = 0x0771D4
    kirby_ability = 0x0BAF7B
    dyna_blade_stages = 0x05BE0A
    dyna_blade_extras = 0x06C26A
    tgco_treasure_count = 0x06E752
    tgco_gold = 0x06E748
    gourmet_wins = 0x05BE3C
    mww_abilities = 0x071201
    mww_plants = 0x071190
    can_copy_enemies = 0x05B81A
    arena_wins = 0x06FFA2
    hth_wins = 0x06FD40
    samurai_wins = 0x0A8448
    megaton_wins = 0x0A83D1
    card_swipe_wins = 0x0B784A 

# AP Address Offsets
    received_offset = 0x000000
    deathlink_flags = 0x000000
    
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
                    (self.received_offset, 2, self.ram_mem_domain),
                ]
            )
 '''


