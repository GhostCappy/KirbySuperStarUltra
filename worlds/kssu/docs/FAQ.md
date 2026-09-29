# Frequently Asked Questions
  ***

### How would I dump this game from my console to play it with AP?

Here are a couple guides you can use to get a legal dump of your USA Kirby Super Star Ultra:

[Getting your 3DS set up](https://3ds.hacks.guide/) 

[Dumping your KSSU Catridge](https://wiki.hacks.guide/wiki/3DS:Dump_titles_and_game_cartridges)
___
### Does this project use AI? If so, how is it utilized?

- Kirby Super Star Ultra Archipelago is **not** vibe-coded
- Kirby Super Star Ultra Archipelago does **not** contain AI Art
- AI has not and will not be used to brainstorm or design any ideas or new features.
- LLMs have been used as a means to better understand the logic of certain functions (Which was done by looking through Ghidra's de-compiled C code).
- LLMs were rarely used as a [rubber duck](https://en.wikipedia.org/wiki/Rubber_duck_debugging) to help diagnose bugs early in development.
- The APWorld itself re-uses and tweaks some code from pre-existing worlds. For more information, please refer to the [credits](https://github.com/GhostCappy/KirbySuperStarUltra/blob/main/worlds/kssu/docs/credits.md) page.
- Documentation for all assembly changes can be found [here](https://docs.google.com/document/d/17oQgLhXj-Uu3xDFecNxVluyk4rJFPOidhxv2isrZJZo).

___
### Will there be PAL or JPN support in the future?

Most likely not, at least not from me. As the only dev at the moment, I only own the US version of the game.
In addition to this, it would be quite a long process as certain addresses greatly vary across versions.
If you're looking to help with this, feel free to reach out!

___
### Are there any known bugs?

- The "ability selection" menu in MWW is not accurate. It shows which abilities have been collected, not received. Selecting them does nothing, unless it was already received.
- The treasures on the pause screen of TGCO cannot be selected.
- When watching the beginner show, you may experience some visual bugs. It's best to skip these.

___
### I found another bug, where do I report it?

Report in the discord thread, which can be found [here](https://discord.com/channels/731205301247803413/1373856853775220836).
I will review it and try to fix it for a future version.

___  
### Is there a tracker for this game?

There is no dedicated tracker for this game at the moment. However, it was made in mind to be compatible with Universal Tracker, which
can be found [here](https://github.com/FarisTheAncient/Archipelago/releases)

___  
### How do I check the gold thresholds for TGCO (and other important items)? 

Inside the client, you can run /sub_area (area) to see how much gold is required to progress.
Ex. /sub_area Old Tower

There are also some other useful commands inside the client, including:
- /games (Shows all the games you currently have unlocked)
- /planets (Shows all the planets you currently have unlocked)
- /ability (Shows all the abilities you currently have unlocked)
- /keys (Shows all the keys / progressive stages you currently have.)
- /sub_area (Tells you the gold threshold to progress through an area in TGCO.)
___
### When I try to enter a game, it kicks me back out to the game select menu!

This happens when you try to enter a game you do not have unlocked yet. Double-check to make sure you are properly connected
with the LUA and to the Archipelago server.

___
### Are there any features you plan to add?

Most updates will focus on bug fixes and quality of life. Outside of those, some features I plan to add at a later date are:
- Traps
- Locking helpers in Helper to Hero based on abilities unlocked
- "Helpersanity" (Locations for each helper in Helper to Hero)
- "Foodsanity" (Locations for each food item)

___
### I lost my save game! How do I make sure this doesn't happen again?

In some versions of Bizhawk, there is an option that tries to save the game, but fails. You can turn this options off by
going to Config→Customize, switching to the advanced tab and turning off AutoSaveRAM. Another way to ensure that Bizhawk 
saves properly is by saving the game like normal (at a bed) and then going to File->Save Ram->Flush Save Ram or pressing 
Control+S

