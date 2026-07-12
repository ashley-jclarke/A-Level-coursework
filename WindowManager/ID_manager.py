# WindowManager/ID_manager.py

class IDManager:
	ID: int = -1
	@staticmethod
	def new_ID() -> int:
		IDManager.ID += 1
		return_id = IDManager.ID
		return return_id
