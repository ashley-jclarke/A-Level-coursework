# CreatureBuildTool/editor/interfaces/material_list.py

from CreatureBuildTool.editor.interface import EditorInterface
from CreatureBuildTool.editor.materials import Material
from WindowManager.panel import Panel
from WindowManager.passdowninfo import Passdowninfo
from WindowManager.program import Program
from WindowManager import pygame as pg
from CreatureBuildTool import colours

class MaterialListProgram(Program):
	def __init__(self, interface: EditorInterface):
		super().__init__()
		# Interfacing functions
		self.interface = interface

		# List of materials
		self.materials: list[Material] = []
		# Index of what is being hovered over
		self.hover_over = -1
		# Size of the square that it is drawn to
		self.icon_size = 32
		# Size of the padding inside the square
		self.padding = 8
	
	# CreatureBuildTool/editor/interfaces/material_list.py : MaterialListProgram.update
	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		# Retrieve the materials
		self.materials = self.interface.get_material_list()

		if Program.mouse_in_panel(surface, pdi):
			# The x and y position of the square to be drawn
			start_x = 0
			start_y = 0

			rmp = Program.get_relative_mouse_pos(pdi)
			
			# Iterate and draw each material
			self.hover_over = -1
			for i in range(len(self.materials)):
				if start_x <= rmp.x and start_y <= rmp.y and rmp.x <= start_x + self.icon_size and rmp.y <= start_y + self.icon_size:
					self.hover_over = i
					if pg.mouse.get_just_pressed()[0]:
						if self.interface.capture_focus(self.ID):
							self.interface.set_selected_material(i)
							self.interface.release_focus(self.ID)

				# Go to next x
				start_x += self.icon_size
				# Wrap around
				if start_x + self.icon_size > surface.get_width():
					start_x = 0
					start_y += self.icon_size

	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		# Fill the background
		surface.fill(colours.BACKGROUND)

		# The x and y position of the square to be drawn
		start_x = 0
		start_y = 0
		
		# Iterate and draw each material
		for i, material in enumerate(self.materials):
			# Give it a different background if it is the current material in use
			if i == self.interface.get_selected_material():
				pg.draw.rect(surface, colours.SELECTED, (start_x, start_y, self.icon_size, self.icon_size))
			if i == self.hover_over:
				pg.draw.rect(surface, colours.HOVER, (start_x, start_y, self.icon_size, self.icon_size))
			# Add a border around the tile for contrast
			pg.draw.rect(surface, colours.BORDER, (start_x+self.padding/4, start_y+self.padding/4, self.icon_size-self.padding/2, self.icon_size-self.padding/2))
			# Draw the material colour
			pg.draw.rect(surface, material.colour, (start_x+self.padding/2, start_y+self.padding/2, self.icon_size-self.padding, self.icon_size-self.padding))
			# Go to next x
			start_x += self.icon_size
			# Wrap around
			if start_x + self.icon_size > surface.get_width():
				start_x = 0
				start_y += self.icon_size

	def get_material_for_info(self) -> Material:
		if self.hover_over != -1:
			return self.materials[self.hover_over]
		return self.materials[self.interface.get_selected_material()]


class MaterialListPanel(Panel):
	def __init__(self, interface: EditorInterface):
		super().__init__()
		self.child = MaterialListProgram(interface)

	def get_material_for_info(self):
		return self.child.get_material_for_info()




