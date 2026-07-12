from WindowManager.panel import Panel
from CreatureBuildTool import colours
from WindowManager import pygame as pg
from WindowManager.passdowninfo import Passdowninfo

class Spacer(Panel):
	def __init__(self):
		super().__init__()
	
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		surface.fill(colours.BUTTON)


