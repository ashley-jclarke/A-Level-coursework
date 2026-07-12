# WindowManager/interface.py

from typing import Any, Callable
class Interface:
	def __init__(self,
		move_to_top : 			Callable[[int], None],
		capture_focus : 		Callable[[int], bool],
		release_focus : 		Callable[[int], bool],
		close_floater : 		Callable[[int], bool],
		create_floater : 		Callable[[Any], None],
		quit_window : 			Callable[[], None],
		window_id:				int,
		create_window: 			Callable[[Any], None]|None,
			  ) -> None:
		self.move_to_top = move_to_top
		self.capture_focus = capture_focus
		self.release_focus = release_focus
		self.close_floater = close_floater
		self.create_floater = create_floater
		self.quit_window = quit_window
		self.window_id = window_id
		self.create_window = create_window
		self.events: list = []