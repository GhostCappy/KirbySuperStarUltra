from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from typing import Iterable, TYPE_CHECKING, Optional

from .options import maingame_mapping

if TYPE_CHECKING:
    from . import KSSUWorld
    
starting_stage = 0x09EAC0

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().kssu_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes

class KSSUPathExtension(APPatchExtension):
    game = "Kirby Super Star Ultra"

class KSSUProcedurePatch(APProcedurePatch, APTokenMixin):
    # settings for what the end file is going to look like
    game = "Kirby Super Star Ultra"
    hash = "c0c84468ce0c9c7b3b97246ec443df1f"
    patch_file_ending = ".apkssu"
    result_file_ending = ".nds"
    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

def patch_rom(world: "KSSUWorld", patch: KSSUProcedurePatch) -> None:
    # starting subgame (index)
    patch.write_token("starting_maingame", world.options.starting_maingame.value)

    # numeric goal (how many subgames must be completed)
    patch.write_token(
        "required_subgame_completions",
        world.options.required_subgame_completions.value,
    )
    
    required_maingames = 0
    for val, maingame in maingame_mapping.items():
        if maingame in world.options.required_maingames:
            required_maingames_mask |= (1 << val)

    patch.write_token("required_maingames", required_maingames)
    
# Might need more added
def write_tokens(patch: KSSUProcedurePatch) -> None:
    patch.write_file("token_data.bin", patch.get_token_binary())
