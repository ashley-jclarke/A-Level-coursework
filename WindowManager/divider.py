# WindowManager/divider.py

from typing import Callable

from WindowManager import pygame as pg
from WindowManager.interface import Interface
from WindowManager.panel import Panel
from WindowManager.vec2 import Vec2
from WindowManager.program import Program
from WindowManager.containersplit import ContainerSplit
from WindowManager.passdowninfo import Passdowninfo
from WindowManager.fonts import REGULAR_SMALL



class DividerProgram(Program):
	def __init__(self, 
			  interface: Interface,
			  parent_close_function: Callable[[],None], 
			  move_divider: Callable[[pg.surface.Surface, float],None], 
			  split_mode: int):
		super().__init__()
		self.interface = interface
		self.split_mode = split_mode		# Store the split mode for future reference
		self.clicked = False				# Variable to know if the divider has been clicked
		self.clicked_pos = None				# The last position that got clicked in this divider
		self.parent_close_function = parent_close_function	# The function to call on collapsing the divider
		self.move_divider = move_divider					# The function to call to move the divider

	## DividerProgram
	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		# Get the position of the mouse relative to the panel
		new_pos = Program.get_relative_mouse_pos(pdi)
		# Check LMB clicked inside the dividers screen space
		if pg.mouse.get_just_pressed()[0]:
			if Program.mouse_in_panel(surface, pdi):
				if self.interface.capture_focus(self.ID):
					# Mark divider as clicked
					self.clicked = True
					# Set the clicked position
					self.clicked_pos = new_pos

		# If there is a clicked position 
		if self.clicked_pos != None:
			# Move it relative to the clicked position on the correct axis
			if self.split_mode == ContainerSplit.SPLIT_X:
				self.move_divider(pdi.parent_surface, new_pos.x - self.clicked_pos.x)
			if self.split_mode == ContainerSplit.SPLIT_Y:
				self.move_divider(pdi.parent_surface, new_pos.y - self.clicked_pos.y)
		
		# Check LMB released
		if pg.mouse.get_just_released()[0] and self.clicked:
			# If mouse hasn't moved, is within the panel and the mouse was clicked inside the program before release
			if self.clicked_pos == new_pos and Program.mouse_in_panel(surface, pdi):
				self.parent_close_function()
			# Reset variables because of unclick
			self.clicked = False
			self.clicked_pos = None
			self.interface.release_focus(self.ID)
	
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		# Base colour for the divider
		surface.fill((255, 0, 0))

		# Draw an outline around the divider
		pg.draw.line(surface, (255, 255, 255), (0, 0), (surface.get_width(), 0), 1)
		pg.draw.line(
			surface,
			(255, 255, 255),
			(surface.get_width() - 1, surface.get_height()),
			(surface.get_width() - 1, 0),
			1,
		)
		pg.draw.line(surface, (255, 255, 255), (0, 0), (0, surface.get_height()), 1)

		# Render and draw the pointer value of the divider to the draw space
		text = REGULAR_SMALL.render(str(self.ID), True, (255, 255, 255))
		surface.blit(text, (0, 0))

class Divider(Panel):
	UNIT_PERCENTAGE 	= 0
	UNIT_PIXEL 			= 1
	def __init__(self, 
			  interface: Interface,
			  position: float = 0.5,
			  pointer: int=-1, 
			  SPLIT_MODE: int=ContainerSplit.SPLIT_X
			  ):
		super().__init__()
		self.relative_position: float = position				# The position along the parent screenspace
		self.bounce_position = self.relative_position	# The position set by the user to snap to when possible
		self.interface = interface
		self.unit = Divider.UNIT_PERCENTAGE
		self.movement_disabled = False					# Disables the ability to move the divider
		self.state_change_disabled = False				# Disables the ability to make the divider collapsed
		self.open_width = 15							# The size of the divider when it is not collapsed
		self.closed_width = 8							# The size of the divider when it is collapsed
		self.open = True					# Store if the divider is not collapsed	
		self.pointer: int = pointer				# Store the index of the panel this divider
											# divider is linked to in the parent 
											# container panel list
		self.split_mode = SPLIT_MODE		# Store the split mode to use when 
											# calculating which axis to use
		self.min_size = Vec2(				# Set the minimum size to the open width of
			self.open_width 				# the divider
			if SPLIT_MODE == ContainerSplit.SPLIT_X 
			else 0,
			0 if SPLIT_MODE == ContainerSplit.SPLIT_X 
			else self.open_width)
											# Create the "processor" for the divider 
											# and pass the dividers functions to use 
		self.child: DividerProgram = DividerProgram(
			interface,self.toggle_close,
			self.move_relative_position, SPLIT_MODE
		)


	# Function to get the size of divider based on collapsed or not
	def get_size(self) -> int:
		return self.open_width if self.open else self.closed_width

	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		# Update the program
		self.child.update(surface, pdi)
		self.relative_position = self.bounce_position

	# Draw the divider
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		self.child.draw(surface, pdi)

	# Self explanitory toggles the collapsed state of the divider
	# If closed => open
	# If open => close
	def toggle_close(self) -> None:
		if self.state_change_disabled: return
		self.open = not self.open

	# Shift the position of the divider based on screen space pixel units
	def move_relative_position(self, parent_surface: pg.surface.Surface, change:float=0) -> None:
		if self.movement_disabled: return
		# Get the old position and add the change then reset it using this new position
		new_pos = self.get_pos(parent_surface) + change
		self.set_pos(new_pos, parent_surface)
		self.bounce_position = self.relative_position
	
	# Get the position of the divder, requires the parent size to get the correct position as it's a percentage value
	# Returns a screen space pixel unit value
	def get_pos(self, parent_size:pg.surface.Surface) -> float:
		if self.unit == Divider.UNIT_PIXEL:
			return self.relative_position
		# Get the size proportional to the size given
		return (parent_size.get_width() if self.split_mode == ContainerSplit.SPLIT_X else parent_size.get_height())*self.relative_position

	# Set position of the divider, requires the parent size to get the percentage value. 
	# Pos parameter is a screen space pixel unit
	def set_pos(self, pos: float, parent_size: pg.surface.Surface) -> None:
		if self.unit == Divider.UNIT_PIXEL:
			self.relative_position = pos
			return
		# Ignore if size is zero
		try:
			# Set the size proporitional to the size given
			self.relative_position = pos / (parent_size.get_width() if self.split_mode == ContainerSplit.SPLIT_X else parent_size.get_height())
		except ZeroDivisionError:
			print("Size: zero")
	
	def set_pos_forced(self, pos: float, parent_size: pg.surface.Surface) -> None:
		self.set_pos(pos, parent_size)
		self.bounce_position = self.relative_position