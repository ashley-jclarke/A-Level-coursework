from CreatureBuildTool.editor.interface import EditorInterface
from CreatureBuildTool.spacer import Spacer
from WindowManager.container import Container
from WindowManager.containersplit import ContainerSplit
from WindowManager.panel import Panel
from CreatureBuildTool.settings_bar import Break, HeaderProgram

class BrushControl(HeaderProgram):
	def __init__(self, interface: EditorInterface):
		super().__init__("Brush Size", interface)
		self.options = {"Increase Size":None, "Decrease Size":None}

class FillTool(HeaderProgram):
	def __init__(self, interface: EditorInterface):
		super().__init__("Brush Mode", interface)
		self.options = {"Fill":self.set_brush_fill, "Pen":self.set_pen_fill}
	def set_brush_fill(self):
		self.interface.set_brush_mode(1)
	def set_pen_fill(self):
		self.interface.set_brush_mode(0)



class TabBar(Container[Break]):
	def __init__(self, interface: EditorInterface):
		super().__init__(interface, ContainerSplit.SPLIT_X, Break)
		self.add_child_positioned(Panel(BrushControl(interface)), 0)
		self.add_child_positioned(Panel(FillTool(interface)), 100)
		self.add_child_positioned(Spacer(), 200)



