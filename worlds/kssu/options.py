from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice, OptionSet, OptionDict, DeathLinkMixin, Toggle
from schema import Schema, And

subgame_mapping = {
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

class RequiredSubgameCompletions(Range):
    """
    How many subgames must be completed for the game to be considered complete.
    """
    display_name = "Required Subgame Completions"
    range_start = 1
    range_end = 10
    default = 6
    
class RequiredSubgames(OptionSet):
    """
    Which subgames are required to be completed for the game to be considered complete.
    """
    display_name = "Required Subgames"
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
    
class StartingSubgame(Choice):
    """
    The subgame that will be unlocked by default.
    """
    display_name = "Starting Subgame"
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


class IncludedSubgames(OptionSet):
    """
    Which subgames should be included as locations.
    """
    display_name = "Included Subgames"
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
    
class MilkyWayWishesMode(Choice):
    """
    Determines how Marx is unlocked in Milky Way Wishes.
    Local: Marx is unlocked after completing the 7 main planets
    (Floria, Aqualiss, Skyhigh, Hotbeat, Cavios, Mecheye, Halfmoon)
    Multiworld: Marx is unlocked after receiving 7 Rainbow Stars scattered across the multiworld
    """
    display_name = "Milky Way Wishes Mode"
    option_local = 0
    option_multiworld = 1
    default = 0
    

class Consumables(OptionSet):
    """
    Adds the specified consumables to the location pool. Options are Maxim Tomato, 1-Up,
    and Invincibility Candy.
    """
    display_name = "Consumable Checks"
    valid_keys = ("Maxim Tomato", "1-Up", "Invincibility Candy")

    default = frozenset()

class Essences(Toggle):
    """
    Adds Copy Essence pedestals to the location pool.
    """
    display_name = "Essence-sanity"
    
@dataclass
class KSSUOptions(PerGameCommonOptions, DeathLinkMixin):
    required_subgame_completions: RequiredSubgameCompletions
    required_subgames: RequiredSubgames
    starting_subgame: StartingSubgame
    included_subgames: IncludedSubgames
    consumables: Consumables
    essences: Essences
    milky_way_wishes_mode: MilkyWayWishesMode