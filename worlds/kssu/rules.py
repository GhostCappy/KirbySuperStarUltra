from typing import Dict, TYPE_CHECKING
from .items import sub_game_completion
from .names import location_names, item_names
from worlds.generic.Rules import set_rule, add_rule

if TYPE_CHECKING:
    from . import KSSUWorld


def set_rules(world: "KSSUWorld", excluded):
    player = world.player
    options = world.options