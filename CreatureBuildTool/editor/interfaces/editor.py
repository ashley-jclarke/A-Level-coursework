# CreatureBuildTool/editor/interfaces/editor.py

from WindowManager.panel import Panel
from WindowManager.passdowninfo import Passdowninfo
from WindowManager.program import Program
from WindowManager.vec2 import Vec2
from WindowManager import pygame as pg
from math import floor
from math import ceil
from CreatureBuildTool import colours

from CreatureBuildTool.editor.interface import EditorInterface


class EditorProgram(Program):
	def __init__(self, interface: EditorInterface):
		super().__init__()
		# Interface functions
		self.interface = interface

		self.view_position = Vec2()
		self.hover_position = None
		self.scale = 8

		self.first_click: Vec2|None = None
		self.last_click: Vec2|None = None

		self.brush_size = 8
	
	def draw_pixel(self, coordinates: Vec2, material: int):
		self.interface.set_pixel(coordinates, material)
		if self.brush_size > 1 and self.interface.get_brush_mode() == 0:
			for y in range(-int(self.brush_size/2), int(self.brush_size/2)):
				for x in range(-int(self.brush_size/2), int(self.brush_size/2)):
					self.interface.set_pixel(coordinates + Vec2(x, y), material)
	
	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		if Program.mouse_in_panel(surface, pdi): 
			click = Program.get_relative_mouse_pos(pdi)
			self.hover_position = click
			if pg.mouse.get_pressed()[0]:
				if self.interface.capture_focus(self.ID):
					self.interface.release_focus(self.ID)
					if self.first_click != None:
						self.last_click = click
					else:
						self.first_click = click

					if self.first_click:
						diff = Vec2()
						if self.last_click:
							diff = self.last_click-self.first_click

						start_pos = self.first_click
						
						mx = 0
						my = 0
						if diff.magnitude() != 0:
							mx = diff.x / diff.magnitude()
							my = diff.y / diff.magnitude()

						for t in range(ceil(max(1,diff.magnitude()))):
							adjustment = Vec2(int(t*mx),int(t*my))
							self.draw_pixel((start_pos + adjustment)/self.scale, self.interface.get_selected_material())
						
						if self.last_click != None:
							diff += self.last_click
							self.last_click = self.first_click
							self.first_click = None

					else: 
						self.last_click = None
				else:
					self.hover_position = None
					self.last_click = None
					self.first_click = None
			else: 
				self.last_click = None
		else:
			self.hover_position = None
			self.last_click = None
			self.first_click = None



	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		surface.fill(colours.BACKGROUND)
		start_x = self.view_position.x 
		start_y = self.view_position.y 
		end_x = min(start_x + surface.get_width()/self.scale, self.interface.get_width())
		end_y = min(start_y + surface.get_height()/self.scale, self.interface.get_height())

		for y in range(int(start_y), int(end_y)):
			for x in range(int(start_x), int(end_x)):
				mat_index = self.interface.get_pixel(Vec2(x,y))
				material = self.interface.get_material(mat_index)
				if material.transparent: 
					colour = (0,0,0)
				else:
					colour = material.colour
				pg.draw.rect(surface, colour, (x*self.scale,y*self.scale,self.scale,self.scale))


		# rects = self.get_meshes(start_x, start_y, end_x, end_y)
		# print(len(rects))
		# for x, y, width, height, material in rects:
		# 	print(x,y,width,height)
		# 	colour = self.get_material(material).colour
		# 	pg.draw.rect(surface, colour, (x*self.scale,y*self.scale,width*self.scale,height*self.scale))

		if self.hover_position != None:
			x = floor(self.hover_position.x/self.scale)
			y = floor(self.hover_position.y/self.scale)

			current_index = self.interface.get_selected_material()
			material = self.interface.get_material(current_index)
			colour = material.colour

			pg.draw.rect(surface, colour, (x*self.scale,y*self.scale,self.scale,self.scale))
		if self.first_click != None:
			x = floor(self.first_click.x/self.scale)
			y = floor(self.first_click.y/self.scale)

			pg.draw.rect(surface, (255,255,255), (x*self.scale,y*self.scale,self.scale,self.scale))
	

		

class EditorPanel(Panel):
	def __init__(self, interface: EditorInterface):
		super().__init__()
		self.child = EditorProgram(interface)





