from WindowManager.container import Container
from WindowManager.containersplit import ContainerSplit
from WindowManager.divider import Divider
from WindowManager.interface import Interface
from WindowManager.panel import Panel
from WindowManager.program import Program
from WindowManager.fonts import REGULAR_SMALL

class TextLineProgram(Program):
	def __init__(self):
		super().__init__()
		self.buffer = ""

class EnterButtonProgram(Program):
	pass


class TextInput(Container):
	def __init__(self, interface: Interface, divider = Divider) -> None:
		super().__init__(interface, ContainerSplit.SPLIT_X, divider)
		self.add_child(Panel(TextLineProgram()))