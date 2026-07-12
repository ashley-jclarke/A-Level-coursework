# CreatureBuildTool/dropdown_menu.py

from typing import Callable

from WindowManager.floating_panel import FloatingPanel
from WindowManager.interface import Interface
from WindowManager.passdowninfo import Passdowninfo
from WindowManager.program import Program
from WindowManager.fonts import REGULAR_SMALL
from WindowManager.vec2 import Vec2
from WindowManager import pygame as pg
import time
from CreatureBuildTool import colours

class DropDownMenuProgram(Program):
	def __init__(self, 
			  	interface: Interface,
				options: dict[str, Callable[[],None]|None],								# A list of options mapped to functions to use when clicked
				resize: Callable[[Vec2], None],											# Function to resize the floating panel
				parent_id: int,
				masks: list[tuple[int|float, int|float, int|float, int|float]]=[],		# list of rect data that the mouse can be inside of to prevent closing
				):
		super().__init__()
		self.parent_id = parent_id
		self.interface = interface
		self.options = options
		self.resize = resize
		self.masks = masks
		self.creation_time = time.time()		# The time this panel was created
		self.hover_index:int = -1				# The index of the option being hovered over by the mouse
		self.true_size = Vec2()					# The full size of the panel without animations
		self.give = 1							# The distance away from the panel the mouse can get before closing
		self.closing = False					# Boolean if the panel is closing to play animations
		self.closeable = False					# Boolean for if the panel should be fully closed now
		self.option_height:int = 1
		self.clicked = False					# Store if the panel has been clicked on

		self.closing_signals: list[Callable[[],None]] = []


		self.printed_animation_time = False
		self.start_of_animation = time.time()

	# CreatureBuildTool/dropdown_menu.py : DropDownMenuProgram.update
	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo):

		grabbed_window = pg.window.get_grabbed_window()
		grabbed_window_id = None if not grabbed_window else grabbed_window.id

		# Check if the mouse is in the bounds of the true size and the give variable
		relative_pos = Program.get_relative_mouse_pos(pdi)
		in_bound = relative_pos.x >= -self.give and relative_pos.y >= -self.give and relative_pos.x <= self.true_size.x + self.give and relative_pos.y <= self.true_size.y + self.give

		in_bound_mask = False
		global_pos = pg.mouse.get_pos()
		global_pos = Vec2(global_pos[0], global_pos[1])
		for x, y, width, height in self.masks:
			relative_pos_mask = global_pos - Vec2(x,y)
			if relative_pos_mask.x >= 0 and relative_pos_mask.y >= 0 and relative_pos_mask.x <= width and relative_pos_mask.y <= height:
					in_bound_mask = True
					break

		# print(not self.clicked, pg.mouse.get_just_released()[0], not (in_bound or in_bound_mask))

		if not (in_bound or in_bound_mask) and not self.clicked and pg.mouse.get_just_released()[0]:
			self.closing = True	# Start closing the panel
		
		if self.closeable:
			self.interface.close_floater(self.parent_id)	# Fully close the panel
			for signal in self.closing_signals:
				signal()

		
		# if mouse is over the panel
		if in_bound:
			self.closing = False
			# Set to hover and calculate the option being hovered over
			y = relative_pos.y
			self.hover_index = int(y//self.option_height)

			if pg.mouse.get_just_pressed()[0] and self.interface.capture_focus(self.ID):
				self.clicked = True
		else:
			self.hover_index = -1
			
		if pg.mouse.get_just_released()[0] and self.clicked and grabbed_window_id == self.interface.window_id:
			# Unfocus the mouse and unmark as clicked
			self.interface.release_focus(self.ID)
			self.clicked = False
			# Run function if an option has been selected
			if self.hover_index != -1 and in_bound:
				func = self.options[list(self.options.keys())[int(self.hover_index)]]
				if func != None:
					self.options[list(self.options.keys())[int(self.hover_index)]]() # type: ignore

	def toggle_closing(self):
		self.closing = not self.closing

	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		surface.fill(colours.BUTTON)

		# First guess to calculate size of the panel
		size = Vec2(surface.get_width(), 0)
		texts: list[pg.surface.Surface] = []	# The text surfaces of the options
		# Render each word first to calculate the size
		for word in list(self.options.keys()):
			text_surface = REGULAR_SMALL.render(word, False, colours.TEXT)
			texts.append(text_surface)

			# Add the height to the size
			size.y += text_surface.get_height()
			# Change the width to the text surfaces width if it is bigger
			w = text_surface.get_width()
			if size.x < w: 
				size.x = w
		
		# Set the true size to the larger size of the panel
		self.true_size = size

		# If the panel is not fully open, continue playing the open animation unless closing
		if surface.get_height() < size.y and not self.closing:
			self.resize(Vec2(size.x, surface.get_height() + 5))
		elif not self.printed_animation_time:
			# print(f"Time to open:", time.time() - self.start_of_animation)
			self.printed_animation_time = True

		# Play the closing animation if closing
		if self.closing:
			# Resize and prevent from negative size
			self.resize(Vec2(size.x, max(0, surface.get_height() - 10)))
			# If the panel no longer appears to exist the animation is complete so the window should close
			if surface.get_height() - 10 <= 0: self.closeable = True
		
		# The last y-position is stored so that it can be used by the next surface to draw from
		last_pos = 0
		for i, text in enumerate(texts):
			# If this option is being hovered over, highlight it
			if i == self.hover_index:
				pg.draw.rect(surface, colours.HOVER, (0, last_pos, self.true_size.x, text.get_height()))
			# Draw the text to the screen space and make it centered
			surface.blit(text, ((surface.get_width()-text.get_width())/2,last_pos))
			# Shift the last position
			self.option_height = text.get_height()
			last_pos += self.option_height
			

class DropDownMenu(FloatingPanel):
	def __init__(self, position: Vec2, 														# Global position of the panel
					size: Vec2, 															# Size of the floating panel
					interface: Interface,
					options: dict[str, Callable[[],None]|None],								# List of options linked to functions to call on click
					masks: list[tuple[int|float, int|float, int|float, int|float]] = [], 	# does something
					):
		super().__init__(position, size, interface)
		# Create and pass the parameters down for a DropDownMenu processor
		self.child = DropDownMenuProgram(interface, options, self.resize, self.ID, masks)
	
	# Custom function to change the size of the floating panel # ! should be built into WindowManager library
	def resize(self, new_size: Vec2):
		self.size = new_size
