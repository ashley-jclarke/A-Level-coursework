# CreatureBuildTool/editor/interfaces/material_display.py

from WindowManager.panel import Panel
from WindowManager.program import Program
from CreatureBuildTool import colours
from WindowManager.fonts import REGULAR_SMALL as REGULAR
from WindowManager.fonts import BOLD_SMALL as BOLD

class MaterialDisplayProgram(Program):
	def __init__(self, get_material_function):
		super().__init__()
		self.current_material = None
		self.get_material = get_material_function
	
	def update(self, surface, pdi):
		self.current_material = self.get_material()

	def draw(self, surface, pdi):
		surface.fill(colours.BACKGROUND)

		if self.current_material != None:
			name = BOLD.render(f"Name: {self.current_material.name}", False, colours.TEXT)
			density = REGULAR.render(f"Density: {self.current_material.density}kg", False, colours.TEXT)
			transparency = REGULAR.render(f"Transparent: {self.current_material.transparent}", False, colours.TEXT)

			last_pos = 5
			for info in [name, density, transparency]:
				surface.blit(info, (5, last_pos))
				last_pos += info.get_height() + 5


class MaterialDisplay(Panel):
	def __init__(self, get_material_function):
		super().__init__()
		self.child = MaterialDisplayProgram(get_material_function)

