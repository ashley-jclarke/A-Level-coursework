# CreatureBuildTool/window.py

from typing import Callable

from CreatureBuildTool.slider import Slider
from WindowManager import window
from WindowManager.container import Container
from WindowManager.containersplit import ContainerSplit
# from WindowManager.panel import Panel
# from WindowManager.program import DemoProgram
from WindowManager import pygame

from CreatureBuildTool.settings_bar import SettingsBar
from CreatureBuildTool.border import Border
from CreatureBuildTool.moveable_border import MoveBorder

from CreatureBuildTool.editor.core import Core
from CreatureBuildTool.editor.interfaces.material_list import MaterialListPanel
from CreatureBuildTool.editor.interfaces.material_display import MaterialDisplay
from CreatureBuildTool.editor.interfaces.editor import EditorPanel

from CreatureBuildTool.editor.interface import EditorInterface
 
class MainWindow(window.Window):
	def __init__(self, width:int=500, height:int=500):
		super().__init__(width, height)
		# Set the title of the window to design tool
		self.win.title = "DT"
		# Set the icon (the image at the top left of the window)
		icon = pygame.image.load("CreatureBuildTool/assets/icon.ico")
		self.win.set_icon(icon)

		
		self.editor = Core()

		self.interface = EditorInterface(
			self.move_floater_top,
			self.capture_focus,
			self.release_focus,
			self.close_floater,
			self.add_floating_panel,
			self.quit,
			self.win.id,
			self.interface.create_window,
			self.editor.get_pixel, 
			self.editor.get_material,
			self.editor.set_pixel, 
			self.editor.shift_z,
			self.editor.get_current_material,
			self.editor.set_current_material,
			self.editor.get_material_list,
			self.editor.get_width,
			self.editor.get_height, 
			self.editor.get_meshes_in_range,
			self.editor.get_brush_mode,
			self.editor.set_brush_mode
		)
		
		
		# Create the root container for the layout
		main_container = Container(self.interface, ContainerSplit.SPLIT_Y, divider=Border)
		

		# Add a settings bar object to the top
		settings_bar = SettingsBar(self.interface)
		self.set_title: Callable[[str], None] = settings_bar.get_set_title()
		main_container.add_child(settings_bar)
		

		center_container = Container(
			self.interface,
			ContainerSplit.SPLIT_X, MoveBorder
			)
		
		left_space = Container(
			self.interface,
			ContainerSplit.SPLIT_Y, MoveBorder
			)

		editorpanel = EditorPanel(self.interface)

		left_space.add_child_positioned(editorpanel, 0)
		left_space.add_child(Slider(self.interface))

		preview = Container(self.interface, ContainerSplit.SPLIT_X, MoveBorder)
		# preview.add_child(Panel(DemoProgram()))
		# preview.add_child_positioned(Panel(DemoProgram()), 0.5)
		left_space.add_child_positioned(preview, 0.8)
		
		right_space = Container(
			self.interface,
			ContainerSplit.SPLIT_Y, MoveBorder
			)
		
		material_list = MaterialListPanel(self.interface)
		get_material = material_list.get_material_for_info

		material_display = MaterialDisplay(get_material)

		right_space.add_child_positioned(material_list, 0)
		right_space.add_child_positioned(material_display, 0.33)
		# right_space.add_child_positioned(Panel(DemoProgram()), 0.66)
		
		center_container.add_child(left_space)
		center_container.add_child_positioned(right_space, 0.75)

		# Add a random coloured panel to fill the space
		main_container.add_child_positioned(center_container, 24)
		
		# Finalise the root container
		self.container = main_container

