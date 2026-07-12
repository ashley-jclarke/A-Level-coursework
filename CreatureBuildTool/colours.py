# CreatureBuildTool/colours.py

import json

with open("CreatureBuildTool/assets/theme.json", "r") as f:
	theme = json.load(f)

BORDER = theme["border"]
TEXT = theme["text"]
HOVER = theme["hover"]
BACKGROUND = theme["background"]
SELECTED = theme["selected"]
BUTTON = theme["button_background"]

