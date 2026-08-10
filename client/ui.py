"""Pygame UI shell."""
from __future__ import annotations
import pygame

WIDTH = 960
HEIGHT = 540
TITLE = "Blackout Protocol"

def run_ui() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("arial", 28)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((12, 16, 24))
        text = font.render("Blackout Protocol - UI Shell", True, (230, 230, 230))
        screen.blit(text, (40, 40))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_ui()
