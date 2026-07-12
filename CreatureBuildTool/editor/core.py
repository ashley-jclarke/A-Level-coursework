# CreatureBuildTool/core.py

from pathlib import Path

from CreatureBuildTool.editor.materials import Material, BONE, AIR, BLOOD, LIVER, CONNECTIVE, MUSCLE, NERVOUS, KERATIN, SKIN, MELON
from math import floor
# from random import choice
# from time import time_ns as time
from WindowManager.vec2 import Vec2
import json

type rle_layer = list[tuple[int, int, int]]
type mesh_layer = list[tuple[int, int, int, int, int]]
type raw_layer = int

class Core:
	def __init__(self):
		self.brush_mode = 0

		# Material pallete
		self.materials: list[Material] = [AIR, BONE, BLOOD, LIVER, CONNECTIVE, MUSCLE, NERVOUS, KERATIN, SKIN, MELON]
		# Index of the current material in use
		self.current_material: int = 0
		# The volume of a single cell in milimeters cubed
		self.cell_volume: int = 1

		# The current file that the information was loaded from
		self.save_file: str|None = None

		# Width of the slice
		self.width: int = 100
		# Height of the slice
		self.height: int = 100

		# The model of the creature
		self.model: list[rle_layer] = []

		self.onion_skin_depth: int = 5
		self.view_direction: int = 1
		self.onion_skin: list[rle_layer] = []

		# Randomly generated slice, 50/50 0 or 1
		print("Creating slice")
		self.slice: list[int] = [0 for _ in range(self.width*self.height)]
		# self.slice = self.encode_slice()
		self.slice_index: int = 0	# Z coordinate of the slice
	
	def set_brush_mode(self, mode: int):
		self.brush_mode = mode
	
	def get_brush_mode(self) -> int:
		return self.brush_mode
	
	def flatten_coordinate(self, position: Vec2) -> int:
		return floor(position.y)*self.width + floor(position.x)

	def expand_index(self, index: int) -> Vec2:
		return Vec2(index % self.width, index // self.height)
	
	def set_pixel(self, position: Vec2, material: int):
		pos = self.flatten_coordinate(position)
		if pos >= len(self.slice):return
		origin_material = self.slice[pos]
		if self.brush_mode == 1: 		# * Fill tool
			if origin_material == material:
				return
			checked: list[Vec2] = [] # store positions already checked
			checks = [position]		# store the next positions to check
			while len(checks) > 0:
				current = checks.pop(0) # get the next position to check
				checked.append(current)	# mark it as checked
				flat = self.flatten_coordinate(current) # get the 1D position
				if self.slice[flat] == origin_material:	# Only add adjacent cells and set the cell if this one matches material
					self.slice[flat] = material			# Set the current cell
					for i in [Vec2(-1,0), Vec2(1,0), Vec2(0,-1), Vec2(0,1)]:
						next_pos = current + i	
						# Don't apply if the next position is out of bounds
						if next_pos.x >= 0 and next_pos.x < self.width and next_pos.y >= 0 and next_pos.y < self.height:
							if next_pos not in checked:
								checks.append(next_pos)
		elif self.brush_mode == 2:
			# * line tool
			pass

		else:
			self.slice[pos] = material

	
	def get_meshes_in_range(self, start_x: int, end_x: int, start_y: int, end_y: int) -> mesh_layer:
		# range_x = end_x - start_x + 1
		# range_y = end_y - start_y + 1
		output: mesh_layer = []
		for mesh in self.encode_slice():
			i = mesh[0]
			i_height = mesh[1]
			mesh_x = i % self.width
			mesh_y = i // self.height
			mesh_width = (i + i_height) % self.width + 1
			mesh_height = (i + i_height) // self.height + 1

			# overlap_x = (start_x >= mesh_x and start_x <= (mesh_x + mesh_width)) or (mesh_x >= start_x and mesh_x <= (start_x + range_x))
			# overlap_y = (start_y >= mesh_y and start_y <= (mesh_y + mesh_width)) or (mesh_y >= start_y and mesh_y <= (start_y + range_y))
			output.append((mesh_x, mesh_y, mesh_width, mesh_height, mesh[2]))
		return output

	def get_pixel(self, position: Vec2) -> int:
		return self.slice[self.flatten_coordinate(position)]
	
		# Simplifies the slice data into long strips of the same value
	

	# CreatureBuildTool/editor/core.py
	def encode_slice(self) -> list[tuple[int, int, int]]:
		# Encode current slice
		meshes: list[tuple[int, int, int]] = []
		material = -1
		start_i = 0
		i = 0
		# Iterate through each value
		for i, selected in enumerate(self.slice):
			# If there's a change in material add the current material and its height and restart
			if selected != material:
				meshes.append((start_i, i-start_i, material))
				start_i = i
			material = selected
		
		# Add the last mesh
		meshes.append((start_i, i-start_i+1, material))

		return meshes

	def decode_slice(self, meshes: list[tuple[int, int, int]]) -> list[int]:
		slice : list[int] = []
		# Loading bar
		from tqdm import tqdm
		for _i, height, material in tqdm(meshes):
			# Fill in empty space with empty material
			# Place the mesh
			slice += [material]*height
		
		return slice

	def set_slice_index(self, new_z: int):
		new_z = max(0, min(len(self.model)-1, new_z))
		# Don't process if no change in slide index
		if new_z == self.slice_index:
			return
		
		encoding = self.encode_slice()
		self.model[self.slice_index] = encoding
		self.slice_index = new_z
		new_slice_encoded = self.model[new_z]
		self.slice = self.decode_slice(new_slice_encoded)

		self.onion_skin.clear()

		for i in range(self.onion_skin_depth):
			self.onion_skin.append(self.model[self.slice_index + (i + 1*self.view_direction)])
		# die

	def load_from_file(self, fp: str|Path):
		with open(fp, "r") as f:
			data = json.load(f)
			self.width = data[0]
			self.height = data[1]
			self.model = data[2]

	def save_to_file(self, fp: str|Path):
		with open(fp, "w") as f:
			data: tuple[int,int,list[rle_layer]] = (
				self.width,
				self.height,
				self.model
			)
			json.dump(data, f)
	
	def get_material_list(self):
		return self.materials

	def set_current_material(self, i: int):
		self.current_material = i
	
	def get_current_material(self):
		return self.current_material

	def shift_z(self, amount: int):
		self.set_slice_index(self.slice_index + amount)

	def get_material(self, i: int) -> Material:
		return self.materials[i]

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height
	
	def get_mass(self):
		total_mass = 0
		for slice in self.model:
			slice = self.decode_slice(slice)
			for value in slice:
				total_mass += self.get_material(value).density * self.cell_volume

	def get_center_of_mass(self):
		from CreatureBuildTool.editor.vec3 import Vec3
		measure = Vec3()

		x = 0
		y = 0
		z = 0

		for z, slice in enumerate(self.model):
			for i, value in enumerate(self.decode_slice(slice)):
				# get x and y from index
				coordinate = self.expand_index(i)
				x, y = coordinate.x, coordinate.y 
				# get mass of cell
				mass = self.get_material(value).density * self.cell_volume
				# apply to measure
				measure.x += mass*x
				measure.y += mass*y
				measure.z += mass*z
		
		
		measure.x /= x 
		measure.y /= y
		measure.z /= z