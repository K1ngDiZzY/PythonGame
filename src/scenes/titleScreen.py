import pygame
from typing import Optional

class TitleScene:
    """
    Simple title/intro scene.
    Usage: game.change_scene(TitleScene(game))
    This file intentionally does not import other scenes to avoid circular imports;
    scene transitions should import lazily inside handlers if needed.
    """
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.SysFont(None, 72)
        self.sub_font = pygame.font.SysFont(None, 28)
        self.bg_color = (12, 18, 30)
        self.elapsed = 0.0
        self.display_time = 2.5  # auto-advance to menu after this many seconds
        self.logo_scale = 1.0
        self.pulse_speed = 1.5

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN:
            # on any key press go to main menu (lazy import to avoid circular dependency)
            try:
                from scenes.mainMenuScreen import MainMenuScene
            except Exception:
                MainMenuScene = None
            if MainMenuScene:
                self.game.change_scene(MainMenuScene(self.game))

    def update(self, dt: float) -> None:
        self.elapsed += dt
        # simple pulsing effect for logo
        import math
        self.logo_scale = 1.0 + 0.04 * math.sin(self.elapsed * self.pulse_speed * 2.0 * math.pi)

        # auto-advance to main menu after display_time
        if self.elapsed >= self.display_time:
            try:
                from scenes.mainMenuScreen import MainMenuScene
            except Exception:
                MainMenuScene = None
            if MainMenuScene:
                self.game.change_scene(MainMenuScene(self.game))

    def render(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        surface.fill(self.bg_color)

        # Title / logo
        title_text = "Python Game"
        title_surf = self.title_font.render(title_text, True, (240, 235, 220))
        # apply simple scale by resizing surface (fast enough for title)
        ts = title_surf
        if abs(self.logo_scale - 1.0) > 0.001:
            new_size = (max(1, int(ts.get_width() * self.logo_scale)),
                        max(1, int(ts.get_height() * self.logo_scale)))
            ts = pygame.transform.smoothscale(ts, new_size)
        rect = ts.get_rect(center=(w // 2, h // 2 - 20))
        surface.blit(ts, rect)

        # Subtitle / hint
        hint = "Press any key to continue"
        hint_surf = self.sub_font.render(hint, True, (180, 180, 180))
        hint_rect = hint_surf.get_rect(center=(w // 2, h // 2 + 60))
        surface.blit(hint_surf, hint_rect)

        # optionally show a progress dot / timer
        progress = min(1.0, self.elapsed / max(0.0001, self.display_time))
        bar_w = int(w * 0.4)
        bar_h = 6
        bx = (w - bar_w) // 2
        by = hint_rect.bottom + 18
        pygame.draw.rect(surface, (60, 60, 80), (bx, by, bar_w, bar_h))
        pygame.draw.rect(surface, (100, 200, 140), (bx, by, int(bar_w * progress), bar_h))
# filepath: c:\Users\bende\source\PythonGame\src\scenes\titleScreen.py
