
import copy
import os
import pickle
import random
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, List, Optional, Sequence, Text, Tuple, Union, overload

import pygame
import pygame_menu
from pygame.key import key_code
from pygame.locals import *
from xpinyin import Pinyin

from primaryschool._abc_ import GameBase
from primaryschool.dirs import *
from primaryschool.locale import _, sys_lang_code
from primaryschool.resource import (default_font, default_font_path,
                                    get_default_font, get_font_path)
from primaryschool.subjects import *


class Target(self):
    def __init__(
        self,
        content,
        key,
        font=None,
        font_name='',
        font_size=20,
    ):
        self._content = content
        self._key = key
        self._font = font
        self._font_name = font_name
        self._font_size = font_size
        self._surface = None

    @property
    def content(self): return self._content
    @property
    def key(self): return self._key
    @property
    def surface(self): return self._surface

    @property
    def font(self):
        if self._font:
            return self._font
        if self._font_name:
            return pygame.font.Font(self._font_name, self._font_size)

    @surface.setter
    def surface(self, surface):
        self._surface = surface


class TargetsManager(self):
    def __init__(
        self,
        targets
    ):
        self._targets = targets


class ShootingBase(GameBase):
    def __init__(self, module_str,):
        self.module_str = module_str
        ...

    def load(self):
        ...

    def save(self):
        ...

    def play(self):
        ...

    def start(self):
        ...

    def _start(self):
        ...
