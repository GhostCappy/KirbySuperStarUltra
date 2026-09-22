from typing import Dict, TYPE_CHECKING
from .items import main_game_completion
from .names import location_names, item_names
from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import KSSUWorld

# Abilities that can beat wind  
def can_fight_wind(state: "CollectionState", player: int) -> bool:
    return state.has_any([item_names.wing, item_names.jet, item_names.ninja], player)

# Abilities that can hit switches (and food if enabled)
def dyna_blade_rules(world: "KSSUWorld") -> None:
    set_rule(world.get_location(location_names.db_switch_1),
             lambda state: state.has_any([item_names.mirror, item_names.beam], world.player) or
                           (state.has(item_names.plasma, world.player)
                            and state.has_any_count({item_names.dyna_blade_ex1: 1,
                                                     item_names.progressive_dyna_blade: 2}, world.player)))

    set_rule(world.get_entrance("Mallow Castle -> Dyna Blade Bonus 1"),
             lambda state: state.has(item_names.dyna_blade_ex1, world.player))
    set_rule(world.get_entrance("Candy Mountain -> Dyna Blade Bonus 2"),
             lambda state: state.has(item_names.dyna_blade_ex2, world.player))

# Abilities that can access treasure, food, essences, etc.
def the_great_cave_rules(world: "KSSUWorld") -> None:
    # Treasures
    set_rule(world.get_location(location_names.tgco_treasure_4),
             lambda state: state.has_any([item_names.wing, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_7),
             lambda state: state.has_any([item_names.beam, item_names.wing, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_13),
             lambda state: state.has_any([item_names.cutter, item_names.sword, item_names.wing], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_18),
             lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_19),
             lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_20),
             lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_21),
             lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_22),
             lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_28),
             lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_31),
             lambda state: state.has_any([item_names.hammer, item_names.stone], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_32),
             lambda state: state.has_any([item_names.hammer, item_names.stone], world.player)
                           and state.has(item_names.fire, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_33),
             lambda state: state.has_any([item_names.hammer, item_names.stone], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_34),
             lambda state: state.has_any([item_names.cutter, item_names.beam, item_names.hammer,
                                          item_names.bomb, item_names.jet, item_names.wing, item_names.stone,
                                          item_names.plasma, item_names.parasol], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_36),
             lambda state: state.has_any([item_names.beam, item_names.yoyo, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_37),
             lambda state: state.has_any([item_names.parasol, item_names.yoyo, item_names.beam, item_names.plasma,
                                          item_names.hammer, item_names.stone, item_names.bomb], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_42),
             lambda state: state.has(item_names.stone, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_43),
             lambda state: state.has(item_names.plasma, world.player) or
             (state.has_any([item_names.ninja, item_names.sword, item_names.wing], world.player)
              and state.has(item_names.stone, world.player)))
    set_rule(world.get_location(location_names.tgco_treasure_45),
             lambda state: state.has_any([item_names.jet, item_names.fire], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_47),
             lambda state: can_fight_wind(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_49),
             lambda state: state.has(item_names.jet, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_52),
             lambda state: state.has_any([item_names.parasol, item_names.wing, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_53),
             lambda state: state.has(item_names.wheel, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_58),
             lambda state: state.has_any([item_names.beam, item_names.crash], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_59),
             lambda state: state.has_any([item_names.ninja, item_names.sword, item_names.wing, item_names.cutter],
                                         world.player))

# Abilities that can access cannon, food and essences
def revenge_of_metaknight_rules(world: "KSSUWorld") -> None:
    set_rule(world.get_location(location_names.romk_chapter_3),
             lambda state: state.has(item_names.fire, world.player))
    set_rule(world.get_entrance("RoMK - Chapter 3 -> RoMK - Chapter 4"),
             lambda state: state.has(item_names.fire, world.player))
    set_rule(world.get_entrance("RoMK - Chapter 4 -> RoMK - Chapter 5"),
             lambda state: state.has_any([item_names.beam, item_names.yoyo, item_names.jet, item_names.bomb],
                                         world.player))
    set_rule(world.get_location(location_names.romk_chapter_6),
             lambda state: state.has_any([item_names.wing, item_names.suplex], world.player))
    set_rule(world.get_entrance("RoMK - Chapter 6 -> RoMK - Chapter 7"),
             lambda state: state.has_any([item_names.wing, item_names.suplex], world.player))

# Abilities that can access essences and food
def milky_way_wishes_rules(world: "KSSUWorld") -> None:
    if world.options.milky_way_wishes_mode == "local":
        set_rule(world.get_location(location_names.mww_complete),
                 lambda state: state.has_all([item_names.floria, item_names.aqualiss,
                                              item_names.skyhigh, item_names.hotbeat,
                                              item_names.cavios, item_names.mecheye,
                                              item_names.halfmoon], world.player))
    else:
        set_rule(world.get_location(location_names.mww_complete),
                 lambda state: state.has(item_names.rainbow_star, world.player, 7))

    set_rule(world.get_location(location_names.mww_sword),
             lambda state: state.has_any([item_names.beam, item_names.bomb, item_names.cutter, item_names.fire,
                                          item_names.hammer, item_names.jet, item_names.mirror, item_names.parasol,
                                          item_names.plasma, item_names.stone, item_names.wing, item_names.yoyo],
                                         world.player))

    set_rule(world.get_location(location_names.mww_wheel),
             lambda state: state.has_any([item_names.fire, item_names.jet], world.player))

    set_rule(world.get_location(location_names.mww_suplex),
             lambda state: state.has_any([item_names.fighter, item_names.yoyo], world.player))

    set_rule(world.get_location(location_names.mww_ninja),
             lambda state: state.has_any([item_names.beam, item_names.cutter, item_names.fire, item_names.hammer,
                                          item_names.jet, item_names.mirror, item_names.parasol, item_names.plasma,
                                          item_names.stone, item_names.sword, item_names.wing, item_names.yoyo],
                                         world.player))

# More rules that need to be made:
# Helper to Hero (When helpers are blocked behind ability)
# The True Arena (Same thing as arena)
def set_rules(world: "KSSUWorld") -> None:
    # Dyna Blade
    if "Dyna Blade" in world.options.included_maingames:
        dyna_blade_rules(world)
    
    # Great Cave Offensive
    if "The Great Cave Offensive" in world.options.included_maingames:
        the_great_cave_rules(world)
        
    # Revenge of Meta Knight
    if "Revenge of Meta Knight" in world.options.included_maingames:
        revenge_of_metaknight_rules(world)
        
    # Milky Way Wishes
    if "Milky Way Wishes" in world.options.included_maingames:
        milky_way_wishes_rules(world)
    
    # The Arena 
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
        
    
