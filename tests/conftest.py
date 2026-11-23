import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest


@pytest.fixture(autouse=True, scope="session")
def _pygame_session():
    pygame.init()
    pygame.display.set_mode((800, 450))
    yield
    pygame.quit()
