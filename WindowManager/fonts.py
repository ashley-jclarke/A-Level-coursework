# WindowManager/fonts.py

from WindowManager import pygame as pg

pg.font.init()

# The current font
FONT = "0xProtoNerdFontMono"

# Load the fonts through pygame
REGULAR = pg.font.Font(f"WindowManager/fonts/{FONT}-Regular.ttf", 20)
BOLD = pg.font.Font(f"WindowManager/fonts/{FONT}-Bold.ttf", 20)
REGULAR_SMALL = pg.font.Font(f"WindowManager/fonts/{FONT}-Regular.ttf", 12)
BOLD_SMALL = pg.font.Font(f"WindowManager/fonts/{FONT}-Bold.ttf", 12)

