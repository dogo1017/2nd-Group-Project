import pygame
import random
import os


# NOTES FOR SELF (IGNORE)

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


high_score = 155

pygame.init()
screen = pygame.display.set_mode((1000, 250))
pygame.display.set_caption("Dino Game")
screen_width, screen_height = 1000, 250
player = pygame.Rect(50, 160, 44, 47)
player_color = (0, 255, 0)

def load_image(name, scale=None):
    try:
        image = pygame.image.load(os.path.join(name)).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        surf = pygame.Surface((30, 50))
        surf.fill((255, 0, 0))
        return surf

jump = pygame.mixer.Sound('src/dino_game_folder/sounds/jump.mp3')
point = pygame.mixer.Sound('src/dino_game_folder/sounds/point.mp3')

small_cacti = [load_image(f'src/dino_game_folder/images/small{i}.png') for i in range(1, 7)]
large_cacti = [load_image(f'src/dino_game_folder/images/large{i}.png') for i in range(1, 7)]
ground = load_image('src/dino_game_folder/images/ground.png')
font_imgs = [load_image(f'src/dino_game_folder/images/{i}.png') for i in range(0, 10)]
hi_img = load_image('src/dino_game_folder/images/hi.png')

use_image = False
image_surface_standing = None
image_surface_run1 = None
image_surface_run2 = None
current_image = None

try:
    image_surface_standing = load_image('src/dino_game_folder/images/standing_dino.jpg', (player.width, player.height))
    image_surface_run1 = load_image('src/dino_game_folder/images/running1.png', (player.width, player.height))
    image_surface_run2 = load_image('src/dino_game_folder/images/running2.png', (player.width, player.height))
    image_surface_duck1 = load_image('src/dino_game_folder/images/duck_left.webp', (59, 50))
    image_surface_duck2 = load_image('src/dino_game_folder/images/duck_right.webp', (59, 50))
    current_image = image_surface_standing
    use_image = True
except:
    use_image = False

use_bird_image = False
bird_img1 = None
bird_img2 = None

try:
    bird_img1 = load_image('src/dino_game_folder/images/bird1.png', (46, 40))
    bird_img2 = load_image('src/dino_game_folder/images/bird2.png', (46, 40))
    use_bird_image = True
except:
    use_bird_image = False

velocity_y = 0
gravity = 0.6
ground_y = 175
player.y = ground_y
obstacles = []
speed = 0
is_ducking = False
normal_height = 47
duck_height = 30

SPAWN_CACTUS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000)
ANIMATION_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATION_EVENT, 100)
BIRD_ANIM_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(BIRD_ANIM_EVENT, 150)

start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True
game_started = False
first_jump_made = False
difficulty = 0
is_first_play = True
curtain_x = 0
score_time = 0
bird_frame = 0

try:
    restart_img = load_image('src/dino_game_folder/images/restart.png', (60, 60))
except:
    restart_img = None

ui_font = pygame.font.SysFont(None, 28)
instr_font = pygame.font.SysFont(None, 30)

BIRD_HEIGHTS = [130, 158, 175]

def spawn_cactus_group():
    bird_chance = min(0.4, 0.05 + (difficulty / 100) * 0.35)
    if random.random() < bird_chance:
        bird_y = random.choice(BIRD_HEIGHTS)
        bird_rect = pygame.Rect(1000, bird_y, 46, 40)
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

    sizes = {"small": (17, 35), "large": (25, 50)}
    for i in range(count):
        is_large = random.random() > prefer_small
        if is_large:
            size = sizes["large"]
            img = random.choice(large_cacti)
        else:
            size = sizes["small"]
            img = random.choice(small_cacti)
        img = pygame.transform.scale(img, size)
        new_rect = pygame.Rect(1000 + (i * 30), 207 - size[1], size[0], size[1])
        obstacles.append({'rect': new_rect, 'image': img, 'is_bird': False})

ground_scaled = pygame.transform.scale(ground, (2400, 14))
ground_width = ground_scaled.get_width()
ground_x1 = 0
ground_x2 = ground_width

while True:

    if score_time > high_score:
        high_score = score_time

    velocity_y = 0
    player.y = ground_y
    obstacles = []
    speed = 0
    is_ducking = False

    pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000)
    pygame.time.set_timer(ANIMATION_EVENT, 100)
    pygame.time.set_timer(BIRD_ANIM_EVENT, 150)

    start_ticks = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    running = True
    game_started = False
    first_jump_made = False
    difficulty = 0
    curtain_x = 0
    bird_frame = 0

    if not is_first_play:
        game_started = True
        speed = 4
        if use_image:
            current_image = image_surface_run1

    while running:
        dig1, dig2, dig3, dig4, dig5 = 0, 0, 0, 0, 0
        score_time = 0
        if game_started:
            score_time = (pygame.time.get_ticks() - start_ticks) // 100
            difficulty = min(100, score_time / 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == SPAWN_CACTUS_EVENT:
                if game_started:
                    spawn_cactus_group()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP]:
                    if is_first_play and not game_started and not first_jump_made and player.y >= ground_y:
                        velocity_y = -10.5
                        jump.play()
                        first_jump_made = True
                        if use_image:
                            current_image = image_surface_standing
                    elif game_started and player.y >= ground_y:
                        velocity_y = -10.5
                        jump.play()
                        if use_image:
                            current_image = image_surface_standing
                elif event.key == pygame.K_DOWN:
                    if game_started and player.y >= ground_y:
                        is_ducking = True
                        player.height = duck_height
                        player.y = ground_y + (normal_height - duck_height)
                        if use_image:
                            current_image = image_surface_duck1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    if is_ducking:
                        is_ducking = False
                        player.height = normal_height
                        player.y = ground_y
                        if use_image:
                            current_image = image_surface_run1
            elif event.type == ANIMATION_EVENT:
                if game_started and use_image and player.y >= ground_y:
                    if is_ducking:
                        if current_image == image_surface_duck1:
                            current_image = image_surface_duck2
                        else:
                            current_image = image_surface_duck1
                    else:
                        if current_image == image_surface_run1:
                            current_image = image_surface_run2
                        else:
                            current_image = image_surface_run1
            elif event.type == BIRD_ANIM_EVENT:
                bird_frame = 1 - bird_frame

        player.y += velocity_y
        velocity_y += gravity
        if is_first_play and first_jump_made and not game_started and velocity_y > 0 and player.y >= ground_y - 5:
            game_started = True
            start_ticks = pygame.time.get_ticks()
            speed = 4
            if use_image:
                current_image = image_surface_run1
        if player.y >= ground_y:
            player.y = ground_y
            velocity_y = 0

        if game_started:
            if score_time % 100 == 0:
                if score_time != 0:
                    point.play()
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
                        screen.fill((255, 255, 255))
                        screen.blit(ground_scaled, (ground_x1, 207))
                        screen.blit(ground_scaled, (ground_x2, 207))
                        if use_image:
                            screen.blit(image_surface_standing, player.topleft)
                        else:
                            pygame.draw.rect(screen, (0, 255, 0), player)
                        for o in obstacles:
                            if o['is_bird']:
                                if use_bird_image:
                                    bimg = bird_img1 if bird_frame == 0 else bird_img2
                                    screen.blit(bimg, o['rect'].topleft)
                                else:
                                    pygame.draw.rect(screen, (80, 80, 200), o['rect'])
                            else:
                                screen.blit(o['image'], o['rect'].topleft)
                        pygame.draw.rect(screen, (180, 180, 180), restart_rect)
                        quit_surf = ui_font.render("QUIT", True, (0, 0, 0))
                        pygame.draw.rect(screen, (200, 200, 200), quit_rect)
                        screen.blit(quit_surf, (quit_rect.x + 8, quit_rect.y + 7))
                        pygame.display.flip()
                        clock.tick(60)
                    running = False

        screen.fill((255, 255, 255))

        screen.blit(ground_scaled, (ground_x1, 207))
        screen.blit(ground_scaled, (ground_x2, 207))

        score_str = str(score_time).zfill(5)
        for i, num in enumerate(score_str):
            exec(f"dig{i+1} = int(num)")
        screen.blit(pygame.transform.scale(font_imgs[dig1], (12, 14)), (930, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig2], (12, 14)), (942, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig3], (12, 14)), (954, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig4], (12, 14)), (966, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig5], (12, 14)), (978, 15))
        screen.blit(pygame.transform.scale(hi_img, (24, 14)), (820, 15))

        high_score_str = str(high_score).zfill(5)
        for i, num in enumerate(high_score_str):
            exec(f"dig{i+1} = int(num)")
        screen.blit(pygame.transform.scale(font_imgs[dig1], (12, 14)), (850, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig2], (12, 14)), (862, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig3], (12, 14)), (874, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig4], (12, 14)), (886, 15))
        screen.blit(pygame.transform.scale(font_imgs[dig5], (12, 14)), (898, 15))

        if use_image:
            screen.blit(current_image, player.topleft)
        else:
            pygame.draw.rect(screen, (0, 255, 0), player)

        for obs in obstacles:
            if obs['is_bird']:
                if use_bird_image:
                    bimg = bird_img1 if bird_frame == 0 else bird_img2
                    screen.blit(bimg, obs['rect'].topleft)
                else:
                    pygame.draw.rect(screen, (80, 80, 200), obs['rect'])
            else:
                screen.blit(obs['image'], obs['rect'].topleft)

        if is_first_play and (not game_started or curtain_x < screen_width):
            curtain_left = player.right + 10 + curtain_x
            if curtain_left < screen_width:
                curtain_w = screen_width - curtain_left
                curtain_surf = pygame.Surface((curtain_w, screen_height))
                curtain_surf.fill((255, 255, 255))
                line1 = instr_font.render("SPACE / UP  -  Jump", True, (83, 83, 83))
                line2 = instr_font.render("DOWN  -  Duck", True, (83, 83, 83))
                line3 = instr_font.render("Dodge cacti and birds!", True, (83, 83, 83))
                for surf, y in [(line1, 55), (line2, 95), (line3, 140)]:
                    tx = screen_width // 2 - surf.get_width() // 2 - curtain_left
                    if 0 <= tx + surf.get_width():
                        curtain_surf.blit(surf, (tx, y))
                screen.blit(curtain_surf, (curtain_left, 0))
            if first_jump_made or game_started:
                curtain_x += 7

        pygame.display.flip()
        clock.tick(60)


pygame.quit()