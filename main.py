import pygame
from settings import *
from level import Level

pygame.init()

# --- MUSIC SETUP ---
pygame.mixer.init()
try:
    pygame.mixer.music.load("playing-pac-man-6783.mp3")  # adjust path if needed
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)  # loop forever
except pygame.error as e:
    print("Could not load or play music:", e)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eco-Man: Clean the Planet")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)
big_font = pygame.font.Font(None, 40)

ecosystems = ["city", "ocean"]
score = 0


def draw_pollution_bar(pollution):
    pollution = max(0.0, pollution)
    ratio = pollution / POLLUTION_MAX
    if ratio > 0.6:
        col = RED
    elif ratio > 0.3:
        col = (255, 200, 0)
    else:
        col = GREEN

    pygame.draw.rect(screen, WHITE, (20, 20, 200, 18), 2)
    pygame.draw.rect(screen, col, (20, 20, int(200 * ratio), 18))
    text = font.render(f"Pollution {int(ratio * 100)}%", True, WHITE)
    screen.blit(text, (230, 20))


def show_fact_screen(ecosystem: str):
    fact = ECOSYSTEM_FACTS[ecosystem][0]
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                running = False

        screen.fill(BLACK)
        title = big_font.render(f"{ecosystem.capitalize()} Cleaned!", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 170))

        label = font.render("Ecosystem Fact:", True, WHITE)
        screen.blit(label, (60, 230))

        fact_surf = font.render(fact, True, WHITE)
        screen.blit(fact_surf, (60, 260))

        cont = font.render("Press any key to continue", True, WHITE)
        screen.blit(cont, (WIDTH // 2 - cont.get_width() // 2, 320))

        pygame.display.flip()
        clock.tick(30)


def start_menu():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(BLACK)
        title = big_font.render("Eco-Man: Clean the Planet", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

        press_start = font.render("Press ENTER to start", True, WHITE)
        press_exit = font.render("Press ESC to exit", True, WHITE)
        controls = font.render("Use arrow keys to move Eco-Man", True, WHITE)

        screen.blit(press_start, (WIDTH // 2 - press_start.get_width() // 2, 270))
        screen.blit(press_exit,  (WIDTH // 2 - press_exit.get_width() // 2, 300))
        screen.blit(controls,    (WIDTH // 2 - controls.get_width() // 2, 340))

        pygame.display.flip()
        clock.tick(30)


def game_over_screen():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(BLACK)
        title = big_font.render("Game Over", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

        msg1 = font.render("Eco-Man was caught by a ghost!", True, WHITE)
        msg2 = font.render("Press ENTER to return to menu", True, WHITE)
        msg3 = font.render("Press ESC to exit", True, WHITE)

        screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, 250))
        screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, 290))
        screen.blit(msg3, (WIDTH // 2 - msg3.get_width() // 2, 320))

        pygame.display.flip()
        clock.tick(30)


# ------------- MAIN APP LOOP -------------
while True:
    level_index = 0
    score = 0

    start_menu()

    while level_index < len(ecosystems):
        ecosystem = ecosystems[level_index]
        level = Level(ecosystem)

        pollution = float(POLLUTION_MAX)

        # --- FAST POLLUTION DROP ---
        # Only need a few pollutants (e.g., 5) to reach 0%
        TARGET_POLLUTANTS_TO_CLEAR = 40
        pollution_per_pollutant = POLLUTION_MAX / TARGET_POLLUTANTS_TO_CLEAR

        level_running = True

        while level_running:
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            level.update()

            # Yellow dots: score ONLY (no pollution impact)
            pellet_hits = pygame.sprite.spritecollide(
                level.recycler, level.pellets, True
            )
            if pellet_hits:
                score += len(pellet_hits)

            # Big pollutants: main objective and bar progress
            rec_hits = pygame.sprite.spritecollide(
                level.recycler, level.recyclables, True
            )
            if rec_hits:
                score += 15 * len(rec_hits)
                pollution -= pollution_per_pollutant * len(rec_hits)
                pollution = max(0.0, pollution)

            # Game over on ghost hit
            if pygame.sprite.spritecollide(level.recycler, level.pollutants, False):
                game_over_screen()
                level_running = False
                level_index = len(ecosystems)
                break

            # ✅ WIN ONLY WHEN BAR REACHES 0%
            if pollution <= 0.0:
                pollution = 0.0

                screen.fill(BLACK)
                level.draw(screen)
                draw_pollution_bar(pollution)
                pygame.display.flip()
                pygame.time.delay(800)

                show_fact_screen(ecosystem)
                level_index += 1
                level_running = False
                break

            # Draw frame
            screen.fill(BLACK)
            level.draw(screen)
            draw_pollution_bar(pollution)

            screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 45))
            eco_label = font.render(f"Ecosystem: {ecosystem.capitalize()}",
                                    True, WHITE)
            screen.blit(eco_label, (20, HEIGHT - 30))

            fact_text = ECOSYSTEM_FACTS[ecosystem][0]
            fact_surface = font.render(f"Fact: {fact_text}", True, WHITE)
            screen.blit(
                fact_surface,
                (WIDTH // 2 - fact_surface.get_width() // 2, HEIGHT - 30),
            )

            pygame.display.flip()
