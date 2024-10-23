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
pygame.display.set_caption("Heart beat")

def draw_circle(screen, x, y, r, color):
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)

def rand(a0, a1):
    return random.uniform(a0,a1)


size_steps = 100
a = np.linspace(13, 13, size_steps)
b = np.linspace(-5, -3.3, size_steps)
c = np.linspace(-2, -2.4, size_steps)
d = np.linspace(-1, -0.16, size_steps)
scalex = np.linspace(1, 1.18, size_steps) * 10
scaley = np.linspace(1, 1.36, size_steps) * 10

class PersistentParticle:
    def __init__(self, t, size, off_s):
        self.t = t
        self.off_s = off_s
        self.size = size


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
        x_pos *= (scalex[i] + self.off_s)

        y_pos = a[i] * np.cos(t) + b[i] * np.cos(2*t) + c[i] * np.cos(3*t) + d[i] * np.cos(4*t)
        y_pos *= (scaley[i] + self.off_s)

        return int(x_pos + W / 2), int(-y_pos + H / 2)

class GlitterParticle:
    def __init__(self, t, size, off_x, off_y, off_s, phi):
        self.t = t
        self.off_x = off_x
        self.off_y = off_y
        self.off_s = off_s
        self.size = size
        self.phi = phi

    def get_pos(self, i):
        t = self.t

        x_pos = 16 * np.sin(t) ** 3
        x_pos += self.off_x
        x_pos *= (scalex[i] + self.off_s)

        y_pos = a[i] * np.cos(t) + b[i] * np.cos(2*t) + c[i] * np.cos(3*t) + d[i] * np.cos(4*t)
        y_pos += self.off_y
        y_pos *= (scaley[i] + self.off_s)

        return int(x_pos + W / 2), int(-y_pos + H / 2)
    

    def draw(self, screen: pygame.Surface, i):
        x, y = self.get_pos(i)
        hue = ((self.t / (2 * np.pi)) + (i / 100.0)) % 1  # Cycle through hues based on angle t
        red, green, blue = hsv_to_rgb(hue, float(rand(0.5,0.8)), float(rand(0.85,1)))
        alpha = int(128 * np.cos(self.phi + i / 5) + 127)
        color = (int(red * 255), int(green * 255), int(blue * 255), alpha)
        
        # Create a surface for the particle with per-pixel alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (self.size, self.size), self.size)
        
        # Blit the particle surface onto the main screen
        screen.blit(particle_surface, (x - self.size, y - self.size))


persistent_particles = []
glitter_particles = []

# Create persistent particles
for repeat in range(3):
    for t in np.concatenate((np.linspace(0.18, 3.14-0.18, 1000), np.linspace(3.14+0.18, 2*3.1415-0.18, 1000)), axis=0):
        off_s = -np.random.exponential(1.8)
        size = int(rand(1.5, 2.5))

        particle = PersistentParticle(t, size, off_s)
        persistent_particles.append(particle)

# Create glitter particles
for repeat in range(3):
    for t in np.concatenate((np.linspace(0.2, 3.14-0.2, 1000), np.linspace(3.14+0.2, 2*3.1415-0.2, 1000)), axis=0):
        off_x = np.random.randn() * 2
        off_y = np.random.randn() * 2
        off_s = np.random.randn() * 1.5 - 1.8
        size = int(rand(1.5, 2.5))

        # phi
        phi = rand(0, 2 * np.pi)

        particle = GlitterParticle(t, size, off_x, off_y, off_s, phi)
        glitter_particles.append(particle)

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
    for p in persistent_particles:
        p.draw(screen, index)
    for p in glitter_particles:
        p.draw(screen, size_steps - 1 - index)
    frame += 150
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()