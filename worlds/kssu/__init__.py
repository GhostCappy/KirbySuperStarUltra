import os
import typing
import logging
import base64
import threading
import math
import pkgutil

# Shows warning but should work without issue
import settings
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, MultiWorld, CollectionState, Item, ItemClassification
from Options import OptionError

from typing import Dict, List, ClassVar, Any, Mapping

from .rom import KSSUProcedurePatch, write_tokens
from .regions import create_regions
from .options import KSSUOptions, subgame_mapping, IncludedSubgames, Consumables
from .client import KSSUClient 
from .items import item_table, KSSUItem, filler_item_weights, trap, item_lookup_by_name
from .locations import location_lookup_by_name
from .rules import set_rules

logger = logging.getLogger("Kirby Super Star Ultra")

class KSSUWeb(WebWorld):
    theme = "partyTime" 
    setup_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up YourGame for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["GhostCappy"]
    )
    tutorials = [setup_en]
    
class KSSUSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Kirby Super Star Ultra rom"""

        copy_to = "Kirby Super Star Ultra (USA).nds"
        description = "Kirby Super Star Ultra (USA) ROM File"
        md5s = ["c0c84468ce0c9c7b3b97246ec443df1f"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True

class KSSUWorld(World):
    """
    Kirby Super Star Ultra is a remake of the Super Nintendo Entertainment System game Kirby Super Star.
    The remake retains all game modes found in the original and adds four major new ones.
    """
    game = "Kirby Super Star Ultra"
    options_dataclass = KSSUOptions
    options: KSSUOptions
    web = KSSUWeb()
    settings: typing.ClassVar[KSSUSettings]
    item_name_to_id = item_lookup_by_name
    location_name_to_id = location_lookup_by_name
    
    create_regions = create_regions
    
    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_count: int = 0
        
    def generate_early(self) -> None:
        if not self.options.included_subgames.value.intersection(
                {"The Great Cave Offensive", "Milky Way Wishes", "The Arena"}):
            raise OptionError(f"Kirby Super Star Ultra({self.player_name}): At least one of The Great Cave Offensive, "
                              f"Milky Way Wishes, or The Arena must be included")

        for game in sorted(self.options.required_subgames.value):
            if game not in self.options.included_subgames.value:
                logger.warning(F"Kirby Super Star Ultra({self.player_name}): Required subgame {game} not included, "
                               F"adding to included subgames")
                self.options.included_subgames.value.add(game)

        if self.options.starting_subgame.current_option_name not in self.options.included_subgames:
            logger.warning(f"Kirby Super Star Ultra({self.player_name}): Starting subgame not included, choosing random.")
            self.options.starting_subgame.value = self.random.choice([value[0] for value in subgame_mapping.items()
                                                                      if value[1] in self.options.included_subgames])

        if self.options.required_subgame_completions > len(self.options.included_subgames.value):
            logger.warning(f"Kirby Super Star Ultra ({self.player_name}): Required subgame count greater than "
                           f"included subgames, reducing to all included.")
            self.options.required_subgame_completions.value = len(self.options.included_subgames.value)
                
            # proper UT support
        if hasattr(self.multiworld, "generation_is_fake"):
            self.options.included_subgames = IncludedSubgames.valid_keys
            self.options.consumables.value = Consumables.valid_keys
            self.options.essences.value = True
                
    def create_item(self, name, force_classification: ItemClassification | None = None):
        if name not in item_table:
            raise Exception(f"{name} is not a valid item name for Kirby Super Star.")
        data = item_table[name]
        classification = force_classification if force_classification else data.classification
        return KSSUItem(name, data.classification, data.code, self.player)

    def create_items(self) -> None:
        itempool = []
        modes = [self.create_item(name) for name in sub_games if name in self.options.included_subgames]
        starting_mode = self.create_item(subgame_mapping[self.options.starting_subgame])
        modes.remove(starting_mode)
        self.multiworld.push_precollected(starting_mode)
        itempool.extend([self.create_item(name) for name in copy_abilities])
        itempool.extend(modes)
        
        if "Dyna Blade" in self.options.included_subgames:
            force = None
            if not self.options.essences and "Maxim Tomato" not in self.options.consumables:
                force = ItemClassification.useful
            itempool.extend([self.create_item(name, force) for name in dyna_items])
        if "The Great Cave Offensive" in self.options.included_subgames:
            for name, treasure in sorted(treasures.items(), key=(lambda treasure: treasure[1].value), reverse=True):
                itempool.append(self.create_item(name))
        if "Milky Way Wishes" in self.options.included_subgames:
            planet = [self.create_item(name) for name in planets]
            starting_planet = self.random.choice(planet)
            planet.remove(starting_planet)
            self.multiworld.push_precollected(starting_planet)
            itempool.extend(planet)

            if self.options.milky_way_wishes_mode == "multiworld":
                itempool.extend(self.create_item(item_names.rainbow_star) for _ in range(7))
                
        location_count = len(list(self.multiworld.get_unfilled_locations(self.player))) - len(itempool)
        if location_count < 0:
            if "The Great Cave Offensive" in self.options.included_subgames:
                sorted_treasures = sorted(treasures.items(), key=lambda treasure: treasure[1].value)
                while location_count < 0:
                    name, treasure = sorted_treasures.pop(0)
                    item = next((item for item in itempool if item.name == name), None)
                    if item:
                        itempool.remove(item)
                        treasure_value -= treasure.value
                        location_count += 1
            else:
                raise OptionError("Unable to create item pool with current settings.")
        itempool.extend([self.create_item(filler) for filler in
                         self.random.choices(list(filler_item_weights.keys()),
                                             weights=list(filler_item_weights.values()),
                                             k=location_count)])
        
        self.multiworld.itempool += itempool
        set_rules = set_rules

    
    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()), weights=list(filler_item_weights.values()), k=1)[0]
    
    def set_rules(self) -> None:
        # no current rules
        pass

    def generate_output(self, output_directory: str) -> None:
        patch = KSSUProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/KSSUAPPatch.bsdiff"))
        write_tokens(patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Options that are relevant to the client
        option_data = {
        "included_subgames": list(self.options.included_subgames.value),
        "required_subgames": list(self.options.required_subgames.value),
        "required_subgame_completions": self.options.required_subgame_completions.value,
        "starting_subgame": self.options.starting_subgame.value,
        "consumables": list(self.options.consumables.value),
        "essences": self.options.essences.value
        }

        return option_data