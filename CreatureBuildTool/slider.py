from pygame import Surface

from WindowManager.container import Container
from WindowManager.containersplit import ContainerSplit
from CreatureBuildTool.border import Border
from WindowManager.interface import Interface
from WindowManager.panel import Panel
from WindowManager.passdowninfo import Passdowninfo
from WindowManager.program import Program

class Slider(Container):
	def __init__(self, interface: Interface, split_mode: int = ContainerSplit.SPLIT_X) -> None:
		super().__init__(interface, split_mode, Border)
		self.add_child(Panel())
		
		self.value = 50
		self.add_child_positioned(Panel(), self.value)
	
	def update(self, surface: Surface, pdi: Passdowninfo) -> None:
		super().update(surface, pdi)
		
		print(self.positions[2])