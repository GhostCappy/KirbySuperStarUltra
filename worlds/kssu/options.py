from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice, OptionSet, DeathLink, Toggle, OptionGroup, OptionCounter
from schema import Schema, And, Use, Optional, Or

maingame_mapping = {
        0: "Spring Breeze",
        1: "Dyna Blade",
        2: "Gourmet Race",
        3: "The Great Cave Offensive",
        4: "Revenge of Meta Knight",
        5: "Milky Way Wishes",
        6: "The Arena",
        7: "Revenge of The King",
        8: "Meta Knightmare Ultra",
        9: "Helper to Hero",
        10: "The True Arena"
}

class Goal(Choice):
    """Sets the goal of your world.

    - **Milky Way Wishes:** Defeat Marx and complete Milky Way Wishes.
    - **Main-Game Completion:** Complete a set of required Main Games.
    - **The Arena:** Complete The Arena.
    - **Revenge of the King:** Defeat Masked Dedede and complete Revenge of the King.
    - **Meta Knightmare Ultra:** Defeat Galacta Knight and complete Meta Knightmare Ultra.
    - **Marx Soul:** Unlock the true arena and defeat Marx Soul."""
    display_name = "Goal"
    rich_text_doc = True
    option_milky_way_wishes = 0
    option_main_game_completion = 1
    option_the_arena = 2
    option_revenge_of_the_king = 3
    option_meta_knightmare_ultra = 4
    option_marx_soul = 5
    default = 0

class RequiredMainGameCompletions(Range):
    """
    How many main-games must be completed for the game to be considered complete.
    
    This option only applies when Main-Game Completion is set as the goal.
    """
    display_name = "Required Main-Game Completions"
    range_start = 1
    range_end = 10
    default = 6
    
class RequiredMainGames(OptionSet):
    """
    Which main-games are required to be completed for the game to be considered complete.
    
    This option only applies when Main-Game Completion is set as the goal.
    """
    display_name = "Required Main-Games"
    valid_keys = {
        "Spring Breeze",
        "Dyna Blade",
        "Gourmet Race",
        "The Great Cave Offensive",
        "Revenge of Meta Knight",
        "Milky Way Wishes",
        "The Arena",
        "Revenge of The King",
        "Meta Knightmare Ultra",
        "Helper to Hero",
        "The True Arena"
    }
    default = ["Milky Way Wishes"]
    
class StartingMainGame(Choice):
    """
    The main-game that will be unlocked by default.
    """
    display_name = "Starting Main-Game"
    option_spring_breeze = 0
    option_dyna_blade = 1
    option_gourmet_race = 2
    option_the_great_cave_offensive = 3
    option_revenge_of_meta_knight = 4
    option_milky_way_wishes = 5
    option_the_arena = 6
    option_revenge_of_the_king = 7
    option_meta_knightmare_ultra = 8
    option_helper_to_hero = 9
    option_the_true_arena = 10
    default = 0

class IncludedMainGames(OptionSet):
    """
    Which main-games should be included as locations.
    """
    display_name = "Included Main-Games"
    valid_keys = {
        "Spring Breeze",
        "Dyna Blade",
        "Gourmet Race",
        "The Great Cave Offensive",
        "Revenge of Meta Knight",
        "Milky Way Wishes",
        "The Arena",
        "Revenge of The King",
        "Meta Knightmare Ultra",
        "Helper to Hero",
        "The True Arena"
    }
    default = sorted(valid_keys)
    
    
class TGCOAreas(Choice):
    """
    [Not currently implemented]
    Determines how new areas are unlocked in The Great Cave Offensive
    
    Key: New areas are unlocked with progressive keys found in the pool. Three keys are required to finish the mode.
    
    Gold: Certain gold thresholds must be met before progressing into the next area. This means collecting
    enough treasure to reach a specified amount of gold.
    """
    display_name = "The Great Cave Offensive Areas"
    option_key = 0
    option_gold = 1
    default = 0
    
class TGCOKeys(Range):
    """
    Determines how many extra keys are added in the pool for The Great Cave Offensive.
    
    This option only applies when Keys is selected for the area option.
    """
    display_name = "The Great Cave Offensive Extra Keys"
    range_start = 0
    range_end = 3
    default = 0
    
class TGCOrequiredGold(Range):
    """
    Required amount of gold that is needed in order to complete The Great Cave Offensive.
    """
    display_name = "The Great Cave Offensive Required Gold"
    range_start = 2500000
    range_end = 9999990
    default = range_end

class TGCOThresholds(OptionCounter):
    """
    Percentange of the required gold required before allowing access to
    Crystal/Old Tower/Garden areas in The Great Cave Offensive
    """
    display_name = "The Great Cave Offensive Gold Thresholds"
    valid_keys = ("Crystal", "Old Tower", "Garden")
    schema = Schema({
        area: And(int, lambda i: 0 <= i <= 100, error="Value must be between 0 and 100")
        for area in ["Crystal", "Old Tower", "Garden"]
    })
    min = 0
    max = 100
    default = {
        "Crystal": 25,
        "Old Tower": 50,
        "Garden": 75
    }

class TGCOExcessGold(Range):
    """
    Percentange of the excess gold kept within the multiworld.
    
    This option only applies if the required number of gold is less than the max.
    """
    display_name = "The Great Cave Offensive Excess Gold"
    range_start = 0
    range_end = 100
    default = 0
        
class MilkyWayWishesMode(Choice):
    """
    [Not currently implemented] 
    Determines how Marx is unlocked in Milky Way Wishes.
    
    Local: Marx is unlocked after completing the 7 main planets
    (Floria, Aqualiss, Skyhigh, Hotbeat, Cavios, Mecheye, Halfmoon)
    
    Multiworld: Marx is unlocked after receiving 7 Rainbow Stars scattered across the multiworld
    """
    display_name = "Milky Way Wishes Mode"
    option_local = 0
    option_multiworld = 1
    default = 0
    
# Not yet implemented
class Foodsanity(OptionSet):
    """
    [Not currently implemented]
    
    Adds the specified consumables to the location pool. 
    Options are Maxim Tomato, 1-Up, and Invincibility Candy.
    """
    display_name = "Foodsanity"
    valid_keys = ("Maxim Tomato", "1-Up", "Invincibility Candy")

    default = frozenset()

# Not yet implemented
class EssencesSanity(Toggle):
    """
    [Not currently implemented]
    Adds Copy Essence pedestals across all main-games to the location pool.
    This includes Dyna Blade, The Great Cave Offensive, Gourmet Race, Revenge Of Meta Knight, and Milky Way Wishes
    
    AKA Essence-Sanity.
    """
    display_name = "Essence-sanity"
    
class Helpersanity(Choice):
    """
    [Not currently implemented] 
    Determines how locations in Helper to Hero are determined.
    
    Off: Helper to Hero will behave like The Arena. Each win is counted as a location.
    
    Simple: Completing Helper to Hero with different helpers will send a location.
    
    Full: For each helper, each win will be counted as a location.
    """
    display_name = "Milky Way Wishes Mode"
    option_off = 0
    option_simple = 1
    option_full = 2
    default = 0
    
class IncludeSubgames(Toggle):
    """
    If enabled, all Sub-Games will be included as location checks.
    
    This includes Megaton Punch, Samurai Kirby, Kirby Card Swipe, Kirby on the Draw, and Snack Tracks.
    """
    display_name = "Include Sub-Games"
    default = True
    
class MegatonDifficulties(Toggle):
    """
    [Not currently implemented] 
    
    Adds 6 more locations for beating a foe on each level in Megaton Punch.
    """
    display_name = "Megaton Punch Levels"
    default = False
    
class SamuraiDifficulties(Toggle):
    """
    [Not currently implemented] 
    
    Adds extra locations for beating a foe on each difficulty in Samurai Kirby.
    """
    display_name = "Samurai Kirby Difficulty"
    default = False
    
class SamuaraiWins(Range):
    """
    How many opponents / wins to include as locations in Samurai Kirby.
    """
    display_name = "Samurai Kirby Wins"
    range_start = 1
    range_end = 5
    default = 4
    
@dataclass
class KSSUOptions(PerGameCommonOptions):
    deathlink: DeathLink
    goal: Goal
    required_maingame_completions: RequiredMainGameCompletions
    required_maingames: RequiredMainGames
    starting_maingame: StartingMainGame
    included_maingames: IncludedMainGames
    include_subgames: IncludeSubgames
    the_great_cave_offensive_areas: TGCOAreas
    the_great_cave_offensive_keys: TGCOKeys
    the_great_cave_offensive_required_gold: TGCOrequiredGold
    the_great_cave_offensive_thresholds: TGCOThresholds
    the_great_cave_offensive_excess_gold: TGCOExcessGold
    milky_way_wishes_mode: MilkyWayWishesMode
    helpersanity: Helpersanity
    foodsanity: Foodsanity
    essences: EssencesSanity
    megaton_punch_difficulties: MegatonDifficulties
    samurai_kirby_difficulties: SamuraiDifficulties
    samurai_kirby_wins: SamuaraiWins
    
option_groups = [
    OptionGroup("General Options", [
        Goal,
        RequiredMainGameCompletions,
        RequiredMainGames,
        StartingMainGame,
        IncludedMainGames,
        IncludeSubgames
    ]),
    OptionGroup("Game Settings", [
        TGCOAreas,
        TGCOKeys,
        TGCOrequiredGold,
        TGCOThresholds,
        TGCOExcessGold,
        MilkyWayWishesMode,
        Helpersanity,
        Foodsanity,
        EssencesSanity,
        MegatonDifficulties,
        SamuraiDifficulties,
        SamuaraiWins
    ])
]


option_presets = {
    '''
    "SNES Default": {

    },
    "Revenge of the King": {

    },
    "Marx Soul": {

    },
    "Marx Soul": {

    },
    "Insanity": {

    },
'''
}


