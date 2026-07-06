# level.py

import pygame, random
from sprites import Wall, Pellet, Recyclable, Recycler, Pollutant

PACMAN_WALLS = [
    [0,0,6,600],[0,0,600,6],[0,600,606,6],[600,0,6,606],
    [300,0,6,66],[60,60,186,6],[360,60,186,6],
    [60,120,66,6],[60,120,6,126],[180,120,246,6],
    [300,120,6,66],[480,120,66,6],[540,120,6,126],
    [120,180,126,6],[120,180,6,126],[360,180,126,6],
    [480,180,6,126],[180,240,6,126],[180,360,246,6],
    [420,240,6,126],[240,240,42,6],[324,240,42,6],
    [240,240,6,66],[240,300,126,6],[360,240,6,66],
    [0,300,66,6],[540,300,66,6],[60,360,66,6],
    [60,360,6,186],[480,360,66,6],[540,360,6,186],
    [120,420,366,6],[120,420,6,66],[480,420,6,66],
    [180,480,246,6],[300,480,6,66],[120,540,126,6],
    [360,540,126,6]
]

class Level:
    def __init__(self, eco):
        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.recyclables = pygame.sprite.Group()   # big pollutants
        self.pollutants = pygame.sprite.Group()    # ghosts
        self.all = pygame.sprite.Group()

        # Walls
        for x, y, w, h in PACMAN_WALLS:
            wall = Wall(x, y, w, h)
            self.walls.add(wall)
            self.all.add(wall)

        # Player (Eco-Man)
        self.recycler = Recycler((287, 439), self.walls)
        self.all.add(self.recycler)

        # Pellets (yellow dots)
        for r in range(19):
            for c in range(19):
                cx = (30 * c + 6) + 26
                cy = (30 * r + 6) + 26
                p = Pellet((cx, cy))
                if not any(p.rect.colliderect(w.rect) for w in self.walls):
                    self.pellets.add(p)
                    self.all.add(p)

        # Pollutants (bottles, smoke, etc.)
        if eco == "city":
            pollutant_count = 50   # tweak these to change difficulty
        elif eco == "ocean":
            pollutant_count = 65
        else:
            pollutant_count = 40   # default

        for _ in range(pollutant_count):
            while True:
                rx = random.randint(40, 560)
                ry = random.randint(40, 560)
                rec = Recyclable((rx, ry))
                if not any(rec.rect.colliderect(w.rect) for w in self.walls):
                    self.recyclables.add(rec)
                    self.all.add(rec)
                    break

        # Ghosts (NO CENTER GHOST)
        starts = [
            (247, 259),
            (327, 259),
            (287, 199),
            (287, 299),
        ]
        for s in starts:
            g = Pollutant(s, self.walls)
            self.pollutants.add(g)
            self.all.add(g)

    def update(self):
        self.all.update()

    def draw(self, s):
        self.all.draw(s)
