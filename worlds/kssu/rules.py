from typing import Dict, TYPE_CHECKING
from .items import main_game_completion
from .names import location_names, item_names
from rule_builder.rules import HasAll, HasAny, Has, HasAnyCount, HasGroupUnique
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import KSSUWorld

# Abilities that can beat wind  
def can_fight_wind(state: "CollectionState", player: int) -> bool:
    return HasAny([item_names.wing, item_names.jet, item_names.ninja], player)

# Abilities that can hit switches (and food if enabled)
def dyna_blade_rules(world: "KSSUWorld") -> None:
    set_rule = world.set_rule
    set_rule(world.get_location(location_names.db_switch_1),
             HasAny([item_names.mirror, item_names.beam], world.player) or
                           (Has(item_names.plasma, world.player)
                            and HasAnyCount({item_names.dyna_blade_ex1: 1,
                                                     item_names.progressive_dyna_blade: 2}, world.player)))

    set_rule(world.get_entrance("Mallow Castle -> Dyna Blade Bonus 1"),
             Has(item_names.dyna_blade_ex1, world.player))
    set_rule(world.get_entrance("Candy Mountain -> Dyna Blade Bonus 2"),
             Has(item_names.dyna_blade_ex2, world.player))

# Abilities that can access treasure, food, essences, etc.
def the_great_cave_rules(world: "KSSUWorld") -> None:
    set_rule = world.set_rule
    # Treasures
    set_rule(world.get_location(location_names.tgco_treasure_4),
             HasAny([item_names.wing, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_7),
             HasAny([item_names.beam, item_names.wing, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_13),
             HasAny([item_names.cutter, item_names.sword, item_names.wing], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_18),
             HasAny([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_19),
             HasAny([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_20),
             HasAny([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_21),
             HasAny([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_22),
             HasAny([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_28),
             HasAny([item_names.crash, item_names.yoyo,
                                          item_names.bomb, item_names.beam], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_31),
             HasAny([item_names.hammer, item_names.stone], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_32),
             HasAny([item_names.hammer, item_names.stone], world.player)
                           and Has(item_names.fire, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_33),
             HasAny([item_names.hammer, item_names.stone], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_34),
             HasAny([item_names.cutter, item_names.beam, item_names.hammer,
                                          item_names.bomb, item_names.jet, item_names.wing, item_names.stone,
                                          item_names.plasma, item_names.parasol], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_36),
             HasAny([item_names.beam, item_names.yoyo, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_37),
             HasAny([item_names.parasol, item_names.yoyo, item_names.beam, item_names.plasma,
                                          item_names.hammer, item_names.stone, item_names.bomb], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_42),
             Has(item_names.stone, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_43),
             Has(item_names.plasma, world.player) or
             (HasAny([item_names.ninja, item_names.sword, item_names.wing], world.player)
              and Has(item_names.stone, world.player)))
    set_rule(world.get_location(location_names.tgco_treasure_45),
             HasAny([item_names.jet, item_names.fire], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_47),
             lambda state: can_fight_wind(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_49),
             Has(item_names.jet, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_52),
             Has([item_names.parasol, item_names.wing, item_names.plasma], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_53),
             Has(item_names.wheel, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_58),
             HasAny([item_names.beam, item_names.crash], world.player))
    set_rule(world.get_location(location_names.tgco_treasure_59),
             HasAny([item_names.ninja, item_names.sword, item_names.wing, item_names.cutter],
                                         world.player))

# Abilities that can access cannon, food and essences
def revenge_of_metaknight_rules(world: "KSSUWorld") -> None:
    set_rule = world.set_rule
    set_rule(world.get_location(location_names.romk_chapter_3),
             Has(item_names.fire, world.player))
    set_rule(world.get_entrance("RoMK - Chapter 3 -> RoMK - Chapter 4"),
             Has(item_names.fire, world.player))
    set_rule(world.get_entrance("RoMK - Chapter 4 -> RoMK - Chapter 5"),
             HasAny([item_names.beam, item_names.yoyo, item_names.jet, item_names.bomb],
                                         world.player))
    set_rule(world.get_location(location_names.romk_chapter_6),
             HasAny([item_names.wing, item_names.suplex], world.player))
    set_rule(world.get_entrance("RoMK - Chapter 6 -> RoMK - Chapter 7"),
             HasAny([item_names.wing, item_names.suplex], world.player))

# Abilities that can access essences and food
def milky_way_wishes_rules(world: "KSSUWorld") -> None:
    set_rule = world.set_rule
    if world.options.milky_way_wishes_mode == "local":
        set_rule(world.get_location(location_names.mww_complete),
                 HasAll([item_names.floria, item_names.aqualiss,
                                              item_names.skyhigh, item_names.hotbeat,
                                              item_names.cavios, item_names.mecheye,
                                              item_names.halfmoon], world.player))
    else:
        set_rule(world.get_location(location_names.mww_complete),
                 Has(item_names.rainbow_star, world.player, 7))

    set_rule(world.get_location(location_names.mww_sword),
             HasAny([item_names.beam, item_names.bomb, item_names.cutter, item_names.fire,
                                          item_names.hammer, item_names.jet, item_names.mirror, item_names.parasol,
                                          item_names.plasma, item_names.stone, item_names.wing, item_names.yoyo],
                                         world.player))

    set_rule(world.get_location(location_names.mww_wheel),
             HasAny([item_names.fire, item_names.jet], world.player))

    set_rule(world.get_location(location_names.mww_suplex),
             HasAny([item_names.fighter, item_names.yoyo], world.player))

    set_rule(world.get_location(location_names.mww_ninja),
             HasAny([item_names.beam, item_names.cutter, item_names.fire, item_names.hammer,
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
        set_rule = world.set_rule
        for i in range(10, 21):
            set_rule(world.get_location(f"The Arena - {i} Straight Wins"),
                        HasGroupUnique("Copy Ability", world.player, 5))

    # Helper to Hero

    # The True Arena
        
    main_game_complete = list(main_game_completion.keys())
    main_game_required = []
    for main_game in main_game_completion.keys():
        if main_game.rsplit(" - ")[0] in world.options.required_maingames:
            main_game_required.append(main_game)

    world.multiworld.completion_condition[world.player] = lambda state: \
        HasAll(main_game_required, world.player) and state.has_from_list(
            main_game_complete, world.player, world.options.required_maingame_completions)
        
    
