class Option:
	FUNC = 0
	NESTED_OPTIONS = 1

class NestedDropDown:
	def __init__(self, future):
		self.panel = future

class FunctionalDropDown:
	def __init__(self, function):
		self.function = function
		