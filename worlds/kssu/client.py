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
class KSSUClient(BizHawkClient):
    game = "Kirby Super Star Ultra"
    system = "NDS"
    patch_suffix = ".apkssu"
    local_checked_locations: Set[int]
    goal_flag: int
    ram_mem_domain = "Main RAM"
    goal_complete = False
    
# Game Address Offsets
    # Generic
    unlock_games = 0x05c174
    unlock_true_arena = 0x05C175
    ignore_game_notice = 0x05C176
    ignore_arena_notice = 0x05C177
    
    # Current State
    current_game = 0x05B6A5
    current_stage = 0x05B6A6
    current_screen = 0x05B6A7
    transition_state = 0x05B6A4
    
    # Kirby
    kirby_lifes = 0x05B824
    kirby_hp = 0x0771D4
    kirby_ability = 0x0BAF7B
    
    # Dyna Blade
    dyna_blade_stages = 0x05BE0A
    dyna_blade_extras = 0x06C26A
    
    # TGCO
    tgco_treasure_count = 0x06E752
    tgco_gold = 0x06E748
    
    # Gourmet
    gourmet_wins = 0x05BE3C
    
    # MWW
    mww_abilities = 0x071201
    mww_plants = 0x071190
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

# AP Address Offsets
    received_offset = 0x29EAC0
    deathlink_flags = 0x29EAC1
    
    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.seed_verify = False
        self.datapackage_requested = False
        self.location_name_to_id = None
        
        self.deathlink_enabled = False
        self.received_deathlink = False
        
        # State tracking
        self.prev_game: int | None = None
        self.prev_stage: int | None = None
        self.prev_transition: int | None = None

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
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        return True
    
    async def deathlink_kill_player(self, ctx):
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(self.kirby_hp, (0).to_bytes(1, "little"), self.ram_mem_domain)]
        )
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
                
    def get_location(self, game: str, label: str) -> int | None:
        name = f"{game} - {label}"
        return self.location_name_to_id.get(name)
                    
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        
        try:
            if ctx.slot_data is None:
                return
            
            if ctx.slot_data:
                if "deathlink" in ctx.slot_data:
                    if ("DeathLink" not in ctx.tags) and ctx.slot_data["deathlink"]:
                        await ctx.update_death_link(True)
                        self.deathlink_enabled = True
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

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (self.current_game, 1, self.ram_mem_domain),        # 0
                    (self.current_stage, 1, self.ram_mem_domain),       # 1
                    (self.transition_state, 1, self.ram_mem_domain),    # 2
                    (self.kirby_hp, 1, self.ram_mem_domain),            # 3

                    (self.arena_wins, 1, self.ram_mem_domain),          # 4
                    (self.hth_wins, 2, self.ram_mem_domain),            # 5
    
                    # Samurai Kirby
                    (self.samurai_wins, 1, self.ram_mem_domain),        # 6

                    # Megaton Punch
                    (self.megaton_wins, 1, self.ram_mem_domain),        # 7

                    # Kirby Card Swipe
                    (self.card_swipe_difficulty, 1, self.ram_mem_domain),  # 8
                    (self.card_swipe_wins, 1, self.ram_mem_domain),  # 9

                    # Kirby on the Draw
                    (self.draw_difficulty, 1, self.ram_mem_domain),     # 10
                    (self.draw_pink_score, 2, self.ram_mem_domain),     # 11
                    (self.draw_yellow_score, 2, self.ram_mem_domain),   # 12
                    (self.draw_red_score, 2, self.ram_mem_domain),      # 13
                    (self.draw_green_score, 2, self.ram_mem_domain),    # 14
                    (self.draw_ending, 2, self.ram_mem_domain),         # 15

                    # Snack Tracks
                    (self.snack_difficulty, 1, self.ram_mem_domain),    # 16
                    (self.snack_pink_score, 2, self.ram_mem_domain),    # 17
                    (self.snack_yellow_score, 2, self.ram_mem_domain),  # 18
                    (self.snack_red_score, 2, self.ram_mem_domain),     # 19
                    (self.snack_green_score, 2, self.ram_mem_domain),   # 20
                    (self.snack_timer, 2, self.ram_mem_domain),         # 21
                ]
            )
            
            curr  = int.from_bytes(read_state[0], "little")
            stage = int.from_bytes(read_state[1], "little")
            trans = int.from_bytes(read_state[2], "little")
            hp = int.from_bytes(read_state[3], "little")

            arena = int.from_bytes(read_state[4], "little")
            hth = int.from_bytes(read_state[5], "little")

            samurai = int.from_bytes(read_state[6], "little")
            megaton = int.from_bytes(read_state[7], "little")

            card_difficulty = int.from_bytes(read_state[8], "little")
            card_score = int.from_bytes(read_state[9], "little")

            draw_difficulty = int.from_bytes(read_state[10], "little")
            draw_pink = int.from_bytes(read_state[11], "little")
            draw_yellow = int.from_bytes(read_state[12], "little")
            draw_red = int.from_bytes(read_state[13], "little")
            draw_green = int.from_bytes(read_state[14], "little")
            draw_timer = int.from_bytes(read_state[15], "little")

            snack_difficulty = int.from_bytes(read_state[16], "little")
            snack_pink = int.from_bytes(read_state[17], "little")
            snack_yellow = int.from_bytes(read_state[18], "little")
            snack_red = int.from_bytes(read_state[19], "little")
            snack_green = int.from_bytes(read_state[20], "little")
            snack_timer = int.from_bytes(read_state[21], "little")

            # Spring Breeze
            if curr == 0:  # Spring Breeze
                game_name = "Spring Breeze"
                if stage > 0:
                    if self.prev_stage is None or stage != self.prev_stage:
                        loc = self.get_location(game_name, f"Stage {stage}")
                        if loc is not None:
                            send_locations.add(loc)

                # Completion check: Stage 3 + transition = 3
                if stage == 3 and trans == 3:
                    loc = self.get_location(game_name, "Stage 4")
                    if loc is not None:
                        send_locations.add(loc)

            # Dyna Blade 
            if curr == 1:  # Dyna Blade
                game_name = "Dyna Blade"
                if stage > 0:
                    if self.prev_stage is None or stage != self.prev_stage:
                        loc = self.get_location(game_name, f"Stage {stage}")
                        if loc is not None:
                            send_locations.add(loc)

                if stage == 4 and trans == 3:
                    loc = self.get_location(game_name, "Complete")
                    if loc is not None:
                        send_locations.add(loc)

            # The Great Cave Offensive
            if curr == 3:
                game_name = "The Great Cave Offensive"

            # Revenge of Meta Knight
            if curr == 4:  
                game_name = "Revenge of Meta Knight"
                if stage > 0:
                    if self.prev_stage is None or stage != self.prev_stage:
                        loc = self.get_location(game_name, f"Chapter {stage}")
                        if loc is not None:
                            send_locations.add(loc)
                if stage == 6 and trans == 3:
                    loc = self.get_location(game_name, "Chapter 7")
                    if loc is not None:
                        send_locations.add(loc)

            # Milky Way Wishes
            if curr == 5:
                game_name = "Milky Way Wishes"

            # Revenge of the King 
            if curr == 6:  
                game_name = "Revenge of the King"
                if stage > 0:
                    if self.prev_stage is None or stage != self.prev_stage:
                        loc = self.get_location(game_name, f"Stage {stage}")
                        if loc is not None:
                            send_locations.add(loc)
                if stage == 4 and trans == 3:
                    loc = self.get_location(game_name, "Stage 5")
                    if loc is not None:
                        send_locations.add(loc)
            # Arena
            if curr == 7:  # The Arena
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
            if curr == 8: 
                game_name = "Meta Knightmare Ultra"
                if stage > 0:
                    if self.prev_stage is None or stage != self.prev_stage:
                        loc = self.get_location(game_name, f"Level {stage}")
                        if loc is not None:
                            send_locations.add(loc)
                if stage == 4 and trans == 3:
                    loc = self.get_location(game_name, "Level 5")
                    if loc is not None:
                        send_locations.add(loc)

            # Helper to Hero 
            if curr == 9:
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
            if curr == 10: 
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
            if self.deathlink_enabled:
                in_gameplay = (trans == 0)
                alive = (0 < hp < 255 and hp != 28)
                just_died = (hp == 0 and self.last_hp > 0 and in_gameplay)

                # --- SEND DEATHLINK ---
                if (just_died and self.death_state == DeathState.alive and self.last_death_link + 1 < time.time() and not self.suppress_deathlink):
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} has died!")
                    self.death_state = DeathState.dead
                    self.last_death_link = time.time()

                # If HP > 0 and in gameplay, reset death state to alive
                elif alive and in_gameplay:
                    self.death_state = DeathState.alive
                    self.suppress_deathlink = False

                # --- RECEIVE DEATHLINK ---
                if "DeathLink" in ctx.tags and self.last_death_link + 1 < time.time():
                    if self.received_deathlink:
                        self.received_deathlink = False
                        await self.deathlink_kill_player(ctx)

            # --- Send locations if changed ---
            if send_locations != self.local_checked_locations:
                self.local_checked_locations = send_locations
                if send_locations is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(send_locations)}])

            # --- Update previous state ---
            self.prev_game = curr
            self.prev_stage = stage
            self.prev_transition = trans
            self.last_hp = hp

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
