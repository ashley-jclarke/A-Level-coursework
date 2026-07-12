# WindowManager/floating_panel.py

from WindowManager.interface import Interface
from WindowManager.panel import Panel
from WindowManager.vec2 import Vec2

class FloatingPanel(Panel):
	def __init__(self, position: Vec2, size: Vec2, interface: Interface):
		super().__init__()
		# Position of the panel on the window
		self.position = position
		# Size of the panel on the window
		self.size = size
		# Function that can be called to close a floating panel with a given ID
		self.interface = interface
