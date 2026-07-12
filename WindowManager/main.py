from WindowManager.window import Window
from WindowManager import pygame as pg

class Main:
	def __init__(self) -> None:
		self.windows: list[Window] = []

	def handle_events(self):
		for event in pg.event.get():
			if "window" not in event.dict.keys(): continue
			if not event.dict["window"]: continue
			for window in self.windows:
				if event.dict["window"].id == window.win.id:
					window.interface.events.append(event)
	
	def run(self):
		while len(self.windows) > 0:
			self.handle_events()
			to_remove: list[Window] = []	# stores the window objects that need to be removed
			
			for window in self.windows:		# Step each window
				window.step()
				if not window.alive:		# Queue to remove if no longer active
					to_remove.append(window)
			
			for window in to_remove:
				self.windows.remove(window)
				window.destroy()
				del window
	
	def add_window(self, window: Window) -> None:
		self.windows.append(window)
		