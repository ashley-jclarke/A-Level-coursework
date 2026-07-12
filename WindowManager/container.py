# WindowManager/container.py

from WindowManager.interface import Interface
from WindowManager.panel import Panel
from WindowManager.vec2 import Vec2
from WindowManager import pygame as pg
from WindowManager.passdowninfo import Passdowninfo
from WindowManager.divider import Divider
from WindowManager.containersplit import ContainerSplit


from time import time as time 

class Container[Div:Divider](Panel):
	def __init__(self, interface: Interface, split_mode:int=ContainerSplit.SPLIT_X, divider:type[Div]=Divider) -> None:
		super().__init__()					# Allow inheritance initiation for the Panel parent class
		self.interface = interface		# the interfacing class for the window and editor objects
		self.child: list[Panel] = []		# Keep a list to store the child panels that the container will have
		self.split_mode: int = split_mode	# Store the axis on which child panels shall be seperated on
		self.divider = divider
		self.process_info  = []
		self.positions = []
		self.prev_size = ()

	def set_min_size(self) -> None:					# Calculate and set the minimum size of the container panel
											# Based on the children panels it stores
		size = Vec2()						# The new size stored in a Vector 2 default to (0, 0)

		for child in self.child:			# Iterate through all children to get their minimum size and add it
											# to the new size

			size += child.min_size			# Add the child size to the new size
			
		self.min_size = size				# Set the new size
	
	def add_child(self, child: Panel) -> None:				# Function to add new children
		new_divider = self.divider(
			self.interface,		# : Divider
			0.5, len(self.child)+1, 
			self.split_mode)
		self.child.append(new_divider)
		self.min_size += new_divider.min_size
		self.child.append(child)			# Add the child to the children list stored in the self object
		self.min_size += child.min_size
	
	def add_child_positioned(self, child: Panel, position: float) -> None:			# Function to add new children at a position
		new_divider = self.divider(
			self.interface, 
			position, len(self.child)+1, 
			self.split_mode)
		
		self.child.append(new_divider)
		self.child.append(child)			# Add the child to the children list stored in the self object
		self.min_size += new_divider.min_size
		self.min_size += child.min_size

	def add_pair(self, divider: Div, link:Panel) -> None:
		self.child.append(divider)
		divider.pointer = len(self.child)
		self.child.append(link)
	
	def make_dividers_top(self) -> None:
		# Seperate the child panels into dividers and other (children)
		dividers: list[Div] = []
		children: list[tuple[int, Panel]] = []
		# Iterate through and append to the above lists accordingly
		for i, child in enumerate(self.child):
			if type(child) == self.divider:
				dividers.append(child)
			else:
				# If not divider then add the index of the panel that it was at before rearranging.
				children.append((i, child))
		
		# Correct the pointers of the dividers
		for divider in dividers:
			# Iterate through child panels to find the one that this divider pointed to before rearranging
			for i, (old_pos, child) in enumerate(children):
				# Check if it is the old panel
				if divider.pointer == old_pos:
					# Correct the new pointer position
					correction = i + len(dividers)
					divider.pointer = correction
					# Stop iterating through the list so it doesn't attempt to correct
					# because the pointer may match the old index of a different panel
					break

		# Correct the children list to remove the tuple and leave it as just the child object
		moved_children = list(map(lambda x: x[1], children))
		# Set the child object of the Panel to have dividers first and then the other panels.
		self.child = dividers + moved_children
	
	def get_panels(self) -> tuple[list[Panel],list[int]]:
		# Get panels that will be on screen
		to_draw_i: list[int] = []	# A new list to hold the indexes of 
		for i, child in enumerate(self.child):
			# Add dividers and their linked panel if open
			if type(child) == self.divider:
				to_draw_i.append(i)
				# Add the panel that this divider points to only if the divider is open
				if child.open:
					to_draw_i.append(child.pointer)
		
		# Get panels in the correct order
		dividers: list[int] = []	# Indexes of the dividers in to_draw
		to_draw: list[Panel] = []	# List to hold the panels to draw in order
		for i, child in enumerate(self.child):
			# Check if the panel will be drawn
			if i in to_draw_i:
				# Check if the panel is a divider and add the index of it in `to_draw` to dividers
				if type(child) == self.divider:
					dividers.append(len(to_draw))
				# Add the panel to `to_draw`
				to_draw.append(child)
		
		return (to_draw, dividers)

	def get_positions(self, surface: pg.surface.Surface, panels: list[Panel], divider_indexes: list[int]) -> list[int]:
		# Position the dividers
		relative_positions: list[float|None] = []	# New list for the starting positions of the panels
		last_valid_position = 0	# Store the position of the closest position panels can go to
		for i, child in enumerate(panels):
			upper_bound: float = surface.get_width() if self.split_mode == ContainerSplit.SPLIT_X else surface.get_height()
			for j, panel in enumerate(panels[i:]):
				if i + j in divider_indexes: # This line checks if it's a divider
					upper_bound -= panel.get_size() #type:ignore
			# If the child is a divider
			if i in divider_indexes:
				# Store a variable that if `True` means the position of the divider needs to be moved backwards
				bound = False
				if i == 0: bound = True
				if i > 0: 
					if relative_positions[i-1] != None: bound = True
				# Check if the divider position needs to be moved forward and consult the bound variable to check if it needs to move back
				
				if child.get_pos(surface) < last_valid_position or bound:#type:ignore
					# * Move forward or backwards :sob:
					# Move the divider position
					child.set_pos(last_valid_position, surface)#type:ignore
				if child.get_pos(surface) > upper_bound:#type:ignore
					# * Move back
					child.set_pos(upper_bound, surface)#type:ignore
				
				# Add the divider position to the array
				relative_positions.append(child.get_pos(surface))#type:ignore
				# Move the position to make space for this divider and the space it requires
				last_valid_position = child.get_pos(surface) + child.get_size()#type:ignore
			# If child is not a divider
			else:
				# Position is, at this point, unknown so add `None`
				# When tf does it become known??????
				relative_positions.append(None)

		# Add the end edge of the draw space to the array based on the split mode
		# Splitting on the x-axis => width
		# Splitting on the y-axis => height
		relative_positions.append(surface.get_width() if self.split_mode == ContainerSplit.SPLIT_X else surface.get_height())

		result: list[int] = []
		last_group: list[int] = []
		last_valid_position = 0
		for i, pos in enumerate(relative_positions):
			# If position is part of a divider or is the last position (screen space size)
			if i in divider_indexes or i == len(relative_positions)-1:
				# Check for a grouping
				if last_group != []:
					# The size to distribute for the panels in the group
					full_size = pos - last_group[0]
					# Divide the size evenly between each panel
					sub_size = full_size/last_group[1]
					# Add each panel to the result
					for j in range(last_group[1]):
						# `j` increments the position
						result.append(last_group[0] + sub_size*j)
					last_group.clear()
				# Add the position of this divider after adding the group before it
				result.append(pos)
				# If the divider is not the end (edge of the container), move the lvp
				if i in divider_indexes: last_valid_position = pos + panels[i].get_size()
			# Group None positions
			else:
				# If there is not yet a group, create one
				if last_group == []:
					# Set the starting position of this group to the last valid position
					last_group = [last_valid_position, 1]
				# If there is a group, extend it
				else:
					last_group[1] += 1
				
		return result


	#thisisfine:befine
	def set_process_info(self, surface, pdi) -> None:

		panels, divider_indexes = self.get_panels()
		positions = self.get_positions(surface, panels, divider_indexes)
		if positions == self.positions and self.prev_size == surface.get_size():
			return
		self.positions = positions
		self.prev_size = surface.get_size()
		result = []

		# Iterate through each object to draw
		for i, child in enumerate(panels):
			# Get the starting position of the panel
			first = positions[i]
			next_pos = positions[i+1]
			# Get the size by taking it from the next position
			size = next_pos - first
			# If the size is negative then it is invalid, so skip it
			if size < 0: continue

			# If this child is a divider, confirm its position by setting it
			if type(child) == self.divider:
				child.set_pos(first, surface)
				if size > child.get_size():
					child.set_pos_forced(next_pos-child.get_size(), surface)
			# Get the size of the surface for this panel 	(starts for SPLIT_Y)
			screen_space_size = (surface.get_width(), size)
			# Flip if not matching split mode				(flip for SPLIT_X)
			if self.split_mode == ContainerSplit.SPLIT_X:
				screen_space_size = (positions[i+1] - first, surface.get_height())

			# Create a pygame surface based on the size
			screen_space = pg.surface.Surface(screen_space_size)

			# Get the draw position onto the containers draw space for the childs draw space
			pos = Vec2(
				first if self.split_mode == ContainerSplit.SPLIT_X else 0, 
				first if self.split_mode == ContainerSplit.SPLIT_Y else 0
			)
			# Get the top left position of the childs draw space by adding it to this one
			tl: Vec2 = pdi.top_left_position + pos
			
			result.append( (child, pos, screen_space, Passdowninfo(tl, surface)) )
		
		
		self.process_info = result

	def update(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		# before = time()
		self.set_process_info(surface, pdi)
		for child, pos, screen_space, passdown in self.process_info:
			child.update(screen_space, passdown)

			
		# after = time()

		# print(f"{self.ID} Update time: {(after - before)*1000.0}ms")
		
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo) -> None:
		# before = time()

		for child, pos, screen_space, passdown in self.process_info:
			# Get the child to draw to its screen space
			child.draw(screen_space, passdown)
			# Draw the childs draw space onto the containers draw space
			surface.blit(screen_space, pos)

		# after = time()

		# print(f"{self.ID} Draw time: {(after - before)*1000.0}ms")