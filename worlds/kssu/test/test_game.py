from . import KSSUTestBase
from ..options import IncludedMainGames
from ..names import item_names, location_names
from ..items import treasures, copy_abilities, planets

class MaingameTest(KSSUTestBase):
    options = {
        "included_maingames": frozenset(IncludedMainGames.valid_keys),
        "required_maingame_completions": 1,
    }


class TestSpringBreeze(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 0,
        "required_maingames": {"Spring Breeze"}
    }


    # no extra tests needed really, spring breeze logic is simple

    def test_beatable(self):
        self.assertBeatable(True)

class TestGourmetRace(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 2,
        "required_mainames": {"Gourmet Race"}
    }

    # no extra tests needed really, gourmet race logic is simple

    def test_beatable(self):
        self.assertBeatable(True)

# now for the complex ones

class TestDynaBlade(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 1,
        "required_maingames": {"Dyna Blade"},
    }

    def test_accessibility(self):
        self.assertBeatable(False) # we need at least 4 progressive stages
        self.assertFalse(self.can_reach_region("Dyna Blade Bonus 1"))
        self.assertFalse(self.can_reach_region("Dyna Blade Bonus 2"))
        # grant the first extra item
        self.collect_by_name(item_names.dyna_blade_ex1)
        self.assertFalse(self.can_reach_region("Dyna Blade Bonus 1")) # Cannot reach it without at least 1 stage
        self.collect_by_name(item_names.dyna_blade_ex2)
        self.assertFalse(self.can_reach_region("Dyna Blade Bonus 2")) # Cannot reach it without at least 3 stages
        stages = self.get_items_by_name(item_names.progressive_dyna_blade)
        for i, stage in enumerate(stages):
            self.collect(stage)
            self.assertTrue(self.can_reach_region("Dyna Blade Bonus 1"))
            if i >= 2:
                self.assertTrue(self.can_reach_region("Dyna Blade Bonus 2"))
            else:
                self.assertFalse(self.can_reach_region("Dyna Blade Bonus 2"))
            self.assertBeatable(i == 3)

class TestGreatCave(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 3,
        "required_maingames": {"The Great Cave Offensive"}
        # run default options for thresholds/required
    }

    def test_accessibility(self):
        self.assertBeatable(False) # we need treasures
        # now this is kind of a pain to solve specifics for
        # so we'll just collect in order and check that state matches what we expect
        treasure_total = 0
        thresholds = self.world.treasure_value
        for name, treasure in treasures.items():
            self.collect_by_name(name)
            treasure_total += treasure.value
            for i, reg in enumerate(("Crystal", "Old Tower", "Garden", "Goal")):
                if reg == "Goal":
                    self.assertBeatable(treasure_total >= thresholds[i])
                elif treasure_total >= thresholds[i]:
                    self.assertTrue(self.can_reach_region(reg))
                else:
                    self.assertFalse(self.can_reach_region(reg))

    def test_treasures(self):
        self.collect_by_name(treasures.keys()) # gain access to all regions so we can check individual locations
        self.assertAccessDependency([location_names.tgco_treasure_4], [[item_names.plasma], [item_names.wing]], True)
        self.assertAccessDependency([location_names.tgco_treasure_7], [[item_names.plasma], [item_names.wing], [item_names.beam]], True)
        self.assertAccessDependency([location_names.tgco_treasure_13], [[item_names.sword], [item_names.cutter], [item_names.wing]], True)
        self.assertAccessDependency([location_names.tgco_treasure_18, location_names.tgco_treasure_19,
                                     location_names.tgco_treasure_20, location_names.tgco_treasure_21,
                                     location_names.tgco_treasure_22, location_names.tgco_treasure_28],
                                    [[item_names.crash], [item_names.bomb],
                                     [item_names.yoyo], [item_names.beam]], True)
        self.assertAccessDependency([location_names.tgco_treasure_31, location_names.tgco_treasure_33],
                                    [[item_names.hammer], [item_names.stone]], True)
        self.assertAccessDependency([location_names.tgco_treasure_32], [[item_names.hammer, item_names.fire], [item_names.stone, item_names.fire]], True)
        self.assertAccessDependency([location_names.tgco_treasure_34], [
            [item_names.plasma], [item_names.wing], [item_names.jet], [item_names.stone], [item_names.hammer],
            [item_names.bomb], [item_names.beam], [item_names.cutter], [item_names.parasol]], True)
        self.assertAccessDependency([location_names.tgco_treasure_36], [[item_names.plasma], [item_names.beam], [item_names.yoyo]], True)
        self.assertAccessDependency([location_names.tgco_treasure_37], [[item_names.plasma], [item_names.parasol], [item_names.hammer], [item_names.bomb], [item_names.stone], [item_names.beam], [item_names.yoyo]], True)
        self.assertAccessDependency([location_names.tgco_treasure_42], [[item_names.stone]], True)
        self.assertAccessDependency([location_names.tgco_treasure_43], [[item_names.plasma], [item_names.ninja, item_names.stone], [item_names.sword, item_names.stone], [item_names.wing, item_names.stone]], True)
        self.assertAccessDependency([location_names.tgco_treasure_45], [[item_names.jet], [item_names.fire]], True)
        self.assertAccessDependency([location_names.tgco_treasure_47], [[item_names.jet], [item_names.ninja], [item_names.wing]], True)
        self.assertAccessDependency([location_names.tgco_treasure_49], [[item_names.jet]], True)
        self.assertAccessDependency([location_names.tgco_treasure_52], [[item_names.plasma], [item_names.wing], [item_names.parasol]], True)
        self.assertAccessDependency([location_names.tgco_treasure_53], [[item_names.wheel]], True)
        self.assertAccessDependency([location_names.tgco_treasure_58], [[item_names.beam], [item_names.crash]], True)
        self.assertAccessDependency([location_names.tgco_treasure_59], [[item_names.ninja], [item_names.sword], [item_names.cutter], [item_names.wing]], True)

class TestMetaKnight(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 4,
        "required_maingames": {"Revenge of Meta Knight"}
    }

    def test_accessibility(self):
        self.assertBeatable(False) # need a couple of copy abilities at least
        self.assertTrue(self.can_reach_region("RoMK - Chapter 1"))
        self.assertTrue(self.can_reach_region("RoMK - Chapter 2"))
        self.assertTrue(self.can_reach_region("RoMK - Chapter 3"))
        self.assertFalse(self.can_reach_region("RoMK - Chapter 4"))
        self.collect_by_name(item_names.fire)
        self.assertTrue(self.can_reach_region("RoMK - Chapter 4"))
        self.assertFalse(self.can_reach_region("RoMK - Chapter 5"))
        self.collect_by_name(item_names.beam) # multiple options here
        self.assertTrue(self.can_reach_region("RoMK - Chapter 5"))
        self.assertTrue(self.can_reach_region("RoMK - Chapter 6"))
        self.assertFalse(self.can_reach_region("RoMK - Chapter 7"))
        self.collect_by_name(item_names.wing)
        self.assertTrue(self.can_reach_region("RoMK - Chapter 7"))
        self.assertBeatable(True)

class TestMilkyWayWishes(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 5,
        "required_maingames": {"Milky Way Wishes"},
        "milky_way_wishes_mode": "local", # multiworld could warrant another test
    }

    def test_accessibility(self):
        self.assertBeatable(False)
        # first, we need to know which planet was our starting option
        starting_planet = next((item.name for item in self.multiworld.precollected_items[self.player] if item.name in planets), None)
        if not starting_planet:
            self.fail("No starting planet found")
        self.assertTrue(self.can_reach_region(starting_planet))
        other_planets = [planet for planet in planets.keys() if planet not in (starting_planet, item_names.copy_planet)]
        for i, planet in enumerate(other_planets):
            self.assertFalse(self.can_reach_region(planet))
            self.collect_by_name(planet)
            self.assertTrue(self.can_reach_region(planet))
            self.assertBeatable(i == (len(other_planets) - 1))


class TestArena(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 6,
        "required_maingames": {"The Arena"},
    }

    def test_accessibility(self):
        # pretty simple, need 5 abilities excluding Crash
        self.assertBeatable(False)
        abilities = self.get_items_by_name([item for item in copy_abilities.keys() if
                                            item not in (item_names.crash, item_names.paint, item_names.sleep,
                                                         item_names.mike, item_names.cook)])
        # collect the first 4
        self.collect(abilities[:4])
        self.assertBeatable(False)
        self.collect_by_name(item_names.mike)
        self.assertBeatable(False)
        self.collect_by_name(item_names.crash)
        self.assertBeatable(False)
        self.collect(abilities[4:])
        self.assertBeatable(True)

class TestRevengeKing(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 7,
        "required_maingames": {"Revenge of the King"}
    }

    def test_beatable(self):
        self.assertBeatable(True)

class TestMetaUltra(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 8,
        "required_maingames": {"Meta Knightmare Ultra"}
    }

    def test_beatable(self):
        self.assertBeatable(True)

class TestHelperHero(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 9,
        "required_maingames": {"Helper to Hero"}
    }

    def test_beatable(self):
        self.assertBeatable(True)

class TestTrueArena(MaingameTest):
    options = {
        **MaingameTest.options,
        "starting_maingame": 10,
        "required_maingames": {"The True Arena"}
    }

    def test_beatable(self):
        self.assertBeatable(True)