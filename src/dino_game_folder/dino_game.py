import pygame
import random
import os

high_score = 164

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

jump = pygame.mixer.Sound('src/dino_game_folder/jump.mp3') 
point = pygame.mixer.Sound('src/dino_game_folder/point.mp3')

small_cacti = [load_image(f'src/dino_game_folder/small{i}.png') for i in range(1, 7)]
large_cacti = [load_image(f'src/dino_game_folder/large{i}.png') for i in range(1, 7)]
ground = load_image('src/dino_game_folder/ground.png')
font_imgs = [load_image(f'src/dino_game_folder/{i}.png') for i in range(0, 10)]
hi_img = load_image('src/dino_game_folder/hi.png')

use_image = False
image_surface_standing = None
image_surface_run1 = None
image_surface_run2 = None
current_image = None

try:
    image_surface_standing = load_image('src/dino_game_folder/standing_dino.jpg', (player.width, player.height))
    image_surface_run1 = load_image('src/dino_game_folder/running1.png', (player.width, player.height))
    image_surface_run2 = load_image('src/dino_game_folder/running2.png', (player.width, player.height))
    image_surface_duck1 = load_image('src/dino_game_folder/duck_left.webp', (59, 30))
    image_surface_duck2 = load_image('src/dino_game_folder/duck_right.webp', (59, 30))
    current_image = image_surface_standing
    use_image = True
except:
    use_image = False

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

start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True
game_started = False
first_jump_made = False
difficulty = 0

def spawn_cactus_group():
    # Difficulty affects number of cacti and size distribution
    # At low difficulty (0-30), prefer fewer and smaller cacti
    # At high difficulty (70+), allow more and larger cacti
    
    if difficulty < 20:
        # Early game - mostly single small cacti
        count = 1 if random.random() < 0.8 else 2
        prefer_small = 0.85
    elif difficulty < 40:
        # Early-mid game - mix of 1-2 cacti
        count = random.choice([1, 1, 2])
        prefer_small = 0.7
    elif difficulty < 70:
        # Mid game - standard distribution
        count = random.randint(1, 2)
        prefer_small = 0.5
    else:
        # Late game - harder patterns
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
        obstacles.append({'rect': new_rect, 'image': img})

ground_scaled = pygame.transform.scale(ground, (2400, 14))
ground_width = ground_scaled.get_width()
ground_x1 = 0
ground_x2 = ground_width

def pause_game():
    global game_started, velocity_y
    game_started = False
    velocity_y = 0
    if use_image:
        global current_image
        current_image = image_surface_standing


while running:
    dig1, dig2, dig3, dig4, dig5 = 0, 0, 0, 0, 0
    score_time = 0
    # Update difficulty based on score (0-100 scale)
    if game_started:
        score_time = (pygame.time.get_ticks() - start_ticks) // 100
        difficulty = min(100, score_time / 5)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_CACTUS_EVENT:
            if game_started:
                spawn_cactus_group()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP]:
                if not game_started and not first_jump_made and player.y >= ground_y:
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

    player.y += velocity_y
    velocity_y += gravity
    if player.y >= ground_y:
        player.y = ground_y
        velocity_y = 0
        if first_jump_made and not game_started:
            game_started = True
            start_ticks = pygame.time.get_ticks()
            speed = 4
            if use_image:
                current_image = image_surface_run1

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
            if player.colliderect(obs['rect']):
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

    high_score_str = str(high_score ).zfill(5)
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
        screen.blit(obs['image'], obs['rect'].topleft)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()