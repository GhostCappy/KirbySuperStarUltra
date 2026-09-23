''' 
Hello! If you're going through the client with the intent to learn how to make your own NDS APWorld:
Do not.

This is a very ugly fusion of BlastSlimey's Sonic Rush and Silvris's Kirby Super Star APWorlds.
As such, almost none of this code is the "best way" of going about things.
I would highly recommend checking out APQuest for documentation, 
and Pokemon Mystery Dungeon: Explorers of Sky for DS (Bizhawk) for specific functionality.

However, comments were left in the off-chance anyone is still interested in the code.
(And also to keep my sanity)
'''
import time
import asyncio

from NetUtils import ClientStatus
from typing import TYPE_CHECKING, Set, Dict
from .items import treasures, BASE_ID
from .locations import MWW_ABILITY_OFFSETS

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
        
# This is gunna take forever.
# Yeah it did
class KSSUClient(BizHawkClient):
    game = "Kirby Super Star Ultra"
    system = "NDS"
    patch_suffix = ".apkssu"
    local_checked_locations: Set[int]
    ram_mem_domain = "Main RAM"
    goal_complete = False
    received_items_count: int = 0
    datapackage_requested = False
    #item_queue: typing.List[NetworkItem] = []
    player_actionable = False
    
    cave_keys_collected = 0
    progressive_mku_level = 0
    rainbow_stars = 0
    new_gold = 0
    completed_games = 0
    
    # Game Address Offsets
    ## Current State
    current_game = 0x05B6A5
    current_stage = 0x05B6A6
    current_screen = 0x05B6A7
    unlock_true_arena = 0x05C175
    
    games_cleared = 0x05C158
    
    game_state = 0x042219
    
    ## Kirby
    kirby_lifes = 0x05B824
    kirby_hp = 0x0771D4
    candy_timer = 0x0BB22C
    
    ## Spring Breeze
    spring_breeze_stages = 0x05BDFC
    
    ## Dyna Blade
    iron_mam_defeated = 0x06C266
    
    ## The Great Cave Offensive
    tgco_gold = 0x06E748
    
    tgco_door1_room = 0x26EAD4
    tgco_door1_x = 0x26EAD6
    tgco_door1_y = 0x26EAD8
    
    tgco_door2_room = 0x26E720
    tgco_door2_x = 0x26E722
    tgco_door2_y = 0x26E724
    
    tgco_door3_room = 0x26E2FE
    tgco_door3_x = 0x26E300
    tgco_door3_y = 0x26E302
    
    ## Gourmet
    gourmet_kirby_wins = 0x06D600
    ddd_race_1 = 0x06D664
    ddd_race_2 = 0x06D665
    
    ## RoMK
    romk_chapters = 0x05BE6C
    
    ## Milky Way Wishes
    mww_abilities = 0x071201
    
    ## Arena
    arena_wins = 0x06FFA2
    hth_wins = 0x06FD40
    
    # RoTK
    rotk_stages = 0x05BE88
    
    # MKU
    mku_level = 0x05BEF5
    cannon_item = 0x04A55E
    cannon_real = 0x04A556
    
    ## Minigames
    ## Samurai
    samurai_wins = 0x0A8448
    
    ## Megaton
    megaton_wins = 0x0A83D1
    
    ## Kirby Card Swipe
    card_swipe_difficulty = 0x0B7774
    card_swipe_wins = 0x0B784A 
    
    ## Kirby on the Draw
    draw_difficulty = 0x0B7894
    draw_pink_score = 0x0B789C
    draw_yellow_score = 0x0B78AC
    draw_red_score = 0x0B78BC
    draw_green_score = 0x0B78CC
    draw_ending = 0x0B78E0
    
    ## Snack Tracks
    snack_difficulty = 0x0B8821
    snack_pink_score = 0x0B8206
    snack_yellow_score = 0x0B840A
    snack_red_score = 0x0B860E
    snack_green_score = 0x0B8812
    snack_timer = 0x0B8828
    
    ## Generic
    header_offset = 0x3ffe00

    # AP Address Offsets
    dyna_ap_stage = 0x360000
    dyna_ap_ex_stage = 0x360002
    single_use_recieved = 0x360004
    dyna_last_completed = 0x360006
    tgco_collected_1 = 0x360008
    tgco_collected_2 = 0x36000C
    mww_collected = 0x360010
    mww_unlocked_planets = 0x360018
    planets_completed = 0x36001A
    play_sound = 0x36001C
    games_unlocked = 0x360024
    tgco_received_1 = 0x360028
    tgco_received_2 = 0x36002C
    abilities_recieved = 0x360030
    received_offset = 0x360034
    dyna_switch_activated = 0x360038
    
    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.seed_verify = False
        self.location_name_to_id = None
        self.deathlink_enabled = False
        self.received_deathlink = False
     
    # Function checks if the USA version of Kirby Super Star Ultra is being used.
    # A good copy will have "KIRBY USDX E" in the header.
    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        header = await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.header_offset, 18, self.ram_mem_domain),
            )
        )
        if b'KIRBY USDX E' not in header[0]:
            return False
        # If the header is anything else, the wrong copy is being used.
        if header[0] != b'KIRBY USDX EYKWE01':
            from CommonClient import logger
            logger.warning("Rom appears to be a non-US version of Kirby Super Star Ultra. "
                           "Please dump and use your copy of the US version, as this is currently the only supported version.")
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

    # Sending loaction function
    # Done with name of game and location (Ex. Spring Breeze - Stage 1)     
    ## This will not work for TGCO treasures, so "game" gets overwritten later.
    ## This also will not work when foodsanity is added   
    def get_location(self, game: str, label: str) -> int | None:
        name = f"{game} - {label}"
        return self.location_name_to_id.get(name)
    
    # Deathlink not yet implemented
    # Function that kills player when deathlink is recieved
    async def deathlink_kill_player(self, ctx):
        # CHANGE WHEN FOUND
        if self.game_state == 5:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(self.kirby_hp, (0).to_bytes(1, "little"), self.ram_mem_domain)]
            )
            # Set death state (to avoid mulitple deaths in a row)
            self.last_death_link = time.time()
        else:
            pass

    async def play_sfx(self, ctx: "BizHawkClientContext", sfx: str) -> None:
        sound: dict[str, int] = {
            "Major": 67,
            "Filler": 68,
            "Treasure": 69,
            "Planet": 70,
            "Progressive": 71,
            "Ability": 72,
            "1-Up": 73,
        }
        await self.bizhawk_set_halfword(ctx, self.play_sound, sound.get(sfx, 0))
        
    async def in_game(self, ctx: "BizHawkClientContext", sfx: str) -> None:
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (self.game_state, 2, self.ram_mem_domain),
                (self.current_game, 1, self.ram_mem_domain),
            ]
        )
        in_game = int.from_bytes(read_state[0], "little")
        demo_check = int.from_bytes(read_state[1], "little")
    
        if in_game == 68 and demo_check != 11:
            self.player_actionable = True
        else:
            self.player_actionable = False
    
    async def queue_item(self, ctx: "BizHawkClientContext") -> None:
        pass
     
    
    # Main Function                
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        try:
            if ctx.slot_data is None:
                # logger.info("slot data not initialized")
                return   
            # else:
            # logger.info("slot data initialized correctly")
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
            
            # Actual code begins
            # Check for locations
            send_locations = set()
            
            # Convert addresses into variables used for client
            ## Strictly used for reading
            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (self.received_offset, 2, self.ram_mem_domain),
                    
                    (self.current_game, 1, self.ram_mem_domain),
                    (self.current_stage, 1, self.ram_mem_domain),
                    (self.current_screen, 1, self.ram_mem_domain),
                    
                    (self.spring_breeze_stages, 1, self.ram_mem_domain),
                    
                    (self.iron_mam_defeated, 1, self.ram_mem_domain),
                    
                    (self.tgco_gold, 4, self.ram_mem_domain),
                    
                    (self.gourmet_kirby_wins, 1, self.ram_mem_domain),
                    (self.ddd_race_1, 1, self.ram_mem_domain),
                    (self.ddd_race_2, 1, self.ram_mem_domain),
                    
                    (self.romk_chapters, 1, self.ram_mem_domain),
                    
                    (self.mww_abilities, 4, self.ram_mem_domain),
                    
                    (self.arena_wins, 1, self.ram_mem_domain),
                    (self.hth_wins, 4, self.ram_mem_domain),
                    
                    (self.samurai_wins, 1, self.ram_mem_domain),
                    (self.megaton_wins, 1, self.ram_mem_domain),
                    (self.card_swipe_difficulty, 1, self.ram_mem_domain),
                    (self.card_swipe_wins, 1, self.ram_mem_domain),
                    (self.draw_difficulty, 1, self.ram_mem_domain),
                    (self.draw_pink_score, 2, self.ram_mem_domain),
                    (self.draw_yellow_score, 2, self.ram_mem_domain),
                    (self.draw_red_score, 2, self.ram_mem_domain),
                    (self.draw_green_score, 2, self.ram_mem_domain),
                    (self.draw_ending, 2, self.ram_mem_domain),
                    (self.snack_difficulty, 1, self.ram_mem_domain),
                    (self.snack_pink_score, 2, self.ram_mem_domain),
                    (self.snack_yellow_score, 2, self.ram_mem_domain),
                    (self.snack_red_score, 2, self.ram_mem_domain),
                    (self.snack_green_score, 2, self.ram_mem_domain),
                    (self.snack_timer, 2, self.ram_mem_domain),
                    
                    (self.dyna_last_completed, 1, self.ram_mem_domain),
                    (self.tgco_collected_1, 4, self.ram_mem_domain),
                    (self.tgco_collected_2, 4, self.ram_mem_domain),
                    (self.mww_collected, 4, self.ram_mem_domain),
                    (self.dyna_switch_activated, 1, self.ram_mem_domain),
                    (self.games_unlocked, 4, self.ram_mem_domain),

                    (self.dyna_ap_stage, 1, self.ram_mem_domain),
                    (self.dyna_ap_ex_stage, 1, self.ram_mem_domain),
                    (self.mku_level, 1, self.ram_mem_domain),
                    (self.mww_unlocked_planets, 2, self.ram_mem_domain),
                    (self.abilities_recieved, 4, self.ram_mem_domain),
                    (self.single_use_recieved, 2, self.ram_mem_domain),
                    (self.unlock_true_arena, 1, self.ram_mem_domain),
                    (self.rotk_stages, 1, self.ram_mem_domain),
                    (self.planets_completed, 1, self.ram_mem_domain),
                    (self.games_cleared, 2, self.ram_mem_domain),
                    (self.tgco_received_1, 4, self.ram_mem_domain),
                    (self.tgco_received_2, 4, self.ram_mem_domain),
                ]
            )
            
            # Variables in question
            received_index = int.from_bytes(read_state[0], "little")
            
            game = int.from_bytes(read_state[1], "little")
            stage = int.from_bytes(read_state[2], "little")
            screen = int.from_bytes(read_state[3], "little")
            sb_stage = int.from_bytes(read_state[4], "little")
            iron_mam = int.from_bytes(read_state[5], "little")
            gold = int.from_bytes(read_state[6], "little")
            gourmet_wins = int.from_bytes(read_state[7], "little")
            ddd_flag_1 = int.from_bytes(read_state[8], "little")
            ddd_flag_2 = int.from_bytes(read_state[9], "little")
            romk_chapters_completed = int.from_bytes(read_state[10], "little")
            unlocked_abilities = int.from_bytes(read_state[11], "little")
            arena = int.from_bytes(read_state[12], "little")
            hth = int.from_bytes(read_state[13], "little")
            samurai = int.from_bytes(read_state[14], "little")
            megaton = int.from_bytes(read_state[15], "little")
            card_difficulty = int.from_bytes(read_state[16], "little")
            card_score = int.from_bytes(read_state[17], "little")
            draw_difficulty = int.from_bytes(read_state[18], "little")
            draw_pink = int.from_bytes(read_state[19], "little")
            draw_yellow = int.from_bytes(read_state[20], "little")
            draw_red = int.from_bytes(read_state[21], "little")
            draw_green = int.from_bytes(read_state[22], "little")
            draw_timer = int.from_bytes(read_state[23], "little")
            snack_difficulty = int.from_bytes(read_state[24], "little")
            snack_pink = int.from_bytes(read_state[25], "little")
            snack_yellow = int.from_bytes(read_state[26], "little")
            snack_red = int.from_bytes(read_state[27], "little")
            snack_green = int.from_bytes(read_state[28], "little")
            snack_timer = int.from_bytes(read_state[29], "little")
            dyna_stage = int.from_bytes(read_state[30], "little")
            treasure_collected_1 = int.from_bytes(read_state[31], "little")
            treasure_collected_2 = int.from_bytes(read_state[32], "little")
            ability_collected = int.from_bytes(read_state[33], "little")
            switch_activated = int.from_bytes(read_state[34], "little")
            unlocked_games =  int.from_bytes(read_state[35], "little")
            dyna_current_stages = int.from_bytes(read_state[36], "little")
            dyna_ex_current_stages = int.from_bytes(read_state[37], "little")
            mku_complete = int.from_bytes(read_state[38], "little")
            current_unlocked_planets = int.from_bytes(read_state[39], "little")
            current_abils = int.from_bytes(read_state[40], "little")
            current_single_abils = int.from_bytes(read_state[41], "little")
            true_arena_flag = int.from_bytes(read_state[42], "little")
            rotk_stage = int.from_bytes(read_state[43], "little")
            planets_done = int.from_bytes(read_state[44], "little")
            cleared_games = int.from_bytes(read_state[45], "little")
            treasure_received_1 = int.from_bytes(read_state[46], "little")
            treasure_received_2 = int.from_bytes(read_state[46], "little")
               
            # =================================
            # Item Handling Loop
            # =================================
            for index in range(min(self.received_items_count, received_index), len(ctx.items_received)):
                network_item = ctx.items_received[index]
                name = ctx.item_names.lookup_in_game(network_item.item)    
                match name:
                    # Subgame       
                    ## Is this item in the realm of being a subgame 
                    case _ if (network_item.item & 0xFFFF00) == BASE_ID and network_item.item > 0:
                        # If so, which games do we have from the network?
                        subgame_bit = network_item.item & 0xFF
                        new_unlocked = unlocked_games | (1 << subgame_bit)
                        # Update the address
                        if new_unlocked != unlocked_games:
                            await self.bizhawk_set_halfword(ctx, self.games_unlocked, new_unlocked)
                            # Plays a sound
                            await self.play_sfx(ctx, "Major")
                            # Make sure it doesnt repeat (probably not necessary tbh)
                            unlocked_games = new_unlocked
                            
                        # The True Arena unlock
                        if subgame_bit == 0x0A:
                            if true_arena_flag != 15:
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(self.unlock_true_arena, (15).to_bytes(1, "little"), self.ram_mem_domain)],
                                )
                                true_arena_flag = 15

                    # Abilities
                    case _ if (network_item.item & 0xFFFF00) == (BASE_ID | 0x100) and network_item.item > 0:
                        # Check if abilities are non-single use
                        if (network_item.item & 0xFF) <= 0x13:
                            ability_bit = (network_item.item & 0xFF) - 1
                            new_abilities = current_abils | (1 << ability_bit)
                            if new_abilities != current_abils:
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(self.abilities_recieved, new_abilities.to_bytes(4, "little"), self.ram_mem_domain)],
                                )
                                await self.play_sfx(ctx, "Ability")
                                current_abils = new_abilities 
                        else: # Single Use
                            pass
                    # Treasure
                    case _ if (network_item.item & 0xFFFF00) == (BASE_ID | 0x200) and network_item.item > 0:
                        treasure_bit = (network_item.item & 0xFF) - 1
                        treasure_value = treasures[name].value
                        if treasure_bit < 32:
                                new_treasure = treasure_received_1 | (1 << treasure_bit)
                                if new_treasure != treasure_received_1:
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(self.tgco_received_1, new_treasure.to_bytes(4, "little"), self.ram_mem_domain)],
                                    )
                                    await self.play_sfx(ctx, "Treasure")
                                    treasure_received_1 = new_treasure
                                    # gold amount does NOT get updated until TGCO is loaded
                                    self.new_gold = gold + treasure_value
                        # If the bit is greater than 32, it should be written to the 2nd address instead
                        else:
                            high_bit = treasure_bit - 32
                            new_treasure = treasure_received_2 | (1 << high_bit)
                            if new_treasure != treasure_received_2:
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(self.tgco_received_2, new_treasure.to_bytes(4, "little"), self.ram_mem_domain)],
                                )
                                await self.play_sfx(ctx, "Treasure")
                                treasure_received_2 = new_treasure
                                self.new_gold = gold + treasure_value
                    # Planets
                    case _ if (network_item.item & 0xFFFF00) == (BASE_ID | 0x400) and network_item.item > 0:
                        planet_bit = network_item.item & 0xFF
                        new_planets = current_unlocked_planets | (1 << planet_bit)
                        if new_planets != current_unlocked_planets:
                            await self.play_sfx(ctx, "Planet")
                            await self.bizhawk_set_halfword(ctx, self.mww_unlocked_planets, new_planets)
                            current_unlocked_planets = new_planets
                    # Dyna Blade
                    case _ if (network_item.item & 0xFFFF00) == (BASE_ID | 0x800) and network_item.item > 0:
                        match network_item.item & 0xFF:
                            # Dyna Blade EX 1
                            case 0x00:
                                dyna_new_ex_stage = dyna_ex_current_stages | (1 << 0)
                                if dyna_new_ex_stage != dyna_ex_current_stages:
                                    await self.bizhawk_set_halfword(ctx, self.dyna_ap_ex_stage, dyna_new_ex_stage)
                                    await self.play_sfx(ctx, "Filler")
                            # Dyna Blade EX 2
                            case 0x01:
                                dyna_new_ex_stage  = dyna_ex_current_stages | (1 << 1)
                                if dyna_new_ex_stage != dyna_ex_current_stages:
                                    await self.bizhawk_set_halfword(ctx, self.dyna_ap_ex_stage, dyna_new_ex_stage)
                                    await self.play_sfx(ctx, "Filler")
                            # Progressive Dyna Blade
                            case 0x02:
                                dyna_new_stage = min(4, dyna_current_stages + 1)
                                if dyna_new_stage != dyna_current_stages:
                                    await self.bizhawk_set_halfword(ctx, self.dyna_ap_stage, dyna_new_stage)     
                                    await self.play_sfx(ctx, "Progressive")                      
                    # AP-Specific
                    case "Rainbow Star":
                        self.rainbow_stars += 1
                        await self.play_sfx(ctx, "Planet")
                    case "Meta Knightmare Ultra - Progressive Level":
                        if self.progressive_mku_level < 4:
                            self.progressive_mku_level += 1
                        await self.play_sfx(ctx, "Progressive")   
                    case "Cave Key":
                        if self.cave_keys_collected  < 3:
                            self.cave_keys_collected += 1  
                        await self.play_sfx(ctx, "Progressive")                                                          
                    # Filler
                    case "1-Up":
                        # Should check if in game
                        # Alas, can I really?
                        await self.bizhawk_add_halfword(ctx, self.kirby_lifes, 1)
                        await self.play_sfx(ctx, "1-Up")
                    case "Maxim Tomato":
                        await self.bizhawk_add_halfword(ctx, self.kirby_hp, 76)        
                        await self.play_sfx(ctx, "Filler")                                            
                    case "Tomato":
                        await self.bizhawk_add_halfword(ctx, self.kirby_hp, 25)      
                        await self.play_sfx(ctx, "Filler")                                                          
                    case "Invincible Candy":
                        await self.bizhawk_set_halfword(ctx, self.candy_timer, 1320)
                        await self.play_sfx(ctx, "Filler")    
                        
                    # What did you get???
                    case _:
                        raise Exception("Bad item name received: " + name)
                                           
                # Keep APSave updated
                if index >= received_index:
                    await self.bizhawk_set_halfword(ctx, self.received_offset, index + 1)
                self.received_items_count = index + 1
                await asyncio.sleep(0.1)
            
            # =================================
            # Location Handling
            # =================================
            # Spring Breeze
            if sb_stage:  
                game_name = "Spring Breeze"
                for i in range(sb_stage):               
                    loc = self.get_location(game_name, f"Stage {i+1}")
                    if loc is not None:
                        send_locations.add(loc)

            # Dyna Blade 
            if dyna_stage: 
                game_name = "Dyna Blade"
                for i in range(dyna_stage):               
                    loc = self.get_location(game_name, f"Stage {i+1}")
                    if loc is not None:
                        send_locations.add(loc)
                            
                # Check if Iron Mam was defeated         
                if iron_mam == 8:
                    loc = self.get_location(game_name, f"Iron Mam")
                    if loc is not None:
                        send_locations.add(loc)
                        
            # Gourmet Race
            if game == 2:
                game_name = "Gourmet Race"
                if gourmet_wins:
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
            if treasure_collected_1:
                for i in range(32):
                    if treasure_collected_1 & (1 << i):
                        send_locations.add(BASE_ID + 19 + i)
            
            if treasure_collected_2:
                for i in range(28):
                    if treasure_collected_2 & (1 << i):
                        send_locations.add(BASE_ID + 51 + i)

            if game == 3:
                game_name = "The Great Cave Offensive"
                if gold != self.new_gold:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(self.tgco_gold, self.new_gold.to_bytes(4, "little"), self.ram_mem_domain)],
                    )

            # Revenge of Meta Knight
            if romk_chapters_completed:  
                game_name = "Revenge of Meta Knight"
                for i in range(romk_chapters_completed):               
                    loc = self.get_location(game_name, f"Chapter {i+1}")
                    if loc is not None:
                        send_locations.add(loc)

            # Milky Way Wishes
            # Dreadful: Part 2
            # If ability is collected in-game
            if ability_collected:
                for bit, x in MWW_ABILITY_OFFSETS.items():
                    if ability_collected & bit:
                        send_locations.add(BASE_ID + x)

            if game == 5:
                game_name = "Milky Way Wishes"

                # If ability doesnt match received then make it equal
                # NOT WORKING ATM?
                if unlocked_abilities != current_abils:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(self.mww_abilities, current_abils.to_bytes(4, "little"), self.ram_mem_domain)],
                    )
                    unlocked_abilities = current_abils
                    
                # If rainbow key is equal to option number, unlock Galactic Nova
                
                

            # Revenge of the King 
            if rotk_stage:  
                game_name = "Revenge of the King"
                for i in range(rotk_stage):               
                    loc = self.get_location(game_name, f"Stage {i+1}")
                    if loc is not None:
                        send_locations.add(loc)

            # Arena
            if game == 7: 
                game_name = "The Arena"
                if arena:
                    if arena == 1:
                        label = "1 Straight Win"
                    else:
                        label = f"{arena} Straight Wins"           
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)
                        
            
            # Meta Knightmare Ultra
            if mku_complete:
                game_name = "Meta Knightmare Ultra"
                for i in range(mku_complete):               
                    loc = self.get_location(game_name, f"Level {i+1}")
                    if loc is not None:
                        send_locations.add(loc)
                
            if game == 8: 
                game_name = "Meta Knightmare Ultra"


            # Helper to Hero 
            if game == 9:
                game_name = "Helper to Hero"
                if arena:
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
                if arena:
                    if arena == 1:
                        label = "1 Straight Win"
                    else:
                        label = f"{arena} Straight Wins"
                        
                    loc = self.get_location(game_name, label)
                    if loc is not None:
                        send_locations.add(loc)

            # --- Minigames ---
            # Megaton Punch
            if megaton:
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
            if samurai:
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
                    
           # Check for completing the goal and send it to the server
            if not self.goal_complete:
                goalsd: bool
                match ctx.slot_data["goal"]:
                    case "milky_way_wishes":
                        goaled = False
                        if cleared_games & 32:
                            goaled = True
                    case "main_game_completion":
                        goaled = False
                        self.completed_games = bin(cleared_games & 0x7FF).count("1")
                        if self.completed_games >= ctx.slot_data["required_maingame_completions"]:
                            goaled = True
                    case "the_arena":
                        goaled = False
                        if cleared_games & 128:
                            goaled = True
                    case "revenge_of_the_king":
                        goaled = False
                        if cleared_games & 64:
                            goaled = True
                    case "meta_knightmare_ultra":
                        goaled = False
                        if cleared_games & 256:
                            goaled = True
                    case "marx_soul":
                        goaled = False
                        if cleared_games & 1024:
                            goaled = True
                    case _:
                        raise Exception("Bad goal in slot data: " + ctx.slot_data["goal"])

                if goaled:
                    self.goal_complete = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass

    # Bizhawk Functions
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
