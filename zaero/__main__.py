# Copyright 2026 Zilogic Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import shutil
from pathlib import Path
from importlib.resources import files
import zaero.utils.zi_logger as zi_logger


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
                    zi_logger.log(f"Overwritten: {dst}")
                else:
                    zi_logger.log(f"Skipped: {dst}")
            else:
                shutil.copy(file, dst)
                zi_logger.log(f"Created: {dst}")

def main():
    if len(sys.argv) < 2:
        zi_logger.log("Usage:")
        zi_logger.log("    python -m zaero init_config")
        return

    command = sys.argv[1]

    if command == "init_config":
        init_configs()
    else:
        zi_logger.log(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
