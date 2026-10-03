from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets

# Webpage for Archipelago page
class KSSUWeb(WebWorld):
    game = "Kirby Super Star Ultra"
    theme = "partyTime" 
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Kirby Super Star Ultra for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["NewSoupVi"],
    )
    
    tutorials = [setup_en]
    option_groups = option_groups
    options_presets = option_presets