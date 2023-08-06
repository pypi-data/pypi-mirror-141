import os
import sys
from warnings import warn

import pygame
from pgzero.game import PGZeroGame
from .keys import keyboard
from pgzero.runner import prepare_mod







mod = sys.modules["__main__"]
try:
    WIDTH = mod.WIDTH
    HEIGHT = mod.HEIGHT
    pygame.init()
    w, h = pygame.display.get_desktop_sizes()[0]
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{int((w-WIDTH)/2)},{int((h-HEIGHT)/2)}'
except:
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

if not getattr(sys, '_pgzrun', None):
    if not getattr(mod, '__file__', None):
        raise ImportError(
            "You are running from an interactive interpreter.\n"
            "'import pgzrun' only works when you are running a Python file."
        )
    prepare_mod(mod)


def go():
    """Run the __main__ module as a Pygame Zero script."""
    if getattr(sys, '_pgzrun', None):
        return
    app = PGZeroGame(mod)
    app.keyboard = keyboard
    try:
        app.mainloop()
    finally:
        pygame.display.quit()
        pygame.mixer.quit()


def get_screen():
    "返回当前游戏所在的屏幕"
    mod = sys.modules["__main__"]
    return mod.screen
