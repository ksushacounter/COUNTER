import PyInstaller.__main__
from pathlib import Path
import os

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")


def install():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--clean",
            "--onefile",
            "--windowed",
            "--add-data=./cratonml_gui/Themes/images/light/*{sep}./cratonml_gui/Themes/images/light/".format(
                sep=os.pathsep
            ),
            "--add-data=./cratonml_gui/Themes/images/dark/*{sep}./cratonml_gui/Themes/images/dark/".format(
                sep=os.pathsep
            ),
            "--add-data=./cratonml_gui/icons/icon.png{sep}./cratonml_gui/icons/".format(
                sep=os.pathsep
            ),
            "--add-data=./cratonml_gui/icons/splash.png{sep}./cratonml_gui/icons/".format(
                sep=os.pathsep
            ),
            "--icon=cratonml_gui/icons/icon.png",
            "-nMLToolBox",
            # other pyinstaller options...
        ]
    )
