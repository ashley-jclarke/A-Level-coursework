# WindowManager/program.py

from WindowManager.passdowninfo import Passdowninfo
from WindowManager.vec2 import Vec2
from WindowManager import pygame as pg
from WindowManager.ID_manager import IDManager
# from WindowManager.fonts import REGULAR_SMALL

class Program:
	def __init__(self):
		self.ID = IDManager.new_ID()	# Unique identifier for debugging
	# Get the mouse position and return its position relative to the top left position of the panel
	@staticmethod
	def get_relative_mouse_pos(pdi: Passdowninfo) -> Vec2:
		start = pdi.top_left_position					# Top left corner of the panel

		mouse_pos = pg.mouse.get_pos()					# The global position of the mouse
		mouse_pos = Vec2(mouse_pos[0], mouse_pos[1])	# Convert to Vec2 data type

		relative_mouse_pos = mouse_pos - start			# Make local/relative to the panel
		return relative_mouse_pos						# Return value
	
	# Function to check if the mouse is inside the panel
	@staticmethod
	def mouse_in_panel(surface: pg.surface.Surface, pdi: Passdowninfo) -> bool:
		mouse_pos = Program.get_relative_mouse_pos(pdi)		# Get the relative mouse position
		surface_size = surface.get_size()					# Get the size of the panel
		surface_size = Vec2(surface_size[0], surface_size[1])

		# Check the local position against the boundaries. 
		in_bound = mouse_pos.x > 0 and mouse_pos.x <= surface_size.x and mouse_pos.y > 0 and mouse_pos.y <= surface_size.y
		return in_bound
	# no. inherited functions
	def update(self, surface:pg.surface.Surface, pdi: Passdowninfo) -> None:
		...
	def draw(self, surface:pg.surface.Surface, pdi: Passdowninfo) -> None:
		...



# #! DEMO __PROGRAMS__

# from random import randrange
# class DemoProgram(Program):
# 	def __init__(self):
# 		super().__init__()	# Calls the Program initiation
# 		max_value = 140		# Largest value for the value
# 							# Create the colour value for the panel
# 		self.colour = (randrange(max_value),randrange(max_value),randrange(max_value))


# 	def draw(self,surface:pg.surface.Surface, pdi: Passdowninfo):
# 		# Fill the panel with the programs colour
# 		surface.fill(self.colour)
# 		# pass


# import time
# class FPSProgram(Program):
# 	def __init__(self):
# 		super().__init__()
# 		self.before = time.time()
# 		self.fps = 0
# 		self.last_check = self.before
# 		self.display_fps = self.fps
# 	def update(self, surface, pdi):
# 		super().update(surface, pdi)
# 		now = time.time()
# 		elapsed = now - self.before
# 		self.fps = round(1/elapsed,1)
# 		self.before = now

# 		if self.before > self.last_check + 1:
# 			self.last_check = self.before
# 			self.display_fps = self.fps
# 	def draw(self, surface, pdi):
# 		text_surface = REGULAR_SMALL.render(str(self.display_fps), False, (255,255,255))
# 		surface.fill((0,0,0))
# 		surface.blit(text_surface, ((surface.get_width()-text_surface.get_width())/2, (surface.get_height()-text_surface.get_height())/2))
