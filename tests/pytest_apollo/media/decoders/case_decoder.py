from pathlib import PurePath

from pytest_cases import parametrize

from configs import settings


CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")


@parametrize(
    "file",
    [
        "example_48000H_1C.mp3",
        "example_48000H_2C.mp3",
        "example_44100H_1C.mp3",
        "example_44100H_2C.mp3",
        "example_32000H_1C.mp3",
        "example_32000H_2C.mp3",
        "example_48000H_2C_TAGGED.mp3",
    ],
)
def files_mp3(file: str):
    return MEDIA_FOLDER / "mp3" / file
