# ...existing code...
import pygame
from typing import List, Optional, Tuple

class MainMenuScene:
    """
    Main menu scene.
    Usage: game.change_scene(MainMenuScene(game))
    When changing scenes, imports are done lazily to avoid circular imports.
    """
    def __init__(self, game):
        self.game = game
        sw, sh = self.game.screen.get_size()
        self.title_font = pygame.font.SysFont(None, 72)
        self.option_font = pygame.font.SysFont(None, 36)
        self.hint_font = pygame.font.SysFont(None, 20)
        self.bg_color = (18, 24, 32)
        self.options: List[str] = ["Start Game", "Options", "Exit"]
        self.selected: int = 0
        self.option_positions: List[Tuple[int,int,int,int]] = []  # rects for mouse hit
        self.hover = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_selected()
            elif event.key == pygame.K_ESCAPE:
                # optional: return to title if you have one
                try:
                    from scenes.titleScreen import TitleScene
                    self.game.change_scene(TitleScene(self.game))
                except Exception:
                    pass

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i, rect in enumerate(self.option_positions):
                x, y, w, h = rect
                if x <= mx <= x + w and y <= my <= y + h:
                    self.selected = i
                    self.hover = True
                    break
            else:
                self.hover = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, rect in enumerate(self.option_positions):
                x, y, w, h = rect
                if x <= mx <= x + w and y <= my <= y + h:
                    self.selected = i
                    self.activate_selected()
                    break

    def activate_selected(self) -> None:
        choice = self.options[self.selected]
        if choice == "Start Game":
            # try common locations for PlayScene
            PlayScene = None
            try:
                from scenes.playScene import PlayScene  # if you create a dedicated file
            except Exception:
                PlayScene = None
            if PlayScene:
                self.game.change_scene(PlayScene(self.game))
        elif choice == "Options":
            try:
                from scenes.optionsScreen import OptionsScene
                self.game.change_scene(OptionsScene(self.game))
            except Exception:
                # simple in-place placeholder: return to title if available
                try:
                    from scenes.titleScreen import TitleScene
                    self.game.change_scene(TitleScene(self.game))
                except Exception:
                    pass
        elif choice == "Exit":
            self.game.running = False

    def update(self, dt: float) -> None:
        # reserved for subtle animations later
        pass

    def render(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        surface.fill(self.bg_color)

        # Title
        title = "Python Game"
        title_surf = self.title_font.render(title, True, (240, 235, 220))
        title_rect = title_surf.get_rect(center=(w // 2, int(h * 0.2)))
        surface.blit(title_surf, title_rect)

        # Menu options
        start_y = int(h * 0.35)
        spacing = 56
        self.option_positions = []
        for i, opt in enumerate(self.options):
            color = (255, 210, 0) if i == self.selected else (200, 200, 200)
            opt_surf = self.option_font.render(opt, True, color)
            opt_rect = opt_surf.get_rect(center=(w // 2, start_y + i * spacing))
            surface.blit(opt_surf, opt_rect)
            self.option_positions.append((opt_rect.x, opt_rect.y, opt_rect.width, opt_rect.height))

        # Footer / hint
        hint = "Use ↑/↓ or W/S. Enter to select. Mouse supported."
        hint_surf = self.hint_font.render(hint, True, (150, 150, 150))
        surface.blit(hint_surf, (20, h - 30))
# ...existing code...