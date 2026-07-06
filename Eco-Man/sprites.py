# sprites.py

import pygame
import random
import os
from settings import TILE_SIZE, BLUE, YELLOW

ASSET_PATH = "assets/images"


def load_img(name, size):
    img = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
    return pygame.transform.scale(img, (size, size))


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))


class Pellet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (3, 3), 3)
        self.rect = self.image.get_rect(center=pos)


class Recyclable(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        imgs = [
            "pollutant_plastic.png",
            "pollutant_smoke.png",
            "pollutant_car_smoke.png",
            "pollutant_oil.png",
        ]
        self.image = load_img(random.choice(imgs), TILE_SIZE)
        self.rect = self.image.get_rect(center=pos)


class Recycler(pygame.sprite.Sprite):
    def __init__(self, pos, walls):
        super().__init__()
        self.base_image = load_img("recycler_open.png", TILE_SIZE)
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft=pos)
        self.walls = walls
        self.speed = 3
        self.direction = "RIGHT"

    def _rotate(self):
        if self.direction == "RIGHT":
            self.image = self.base_image
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.base_image, 180)
        elif self.direction == "UP":
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.base_image, -90)

    def update(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "LEFT"
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "RIGHT"
        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = "UP"
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = "DOWN"

        self._rotate()

        # move + collide X
        self.rect.x += dx
        for w in self.walls:
            if self.rect.colliderect(w.rect):
                self.rect.x -= dx

        # move + collide Y
        self.rect.y += dy
        for w in self.walls:
            if self.rect.colliderect(w.rect):
                self.rect.y -= dy


class Pollutant(pygame.sprite.Sprite):
    def __init__(self, pos, walls):
        super().__init__()
        ghosts = ["Blinky.png", "Pinky.png", "Inky.png", "Clyde.png"]
        self.image = load_img(random.choice(ghosts), TILE_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.walls = walls
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.speed = 2.6  # slightly slower, fair but still dangerous

    def update(self):
        dx, dy = self.direction
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        hit_wall = False
        for w in self.walls:
            if self.rect.colliderect(w.rect):
                self.rect.x -= dx * self.speed
                self.rect.y -= dy * self.speed
                hit_wall = True
                break

        if hit_wall or random.random() < 0.01:
            # pick a new random direction
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
