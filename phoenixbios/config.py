from pathlib import Path
import yaml

with open("../config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

motherboards = []
with open("../motherboards.txt", 'r', encoding="utf-8") as f:
    for card_name in f.readlines():
        card_name = card_name.strip()
        if card_name:
            motherboards.append(card_name)

MOTHERBOARDS = motherboards
PHOENIX_EXE_PATH = CONFIG["phoenix_editor_path"]
FILENAME = CONFIG["file_name"]
FILEPATH = CONFIG["file_path"]
LAUNCH_TYPE = CONFIG["launch_type"] #todo 19.02.2022 17:14 taima:

FILE_SAVE_NAME = CONFIG["save_file_name"]
FILE_SAVE_PATH = CONFIG["save_file_path"]