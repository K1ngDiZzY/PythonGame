import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

import pygame

# Basic defaults (can be overridden by CLI)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Python Game"

# Ensure the 'src' package directory is on sys.path so `scenes.*` imports work
# when running `python src/main.py` from the repository root.
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))


def parse_args():
    p = argparse.ArgumentParser(description="Run the PythonGame")
    p.add_argument("--width", type=int, default=SCREEN_WIDTH)
    p.add_argument("--height", type=int, default=SCREEN_HEIGHT)
    p.add_argument("--fullscreen", action="store_true")
    p.add_argument("--debug", action="store_true")
    return p.parse_args()


def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


class Game:
    """Small game runner used by scenes.

    Responsibilities:
    - initialize display, clock
    - hold `screen`, `clock`, `running`, and `current_scene`
    - run main loop and forward events to current scene
    """

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, title: str = WINDOW_TITLE):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene: Optional[object] = None

    def change_scene(self, new_scene: object) -> None:
        self.current_scene = new_scene

    def run(self) -> None:
        try:
            while self.running:
                dt = self.clock.tick(FPS) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        self.running = False
                    else:
                        if self.current_scene and hasattr(self.current_scene, "handle_event"):
                            self.current_scene.handle_event(event)

                if self.current_scene and hasattr(self.current_scene, "update"):
                    self.current_scene.update(dt)
                if self.current_scene and hasattr(self.current_scene, "render"):
                    self.current_scene.render(self.screen)

                pygame.display.flip()
        finally:
            try:
                pygame.quit()
            except Exception:
                pass
            # don't call sys.exit here; let main() decide


def main():
    args = parse_args()
    setup_logging(args.debug)

    # ensure assets path available
    project_root = Path(__file__).resolve().parents[1]
    assets_dir = project_root / "assets"
    logging.info("Project root: %s", project_root)
    logging.info("Assets dir: %s", assets_dir)

    # create game and set initial scene
    try:
        game = Game(width=args.width, height=args.height, title=WINDOW_TITLE)

        # lazy import TitleScene to avoid circular imports during module import time
        from scenes.titleScreen import TitleScene
        title = TitleScene(game)
        game.change_scene(title)

        if args.fullscreen:
            pygame.display.set_mode((args.width, args.height), pygame.FULLSCREEN)

        game.run()
    except Exception:
        logging.exception("Unhandled exception running game")


if __name__ == "__main__":
    main()

# to run:
# python src/main.py --width 1024 --height 768 --debug