# CreatureBuildTool/moveable_border.py

from WindowManager.divider import Divider
from WindowManager.containersplit import ContainerSplit
from CreatureBuildTool import colours
from WindowManager import pygame as pg
from WindowManager.interface import Interface
from WindowManager.passdowninfo import Passdowninfo

class MoveBorder(Divider): 
	def __init__(self, 
			  interface: Interface, 
			  position:float=0.5, 
			  pointer:int=-1, 
			  SPLIT_MODE:int=ContainerSplit.SPLIT_X):
		super().__init__(interface, position, pointer, SPLIT_MODE)

		self.open_width = 5	
		self.state_change_disabled = True
		self.unit = Divider.UNIT_PERCENTAGE


	def draw(self, surface:pg.surface.Surface, pdi: Passdowninfo):
		# Fill with the border colour
		surface.fill(colours.BORDER)