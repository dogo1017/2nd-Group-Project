import pygame
import random
import subprocess
import sys


def run_game(high_score):

    pygame.init()
    screen = pygame.display.set_mode((1000, 250))
    pygame.display.set_caption("Dino Game")
    screen_width, screen_height = 1000, 250

    sheet = pygame.image.load('src/dino_game_assets/images/sprite_sheet.png').convert_alpha()

    try:
        import numpy
        numpy_installed = True
    except:
        numpy_installed = False
    if numpy_installed == False:
        while True:
            auto_install = input("It seems you are missing numpy, which is required for some features in the game. Would you like to install it automatically? (y/n): ").lower().strip()
            if auto_install == 'y':
                print("Installing now...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
                    print("NumPy installed successfully.")
                    numpy_installed = True
                    import numpy
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install NumPy: {e}")
                except ImportError:
                    print("NumPy still failed to import after installation attempt.")
                    numpy_installed = False
                break
            else:
                break

    def crop_sprite(sx, sy, sw, sh, scale=0.5):
        surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        surf.blit(sheet, (0, 0), (sx, sy, sw, sh))
        return pygame.transform.scale(surf, (max(1, int(sw * scale)), max(1, int(sh * scale))))

    def invert_surface(surface):
        pixels = pygame.surfarray.pixels3d(surface)
        pixels[:] = 255 - pixels
        return surface

    def make_small_cacti():
        return [crop_sprite(447 + i * 34, 3, 34, 66) for i in range(6)]

    def make_large_cacti():
        return [
            crop_sprite(654, 4, 46, 96),
            crop_sprite(704, 4, 44, 96),
            crop_sprite(754, 4, 46, 96),
            crop_sprite(804, 4, 44, 96),
            crop_sprite(850, 4, 100, 96),
        ]

    img_standing = crop_sprite(1679, 3, 88, 94)
    img_run1 = crop_sprite(1943, 3, 88, 94)
    img_run2 = crop_sprite(1855, 3, 88, 94)
    img_duck1 = crop_sprite(2207, 37, 118, 60)
    img_duck2 = crop_sprite(2325, 37, 118, 60)
    img_dead = crop_sprite(2031 ,3,88,94)
    img_bird1 = crop_sprite(261, 15, 84, 60)
    img_bird2 = crop_sprite(356, 6, 84, 52)

    small_cacti = make_small_cacti()
    large_cacti = make_large_cacti()

    ground_strip = crop_sprite(3, 105, 2400, 16, scale=1.0)
    ground_scaled = pygame.transform.scale(ground_strip, (2400, 14))
    ground_width = ground_scaled.get_width()

    font_imgs = [crop_sprite(1295 + i * 21, 3, 21, 18, scale=12/21) for i in range(10)]
    hi_img = crop_sprite(1495, 3, 42, 21, scale=24/42)

    img_cloud = crop_sprite(167,3,92,27,scale=1.0)

    moon_coord_list = [
        (955, 3, 40, 80),
        (995, 3, 40, 80),
        (1035, 3, 40, 80),
        (1075, 3, 80, 80),
        (1155, 3, 40, 80),
        (1195, 3, 40, 80),
        (1235, 3, 40, 80),
    ]

    moon_imgs = [crop_sprite(x, y, w, h, scale=0.8) for (x, y, w, h) in moon_coord_list]

    star_imgs = [
        crop_sprite(1275, 3, 18, 18, scale=0.5),
        crop_sprite(1275, 20, 19, 18, scale=0.5),
        crop_sprite(1275, 38, 19, 18, scale=0.5),
    ]

    restart_frame_coords = [
        (10, 132, 73, 64),
        (77, 132, 72, 64),
        (147, 132, 72, 64),
        (219, 132, 72, 64),
        (291, 132, 72, 64),
        (363, 132, 72, 64),
        (435, 132, 72, 64),
        (507, 132, 72, 64),
    ]
    restart_frames = [crop_sprite(x, y, w, h, scale=0.75) for (x, y, w, h) in restart_frame_coords]
    BTN_W = restart_frames[0].get_width()
    BTN_H = restart_frames[0].get_height()

    DINO_W = img_standing.get_width()
    DINO_H = img_standing.get_height()
    player = pygame.Rect(50, 0, DINO_W, DINO_H)

    velocity_y = 0
    gravity = 0.6
    ground_y = 225 - DINO_H
    player.y = ground_y
    duck_w = img_duck1.get_width()
    duck_h = img_duck1.get_height()
    normal_height = DINO_H
    duck_height = duck_h

    is_night = False
    is_ducking = False
    current_image = img_standing

    try:
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)
        jump_sfx = pygame.mixer.Sound('src/dino_game_assets/sounds/jump.wav')
        point_sfx = pygame.mixer.Sound('src/dino_game_assets/sounds/point.wav')
        die_sfx = pygame.mixer.Sound('src/dino_game_assets/sounds/die.wav')
        point_sfx.set_volume(0.15)
        sound_enabled = True
    except pygame.error:
        sound_enabled = False

    def play_sound(sfx):
        if sound_enabled:
            try:
                channel = pygame.mixer.find_channel(True) 
                channel.play(sfx)
            except pygame.error:
                pass

    background = [255, 255, 255]
    obstacles = []
    speed = 0

    SPAWN_CACTUS_EVENT = pygame.USEREVENT + 1
    ANIMATION_EVENT = pygame.USEREVENT + 2
    BIRD_ANIM_EVENT = pygame.USEREVENT + 3
    STAR_SPAWN_EVENT = pygame.USEREVENT + 4
    pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000)
    pygame.time.set_timer(ANIMATION_EVENT, 100)
    pygame.time.set_timer(BIRD_ANIM_EVENT, 150)
    pygame.time.set_timer(STAR_SPAWN_EVENT, 700)

    BIRD_HEIGHTS = [180, 158, 175]

    moon_cycle_index = 0
    moon_phase = 0
    moon_x = float(screen_width // 2)
    moon_y = random.randint(10, 50)

    cloud_objects = []

    def spawn_initial_clouds():
        for _ in range(3):
            cloud_objects.append([
                float(random.randint(100, 900)),
                float(random.randint(10, 60)),
                random.uniform(0.3, 0.6),
            ])

    spawn_initial_clouds()

    star_type_counter = 0
    star_objects = []

    def draw_background_elements(surf):
        for cloud in cloud_objects:
            surf.blit(img_cloud,(int(cloud[0]),int(cloud[1])))
        if is_night:
            surf.blit(moon_imgs[moon_phase],(int(moon_x),int(moon_y)))
            for star in star_objects:
                surf.blit(star_imgs[star[2]],(int(star[0]),int(star[1])))

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
    over_font = pygame.font.SysFont(None, 26)

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

        if is_night and numpy_installed:
            img_standing = invert_surface(img_standing)
            img_run1 = invert_surface(img_run1)
            img_run2 = invert_surface(img_run2)
            img_dead = invert_surface(img_dead)
            img_duck1 = invert_surface(img_duck1)
            img_duck2 = invert_surface(img_duck2)
            img_bird1 = invert_surface(img_bird1)
            img_bird2 = invert_surface(img_bird2)
            small_cacti = make_small_cacti()
            large_cacti = make_large_cacti()
            ground_scaled = invert_surface(ground_scaled)
            font_imgs[:] = [invert_surface(crop_sprite(1295 + i * 20, 3, 19, 21, scale=12/21)) for i in range(10)]
            is_night = False
            background = [255, 255, 255]
            star_objects.clear()
            cloud_objects.clear()
            spawn_initial_clouds()

        pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000)
        pygame.time.set_timer(ANIMATION_EVENT, 100)
        pygame.time.set_timer(BIRD_ANIM_EVENT, 150)
        pygame.time.set_timer(STAR_SPAWN_EVENT, 700)

        start_ticks = pygame.time.get_ticks()
        running = True
        game_started = False
        first_jump_made = False
        difficulty = 0
        curtain_x = 0
        bird_frame = 0
        ground_x1 = 0
        ground_x2 = ground_width
        last_switch = 0

        if not is_first_play:
            game_started = True
            speed = 4
            current_image = img_run1

        while running:
            score_time = 0
            if game_started:
                score_time = (pygame.time.get_ticks() - start_ticks) // 100
                difficulty = min(100, score_time / 5)

            if score_time % 300 == 0 and last_switch != score_time and score_time != 0:
                if numpy_installed:
                    img_standing = invert_surface(img_standing)
                    img_run1 = invert_surface(img_run1)
                    img_run2 = invert_surface(img_run2)
                    img_dead = invert_surface(img_dead)
                    img_duck1 = invert_surface(img_duck1)
                    img_duck2 = invert_surface(img_duck2)
                    img_bird1 = invert_surface(img_bird1)
                    img_bird2 = invert_surface(img_bird2)
                    hi_img = invert_surface(hi_img)
                    if is_night:
                        small_cacti = make_small_cacti()
                        large_cacti = make_large_cacti()
                    else:
                        small_cacti = [invert_surface(c) for c in make_small_cacti()]
                        large_cacti = [invert_surface(c) for c in make_large_cacti()]
                    ground_scaled = invert_surface(ground_scaled)
                    font_imgs[:] = [invert_surface(crop_sprite(1295 + i * 20, 3, 19, 21, scale=12/21)) for i in range(10)]
                    last_switch = score_time
                    is_night = not is_night

                    if is_night:
                        moon_phase = moon_cycle_index % 7
                        moon_cycle_index += 1
                        moon_x = float(screen_width // 2)
                        moon_y = random.randint(10, 50)
                        star_objects.clear()
                        star_type_counter = 0
                    else:
                        star_objects.clear()
                        hi_img = hi_img = crop_sprite(1495, 3, 42, 21, scale=24/42)

            if is_night and numpy_installed:
                for i in range(3):
                    if background[i] > 0:
                        background[i] -= 1
            else:
                if not is_night:
                    font_imgs[:] = [crop_sprite(1295 + i * 20, 3, 19, 21, scale=12/21) for i in range(10)]
                for i in range(3):
                    if background[i] < 250:
                        background[i] += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    if score_time > high_score:
                        return score_time
                    else:
                        return high_score

                elif event.type == SPAWN_CACTUS_EVENT:
                    if game_started:
                        spawn_cactus_group()

                elif event.type==STAR_SPAWN_EVENT:
                    if is_night and game_started and len(star_objects)<10:
                        star_objects.append([
                            float(screen_width+10),
                            float(random.randint(5,70)),
                            star_type_counter%3,
                        ])
                        star_type_counter+=1

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if is_first_play and not game_started and not first_jump_made and player.y >= ground_y:
                            velocity_y = -10.5
                            play_sound(jump_sfx)
                            first_jump_made = True
                            current_image = img_standing
                            ground_y = 225 - DINO_H
                        elif game_started and player.y >= ground_y:
                            velocity_y = -10.5
                            play_sound(jump_sfx)
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

            player.y += velocity_y
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
                    play_sound(point_sfx)

                if speed < 13:
                    speed += 0.005

                ground_x1 -= speed
                ground_x2 -= speed
                if ground_x1 + ground_width < 0:
                    ground_x1 = ground_x2 + ground_width
                if ground_x2 + ground_width < 0:
                    ground_x2 = ground_x1 + ground_width

                if is_night:
                    moon_x -= speed * 0.1
                    mw = moon_imgs[moon_phase].get_width()
                    if moon_x + mw < 0:
                        moon_x = float(screen_width - mw)
                    for star in star_objects:
                        star[0]-=speed*0.4
                        if random.random()<0.03:
                            star[2]=(star[2]+1)%3
                    star_objects[:]=[s for s in star_objects if s[0]>-50]

                for cloud in cloud_objects:
                    cloud[0]-=speed*cloud[2]
                cloud_objects[:]=[c for c in cloud_objects if c[0]+img_cloud.get_width()>0]
                if random.random()<0.008:
                    cloud_objects.append([
                        float(screen_width+10),
                        float(random.randint(10,60)),
                        random.uniform(0.3,0.6),
                    ])

                for obs in obstacles[:]:
                    obs['rect'].x -= speed
                    if obs['rect'].x + obs['rect'].width < 0:
                        obstacles.remove(obs)
                        continue

                    if player.colliderect(obs['rect']):
                        is_first_play = False

                        restart_rect = pygame.Rect(
                            screen_width // 2 - BTN_W // 2,
                            screen_height // 2 - BTN_H // 2 + 30,
                            BTN_W, BTN_H,
                        )
                        quit_rect = pygame.Rect(10, screen_height - 38, 70, 28)

                        hover_progress = 0.0
                        last_hover_t = pygame.time.get_ticks()
                        HOVER_SPEED = 30.0

                        dead = True
                        play_sound(die_sfx)
                        while dead:
                            now = pygame.time.get_ticks()
                            dt = (now - last_hover_t) / 1000.0
                            last_hover_t = now

                            mx, my = pygame.mouse.get_pos()
                            hovering = restart_rect.collidepoint(mx, my)

                            if hovering:
                                hover_progress = min(5.0, hover_progress + HOVER_SPEED * dt)
                            else:
                                hover_progress = max(0.0, hover_progress - HOVER_SPEED * dt)
                            btn_frame = int(hover_progress)

                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    if score_time > high_score:
                                        return score_time
                                    else:
                                        return high_score
                                if e.type == BIRD_ANIM_EVENT:
                                    bird_frame = 1 - bird_frame
                                if e.type == pygame.MOUSEBUTTONDOWN:
                                    if restart_rect.collidepoint(mx, my):
                                        dead = False
                                    if quit_rect.collidepoint(mx, my):
                                        pygame.quit()
                                        if score_time > high_score:
                                            return score_time
                                        else:
                                            return high_score

                            screen.fill(background)
                            draw_background_elements(screen)
                            screen.blit(ground_scaled, (ground_x1, 207))
                            screen.blit(ground_scaled, (ground_x2, 207))

                            screen.blit(img_dead, player.topleft)

                            for o in obstacles:
                                if o['is_bird']:
                                    screen.blit(img_bird1 if bird_frame == 0 else img_bird2, o['rect'].topleft)
                                else:
                                    screen.blit(o['image'], o['rect'].topleft)

                            screen.blit(hi_img, (820, 15))
                            draw_score(screen, high_score, 848, 15)
                            draw_score(screen, score_time, 930, 15)

                            go_txt = over_font.render("GAME OVER", True, (83, 83, 83))
                            sub_txt = over_font.render("click to restart", True, (150, 150, 150))
                            screen.blit(go_txt, (screen_width // 2 - go_txt.get_width() // 2, restart_rect.y - 38))
                            screen.blit(sub_txt, (screen_width // 2 - sub_txt.get_width() // 2, restart_rect.y - 18))

                            screen.blit(restart_frames[btn_frame], restart_rect.topleft)

                            quit_surf = ui_font.render("QUIT", True, (0, 0, 0))
                            pygame.draw.rect(screen, (200, 200, 200), quit_rect)
                            screen.blit(quit_surf, (quit_rect.x + 8, quit_rect.y + 5))

                            pygame.display.flip()
                            clock.tick(60)

                        running = False

            screen.fill(background)
            draw_background_elements(screen)
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
                    line2 = instr_font.render("DOWN  -  Duck", True, (83, 83, 83))
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