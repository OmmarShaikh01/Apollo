import os
from pathlib import PurePath

import mutagen
from mutagen.id3 import APIC, ASPI, Frames, ID3, SYLT
from mutagen.id3._specs import SpecError

from apollo.utils import get_logger
from configs import settings

CONFIG = settings
LOGGER = get_logger(__name__)
ROOT_DIR = PurePath(os.path.dirname(__file__))
RAW_FILE = ROOT_DIR / 'dsd' / 'example.dsf'
SOX = CONFIG.SOX_PATH


def create_mp3():
    if os.path.isdir(ROOT_DIR / 'mp3'):
        # import shutil
        # shutil.rmtree(ROOT_DIR / 'mp3')
        return None

    COMPRESSION = 320
    os.mkdir(ROOT_DIR / 'mp3')
    OUTPUT = ROOT_DIR / 'mp3' / 'example_48000H_1C.mp3'
    os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 48000 -c 1 {OUTPUT}")
    OUTPUT = ROOT_DIR / 'mp3' / 'example_48000H_2C.mp3'
    os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 48000 -c 2 {OUTPUT}")
    OUTPUT = ROOT_DIR / 'mp3' / 'example_44100H_1C.mp3'
    os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 44100 -c 1 {OUTPUT}")
    OUTPUT = ROOT_DIR / 'mp3' / 'example_44100H_2C.mp3'
    os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 44100 -c 2 {OUTPUT}")
    OUTPUT = ROOT_DIR / 'mp3' / 'example_32000H_1C.mp3'
    os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 32000 -c 1 {OUTPUT}")
    OUTPUT = ROOT_DIR / 'mp3' / 'example_32000H_2C.mp3'
    os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 32000 -c 2 {OUTPUT}")

    # adds tags
    # noinspection PyBroadException
    try:
        OUTPUT = ROOT_DIR / 'mp3' / 'example_48000H_2C_TAGGED.mp3'
        os.system(f"{SOX} {RAW_FILE} -C{COMPRESSION} -r 48000 -c 2 {OUTPUT}")

        FILE = mutagen.File(OUTPUT)
        FILE.add_tags()
        TAGS = FILE.tags

        for name, item in Frames.items():
            try:
                if name == 'APIC':
                    with open(PurePath(CONFIG.assets_dir, "example.png"), 'rb') as data_file:
                        TAGS.add(APIC(encoding = 0, mime = u'image/png', data = data_file.read()))
                elif name == 'SYLT':
                    TAGS.add(SYLT(text = [("Foo", 1), ("Bar", 2)]))
                elif name == 'ASPI':
                    TAGS.add(ASPI(S=0, L=0, N=0, b=0, Fi=[1, 2, 3, 4]))
                else:
                    TAGS.add(item(text = ["TESTING"]))
                FILE.save()

            except (ValueError, SpecError) as e:
                LOGGER.exception(f"{name} EXCEPTION: {e}")
                TAGS.delall(name)

    except Exception as e:
        LOGGER.exception(f"EXCEPTION: {e}")

    FILE = mutagen.File(OUTPUT)
    LOGGER.debug(FILE.tags)


def main():
    create_mp3()  # pass


if __name__ == '__main__':
    main()
