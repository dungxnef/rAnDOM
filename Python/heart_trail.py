import pygame
import pygame.gfxdraw
import numpy as np
import math
import random
from colorsys import hsv_to_rgb

pygame.init()

# Set up the drawing window
W, H = 800, 800
screen = pygame.display.set_mode((H, W))
pygame.display.set_caption("Heart Trail")

# Helper function to draw a filled circle
def draw_circle(screen, x, y, r, color):
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)

# Helper function to generate a random number in a range
def rand(a0, a1):
    return random.uniform(a0,a1)

size_steps = 100
a = np.linspace(13, 13, size_steps)
b = np.linspace(-5, -3.3, size_steps)
c = np.linspace(-2, -2.4, size_steps)
d = np.linspace(-1, -0.16, size_steps)
scalex = np.linspace(1, 1.18, size_steps) * 10
scaley = np.linspace(1, 1.36, size_steps) * 10

class Particle:
    def __init__(self, t, size, off_s, off_x=0, off_y=0):
        self.t = t
        self.off_s = off_s
        self.size = size
        self.off_x = off_x
        self.off_y = off_y

    def draw(self, screen: pygame.Surface, i):
        x, y = self.get_pos(i)
        hue = ((self.t / (2 * np.pi)) + (i / 100.0)) % 1
        red, green, blue = hsv_to_rgb(hue, float(rand(0.6,1)), float(rand(0.85,1)))
        color = (int(red * 255), int(green * 255), int(blue * 255))

        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (self.size, self.size), self.size)
        screen.blit(particle_surface, (x - self.size, y - self.size))

    def get_pos(self, i):
        t = self.t
        x_pos = 16 * np.sin(t) ** 3
        x_pos += self.off_x
        x_pos *= (scalex[i] + self.off_s)
        y_pos = a[i] * np.cos(t) + b[i] * np.cos(2*t) + c[i] * np.cos(3*t) + d[i] * np.cos(4*t)
        y_pos += self.off_y
        y_pos *= (scaley[i] + self.off_s)
        return int(x_pos + W / 2), int(-y_pos + H / 2)

particles = []

# Create particles
for t in np.concatenate((np.linspace(0.18, 3.14-0.18, 1000), np.linspace(3.14+0.18, 2*3.1415-0.18, 1000)), axis=0):
    off_s = -np.random.exponential(1.8)
    size = int(rand(1.5, 2.5))
    particle = Particle(t, size, off_s)
    particles.append(particle)

bloom_indices = np.linspace(0, size_steps - 1, 40)
shrink_indices = np.linspace(size_steps - 1, 0, 30)
indices = np.concatenate((bloom_indices, shrink_indices), axis=0)
indices = np.uint8(indices)

frame = 0

# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    index = indices[frame % len(indices)]
    
    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Update particle positions to follow the cursor
    for p in particles:
        p.off_x = mouse_x - W / 2
        p.off_y = H / 2 - mouse_y
        p.draw(screen, index)
    
    frame += 1
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
