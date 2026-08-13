import logging
import time
import asyncio
from enum import Enum

from Utils import async_start
from NetUtils import ClientStatus
from typing import TYPE_CHECKING, Optional, Set, List, Dict
from .items import treasures, BASE_ID
from random import Random

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    
class DeathState(Enum):
    alive = 0
    dead = 1
        
# This is gunna take forever.
# Yeah it did
class KSSUClient(BizHawkClient):
    game = "Kirby Super Star Ultra"
    system = "NDS"
    patch_suffix = ".apkssu"
    local_checked_locations: Set[int]
    goal_flag: int
    ram_mem_domain = "Main RAM"
    goal_complete = False
    received_items_count: int = 0
    
# Game Address Offsets
    # Current State
    current_game = 0x05B6A5
    current_stage = 0x05B6A6
    current_screen = 0x05B6A7
    
    # Kirby
    kirby_lifes = 0x05B824
    kirby_hp = 0x0771D4
    # Change to "Ability in kirby's mouth"
    kirby_ability = 0x0BAF7B
    candy_timer = 0x0BB22C
    
    # Spring Breeze
    spring_breeze_stages = 0x05BDFC
    
    # Dyna Blade
    iron_mam_defeated = 0x06C266
    
    # The Great Cave Offensive
    tgco_gold = 0x06E748
    
    # Gourmet
    gourmet_kirby_wins = 0x06D600
    ddd_race_1 = 0x06D664
    ddd_race_2 = 0x06D665
    ddd_race_3 = 0x06D666 # Don't need this
    
    # RoMK
    romk_chapters = 0x05BE6C
    
    # Milky Way Wishes
    mww_abilities = 0x071201
    mww_planets = 0x071190
    can_copy_enemies = 0x05B81A
    
    # Arena
    arena_wins = 0x06FFA2
    hth_wins = 0x06FD40
    
    # Minigames
    # Samurai
    samurai_wins = 0x0A8448
    
    # Megaton
    megaton_wins = 0x0A83D1
    
    # Kirby Card Swipe
    card_swipe_difficulty = 0x0B7774
    card_swipe_wins = 0x0B784A 
    
    # Kirby on the Draw
    draw_difficulty = 0x0B7894
    draw_pink_score = 0x0B789C
    draw_yellow_score = 0x0B78AC
    draw_red_score = 0x0B78BC
    draw_green_score = 0x0B78CC
    draw_ending = 0x0B78E0
    
    # Snack Tracks
    snack_difficulty = 0x0B8821
    snack_pink_score = 0x0B8206
    snack_yellow_score = 0x0B840A
    snack_red_score = 0x0B860E
    snack_green_score = 0x0B8812
    snack_timer = 0x0B8828
    
    # Generic
    header_offset = 0x3ffe00

# AP Address Offsets
    dyna_ap_stage = 0x360000
    dyna_ap_ex_stage = 0x360002
    dyna_ap_mam = 0x360004
    dyna_last_completed = 0x360006
    received_offset = 0x360008
    
    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.seed_verify = False
        self.datapackage_requested = False
        self.location_name_to_id = None
        
        self.deathlink_enabled = False
        self.received_deathlink = False
        
        # State tracking
        self.prev_stage: int | None = None
        self.prev_screen: int | None = None

        self.prev_sb_stage: int = 0
        self.prev_dyna_stage: int = 0
        self.prev_gourmet_win: int = 0
        self.prev_romk_win: int = 0
        self.prev_rotk_stage: int = 0
        
        self.prev_arena_wins: int = 0
        self.prev_true_arena_wins: int = 0
        self.prev_hth_wins: int = 0

        self.prev_samurai_wins: int = 0
        self.prev_megaton_wins: int = 0
        self.prev_card_swipe_wins: int = 0

        self.prev_draw_end: int = 0
        self.prev_snack_time: int = 0

        self.last_hp: int = 0
        self.suppress_deathlink: bool = False
        self.death_state = DeathState.alive
        self.last_death_link = 0
        
    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        header = await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.header_offset, 18, self.ram_mem_domain),
            )
        )
        if b'KIRBY USDX E' not in header[0]:
            return False
        if header[0] != b'KIRBY USDX EYKWE01':
            from CommonClient import logger
            logger.warning("Rom appears to be a non-US version of Kirby Super Star Ultra. "
                           "Please dump and use your copy of the US version, as it is the only supported version.")
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        return True
    
    # Deathlink not yet implemented
    # Function that kills player when deathlink is recieved
    async def deathlink_kill_player(self, ctx):
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(self.kirby_hp, (0).to_bytes(1, "little"), self.ram_mem_domain)]
        )
        # Set death state (to avoid mulitple deaths in a row)
        self.death_state = DeathState.dead
        self.last_death_link = time.time()


    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "DataPackage":
            self.location_name_to_id = args["data"]["games"][self.game]["location_name_to_id"]
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.received_deathlink = True     

    # Sending loaction function
    # Done with Name of game and location (Ex. Spring Breeze - Stage 1)            
    def get_location(self, game: str, label: str) -> int | None:
        name = f"{game} - {label}"
        return self.location_name_to_id.get(name)
        
    # Main Function                
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        
        try:
            if ctx.slot_data is None:
                return
            
            # If deathlink is enabled in options, turn it on for client
            if ctx.slot_data:
                if "deathlink" in ctx.slot_data:
                    if ("DeathLink" not in ctx.tags) and ctx.slot_data["deathlink"]:
                        await ctx.update_death_link(True)
                        self.deathlink_enabled = True
                    # If (somehow) deathlink is in the tags but not enabled, turn it off
                    elif ("DeathLink" in ctx.tags) and not ctx.slot_data["deathlink"]:
                        await ctx.update_death_link(False)
                        self.deathlink_enabled = False
                else:
                    return
            
            if self.location_name_to_id is None:
                if not self.datapackage_requested:
                    await ctx.send_msgs([{"cmd": "GetDataPackage", "games": [self.game]}])
                    self.datapackage_requested = True
                    logger.info("Awaiting datapackage...")
                return
            
            send_locations: Set[int] = set()
            
            # Convert addresses into variables used for client
            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    # Generic 
                    (self.current_game, 1, self.ram_mem_domain),   
                    (self.current_stage, 1, self.ram_mem_domain),       
                    (self.current_screen, 1, self.ram_mem_domain),    
                    
                    # Kirby Attributes
                    (self.kirby_lifes, 1, self.ram_mem_domain),  
                    (self.kirby_hp, 1, self.ram_mem_domain),            
                    (self.kirby_ability, 1, self.ram_mem_domain),    
                    
                    # Spring Breeze
                    (self.spring_breeze_stages, 1, self.ram_mem_domain), 

                    # Dyna Blade
                    (self.iron_mam_defeated, 1, self.ram_mem_domain), 
                    
                    # TGCO
                    (self.tgco_gold, 1, self.ram_mem_domain), 
                    
                    # Gourmet Race
                    (self.gourmet_kirby_wins, 1, self.ram_mem_domain), 
                    (self.ddd_race_1, 1, self.ram_mem_domain), 
                    (self.ddd_race_2, 1, self.ram_mem_domain), 
                    (self.ddd_race_3, 1, self.ram_mem_domain), 
                    
                    # Milky Way Wishes
                    (self.mww_abilities, 4, self.ram_mem_domain), 
                    (self.mww_planets, 1, self.ram_mem_domain), 
                    (self.can_copy_enemies, 1, self.ram_mem_domain), 
      
                    # Arena
                    (self.arena_wins, 1, self.ram_mem_domain),          
                    (self.hth_wins, 2, self.ram_mem_domain),            
    
                    # Samurai Kirby
                    (self.samurai_wins, 1, self.ram_mem_domain),        

                    # Megaton Punch
                    (self.megaton_wins, 1, self.ram_mem_domain),        

                    # Kirby Card Swipe
                    (self.card_swipe_difficulty, 1, self.ram_mem_domain), 
                    (self.card_swipe_wins, 1, self.ram_mem_domain), 

                    # Kirby on the Draw
                    (self.draw_difficulty, 1, self.ram_mem_domain),     
                    (self.draw_pink_score, 2, self.ram_mem_domain),     
                    (self.draw_yellow_score, 2, self.ram_mem_domain),   
                    (self.draw_red_score, 2, self.ram_mem_domain),      
                    (self.draw_green_score, 2, self.ram_mem_domain),    
                    (self.draw_ending, 2, self.ram_mem_domain),         

                    # Snack Tracks
                    (self.snack_difficulty, 1, self.ram_mem_domain),    
                    (self.snack_pink_score, 2, self.ram_mem_domain),    
                    (self.snack_yellow_score, 2, self.ram_mem_domain),  
                    (self.snack_red_score, 2, self.ram_mem_domain),     
                    (self.snack_green_score, 2, self.ram_mem_domain),   
                    (self.snack_timer, 2, self.ram_mem_domain),         
                    
                    # AP-Specific
                    (self.received_offset, 2, self.ram_mem_domain),        
                    (self.dyna_ap_stage, 1, self.ram_mem_domain),        
                    (self.dyna_ap_ex_stage, 1, self.ram_mem_domain),       
                    (self.dyna_last_completed, 1, self.ram_mem_domain),       
                    
                    # Stuff I forgot along the way and now have to add later   
                    (self.romk_chapters, 1, self.ram_mem_domain),    
                ]
            )
            
            game  = int.from_bytes(read_state[0], "little")
            stage = int.from_bytes(read_state[1], "little")
            screen = int.from_bytes(read_state[2], "little")
            
            lifes = int.from_bytes(read_state[3], "little")
            hp = int.from_bytes(read_state[4], "little")
            ability = int.from_bytes(read_state[5], "little")
            
            sb_stage = int.from_bytes(read_state[6], "little")
            
            iron_mam = int.from_bytes(read_state[7], "little")
            
            gold = int.from_bytes(read_state[8], "little")
            
            gourmet_wins = int.from_bytes(read_state[9], "little")
            ddd_flag_1 = int.from_bytes(read_state[10], "little")
            ddd_flag_2 = int.from_bytes(read_state[11], "little")
            ddd_flag_3 = int.from_bytes(read_state[12], "little")
            
            unlocked_abilities = int.from_bytes(read_state[13], "little")
            planets = int.from_bytes(read_state[14], "little")
            copy_flag = int.from_bytes(read_state[15], "little")

            arena = int.from_bytes(read_state[16], "little")
            hth = int.from_bytes(read_state[17], "little")

            samurai = int.from_bytes(read_state[18], "little")
            megaton = int.from_bytes(read_state[19], "little")

            card_difficulty = int.from_bytes(read_state[20], "little")
            card_score = int.from_bytes(read_state[21], "little")

            draw_difficulty = int.from_bytes(read_state[22], "little")
            draw_pink = int.from_bytes(read_state[23], "little")
            draw_yellow = int.from_bytes(read_state[24], "little")
            draw_red = int.from_bytes(read_state[25], "little")
            draw_green = int.from_bytes(read_state[26], "little")
            draw_timer = int.from_bytes(read_state[27], "little")

            snack_difficulty = int.from_bytes(read_state[28], "little")
            snack_pink = int.from_bytes(read_state[29], "little")
            snack_yellow = int.from_bytes(read_state[30], "little")
            snack_red = int.from_bytes(read_state[31], "little")
            snack_green = int.from_bytes(read_state[32], "little")
            snack_timer = int.from_bytes(read_state[33], "little")
            
            received_sav = int.from_bytes(read_state[34], "little")
            dyna_prog_stages = int.from_bytes(read_state[35], "little")
            dyna_ex_stages = int.from_bytes(read_state[36], "little")
            dyna_prev_complete = int.from_bytes(read_state[37], "little")
            
            romk_chapters_completed = int.from_bytes(read_state[38], "little")
            
            # Item Handling
            for index in range(min(self.received_items_count, received_sav), len(ctx.items_received)):
                network_item = ctx.items_received[index]
                name = ctx.item_names.lookup_in_game(network_item.item)

                match name:
                    case "Invincible Candy":
                        await self.bizhawk_add_halfword(ctx, self.candy_timer, 1320)

                # Keep APSave updated
                if index >= received_sav:
                    await self.bizhawk_set_halfword(ctx, self.received_offset, index + 1)

                self.received_items_count = index + 1
                await asyncio.sleep(0.1)
            
            # Location Handeling
            # Spring Breeze
            if game == 0:  
                game_name = "Spring Breeze"
                # The last stage saved is not the same as completed stages (A stage has been completed)
                if sb_stage > self.prev_sb_stage:
                    # For each stage 1 - 4
                    for i in range(self.prev_sb_stage + 1, sb_stage + 1):               
                        loc = self.get_location(game_name, f"Stage {i}")
                        if loc is not None:
                            send_locations.add(loc)

            # Dyna Blade 
            if game == 1: 
                game_name = "Dyna Blade"
                # The last stage saved is not the same as completed stages (A stage has been completed)
                if dyna_prev_complete > self.prev_dyna_stage:
                    # For each stage 1 - 5
                    for i in range(self.prev_dyna_stage + 1, dyna_prev_complete + 1):               
                        loc = self.get_location(game_name, f"Stage {i}")
                        if loc is not None:
                            send_locations.add(loc)
                            
                if iron_mam == 8:
                    loc = self.get_location(game_name, f"Iron Mam")
                    if loc is not None:
                        send_locations.add(loc)

                if self.prev_dyna_stage == 5:
                    loc = self.get_location(game_name, "Complete")
                    if loc is not None:
                        send_locations.add(loc)
                        
            # Gourmet Race
            if game == 2:
                game_name = "Gourmet Race"
                if gourmet_wins > self.prev_gourmet_win:
                    
                    # Introducing the worst code ever
                    if gourmet_wins == 1:
                        # Did DDD win round 2?
                        if ddd_flag_2 == 2:
                            round_won = 3
                        # Did DDD win round 1?
                        elif ddd_flag_1 == 2:
                            round_won = 2
                        else:
                            round_won = 1
                    elif gourmet_wins == 2:
                        # Did DDD win round 1 or round 2?
                        if (ddd_flag_1 == 2) or (ddd_flag_2 == 2):
                            round_won = 3
                        else:
                            round_won = 2
                    elif gourmet_wins == 3:
                        round_won = 3

                    loc = self.get_location(game_name, f"Win Round {round_won}")
                    if loc is not None:
                        send_locations.add(loc)

            # The Great Cave Offensive 
            # Dreadful
            if game == 3:
                game_name = "The Great Cave Offensive"

            # Revenge of Meta Knight
            if game == 4:  
                game_name = "Revenge of Meta Knight"
                if romk_chapters_completed > self.prev_romk_win:
                    # For each chapter 1 - 7
                    for i in range(self.prev_romk_win + 1, romk_chapters_completed + 1):               
                        loc = self.get_location(game_name, f"Stage {i}")
                        if loc is not None:
                            send_locations.add(loc)

            # Milky Way Wishes
            # Dreadful: Part 2
            if game == 5:
                game_name = "Milky Way Wishes"

            # Revenge of the King 
            if game == 6:  
                game_name = "Revenge of the King"


            # Arena
            if game == 7:  # The Arena
                game_name = "The Arena"
                if arena > self.prev_arena_wins:
                    if arena == 1:
                        label = "1 Straight Win"
                    else:
                        label = f"{arena} Straight Wins"           
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)

            # Meta Knightmare Ultra
            if game == 8: 
                game_name = "Meta Knightmare Ultra"
                if stage > 0:
                    if self.prev_stage is None or stage != self.prev_stage:
                        loc = self.get_location(game_name, f"Level {stage}")
                        if loc is not None:
                            send_locations.add(loc)
                if stage == 4: # Fix
                    loc = self.get_location(game_name, "Level 5")
                    if loc is not None:
                        send_locations.add(loc)

            # Helper to Hero 
            if game == 9:
                game_name = "Helper to Hero"
                if arena > self.prev_arena_wins:
                    if arena == 1:
                        label = "1 Straight Win"
                    else:
                        label = f"{arena} Straight Wins"          
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)

            # True Arena 
            if game == 10: 
                game_name = "The True Arena"
                if arena > self.prev_arena_wins:
                    if arena == 1:
                        label = "1 Straight Win"
                    else:
                        label = f"{arena} Straight Wins"
                        
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)

            # --- Minigames ---
            # Megaton Punch
            if megaton != self.prev_megaton_wins:
                game_name = "Megaton Punch"

                labels = {
                    1: "Waddle Dee",
                    2: "Knuckle Joe",
                    3: "Iron Mam",
                }
                
                label = labels.get(megaton)
                if label:
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)

            # Samurai Kirby
            if samurai != self.prev_samurai_wins:
                game_name = "Samurai Kirby"

                labels = {
                    1: "Waddle Doo",
                    2: "Wheelie",
                    3: "Chef Kawasaki",
                    4: "King Dedede",
                    5: "Meta Knight",
                }
            
                label = labels.get(samurai)
                if label:
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)

            # Kirby Card Swipe
            if card_score == 3 and card_difficulty in (0, 1, 2):
                game_name = "Kirby Card Swipe"
                level = card_difficulty + 1
                loc = self.get_location(game_name, f"Level {level}")
                if loc is not None:
                    send_locations.add(loc)

            # Kirby on the Draw
            if draw_timer == 776 and draw_difficulty in (0, 1, 2):
                game_name = "Kirby on the Draw"
                
                if draw_pink > max(draw_yellow, draw_red, draw_green):
                    level = draw_difficulty + 1
                    loc = self.get_location(game_name, f"Level {level}")
                    if loc is not None:
                        send_locations.add(loc)

            # Snack Tracks
            if snack_timer == 3600 and snack_difficulty in (0, 1, 2):
                game_name = "Snack Tracks"
                
                if snack_pink > max(snack_yellow, snack_red, snack_green):
                    level = snack_difficulty + 1
                    loc = self.get_location(game_name, f"Level {level}")
                    if loc is not None:
                        send_locations.add(loc)

            # --- DeathLink ---
            # Need a better way to track player in-game.


            # --- Send locations if changed ---
            if send_locations != self.local_checked_locations:
                self.local_checked_locations = send_locations
                if send_locations is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(send_locations)}])

            # --- Update previous state ---
            self.prev_screen = screen
            self.last_hp = hp

            self.prev_sb_stage = sb_stage
            self.prev_dyna_stage = dyna_prev_complete
            
            self.prev_arena_wins = arena
            self.prev_true_arena_wins = arena
            self.prev_hth_wins = hth

            self.prev_samurai_wins = samurai
            self.prev_megaton_wins = megaton           
                        
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass

    async def bizhawk_set_flag(self, ctx: "BizHawkClientContext", address: int, bit: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_bits = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, (current_bits | (1 << bit)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_2x_set_flag(self, ctx: "BizHawkClientContext",
                                  address_1: int, bit_1: int, address_2: int, bit_2: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address_1, 1, self.ram_mem_domain),
                (address_2, 1, self.ram_mem_domain),
            ]
        )
        current_bits_1 = int.from_bytes(read_state[0])
        current_bits_2 = int.from_bytes(read_state[1])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address_1, (current_bits_1 | (1 << bit_1)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain),
                (address_2, (current_bits_2 | (1 << bit_2)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain),
            ],
        )

    async def bizhawk_unset_flag(self, ctx: "BizHawkClientContext", address: int, bit: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_bits = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, (current_bits & ~(1 << bit)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_increase_byte(self, ctx: "BizHawkClientContext", address: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_byte = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, min(current_byte + 1, 255).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_halve_byte(self, ctx: "BizHawkClientContext", address: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_byte = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, (current_byte // 2).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_is_byte_equal(self, ctx: "BizHawkClientContext", address: int, byte: int) -> bool:
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        read_byte = int.from_bytes(read_state[0])
        return read_byte == byte

    async def bizhawk_2x_is_byte_equal(self, ctx: "BizHawkClientContext",
                                       address_1: int, byte_1: int,
                                       address_2: int, byte_2: int) -> bool:
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address_1, 1, self.ram_mem_domain),
                (address_2, 1, self.ram_mem_domain),
            ]
        )
        read_byte_1 = int.from_bytes(read_state[0])
        read_byte_2 = int.from_bytes(read_state[1])
        return read_byte_1 == byte_1 and read_byte_2 == byte_2

    async def bizhawk_set_halfword(self, ctx: "BizHawkClientContext", address: int, halfword: int) -> None:
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, halfword.to_bytes(length=2, byteorder="little"),self.ram_mem_domain)
            ]
        )

    async def bizhawk_add_halfword(self, ctx: "BizHawkClientContext", address: int, amount: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 2, self.ram_mem_domain),
            ]
        )
        current = int.from_bytes(read_state[0], "little")
        new_value = min(current + amount, 0xFFFF)
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, new_value.to_bytes(2, "little"), self.ram_mem_domain)
            ]
        )
