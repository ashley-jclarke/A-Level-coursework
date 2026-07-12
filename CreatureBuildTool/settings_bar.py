# CreatureBuildTool/settings_bar.py

from typing import Callable

from CreatureBuildTool.editor.interface import EditorInterface
from WindowManager.fonts import REGULAR_SMALL
from WindowManager.container import Container
from WindowManager.container import ContainerSplit
from WindowManager.interface import Interface
from WindowManager.panel import Panel
from WindowManager.program import Program# , FPSProgram
from WindowManager.divider import Divider
from WindowManager import pygame as pg
from WindowManager.vec2 import Vec2
from WindowManager.passdowninfo import Passdowninfo
from CreatureBuildTool.dropdown_menu import DropDownMenu
from CreatureBuildTool.spacer import Spacer
from CreatureBuildTool import colours

class HeaderProgram(Program):
	def __init__(self, name: str, interface: Interface):
		super().__init__()

		# Dropdown menu interaction functions
		self.close_dropdown = None
		self.toggle_dropdown: Callable[[],None]|None = None

		self.interface = interface

		# The text to display on the button
		self.name = name

		# Mouse indicators
		self.clicked = False
		self.hovered = False
		# list of options
		self.options: dict[str, Callable[[],None]|None] = {"Test 1":None,"Test 2":None,"Test 3":None,"Test 4":None,}
	
	
	def close_floater(self, id: int):
		# Reset dropdown interactions
		self.close_dropdown = None
		self.toggle_dropdown: Callable[[],None]|None = None
		# Call the main close floater function
		self.interface.close_floater(id)

	def update(self, surface:pg.surface.Surface, pdi: Passdowninfo):
		# Check if the button is being hovered over
		self.hovered = Program.mouse_in_panel(surface, pdi)

		# If mouse is over button and not claimed
		if self.hovered and pg.mouse.get_just_pressed()[0] and self.interface.capture_focus(self.ID):
			self.clicked = True	# Mark self as clicked
			if self.toggle_dropdown == None:
				# Create a drop down menu for the File options
				new_menu = DropDownMenu(
					pdi.top_left_position + Vec2(0, surface.get_height()), 
					Vec2(surface.get_width(), 0), 
					self.interface,
					self.options, 
					[
						(
							pdi.top_left_position.x, 
							pdi.top_left_position.y, 
							surface.get_width(), 
							surface.get_height()
						)
					])
				self.toggle_dropdown = new_menu.child.toggle_closing
				self.interface.create_floater(new_menu)
				new_menu.child.closing_signals.append(self.release_dropdown)
			else:
				self.toggle_dropdown()

		# Release the mouse if unclicked and focus was claimed by this panel
		if self.hovered and pg.mouse.get_just_released()[0] and self.clicked:
			self.interface.release_focus(self.ID)
			self.clicked = False
	
	def release_dropdown(self):
		self.toggle_dropdown = None
		
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		# Draw the name of this button
		textsurface = REGULAR_SMALL.render(self.name, False, colours.TEXT)
		# Render default background colour or hover colour if hovered over
		colour = colours.BUTTON
		if self.hovered: colour = colours.HOVER
		# Draw background
		surface.fill(colour)
		# Draw text centered to the button
		surface.blit(textsurface, ((surface.get_width()-textsurface.get_width())/2, 0))

# Inherit from the headerprogram but with different options
class FileProgram(HeaderProgram):
	# Not taking name as a paramter
	def __init__(self, interface: Interface):
		super().__init__("File", interface)
		self.options: dict[str, Callable[[],None]|None] = {
			"New": None,
			"Open": None,
			"Save": None,
			"Save As": None,
			"Quit": interface.quit_window,
		}

# Same as FileProgram, different name different options
class EditProgram(HeaderProgram):
	def __init__(self, interface: EditorInterface):
		super().__init__("Edit", interface)
		self.options = {
			"Undo":None,
			"Redo":None
		}

# Same as FileProgram, different name different options
class ViewProgram(HeaderProgram):
	def __init__(self, interface: EditorInterface):
		super().__init__("View", interface)
		self.options = {
			"Zoom":None
		}

class Break(Divider):	# Custom very thin divider
	def __init__(
		self,
		interface: EditorInterface,
		position: float=0.5,
		pointer: int=-1,
		SPLIT_MODE: int=ContainerSplit.SPLIT_X,
	):
		super().__init__(
			interface, position, pointer, SPLIT_MODE
		)
		self.movement_disabled = True
		self.open_width = 1
		self.closed_width = 1
		self.state_change_disabled = True
		self.unit = Divider.UNIT_PIXEL
	def draw(self, surface: pg.surface.Surface, pdi: Passdowninfo):
		surface.fill(colours.BORDER)

class TitleProgram(Program):
	def __init__(self, title:str):
		super().__init__()
		self.title = title
	
	def set_title(self, new_title:str=""):
		self.title = new_title
	
	def draw(self, surface:pg.surface.Surface, pdi:Passdowninfo):
		surface.fill(colours.BACKGROUND)
		text = REGULAR_SMALL.render(self.title, False, colours.TEXT)
		surface.blit(text, ((surface.get_width()-text.get_width())/2, 0))


class SettingsBar(Container[Break]):
	def __init__(self, interface: EditorInterface):
		super().__init__(
			interface, ContainerSplit.SPLIT_X, Break
		)
		# Add the HeaderPanels
		self.add_child_positioned(Panel(FileProgram(interface)), 0)
		self.add_child_positioned(Panel(EditProgram(interface)), 50)
		self.add_child_positioned(Panel(ViewProgram(interface)), 100)
		self.add_child_positioned(Spacer(), 150)
		self.title = Panel(TitleProgram("TITLE"))
		self.add_child(self.title)
		self.child[len(self.child)-2].unit = Divider.UNIT_PERCENTAGE # type: ignore
		self.child[len(self.child)-2].bounce_position = 0.4 # type: ignore

		self.add_child_positioned(Panel(), 150)
		self.child[len(self.child)-2].unit = Divider.UNIT_PERCENTAGE # type: ignore
		self.child[len(self.child)-2].bounce_position = 0.6 # type: ignore
		
		from CreatureBuildTool.editor.interfaces.tabbar import TabBar
		self.add_child(TabBar(interface))


	def get_set_title(self) -> Callable[[str], None]:
		return self.title.child.set_title # type: ignore
	