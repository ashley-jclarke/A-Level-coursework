# CreatureBuildTool/editor/interface.py

from typing import Any, Callable

from CreatureBuildTool.editor.materials import Material
from WindowManager.interface import Interface
from WindowManager.vec2 import Vec2

class EditorInterface(Interface):

	def __init__(self, move_to_top: Callable[[int], None], capture_focus: Callable[[int], bool], release_focus: Callable[[int], bool], close_floater: Callable[[int], bool], create_floater: Callable[[Any], None], quit_window: Callable[[], None], window_id: int, create_window: Callable[[Any], None] | None,
			  
			get_pixel				: Callable[[Vec2],int],		
			get_material			: Callable[[int],Material],	
			set_pixel				: Callable[[Vec2, int],None],
			shift_z					: Callable[[int],None],		
			get_selected_material	: Callable[[],int],			
			set_selected_material	: Callable[[int],None],		
			get_material_list		: Callable[[], list[Material]],
			get_width				: Callable[[],int],			
			get_height				: Callable[[],int],			
			get_meshes				: Callable[[int, int, int, int],list[tuple[int, int, int, int, int]]],
			get_brush_mode			: Callable[[], 		int],	
			set_brush_mode			: Callable[[int], 	None],	
			  ) -> None:
		super().__init__(move_to_top, capture_focus, release_focus, close_floater, create_floater, quit_window, window_id, create_window)
		self.get_pixel = get_pixel
		self.get_material = get_material
		self.set_pixel = set_pixel
		self.shift_z = shift_z
		self.get_selected_material = get_selected_material
		self.set_selected_material = set_selected_material
		self.get_material_list = get_material_list
		self.get_width = get_width
		self.get_height = get_height
		self.get_meshes = get_meshes
		self.get_brush_mode = get_brush_mode
		self.set_brush_mode = set_brush_mode