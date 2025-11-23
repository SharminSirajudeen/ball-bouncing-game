#!/usr/bin/env python3
"""Create a simple bird sprite for the game"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Create a transparent surface for the bird sprite
width, height = 120, 80
surface = pygame.Surface((width, height), pygame.SRCALPHA)

# Colors
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

# Fill with transparency
surface.fill(TRANSPARENT)

# Draw a simple cartoon bird
# Body (ellipse)
body_rect = pygame.Rect(30, 25, 60, 35)
pygame.draw.ellipse(surface, BROWN, body_rect)
pygame.draw.ellipse(surface, DARK_BROWN, body_rect, 2)

# Head (circle)
pygame.draw.circle(surface, BROWN, (75, 35), 18)
pygame.draw.circle(surface, DARK_BROWN, (75, 35), 18, 2)

# Beak (triangle) - Bird faces right, so beak points right
# Head is at x=75, beak starts at x=93 (edge of head)
# Original beak had point at x=105, but triangle was backwards
# Correct: wide base at head (x=93), point away from head (x=105)
beak_points = [(93, 32), (93, 38), (105, 35)]  # Triangle pointing right
pygame.draw.polygon(surface, ORANGE, beak_points)

# Eye
pygame.draw.circle(surface, WHITE, (78, 32), 6)
pygame.draw.circle(surface, BLACK, (80, 32), 3)

# Wing (arc on body)
wing_rect = pygame.Rect(35, 30, 35, 25)
pygame.draw.ellipse(surface, DARK_BROWN, wing_rect)

# Tail feathers
tail_points = [(30, 40), (15, 45), (15, 35), (30, 38)]
pygame.draw.polygon(surface, DARK_BROWN, tail_points)

# Save the sprite
pygame.image.save(surface, "bird_sprite.png")
print("Bird sprite created successfully: bird_sprite.png")

# Also create a flipped version for birds flying left
flipped = pygame.transform.flip(surface, True, False)
pygame.image.save(flipped, "bird_sprite_left.png")
print("Left-facing bird sprite created: bird_sprite_left.png")

pygame.quit()