import json
import os
import sys
from pathlib import PurePath as Path
from typing import Union

import PyInstaller.__main__
import tomli


def kwargs_flat(kwarg: str, _list: Union[list, filter, map]):
    counter = 0
    for i in range(len(_list) * 2):
        if (i % 2) != 0:
            yield _list[counter]
            counter += 1
            continue
        yield kwarg


ROOT = Path(os.path.dirname(__file__))
toml = Path(os.path.dirname(__file__), "pyproject.toml")
with open(toml, "rb") as file:
    parsed = tomli.load(file).get("tool")


base = "Win32GUI"
name = parsed.get("poetry").get("name")
version = parsed.get("poetry").get("version")
description = parsed.get("poetry").get("description")
authors = parsed.get("poetry").get("authors")
_license = parsed.get("poetry").get("license")
readme = parsed.get("poetry").get("readme")
dev_dependencies = parsed.get("poetry").get("dev-dependencies")
dependencies = parsed.get("poetry").get("dependencies")
del dependencies["python"]

exe_options = [
    str(Path(os.path.dirname(__file__), "apollo", "__main__.py")),
    *(
        "--clean",
        "-y",
        "--noupx",
        "--onedir",
        "--windowed",
        "--no-embed-manifest",
        "--win-private-assemblies",
    ),
    # *("--debug", "imports"),
    *("--log-level", "WARN"),
    *("--name", "Apollo"),
    *("--icon", str(ROOT / "icon.ico")),
    *("--specpath", str(ROOT / "dist")),
    *("--distpath", str(ROOT / "dist")),
    *("--workpath", str(ROOT / "dist" / "build")),
    *kwargs_flat(
        "--add-data",
        [
            os.pathsep.join((str(ROOT / "LICENSE"), ".")),
            os.pathsep.join((str(ROOT / "readme.md"), ".")),
            os.pathsep.join((str(ROOT / "icon.ico"), ".")),
            os.pathsep.join((str(ROOT / "icon.bmp"), ".")),
            os.pathsep.join((str(ROOT / "splash.bmp"), ".")),
            os.pathsep.join((str(ROOT / "configs"), "configs")),
            *[
                os.pathsep.join((str(ROOT / "configs" / file), "configs"))
                for file in os.listdir(str(ROOT / "configs"))
            ],
            os.pathsep.join((str(ROOT / "vendor"), "vendor")),
            *[
                os.pathsep.join((str(ROOT / "vendor" / file), "vendor"))
                for file in os.listdir(str(ROOT / "vendor"))
            ],
        ],
    ),
    *kwargs_flat("--collect-all", ["apollo", "dynaconf"]),
    *kwargs_flat("--hidden-import", ["dynaconf", "python-dotenv"]),
    *kwargs_flat("--paths", [str(ROOT)]),
]

# noinspection PyUnresolvedReferences
print(json.dumps(exe_options, indent=2))
sys.path.insert(0, str(ROOT))
PyInstaller.__main__.run(exe_options)
