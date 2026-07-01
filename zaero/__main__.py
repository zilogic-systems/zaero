# zaero/__main__.py

import sys
import shutil
from pathlib import Path
from importlib.resources import files


def init_configs():
    config_dir = files("zaero").joinpath("config")
    destination = Path.cwd()

    for file in config_dir.iterdir():
        if file.name.endswith(".yaml"):
            dst = destination / file.name

            if dst.exists():
                answer = input(
                    f"{file.name} already exists. "
                    "Do you want to overwrite it? (y/N): "
                ).strip().lower()

                if answer in ("y", "yes"):
                    shutil.copy(file, dst)
                    print(f"Overwritten: {dst}")
                else:
                    print(f"Skipped: {dst}")
            else:
                shutil.copy(file, dst)
                print(f"Created: {dst}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("    python -m zaero init_config")
        return

    command = sys.argv[1]

    if command == "init_config":
        init_configs()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
