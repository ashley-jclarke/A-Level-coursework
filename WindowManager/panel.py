# WindowManager/panel.py

from WindowManager.program import Program
from WindowManager.vec2 import Vec2
from WindowManager.ID_manager import IDManager
from WindowManager import pygame as pg
from WindowManager.passdowninfo import Passdowninfo

# Default Panel class to inherit from
class Panel:
	def __init__(self, child: Program|None=None, min_size: Vec2 = Vec2()):
		self.child = child				# The object that this panel will hold
		self.ID = IDManager.new_ID()	# Unique identifier for debugging
		self.min_size: Vec2 = min_size		# The minimum size that the panel can be
		
	# Default draw function
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		# Only call child's draw function if there is a child to avoid the error
		if self.child: self.child.draw(surface, pdi)


	# Default update function 
	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		if self.child:
			# try:
				self.child.update(surface, pdi)
			# except Exception as e:
			# 	print(self.child.ID, e)

	# Default function to draw two lines that represent the minimum size of the panel
	def draw_min_size(self, surface: pg.surface.Surface) -> None:
		# Horizontal line
		pg.draw.line(surface, (255,255,255), (0,0), (self.min_size.x,0), 4)
		# Vertical line
		pg.draw.line(surface, (255,255,255), (0,0), (0,self.min_size.y), 4)
