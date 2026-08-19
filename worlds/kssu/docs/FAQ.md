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
- LLMs have been used as a means to better understand the logic of certain functions (Which was done by looking through Ghidra's de-compiled C code). However, it was not used to write code for assembly nor the APWorld.
- LLMs were rarely used as a [rubber duck](https://en.wikipedia.org/wiki/Rubber_duck_debugging) to help diagnose bugs early in development.

___
### Will there be PAL or JPN support in the future?

Most likely not, at least not from me. As the only dev at the moment, I only own the US version of the game.
In addition to this, it would be quite a long process as certain addresses greatly vary across versions.
If you're looking to help with this, feel free to reach out!

___
### I found a bug, where do I report it?

Report in the discord thread, which can be found [here](https://discord.com/channels/731205301247803413/1373856853775220836)
We will review it and try to fix it for a future version

___  
### Is there a tracker for this game?

There is no dedicated tracker for this game at the moment. However, it was made in mind to be compatible with Universal Tracker, which
can be found [here](https://github.com/FarisTheAncient/Archipelago/releases)

___
### When I try to enter a game, it kicks me back out to the game select menu!

This happens when you try to enter a game you do not have unlocked yet. Double-check to make sure you are properly connected
with the LUA and to the Archipelago server.

___
### I lost my save game! How do I make sure this doesn't happen again?

In some versions of Bizhawk, there is an option that tries to save the game, but fails. You can turn this options off by
going to Config→Customize, switching to the advanced tab and turning off AutoSaveRAM. Another way to ensure that Bizhawk 
saves properly is by saving the game like normal (at a bed) and then going to File->Save Ram->Flush Save Ram or pressing 
Control+S

