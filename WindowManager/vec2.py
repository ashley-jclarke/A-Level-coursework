# WindowManager/vec2.py

from WindowManager import pygame as pg

# Inherit the Vector2 class from pygame
class Vec2(pg.Vector2):
	def __init__(self, x:float|int=0, y:float|int=0):
		self.x = x
		self.y = y
	# Override for displaying the Vec2 class when using print() or converting to string
	def __str__(self) -> str:
		return f"({self.x}, {self.y})"
	def __int__(self):
		return Vec2(int(self.x), int(self.y))