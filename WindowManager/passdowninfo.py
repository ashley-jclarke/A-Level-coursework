# WindowManager/passdowninfo.py

from dataclasses import dataclass

from WindowManager.vec2 import Vec2
from WindowManager import pygame as pg

@ dataclass
class Passdowninfo:
	top_left_position: Vec2
	parent_surface: pg.surface.Surface|None	= None
