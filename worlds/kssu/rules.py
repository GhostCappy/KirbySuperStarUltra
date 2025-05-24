from typing import Dict, TYPE_CHECKING
from .items import main_game_completion
from .names import location_names, item_names
from worlds.generic.Rules import set_rule, add_rule

if TYPE_CHECKING:
    from . import KSSUWorld
    from BaseClasses import CollectionState

def can_fight_wind(state: "CollectionState", player: int):
    return state.has_any([item_names.wing, item_names.jet, item_names.ninja], player)

def dyna_blade_rules(world: "KSSUWorld"):
    pass

def great_cave_rules(world: "KSSUWorld"):
    pass

def revenge_metaknight_rules(world: "KSSUWorld"):
    pass

def milky_way_wishes_rules(world: "KSSUWorld"):
    pass


def set_rules(world: "KSSUWorld", excluded):
    # Dyna Blade
    if "Dyna Blade" in world.options.included_maingames:
        dyna_blade_rules(world)
    
    # Great Cave Offensive
    if "The Great Cave Offensive" in world.options.included_maingames:
        great_cave_rules(world)
        
    # Revenge of Meta Knight
    if "Revenge of Meta Knight" in world.options.included_maingames:
        revenge_metaknight_rules(world)
        
    # Milky Way Wishes
    if "Milky Way Wishes" in world.options.included_maingames:
        milky_way_wishes_rules(world)
        
    if "The Arena" in world.options.included_maingames:
        for i in range(10, 21):
            set_rule(world.get_location(f"The Arena - {i} Straight Wins"),
                        lambda state: state.has_group_unique("Copy Ability", world.player, 5))
        
    main_game_complete = list(main_game_completion.keys())
    main_game_required = []
    for main_game in main_game_completion.keys():
        if main_game.rsplit(" - ")[0] in world.options.required_maingames:
            main_game_required.append(main_game)

    world.multiworld.completion_condition[world.player] = lambda state: \
        state.has_all(main_game_required, world.player) and state.has_from_list(
            main_game_complete, world.player, world.options.required_maingame_completions)
        
    
