# WindowManager/window.py

from WindowManager.ID_manager import IDManager
from WindowManager.interface import Interface
from WindowManager.vec2 import Vec2
from WindowManager import pygame as pg
from WindowManager.passdowninfo import Passdowninfo
# from WindowManager.program import DemoProgram, FPSProgram
from WindowManager.floating_panel import FloatingPanel
import time


class Window:
	def __init__(self, width:int=500, height:int=500, create_window=None):
		self.ID = IDManager.new_ID()										# Unique ID for debugging
		self.win = pg.Window("Untitled", (width, height), resizable=True)	# Creates a resizeable pygame window
		self.alive = True													# Variable for the program to be running

		# List to contain any floating panels
		self.floating_panels: list[FloatingPanel] = []
		self.container = None
		self.prev_size = ()

		# WindowManager/window.py.Window:__init__
		self.focus_captured_by: int|None = None

		self.interface = Interface(self.move_floater_top, self.capture_focus, self.release_focus, self.close_floater, self.add_floating_panel, self.quit, self.win.id, create_window)
		
		self.elapsed  = 0
		self.target_fps = 30
		self.before = 0
		self.after = 1

	
	def move_floater_top(self, ID: int) -> None:
		target_floater = None
		i = -1
		for i, floater in enumerate(self.floating_panels):
			if floater.ID == ID:
				target_floater = i
		
		if target_floater == None: raise ValueError(f"{ID} not found.")

		target_floater = self.floating_panels.pop(i)
		self.floating_panels.insert(0, target_floater)

	# Attempt to capture mouse and return if it was successful
	def capture_focus(self, ID:int) -> bool:
		if self.focus_captured_by == None:
			self.focus_captured_by = ID
			return True
		return False
	
	def release_focus(self, ID:int) -> bool:
		if ID == self.focus_captured_by:
			self.focus_captured_by = None
			return True
		return False
	
	def close_floater(self, ID: int) -> bool:
		# Find index of target panel
		target = None
		for i, panel in enumerate(self.floating_panels):
			if panel.ID == ID:
				target = i
		# Return false if target not found
		if target == None: return False
		# Remove target
		self.floating_panels.pop(target)
		# Return true as target was found and removed
		return True
	
	# Adds a floating panel to the floating panel array
	def add_floating_panel(self, panel:FloatingPanel) -> None:
		self.floating_panels.append(panel)

	# Root update function
	def _update(self) -> None: 
		# Check for key presses
		self._event()
		# Basic Passdowninfo creation for the root window
		pdi = Passdowninfo(Vec2(0,0), self.win.get_surface())
		# Update the window with the Passdowninfo above
		self.update(pdi)

	# Root draw function
	def _draw(self) -> None:
		framerate = 1/(self.elapsed  if self.elapsed  != 0 else 1)
		pg.display.set_caption(str(framerate))
		if framerate > self.target_fps: return 	# Don't draw unless framerate exceeds the target fps
		
		self.before = time.time()
		# print("Set")

		pdi = Passdowninfo(Vec2(0,0), self.win.get_surface())
		self.draw(pdi)

	# Default draw function
	def draw(self, passdown: Passdowninfo) -> None:

		self.win.get_surface().fill((255,255,255))
		if self.container:
			self.container.draw(self.win.get_surface(), passdown)

		# Draw floating panels
		for panel in reversed(self.floating_panels):	# Draw the top panel last but process first so reverse in draw function
			surface = pg.surface.Surface(panel.size)
			panel.draw(surface, Passdowninfo(panel.position))
			self.win.get_surface().blit(surface, panel.position)

		# Update the window at the end of the draw function so all changes are sent to it
		self.update_window()

	# Default quit function that only closes the window
	def quit(self) -> None:
		self.alive = False

	# root event handling function
	def _event(self) -> None:
		## Iterate through all the events sent to the event buffer for this window
		for event in self.interface.events:
			if event.type == pg.WINDOWCLOSE:
				# Calls the quit function to close the window
				self.quit()

	# Default update function 
	def update(self, passdown: Passdowninfo) -> None:
		for floater in self.floating_panels:
			surface = pg.surface.Surface(floater.size)
			floater.update(surface, Passdowninfo(floater.position))
		if self.container:
			self.container.update(self.win.get_surface(), passdown)
		
		self.interface.events.clear()
	
	def step(self):
		self._draw()
		self._update()
		self.after = time.time()
		self.elapsed = self.after - self.before


	def run(self) -> None:
		# Run function loops over updating and drawing whist the window has not been quit
		while self.alive:
			self.step()

	def update_window(self) -> None:
		# Calls display update which places any updates to the display windows
		# Used so that all changes are displayed at once
		self.win.flip()

	def destroy(self):
		self.win.destroy()
