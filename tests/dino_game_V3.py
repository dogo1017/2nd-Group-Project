import pygame
import random
import os
import time


# NOTES FOR SELF (IGNORE)

# Photopea

# pygame.Surface.blit(source, dest) - draw one surface onto another at position
# pygame.transform.scale(surface, (w, h)) - resize a surface to given dimensions
# pygame.draw.rect(surface, color, Rect) - draw a filled rectangle
# pygame.Rect(x, y, w, h) - defines a rectangle (position + size)
# pygame.rect.colliderect(other) - returns True if two rects overlap
# pygame.event.get() - returns list of all pending events this frame
# pygame.time.set_timer(event, ms) - fire a custom event every ms milliseconds
# pygame.display.flip() - push the current frame to the screen
# pygame.image.load(path).convert_alpha() - load image, keep transparency
# pygame.font.SysFont(name, size) - load a system font at given size
# pygame.font.Font.render(text, antialias, color) - draw text to a surface
# pygame.Surface.set_alpha(0-255) - set transparency of whole surface
# pygame.mixer.Sound(path) - load a sound file
# pygame.mixer.Sound.play() - play a loaded sound
# pygame.time.get_ticks() - milliseconds since pygame.init()
# clock.tick(fps) - cap framerate, returns ms since last call
# surface.get_width() / get_height() - dimensions of a surface
# rect.topleft - (x, y) tuple of top-left corner
# rect.collidepoint(x, y) - True if point is inside rect
# pygame.mouse.get_pos() - (x, y) of current mouse position


pygame.init()
screen = pygame.display.set_mode((1000, 250))
pygame.display.set_caption("Dino Game")
screen_width, screen_height = 1000, 250

sheet = pygame.image.load('src/dino_game_assets/images/sprite_sheet.png').convert_alpha()

def run_game(high_score):

    def crop_sprite(sx, sy, sw, sh, scale=0.5):
        surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        surf.blit(sheet, (0, 0), (sx, sy, sw, sh))
        return pygame.transform.scale(surf, (max(1, int(sw * scale)), max(1, int(sh * scale))))

    def invert_surface(surface):
        pixels = pygame.surfarray.pixels3d(surface)
        pixels[:] = 255 - pixels
        return surface

    img_standing = crop_sprite(1679, 3, 88, 94)
    img_run1 = crop_sprite(1943, 3, 88, 94)
    img_run2 = crop_sprite(1855, 3, 88, 94)
    img_duck1 = crop_sprite(2207, 37, 118, 60)
    img_duck2 = crop_sprite(2325, 37, 118, 60)
    img_bird1 = crop_sprite(261, 15, 84, 60)
    img_bird2 = crop_sprite(356, 6, 84, 52)

    small_cacti = [crop_sprite(447 + i * 34, 3, 34, 66) for i in range(6)]
    large_cacti = [
        crop_sprite(654, 4, 46, 96),
        crop_sprite(704, 4, 44, 96),
        crop_sprite(754, 4, 46, 96),
        crop_sprite(804, 4, 44, 96),
        crop_sprite(850, 4, 100, 96),
    ]

    ground_strip = crop_sprite(3, 105, 2400, 16, scale=1.0)
    ground_scaled = pygame.transform.scale(ground_strip, (2400, 14))
    ground_width = ground_scaled.get_width()

    font_imgs = [crop_sprite(1294 + i * 21, 2, 21, 21, scale=12/21) for i in range(10)]
    hi_img = crop_sprite(1294 + 10 * 21, 2, 42, 21, scale=24/42)

    DINO_W = img_standing.get_width()
    DINO_H = img_standing.get_height()
    player = pygame.Rect(50, 0, DINO_W, DINO_H)

    background = [255,255,255]
    velocity_y = 0
    gravity = 0.6
    ground_y = 225 - DINO_H
    player.y = ground_y
    duck_w = img_duck1.get_width()
    duck_h = img_duck1.get_height()
    normal_height = DINO_H
    duck_height = duck_h 
    is_night = True
    is_ducking = False
    current_image = img_standing

    jump_sfx = pygame.mixer.Sound('src/dino_game_assets/sounds/jump.mp3')
    point_sfx = pygame.mixer.Sound('src/dino_game_assets/sounds/point.mp3')

    obstacles = []
    speed = 0

    SPAWN_CACTUS_EVENT = pygame.USEREVENT + 1
    ANIMATION_EVENT = pygame.USEREVENT + 2
    BIRD_ANIM_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000)
    pygame.time.set_timer(ANIMATION_EVENT, 100)
    pygame.time.set_timer(BIRD_ANIM_EVENT, 150)

    BIRD_HEIGHTS = [180, 158, 175]

    def spawn_cactus_group():
        bird_chance = min(0.4, 0.05 + (difficulty / 100) * 0.35)
        if random.random() < bird_chance:
            bird_y = random.choice(BIRD_HEIGHTS)
            bw, bh = img_bird1.get_size()
            bird_rect = pygame.Rect(1000, bird_y - bh, bw, bh)
            obstacles.append({'rect': bird_rect, 'image': None, 'is_bird': True})
            return

        if difficulty < 20:
            count = 1 if random.random() < 0.8 else 2
            prefer_small = 0.85
        elif difficulty < 40:
            count = random.choice([1, 1, 2])
            prefer_small = 0.7
        elif difficulty < 70:
            count = random.randint(1, 2)
            prefer_small = 0.5
        else:
            count = random.randint(1, 3)
            prefer_small = 0.4

        for i in range(count):
            img = random.choice(large_cacti if random.random() > prefer_small else small_cacti)
            cw, ch = img.get_size()
            new_rect = pygame.Rect(1000 + i * (cw + 4), 220 - ch, cw, ch)
            obstacles.append({'rect': new_rect, 'image': img, 'is_bird': False})

    ui_font = pygame.font.SysFont(None, 28)
    instr_font = pygame.font.SysFont(None, 30)

    restart_img = pygame.transform.scale(crop_sprite(131,506,72,64).convert_alpha(), (60, 60))


    def draw_score(surface, score, x_start, y):
        s = str(score).zfill(5)
        cx = x_start
        for ch in s:
            glyph = font_imgs[int(ch)]
            surface.blit(glyph, (cx, y))
            cx += glyph.get_width() + 1

    clock = pygame.time.Clock()
    is_first_play = True
    score_time = 0

    while True:
        if score_time > high_score:
            high_score = score_time

        velocity_y = 0
        player.width = DINO_W
        player.height = DINO_H
        player.y = ground_y
        obstacles.clear()
        speed = 0
        is_ducking = False
        current_image = img_standing

        pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000)
        pygame.time.set_timer(ANIMATION_EVENT, 100)
        pygame.time.set_timer(BIRD_ANIM_EVENT, 150)

        start_ticks = pygame.time.get_ticks()
        running = True
        game_started = False
        first_jump_made = False
        difficulty = 0
        curtain_x = 0
        bird_frame = 0
        ground_x1 = 0
        ground_x2 = ground_width

        if not is_first_play:
            game_started = True
            speed = 4
            current_image = img_run1

        last_switch = 0

        while running:
            score_time = 0
            if game_started:
                score_time = (pygame.time.get_ticks() - start_ticks) // 100
                difficulty = min(100, score_time / 5)

            if score_time % 200 == 0 and last_switch != score_time:
                img_standing = invert_surface(img_standing)
                img_run1 = invert_surface(img_run1)
                img_run2 = invert_surface(img_run2)
                img_duck1 = invert_surface(img_duck1)
                img_duck2 = invert_surface(img_duck2)
                img_bird1 = invert_surface(img_bird1)
                img_bird2 = invert_surface(img_bird2)

                #small_cacti = invert_surface(small_cacti)
                #large_cacti = invert_surface(large_cacti)
                ground_scaled = invert_surface(ground_scaled)
                #font_imgs = invert_surface(font_imgs)
                #hi_img = invert_surface(hi_img)
                last_switch = score_time


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == SPAWN_CACTUS_EVENT:
                    if game_started:
                        spawn_cactus_group()

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if is_first_play and not game_started and not first_jump_made and player.y >= ground_y:
                            velocity_y = -10.5
                            jump_sfx.play()
                            first_jump_made = True
                            current_image = img_standing
                            ground_y = 225 - DINO_H
                        elif game_started and player.y >= ground_y:
                            velocity_y = -10.5
                            jump_sfx.play()
                            current_image = img_standing
                    elif event.key == pygame.K_DOWN:
                        if game_started and player.y >= ground_y:
                            is_ducking = True
                            ground_y = 225 - DINO_H + 17
                            player.width = duck_w
                            player.height = duck_height - 20
                            player.y = ground_y + (normal_height - duck_height)
                            current_image = img_duck1

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN and is_ducking:
                        is_ducking = False
                        player.width = DINO_W
                        player.height = DINO_H
                        player.y = ground_y
                        current_image = img_run1
                        ground_y = 225 - DINO_H

                elif event.type == ANIMATION_EVENT:
                    if game_started and player.y >= ground_y:
                        if is_ducking:
                            current_image = img_duck2 if current_image is img_duck1 else img_duck1
                        else:
                            current_image = img_run2 if current_image is img_run1 else img_run1

                elif event.type == BIRD_ANIM_EVENT:
                    bird_frame = 1 - bird_frame

            player.y   += velocity_y
            velocity_y += gravity

            if is_first_play and first_jump_made and not game_started and velocity_y > 0 and player.y >= ground_y - 5:
                game_started = True
                start_ticks = pygame.time.get_ticks()
                speed = 4
                current_image = img_run1

            if player.y >= ground_y:
                player.y = ground_y
                velocity_y = 0

            if game_started:
                if score_time % 100 == 0 and score_time != 0:
                    point_sfx.play()

                if speed < 13:
                    speed += 0.005

                ground_x1 -= speed
                ground_x2 -= speed
                if ground_x1 + ground_width < 0:
                    ground_x1 = ground_x2 + ground_width
                if ground_x2 + ground_width < 0:
                    ground_x2 = ground_x1 + ground_width

                for obs in obstacles[:]:
                    obs['rect'].x -= speed
                    if obs['rect'].x + obs['rect'].width < 0:
                        obstacles.remove(obs)
                        continue
                    if player.colliderect(obs['rect']):
                        is_first_play = False
                        dead = True
                        restart_rect = pygame.Rect(500 - 30, 125 - 30, 60, 60)
                        quit_rect = pygame.Rect(screen_width - 90, 8, 70, 30)

                        while dead:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                if e.type == BIRD_ANIM_EVENT:
                                    bird_frame = 1 - bird_frame
                                if e.type == pygame.MOUSEBUTTONDOWN:
                                    mx, my = pygame.mouse.get_pos()
                                    if restart_rect.collidepoint(mx, my):
                                        dead = False
                                    if quit_rect.collidepoint(mx, my):
                                        pygame.quit()
                                        exit()

                            screen.fill(background)
                            screen.blit(ground_scaled, (ground_x1, 207))
                            screen.blit(ground_scaled, (ground_x2, 207))
                            screen.blit(img_standing, player.topleft)

                            for o in obstacles:
                                if o['is_bird']:
                                    screen.blit(img_bird1 if bird_frame == 0 else img_bird2, o['rect'].topleft)
                                else:
                                    screen.blit(o['image'], o['rect'].topleft)

                            pygame.draw.rect(screen, (180, 180, 180), restart_rect)
                            screen.blit(restart_img, restart_rect.topleft)

                            quit_surf = ui_font.render("QUIT", True, (0, 0, 0))
                            pygame.draw.rect(screen, (200, 200, 200), quit_rect)
                            screen.blit(quit_surf, (quit_rect.x + 8, quit_rect.y + 7))

                            screen.blit(hi_img, (820, 15))
                            draw_score(screen, high_score, 848, 15)
                            draw_score(screen, score_time, 930, 15)

                            pygame.display.flip()
                            clock.tick(60)

                        running = False

            screen.fill(background) 
            screen.blit(ground_scaled, (ground_x1, 207))
            screen.blit(ground_scaled, (ground_x2, 207))

            screen.blit(hi_img, (820, 15))
            draw_score(screen, high_score, 848, 15)
            draw_score(screen, score_time, 930, 15)

            screen.blit(current_image, player.topleft)

            for obs in obstacles:
                if obs['is_bird']:
                    screen.blit(img_bird1 if bird_frame == 0 else img_bird2, obs['rect'].topleft)
                else:
                    screen.blit(obs['image'], obs['rect'].topleft)

            if is_first_play and (not game_started or curtain_x < screen_width):
                curtain_left = player.right + 10 + curtain_x
                if curtain_left < screen_width:
                    curtain_w = screen_width - curtain_left
                    curtain_surf = pygame.Surface((curtain_w, screen_height))
                    curtain_surf.fill(background)
                    line1 = instr_font.render("SPACE / UP  -  Jump", True, (83, 83, 83))
                    line2 = instr_font.render("DOWN  -  Duck",   True, (83, 83, 83))
                    line3 = instr_font.render("Dodge cacti and birds!", True, (83, 83, 83))
                    for surf, y in [(line1, 55), (line2, 95), (line3, 140)]:
                        tx = screen_width // 2 - surf.get_width() // 2 - curtain_left
                        if tx + surf.get_width() > 0:
                            curtain_surf.blit(surf, (tx, y))
                    screen.blit(curtain_surf, (curtain_left, 0))
                if first_jump_made or game_started:
                    curtain_x += 7

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

run_game(12345)