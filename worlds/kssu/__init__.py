import os
import typing
import logging
import pkgutil

# Shows warning but should work without issue
import settings
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, MultiWorld, ItemClassification
from Options import OptionError

from typing import Any, Mapping

from .names import item_names
from .rom import KSSUProcedurePatch, write_tokens
from .regions import create_regions
from .options import KSSUOptions, maingame_mapping, IncludedMaingames, Consumables
from .client import KSSUClient 
from .items import (item_lookup_by_name, item_table, item_groups, KSSUItem, filler_item_weights, copy_abilities,
                    main_games, dyna_items, planets, treasures, trap)
from .locations import location_lookup_by_name
from .rules import set_rules

logger = logging.getLogger("Kirby Super Star Ultra")

# Webpage for Archipelago page
class KSSUWeb(WebWorld):
    theme = "partyTime" 
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Kirby Super Star Ultra for Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["GhostCappy"],
        )
    ]
    
# Details for game ROM
class KSSUSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Kirby Super Star Ultra rom"""

        copy_to = "Kirby Super Star Ultra (USA).nds"
        description = "Kirby Super Star Ultra (USA) ROM File"
        md5s = ["c0c84468ce0c9c7b3b97246ec443df1f"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True

# APWorld information
class KSSUWorld(World):
    """
    Kirby Super Star Ultra is a remake of the Super Nintendo Entertainment System game Kirby Super Star.
    The remake retains all game modes found in the original and adds four major new ones.
    """
    game = "Kirby Super Star Ultra"
    item_name_groups = item_groups
    options_dataclass = KSSUOptions
    options: KSSUOptions
    web = KSSUWeb()
    settings: typing.ClassVar[KSSUSettings]
    item_name_to_id = item_lookup_by_name
    location_name_to_id = location_lookup_by_name
    
    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_count: int = 0
        
    # Probably needs more future work
    # Verifies user options
    def generate_early(self) -> None:
        if not self.options.included_maingames.value.intersection(
                {"The Great Cave Offensive", "Milky Way Wishes", "The Arena"}):
            raise OptionError(f"Kirby Super Star Ultra({self.player_name}): At least one of The Great Cave Offensive, "
                              f"Milky Way Wishes, or The Arena must be included")

        for game in sorted(self.options.required_maingames.value):
            if game not in self.options.included_maingames.value:
                logger.warning(F"Kirby Super Star Ultra({self.player_name}): Required main-game {game} not included, "
                               F"adding to included main-games")
                self.options.included_maingames.value.add(game)

        if self.options.starting_maingame.current_option_name not in self.options.included_maingames:
            logger.warning(f"Kirby Super Star Ultra({self.player_name}): Starting maingame not included, choosing random.")
            self.options.starting_maingame.value = self.random.choice([value[0] for value in maingame_mapping.items()
                                                                      if value[1] in self.options.included_maingames])

        if self.options.required_maingame_completions > len(self.options.included_maingames.value):
            logger.warning(f"Kirby Super Star Ultra ({self.player_name}): Required maingame count greater than "
                           f"included maingames, reducing to all included.")
            self.options.required_maingame_completions.value = len(self.options.included_maingames.value)
                
            # proper UT support
        if hasattr(self.multiworld, "generation_is_fake"):
            self.options.included_maingames = IncludedMaingames.valid_keys
            self.options.consumables.value = Consumables.valid_keys
            self.options.essences.value = True
                
    def create_item(self, name, force_classification: ItemClassification | None = None):
        if name not in item_table:
            raise Exception(f"{name} is not a valid item name for Kirby Super Star.")
        data = item_table[name]
        classification = force_classification if force_classification else data.classification
        return KSSUItem(name, classification, data.code, self.player)

    def create_items(self) -> None:
        itempool = []
        modes = [self.create_item(name) for name in main_games if name in self.options.included_maingames]
        starting_mode = self.create_item(maingame_mapping[self.options.starting_maingame])
        modes.remove(starting_mode)
        self.multiworld.push_precollected(starting_mode)
        itempool.extend([self.create_item(name) for name in copy_abilities])
        itempool.extend(modes)
        
        if "Dyna Blade" in self.options.included_maingames:
            force = None
            if not self.options.essences and "Maxim Tomato" not in self.options.consumables:
                force = ItemClassification.useful
            itempool.extend([self.create_item(name, force) for name in dyna_items])
        if "The Great Cave Offensive" in self.options.included_maingames:
            for name, treasure in sorted(treasures.items(), key=(lambda treasure: treasure[1].value), reverse=True):
                itempool.append(self.create_item(name))
        if "Milky Way Wishes" in self.options.included_maingames:
            planet = [self.create_item(name) for name in planets]
            starting_planet = self.random.choice(planet)
            planet.remove(starting_planet)
            self.multiworld.push_precollected(starting_planet)
            itempool.extend(planet)

            if self.options.milky_way_wishes_mode == "multiworld":
                itempool.extend(self.create_item(item_names.rainbow_star) for _ in range(7))
                
        location_count = len(list(self.multiworld.get_unfilled_locations(self.player))) - len(itempool)
        if location_count < 0:
            if "The Great Cave Offensive" in self.options.included_maingames:
                sorted_treasures = sorted(treasures.items(), key=lambda treasure: treasure[1].value)
                while location_count < 0:
                    name, treasure = sorted_treasures.pop(0)
                    item = next((item for item in itempool if item.name == name), None)
                    if item:
                        itempool.remove(item)
                        location_count += 1
            else:
                raise OptionError("Unable to create item pool with current settings.")
        itempool.extend([self.create_item(filler) for filler in
                         self.random.choices(list(filler_item_weights.keys()),
                                             weights=list(filler_item_weights.values()),
                                             k=location_count)])
        
        self.multiworld.itempool += itempool

    # Proably needs more future work
    def create_regions(self) -> None:
        create_regions(self)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()), weights=list(filler_item_weights.values()), k=1)[0]
    
    def set_rules(self) -> None:
        set_rules(self, self.disabled_locations)

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
        "included_maingames": list(self.options.included_maingames.value),
        "required_maingames": list(self.options.required_maingames.value),
        "required_maingame_completions": self.options.required_maingame_completions.value,
        "starting_maingame": self.options.starting_maingame.value,
        "consumables": list(self.options.consumables.value),
        "essences": self.options.essences.value
        }

        return option_data