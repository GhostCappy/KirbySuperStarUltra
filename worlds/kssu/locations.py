from typing import NamedTuple
from BaseClasses import Location
from .names import location_names
from .items import BASE_ID

class KSSULocation(Location):
    game = "Kirby Super Star Ultra"
    
class LocationData(NamedTuple):
    code: int | None
    tag: str = ""
    
# Dont forget to change BASE_ID.
# Each stage location contains the items and boss of that stage 
# Useful for foodsanity
# Spring Breeze
green_greens_locations = {
    location_names.sb_whispy: LocationData(BASE_ID + 0),
}

float_islands_locations = {
    location_names.sb_lololo: LocationData(BASE_ID + 1),
}

bubbly_clouds_locations = {
    location_names.sb_kracko: LocationData(BASE_ID + 2),
}

mt_dedede_locations = {
    location_names.sb_dedede: LocationData(BASE_ID + 3),
    location_names.sb_complete: LocationData(None),
}

spring_breeze_locations = {
    **green_greens_locations,
    **float_islands_locations,
    **bubbly_clouds_locations,
    **mt_dedede_locations,
}

peanut_plains_locations = {
    location_names.db_stage_1: LocationData(BASE_ID + 4),
}

mallow_castle_locations = {
    location_names.db_stage_2: LocationData(BASE_ID + 5),
    location_names.db_switch_1: LocationData(BASE_ID + 9),
}

bonus_1_locations = {

}

cocoa_cave_locations = {
    location_names.db_stage_3: LocationData(BASE_ID + 6),
    location_names.db_iron_mam: LocationData(BASE_ID + 11),
}

candy_mountain_locations = {
    location_names.db_stage_4: LocationData(BASE_ID + 7),
    location_names.db_switch_2: LocationData(BASE_ID + 10),
}

bonus_2_locations = {

}

dyna_blade_nest_locations = {
    location_names.db_stage_5: LocationData(BASE_ID + 8),
    location_names.db_complete: LocationData(None),

}

dyna_blade_locations = {
    **peanut_plains_locations,
    **mallow_castle_locations,
    **cocoa_cave_locations,
    **candy_mountain_locations,
    **dyna_blade_nest_locations,
    #**bonus_1_locations,
    #**bonus_2_locations,
}

gourmet_race_locations = {
    location_names.gr_stage_1: LocationData(BASE_ID + 12),
    location_names.gr_stage_2: LocationData(BASE_ID + 13),
    location_names.gr_stage_3: LocationData(BASE_ID + 14),
    location_names.gr_complete: LocationData(None),
}

subtree_locations = {
    location_names.tgco_fatty_whale: LocationData(BASE_ID + 15),
    location_names.tgco_treasure_1: LocationData(BASE_ID + 19),
    location_names.tgco_treasure_2: LocationData(BASE_ID + 20),
    location_names.tgco_treasure_3: LocationData(BASE_ID + 21),
    location_names.tgco_treasure_4: LocationData(BASE_ID + 22),
    location_names.tgco_treasure_5: LocationData(BASE_ID + 23),
    location_names.tgco_treasure_6: LocationData(BASE_ID + 24),
    location_names.tgco_treasure_7: LocationData(BASE_ID + 25),
    location_names.tgco_treasure_8: LocationData(BASE_ID + 26),
    location_names.tgco_treasure_9: LocationData(BASE_ID + 27),
    location_names.tgco_treasure_10: LocationData(BASE_ID + 28),
    location_names.tgco_treasure_11: LocationData(BASE_ID + 29),
    location_names.tgco_treasure_12: LocationData(BASE_ID + 30),
    location_names.tgco_treasure_13: LocationData(BASE_ID + 31),
}

crystal_locations = {
    location_names.tgco_virus: LocationData(BASE_ID + 16),
    location_names.tgco_treasure_14: LocationData(BASE_ID + 32),
    location_names.tgco_treasure_15: LocationData(BASE_ID + 33),
    location_names.tgco_treasure_16: LocationData(BASE_ID + 34),
    location_names.tgco_treasure_17: LocationData(BASE_ID + 35),
    location_names.tgco_treasure_18: LocationData(BASE_ID + 36),
    location_names.tgco_treasure_19: LocationData(BASE_ID + 37),
    location_names.tgco_treasure_20: LocationData(BASE_ID + 38),
    location_names.tgco_treasure_21: LocationData(BASE_ID + 39),
    location_names.tgco_treasure_22: LocationData(BASE_ID + 40),
    location_names.tgco_treasure_23: LocationData(BASE_ID + 41),
    location_names.tgco_treasure_24: LocationData(BASE_ID + 42),
    location_names.tgco_treasure_25: LocationData(BASE_ID + 43),
    location_names.tgco_treasure_26: LocationData(BASE_ID + 44),
    location_names.tgco_treasure_27: LocationData(BASE_ID + 45),
    location_names.tgco_treasure_28: LocationData(BASE_ID + 46),
    location_names.tgco_treasure_29: LocationData(BASE_ID + 47),
}

old_tower_locations = {
    location_names.tgco_chameleon: LocationData(BASE_ID + 17),
    location_names.tgco_treasure_30: LocationData(BASE_ID + 48),
    location_names.tgco_treasure_31: LocationData(BASE_ID + 49),
    location_names.tgco_treasure_32: LocationData(BASE_ID + 50),
    location_names.tgco_treasure_33: LocationData(BASE_ID + 51),
    location_names.tgco_treasure_34: LocationData(BASE_ID + 52),
    location_names.tgco_treasure_35: LocationData(BASE_ID + 53),
    location_names.tgco_treasure_36: LocationData(BASE_ID + 54),
    location_names.tgco_treasure_37: LocationData(BASE_ID + 55),
    location_names.tgco_treasure_38: LocationData(BASE_ID + 56),
    location_names.tgco_treasure_39: LocationData(BASE_ID + 57),
    location_names.tgco_treasure_40: LocationData(BASE_ID + 58),
    location_names.tgco_treasure_41: LocationData(BASE_ID + 59),
    location_names.tgco_treasure_42: LocationData(BASE_ID + 60),
    location_names.tgco_treasure_43: LocationData(BASE_ID + 61),
    location_names.tgco_treasure_44: LocationData(BASE_ID + 62),
    location_names.tgco_treasure_45: LocationData(BASE_ID + 63),
}

garden_locations = {
    location_names.tgco_wham_bam: LocationData(BASE_ID + 18),
    location_names.tgco_complete: LocationData(None),
    location_names.tgco_treasure_46: LocationData(BASE_ID + 64),
    location_names.tgco_treasure_47: LocationData(BASE_ID + 65),
    location_names.tgco_treasure_48: LocationData(BASE_ID + 66),
    location_names.tgco_treasure_49: LocationData(BASE_ID + 67),
    location_names.tgco_treasure_50: LocationData(BASE_ID + 68),
    location_names.tgco_treasure_51: LocationData(BASE_ID + 69),
    location_names.tgco_treasure_52: LocationData(BASE_ID + 70),
    location_names.tgco_treasure_53: LocationData(BASE_ID + 71),
    location_names.tgco_treasure_54: LocationData(BASE_ID + 72),
    location_names.tgco_treasure_55: LocationData(BASE_ID + 73),
    location_names.tgco_treasure_56: LocationData(BASE_ID + 74),
    location_names.tgco_treasure_57: LocationData(BASE_ID + 75),
    location_names.tgco_treasure_58: LocationData(BASE_ID + 76),
    location_names.tgco_treasure_59: LocationData(BASE_ID + 77),
    location_names.tgco_treasure_60: LocationData(BASE_ID + 78),
}

tgco_locations = {
    **subtree_locations,
    **crystal_locations,
    **old_tower_locations,
    **garden_locations,
}

romk_chapter_1_locations = {
    location_names.romk_chapter_1: LocationData(BASE_ID + 79),
}

romk_chapter_2_locations = {
    location_names.romk_chapter_2: LocationData(BASE_ID + 80),
}

romk_chapter_3_locations = {
    location_names.romk_chapter_3: LocationData(BASE_ID + 81),
}

romk_chapter_4_locations = {
    location_names.romk_chapter_4: LocationData(BASE_ID + 82),
}

romk_chapter_5_locations = {
    location_names.romk_chapter_5: LocationData(BASE_ID + 83),
}

romk_chapter_6_locations = {
    location_names.romk_chapter_6: LocationData(BASE_ID + 84),
}

romk_chapter_7_locations = {
    location_names.romk_chapter_7: LocationData(BASE_ID + 85),
    location_names.romk_complete: LocationData(None),
}

revenge_of_meta_knight_locations = {
    **romk_chapter_1_locations,
    **romk_chapter_2_locations,
    **romk_chapter_3_locations,
    **romk_chapter_4_locations,
    **romk_chapter_5_locations,
    **romk_chapter_6_locations,
    **romk_chapter_7_locations,
}

floria_locations = {
    location_names.mww_floria: LocationData(BASE_ID + 87),
    location_names.mww_cutter: LocationData(BASE_ID + 88),
    location_names.mww_fighter: LocationData(BASE_ID + 89),
    location_names.mww_ice: LocationData(BASE_ID + 90),
}

aqualiss_locations = {
    location_names.mww_aqualiss: LocationData(BASE_ID + 91),
    location_names.mww_beam: LocationData(BASE_ID + 92),
    location_names.mww_parasol: LocationData(BASE_ID + 93),
    location_names.mww_sword: LocationData(BASE_ID + 94),

}

skyhigh_locations = {
    location_names.mww_skyhigh: LocationData(BASE_ID + 95),
    location_names.mww_jet: LocationData(BASE_ID + 96),
    location_names.mww_wheel: LocationData(BASE_ID + 97),
    location_names.mww_wing: LocationData(BASE_ID + 98),
}

hotbeat_locations = {
    location_names.mww_hotbeat: LocationData(BASE_ID + 99),
    location_names.mww_fire: LocationData(BASE_ID + 100),
    location_names.mww_suplex: LocationData(BASE_ID + 101),
}

cavios_locations = {
    location_names.mww_cavios: LocationData(BASE_ID + 102),
    location_names.mww_bomb: LocationData(BASE_ID + 103),
    location_names.mww_hammer: LocationData(BASE_ID + 104),
    location_names.mww_stone: LocationData(BASE_ID + 105),
}

mecheye_locations = {
    location_names.mww_mecheye: LocationData(BASE_ID + 106),
    location_names.mww_plasma: LocationData(BASE_ID + 107),
    location_names.mww_yoyo: LocationData(BASE_ID + 108),
}

halfmoon_locations = {
    location_names.mww_halfmoon: LocationData(BASE_ID + 109),
    location_names.mww_mirror: LocationData(BASE_ID + 110),
    location_names.mww_ninja: LocationData(BASE_ID + 111),
}

copy_planet_locations = {
    location_names.mww_copy: LocationData(BASE_ID + 112)
}

space_locations = {
    location_names.mww_complete: LocationData(None)
}

milky_way_wishes_locations = {
    **floria_locations,
    **aqualiss_locations,
    **skyhigh_locations,
    **hotbeat_locations,
    **cavios_locations,
    **mecheye_locations,
    **halfmoon_locations,
    **copy_planet_locations,
    **space_locations
}

the_arena_locations = {
    location_names.the_arena_1: LocationData(BASE_ID + 113),
    location_names.the_arena_2: LocationData(BASE_ID + 114),
    location_names.the_arena_3: LocationData(BASE_ID + 115),
    location_names.the_arena_4: LocationData(BASE_ID + 116),
    location_names.the_arena_5: LocationData(BASE_ID + 117),
    location_names.the_arena_6: LocationData(BASE_ID + 118),
    location_names.the_arena_7: LocationData(BASE_ID + 119),
    location_names.the_arena_8: LocationData(BASE_ID + 120),
    location_names.the_arena_9: LocationData(BASE_ID + 121),
    location_names.the_arena_10: LocationData(BASE_ID + 122),
    location_names.the_arena_11: LocationData(BASE_ID + 123),
    location_names.the_arena_12: LocationData(BASE_ID + 124),
    location_names.the_arena_13: LocationData(BASE_ID + 125),
    location_names.the_arena_14: LocationData(BASE_ID + 126),
    location_names.the_arena_15: LocationData(BASE_ID + 127),
    location_names.the_arena_16: LocationData(BASE_ID + 128),
    location_names.the_arena_17: LocationData(BASE_ID + 129),
    location_names.the_arena_18: LocationData(BASE_ID + 130),
    location_names.the_arena_19: LocationData(BASE_ID + 131),
    location_names.the_arena_complete: LocationData(None),
}

purple_plants_locations = {
    location_names.rotk_whispy: LocationData(BASE_ID + 150)
}

illusion_islands_locations = {
    location_names.rotk_lololo: LocationData(BASE_ID + 151)
}

crash_clouds_locations = {
    location_names.rotk_kracko: LocationData(BASE_ID + 152)
}

mt_dedede_sky_locations = {
    location_names.rotk_kabula: LocationData(BASE_ID + 153)
}

the_revenge_locations = {
    location_names.rotk_dedede: LocationData(BASE_ID + 154),
    location_names.rotk_complete: LocationData(None)
}

revenge_of_the_king_locations = {
    **purple_plants_locations,
    **illusion_islands_locations,
    **crash_clouds_locations,
    **mt_dedede_sky_locations,
    **the_revenge_locations
}

# This might need to be changed level to account for beating each individual stage within each level. 
# Memory address only updates stage count for each level.
mku_level_1_locations = {
    location_names.mku_level_1: LocationData(BASE_ID + 156)
}

mku_level_2_locations = {
    location_names.mku_level_2: LocationData(BASE_ID + 157)
}

mku_level_3_locations = {
    location_names.mku_level_3: LocationData(BASE_ID + 158)
}

mku_level_4_locations = {
    location_names.mku_level_4: LocationData(BASE_ID + 159)
}

mku_level_5_locations = {
    location_names.mku_level_5: LocationData(BASE_ID + 160),
    location_names.mku_complete: LocationData(None)
}

meta_knightmare_locations = {
    **mku_level_1_locations,
    **mku_level_2_locations,
    **mku_level_3_locations,
    **mku_level_4_locations,
    **mku_level_5_locations
}

helper_to_hero_locations = {
    location_names.hth_1: LocationData(BASE_ID + 909),
    location_names.hth_2: LocationData(BASE_ID + 910),
    location_names.hth_3: LocationData(BASE_ID + 911),
    location_names.hth_4: LocationData(BASE_ID + 912),
    location_names.hth_5: LocationData(BASE_ID + 913),
    location_names.hth_6: LocationData(BASE_ID + 914),
    location_names.hth_7: LocationData(BASE_ID + 915),
    location_names.hth_8: LocationData(BASE_ID + 916),
    location_names.hth_9: LocationData(BASE_ID + 917),
    location_names.hth_10: LocationData(BASE_ID + 918),
    location_names.hth_11: LocationData(BASE_ID + 919),
    location_names.hth_12: LocationData(BASE_ID + 920),
    location_names.hth_13: LocationData(BASE_ID + 921),
    location_names.hth_14: LocationData(BASE_ID + 922),
    location_names.hth_15: LocationData(BASE_ID + 923),
    location_names.hth_16: LocationData(BASE_ID + 924),
    location_names.hth_17: LocationData(BASE_ID + 925),
    location_names.hth_18: LocationData(BASE_ID + 926),
    location_names.hth_19: LocationData(BASE_ID + 927),
    location_names.hth_20: LocationData(BASE_ID + 928),
    location_names.helper_to_hero_complete: LocationData(None),
}

the_true_arena_locations = {
    location_names.the_true_arena_1: LocationData(BASE_ID + 210),
    location_names.the_true_arena_2: LocationData(BASE_ID + 211),
    location_names.the_true_arena_3: LocationData(BASE_ID + 212),
    location_names.the_true_arena_4: LocationData(BASE_ID + 213),
    location_names.the_true_arena_5: LocationData(BASE_ID + 214),
    location_names.the_true_arena_6: LocationData(BASE_ID + 215),
    location_names.the_true_arena_7: LocationData(BASE_ID + 216),
    location_names.the_true_arena_8: LocationData(BASE_ID + 217),
    location_names.the_true_arena_9: LocationData(BASE_ID + 218),
    location_names.the_true_arena_complete: LocationData(None), 
}

megaton_locations = {
    location_names.megaton_punch_1: LocationData(BASE_ID + 0x450),
    location_names.megaton_punch_2: LocationData(BASE_ID + 0x451),
    location_names.megaton_punch_3: LocationData(BASE_ID + 0x452),
}

samurai_locations = {
    location_names.samurai_kirby_1: LocationData(BASE_ID + 0x500),
    location_names.samurai_kirby_2: LocationData(BASE_ID + 0x501),
    location_names.samurai_kirby_3: LocationData(BASE_ID + 0x502),
    location_names.samurai_kirby_4: LocationData(BASE_ID + 0x503),
    location_names.samurai_kirby_5: LocationData(BASE_ID + 0x504),
}

card_swipe_locations = {
    location_names.kirby_card_swipe_1: LocationData(BASE_ID + 0x550),
    location_names.kirby_card_swipe_2: LocationData(BASE_ID + 0x551),
    location_names.kirby_card_swipe_3: LocationData(BASE_ID + 0x552),
}

kotd_locations = {
    location_names.kirby_on_the_draw_1: LocationData(BASE_ID + 0x600),
    location_names.kirby_on_the_draw_2: LocationData(BASE_ID + 0x601),
    location_names.kirby_on_the_draw_3: LocationData(BASE_ID + 0x602),
}

snack_track_locations = {
    location_names.snack_tracks_1: LocationData(BASE_ID + 0x650),
    location_names.snack_tracks_2: LocationData(BASE_ID + 0x651),
    location_names.snack_tracks_3: LocationData(BASE_ID + 0x652),
}

subgame_locations = {
    **megaton_locations,
    **samurai_locations,
    **card_swipe_locations,
    **kotd_locations,
    **snack_track_locations
}

location_table = {
    **spring_breeze_locations,
    **dyna_blade_locations,
    **gourmet_race_locations,
    **tgco_locations,
    **revenge_of_meta_knight_locations,
    **milky_way_wishes_locations,
    **the_arena_locations,
    **revenge_of_the_king_locations,
    **meta_knightmare_locations,
    **helper_to_hero_locations,
    **the_true_arena_locations,
    **subgame_locations
}

__all__ = [
    "KSSULocation", "LocationData",
    "green_greens_locations", "float_islands_locations", "bubbly_clouds_locations", "mt_dedede_locations",
    "spring_breeze_locations", "peanut_plains_locations", "mallow_castle_locations", "cocoa_cave_locations",
    "candy_mountain_locations", "bonus_1_locations", "bonus_2_locations", "dyna_blade_nest_locations",
    "dyna_blade_locations", "gourmet_race_locations", "subtree_locations", "crystal_locations",
    "old_tower_locations", "garden_locations", "tgco_locations", "romk_chapter_1_locations",
    "romk_chapter_2_locations", "romk_chapter_3_locations", "romk_chapter_4_locations",
    "romk_chapter_5_locations", "romk_chapter_6_locations", "romk_chapter_7_locations",
    "revenge_of_meta_knight_locations", "floria_locations", "aqualiss_locations", "skyhigh_locations",
    "hotbeat_locations", "cavios_locations", "mecheye_locations", "halfmoon_locations",
    "copy_planet_locations", "space_locations", "milky_way_wishes_locations", "the_arena_locations",
    "purple_plants_locations", "illusion_islands_locations", "crash_clouds_locations",
    "mt_dedede_sky_locations", "the_revenge_locations", "revenge_of_the_king_locations",
    "mku_level_1_locations", "mku_level_2_locations", "mku_level_3_locations", "mku_level_4_locations",
    "mku_level_5_locations", "meta_knightmare_locations", "helper_to_hero_locations", 
    "the_true_arena_locations", "megaton_locations", "samurai_locations", "card_swipe_locations", 
    "kotd_locations", "snack_track_locations", "subgame_locations", "location_table"
]