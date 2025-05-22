from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension

# Change these values later
maxims = 0x7FA9F
one_ups = 0x7FABD
candies = 0x7FAD8
starting_stage = 0xAFCA3
goal_numeric = 0xAFCA8
goal_specific = 0xAFCB0
treasure_values = 0xAFCEF
mww_mode = 0xAFD6D

slot_data = 0x3FD00

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().KSSU_options.rom_file, "rb") as infile:
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

# Might need more added
def write_tokens(patch: KSSUProcedurePatch) -> None:
    patch.write_file("token_data.bin", patch.get_token_binary())