from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension


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


def write_tokens(patch: KSSUProcedurePatch) -> None:
    patch.write_file("token_data.bin", patch.get_token_binary())