import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pygame
import math
import random


pygame.init()

pygame.mixer.init()

import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SFX = {
    "cannon":    pygame.mixer.Sound(os.path.join(BASE_PATH, "cannon_fire.mp3")),
    "thud":      pygame.mixer.Sound(os.path.join(BASE_PATH, "ball_thud.mp3")),
    "wall":      pygame.mixer.Sound(os.path.join(BASE_PATH, "ball_hits_wall.mp3")),
    "block_hit": pygame.mixer.Sound(os.path.join(BASE_PATH, "block_breaking.mp3")),
    "shatter":   pygame.mixer.Sound(os.path.join(BASE_PATH, "clay_shatter.mp3")),
    "splash":    pygame.mixer.Sound(os.path.join(BASE_PATH, "splash.mp3")),
    "click":     pygame.mixer.Sound(os.path.join(BASE_PATH, "click_sound.mp3")),
    "escape":    pygame.mixer.Sound(os.path.join(BASE_PATH, "escape.ogg")),
    "menu": pygame.mixer.Sound(os.path.join(BASE_PATH, "menu.ogg"))
}



def load_img(path):
    return pygame.image.load(os.path.join(BASE_PATH, path)).convert_alpha()

def load_bg(path):
    return pygame.image.load(os.path.join(BASE_PATH, path)).convert()

# Create screen FIRST
info = pygame.display.Info()
SCREEN_WIDTH  = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Physics Simulator")



# ── Load Assets ─────────────────────────────
BALL_IMAGES = {
    "Iron": load_img("assets/balls/iron_ball.png"),
    "Wood": load_img("assets/balls/wood_ball.png"),
    "Rubber": load_img("assets/balls/rubber_ball.png"),
    "Plastic": load_img("assets/balls/plastic_ball.png"),
    "Clay": load_img("assets/balls/clay_ball.png"),
}

CLAY_CRACKED_IMG = load_img("assets/balls/clay_ballcracked.png")

BG_IMAGES = {
    "Earth": load_bg("assets/bg/bg_earth.png"),
    "Moon": load_bg("assets/bg/bg_moon.png"),
    "Jupiter": load_bg("assets/bg/bg_jupiter.png"),
    "Pluto": load_bg("assets/bg/bg_pluto.png"),
    "Sun": load_bg("assets/bg/bg_sun.png"),
}

BRICK_IMAGES = {
    "Weak": load_img("assets/bricks/brick.png"),
    "Strong": load_img("assets/bricks/strong.png"),
    "VeryStrong": load_img("assets/bricks/strongest.png"),
}

CRACK_IMAGES = {
    "Weak": load_img("assets/bricks/brick_crack.png"),
    "Strong": load_img("assets/bricks/strong_crack.png"),
    "VeryStrong": load_img("assets/bricks/strongest_crack.png"),
}

SHATTER_IMAGES = {
    "Weak": load_img("assets/bricks/brick_shatter.png"),
    "Strong": load_img("assets/bricks/strong_shatter.png"),
    "VeryStrong": load_img("assets/bricks/strongest_shatter.png"),
}

CANNON_IMG = load_img("assets/cannon/cannon.png")
GROUND_IMG = load_img("assets/ground/ground.png")

LIQUID_IMAGES = {
    "Water": load_img("assets/liquid/water.png"),
    "Oil": load_img("assets/liquid/oil.png"),
    "Glycerine": load_img("assets/liquid/glycerine.png"),
    "Alcohol": load_img("assets/liquid/alcohol.png"),
}

MENU_BG = load_bg("assets/bg/menu_screen.png")

# Fullscreen detection
info = pygame.display.Info()
SCREEN_WIDTH  = info.current_w
SCREEN_HEIGHT = info.current_h

#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Physics Simulator")


SX = SCREEN_WIDTH  / 1200
SY = SCREEN_HEIGHT / 600

def sx(v): return int(v * SX)
def sy(v): return int(v * SY)
def sv(v): return int(v * (SX + SY) / 2)   

clock = pygame.time.Clock()
FPS = 60

# Colours
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
SKY_BLUE   = (135, 206, 235)
GROUND_COL = ( 34, 139,  34)
DARK_GRAY  = ( 50,  50,  50)
PANEL_COL  = ( 20,  20,  40)

#  Block Types 
BLOCK_TYPES = {
    "Weak":       {"health": 30,  "color": (210, 180, 140)},
    "Strong":     {"health": 60,  "color": (160,  82,  45)},
    "VeryStrong": {"health": 100, "color": ( 90,  50,  30)},
}

# Gravity 
GRAVITY_OPTIONS = {
    "Earth":   9.8,
    "Moon":    1.62,
    "Jupiter": 24.8,
    "Sun":     274.0,
    "Pluto":   0.62,
}
current_planet = "Earth"

#  Ball Types 
BALL_TYPES = {
    "Iron":    {"mass": 5, "bounce": 0.3, "drag": 0.002, "damage": 12, "shatter": False, "color": (120, 120, 120)},
    "Wood":    {"mass":  5, "bounce": 0.5, "drag": 0.005, "damage":  6, "shatter": False, "color": (139,  69,  19)},
    "Rubber":  {"mass":  5, "bounce": 0.9, "drag": 0.007, "damage":  4, "shatter": False, "color": (255,   0,   0)},
    "Plastic": {"mass":  5, "bounce": 0.6, "drag": 0.010, "damage":  3, "shatter": False, "color": (240, 240, 120)},
    "Clay":    {"mass":  5, "bounce": 0.2, "drag": 0.004, "damage": 10, "shatter": True,  "color": (210, 140,  90)},
}
current_ball = "Iron"

BALL_DENSITY = {
    "Iron": 7.8,
    "Wood": 0.7,
    "Rubber": 1.1,
    "Plastic": 0.9,
    "Clay": 1.9,
}
#  Liquid Types 
LIQUIDS = {
    "Water":     {"density": 1.0, "drag": 0.02, "color": (  0, 120, 255)},
    "Oil":       {"density": 0.8, "drag": 0.03, "color": (200, 180,  50)},
    "Glycerine": {"density": 1.3, "drag": 0.06, "color": (180, 220, 255)},
    "Alcohol":   {"density": 0.7, "drag": 0.015,"color": (180, 255, 255)},
    #"Mercury":   {"density": 13.6, "drag": 0.05,  "color": (180, 180, 195)},
}
current_liquid = "Water"

ball_trail = []

def get_g():
    return GRAVITY_OPTIONS[current_planet]

def get_ball_color():   return BALL_TYPES[current_ball]["color"]
def get_ball_bounce():  return BALL_TYPES[current_ball]["bounce"]
def get_ball_mass():    return BALL_TYPES[current_ball]["mass"]

#  Launch speed 
launch_speed_kmh = 60

def kmh_to_pixels(kmh):
    return kmh * 0.2 * (SX + SY) / 2   # scale speed with screen size

#  Layout constants 
CANNON_X  = sx(80)
CANNON_Y  = sy(380) 
GROUND_Y  = sy(540)
TOPBAR_H  = sy(44)
SIDEBAR_X = sx(1000)


POOL_X      = sx(300)
POOL_Y      = sy(360)                        # higher up = taller pool
POOL_WIDTH  = SIDEBAR_X - sx(300) - sx(10)  # stretches to near sidebar
POOL_HEIGHT = GROUND_Y - POOL_Y             # fills from POOL_Y down to ground

ball_r = sv(18)


#   Block class  
class Block:
    def __init__(self, x, y, strength):
        self.x = x
        self.y = y
        self.type = strength
        self.health = BLOCK_TYPES[strength]["health"]
        self.color  = BLOCK_TYPES[strength]["color"]

        img = BRICK_IMAGES[self.type]
        self.w = img.get_width()
        self.h = img.get_height()

    def draw(self, surface):
        ratio = self.health / BLOCK_TYPES[self.type]["health"]

        if ratio > 0.6:
            img = BRICK_IMAGES[self.type]
        elif ratio > 0.3:
            img = CRACK_IMAGES[self.type]
        else:
            img = SHATTER_IMAGES[self.type]

        img = pygame.transform.scale(img, (self.w, self.h))
        surface.blit(img, (self.x, self.y))


#  Ball state 
ball_x   = float(CANNON_X)
ball_y   = float(CANNON_Y)
ball_vx  = 0.0
ball_vy  = 0.0
launched = False
particles = []
was_in_liquid = False
clay_cracked = False

# Blocks 
blocks = []

def spawn_blocks():
    heights = [sy(h) for h in [300, 250, 200, 150]]
    while len(blocks) < 2:
        strength  = random.choice(["Weak", "Strong", "VeryStrong"])
        x = random.randint(sx(300), sx(850))
        y = random.choice(heights)
        new_block = Block(x, y, strength)
        overlap = False
        for b in blocks:
            if abs(new_block.x - b.x) < sx(70) and abs(new_block.y - b.y) < sy(50):
                overlap = True
                break
        if not overlap:
            blocks.append(new_block)

spawn_blocks()

#  Trajectory preview 
def get_preview_dots(cx, cy, vx, vy, steps=40, skip=3):
    dots = []
    px, py = cx, cy
    pvx, pvy = vx, vy
    for i in range(steps * skip):
        pvy += get_g() * (1/60)
        px  += pvx
        py  += pvy
        if py > GROUND_Y:
            break
        if i % skip == 0:
            dots.append((int(px), int(py)))
    return dots

def draw_menu(mouse_x, mouse_y):
    # Draw the starfield background image
    bg_scaled = pygame.transform.scale(MENU_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg_scaled, (0, 0))

    font_title = pygame.font.Font(os.path.join(BASE_PATH, "PressStart2P-Regular.ttf"), sv(28))
    font_sub   = pygame.font.Font(os.path.join(BASE_PATH, "PressStart2P-Regular.ttf"), sv(14))
    font_small = pygame.font.Font(os.path.join(BASE_PATH, "PressStart2P-Regular.ttf"), sv(9))

    # ── Two buttons on the LEFT side ──────────────────────────
    btn_w, btn_h = sx(260), sy(55)
    btn_x = sx(80)

    # Button 1 — PLAY (green)
    btn1_y = sy(320)
    hover1 = btn_x < mouse_x < btn_x + btn_w and btn1_y < mouse_y < btn1_y + btn_h
    btn1_color = (80, 220, 120) if hover1 else (40, 140, 70)
    pygame.draw.rect(screen, btn1_color, (btn_x, btn1_y, btn_w, btn_h), border_radius=10)
    pygame.draw.rect(screen, (150, 255, 180), (btn_x, btn1_y, btn_w, btn_h), 2, border_radius=10)
    lbl1 = font_sub.render("PLAY", True, WHITE)
    screen.blit(lbl1, (btn_x + btn_w // 2 - lbl1.get_width() // 2,
                        btn1_y + btn_h // 2 - lbl1.get_height() // 2))

    # Button 2 — PLAY (no buoyancy) (blue)
    btn2_y = sy(395)
    hover2 = btn_x < mouse_x < btn_x + btn_w and btn2_y < mouse_y < btn2_y + btn_h
    btn2_color = (60, 160, 230) if hover2 else (30, 90, 160)
    pygame.draw.rect(screen, btn2_color, (btn_x, btn2_y, btn_w, btn_h), border_radius=10)
    pygame.draw.rect(screen, (120, 200, 255), (btn_x, btn2_y, btn_w, btn_h), 2, border_radius=10)
    lbl2 = font_sub.render("PLAY (no liquid)", True, WHITE)
    screen.blit(lbl2, (btn_x + btn_w // 2 - lbl2.get_width() // 2,
                        btn2_y + btn_h // 2 - lbl2.get_height() // 2))

    pygame.display.flip()
    return (btn_x, btn1_y, btn_w, btn_h)

#  Draw 
def draw_scene(mouse_x, mouse_y):
    global CANNON_Y
    CANNON_Y = sy(480) if not liquid_mode else sy(380)  # lower in no-liquid mode
    bg = pygame.transform.scale(BG_IMAGES[current_planet], (SIDEBAR_X, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))

    # Ground
    ground_img = pygame.transform.scale(GROUND_IMG, (SIDEBAR_X, SCREEN_HEIGHT - GROUND_Y))
    screen.blit(ground_img, (0, GROUND_Y))

    # NEW
    if liquid_mode:
        LIQUID_VISUAL_OFFSET = sy(140)
        liquid_img = pygame.transform.scale(
            LIQUID_IMAGES[current_liquid],
            (POOL_WIDTH, POOL_HEIGHT + LIQUID_VISUAL_OFFSET)
        )
        screen.blit(liquid_img, (POOL_X, POOL_Y - LIQUID_VISUAL_OFFSET))
    

    # Cannon body
    # Cannon rotation
    # Cannon rotation
    angle_rad = math.atan2(mouse_y - CANNON_Y, mouse_x - CANNON_X)
    angle_deg = -math.degrees(angle_rad)

    cannon_scaled = pygame.transform.scale(CANNON_IMG, (sx(80), sy(80)))
    cannon_rot = pygame.transform.rotate(cannon_scaled, angle_deg)
    rect = cannon_rot.get_rect(center=(CANNON_X, CANNON_Y))
    screen.blit(cannon_rot, rect.topleft)

    # Barrel aimed at mouse
    angle_rad = math.atan2(mouse_y - CANNON_Y, mouse_x - CANNON_X)
    bx = CANNON_X + math.cos(angle_rad) * sx(50)
    by = CANNON_Y + math.sin(angle_rad) * sy(50)
    pygame.draw.line(screen, (30, 30, 30),
                     (CANNON_X, CANNON_Y), (int(bx), int(by)), sv(12))

    font_sm = pygame.font.SysFont("Courier New", sv(18))
    font_md = pygame.font.SysFont("Courier New", sv(22), bold=True)
    font_tiny = pygame.font.SysFont("Courier New", sv(13))
    


    if not launched:
        speed_px = kmh_to_pixels(launch_speed_kmh)
        pvx = math.cos(angle_rad) * speed_px
        pvy = math.sin(angle_rad) * speed_px

        for dx, dy in get_preview_dots(CANNON_X, CANNON_Y, pvx, pvy):
            pygame.draw.circle(screen, (80, 80, 150), (dx, dy), sv(4))

        ball_img = CLAY_CRACKED_IMG if (current_ball == "Clay" and clay_cracked) else BALL_IMAGES[current_ball]
        screen.blit(ball_img, (int(ball_x - ball_r), int(ball_y - ball_r)))
    else:
        for i, pos in enumerate(ball_trail):
            alpha = max(80, 255 - (len(ball_trail) - i) * 3)  # fades toward the start
            radius = max(1, sv(3))
            pygame.draw.circle(screen, (255, 180, 50), pos, radius)
        ball_img = CLAY_CRACKED_IMG if (current_ball == "Clay" and clay_cracked) else BALL_IMAGES[current_ball]
        screen.blit(ball_img, (int(ball_x - ball_r), int(ball_y - ball_r)))

    # Top bar 
    pygame.draw.rect(screen, PANEL_COL, (0, 0, SCREEN_WIDTH, TOPBAR_H))
    planets = list(GRAVITY_OPTIONS.keys())
    gravity_label = font_sm.render("Gravity:", True, (150, 200, 255))
    screen.blit(gravity_label, (sx(10), sy(11)))
    
    offset_x = sx(10) + gravity_label.get_width() + sx(10)
    for planet, g in GRAVITY_OPTIONS.items():
        col = (80, 200, 120) if planet == current_planet else (160, 160, 160)
        lbl = font_sm.render(f"{planet} {g}", True, col)
        screen.blit(lbl, (offset_x, sy(11)))
        offset_x += lbl.get_width() + sx(20)

    spd_lbl  = font_md.render(f"Speed: {launch_speed_kmh} km/h", True,WHITE) #(57,175,100))
    ball_lbl = font_md.render(f"Ball: {current_ball}", True,WHITE) #(57,175,100))
    liquid_lbl = font_md.render(f"Liquid: {current_liquid}", True,WHITE) #(57, 175, 100))
    vacuum_lbl  = font_tiny.render("* Trajectory assumes vacuum conditions", True, (128, 0, 128))

    screen.blit(spd_lbl,   (sx(10), sy(50)))
    screen.blit(ball_lbl,  (sx(10), sy(80)))
    screen.blit(liquid_lbl,(sx(10), sy(110)))
    screen.blit(vacuum_lbl, (sx(10), sy(140)))
    #screen.blit(spd_lbl,  (sx(10), sy(50)))
    #screen.blit(ball_lbl, (sx(10), sy(80)))

    #  Sidebar 
    pygame.draw.rect(screen, (15, 15, 35),
                     (SIDEBAR_X, 0, SCREEN_WIDTH - SIDEBAR_X, SCREEN_HEIGHT))
    pygame.draw.line(screen, (60, 60, 80),
                     (SIDEBAR_X, 0), (SIDEBAR_X, SCREEN_HEIGHT), 2)

    stats = [
    ("Planet", current_planet),
    ("Ball", f"{current_ball} ({BALL_DENSITY[current_ball]})"),
    ("Weight", f"{get_ball_mass() * get_g():.1f} N"),
    ("Liquid", f"{current_liquid} ({LIQUIDS[current_liquid]['density']})"),
    ("Gravity", f"{get_g()} m/s²"),
    ("Speed", f"{launch_speed_kmh} km/h"),
    ("vx", f"{ball_vx:.1f}"),
    ("vy", f"{ball_vy:.1f}"),
    ("x", f"{ball_x:.0f}"),
    ("y", f"{ball_y:.0f}"),
    ("Launched", str(launched)),
    ]
    sy_pos = sy(16)
    title = font_md.render("Live Stats", True, (150, 200, 255))
    screen.blit(title, (SIDEBAR_X + sx(10), sy_pos)); sy_pos += sy(30)
    for key, val in stats:
        screen.blit(font_sm.render(key, True, (140, 140, 160)), (SIDEBAR_X + sx(10), sy_pos))
        screen.blit(font_sm.render(val, True, WHITE),            (SIDEBAR_X + sx(10), sy_pos + sy(18)))
        sy_pos += sy(44)

    # Bottom panel 
    panel_top = GROUND_Y
    panel_height = SCREEN_HEIGHT - GROUND_Y
    panel_center_y = panel_top + panel_height // 2
    font_small = pygame.font.SysFont("Courier New", sv(16))
    font_bold  = pygame.font.SysFont("Courier New", sv(18), bold=True)

    #  Bottom panel centered text 
    font_small = pygame.font.SysFont("Courier New", sv(16))
    font_bold  = pygame.font.SysFont("Courier New", sv(18), bold=True)

    panel_top = GROUND_Y
    panel_height = SCREEN_HEIGHT - GROUND_Y
    panel_center_y = panel_top + panel_height // 2

    col_w = SIDEBAR_X // 6

    panel_surf = pygame.Surface((SIDEBAR_X, panel_height), pygame.SRCALPHA)
    panel_surf.fill((250, 250, 250, 140))
    screen.blit(panel_surf, (0, panel_top))
    pygame.draw.line(screen, (180, 180, 180), (0, panel_top), (SIDEBAR_X, panel_top), 2)

    controls = [
        ("Click", "Fire"),
        ("B", "Choose Ball"),
        ("L", "Choose Liquid"),
        ("1–5", "Choose Planet"),
        ("↑ ↓", "Set Speed"),
        ("M", "Menu")
    ]

    for i, (key, action) in enumerate(controls):
        x_center = i * col_w + col_w // 2

        key_text = font_bold.render(key, True, BLACK)
        act_text = font_small.render(action, True, BLACK)

        total_height = key_text.get_height() + act_text.get_height()
        start_y = panel_center_y - total_height // 2

        screen.blit(key_text, (x_center - key_text.get_width() // 2, start_y))
        screen.blit(act_text, (x_center - act_text.get_width() // 2, start_y + key_text.get_height()))

        # vertical separators full height
        if i != 0:
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (i * col_w, panel_top),
                (i * col_w, SCREEN_HEIGHT),
                1
            )

    for block in blocks:
        block.draw(screen)

    for p in particles:
        size = sv(6)
        pygame.draw.rect(screen, (255, 250, 200), (int(p["x"]), int(p["y"]), size, size))


    pygame.display.flip()

#  Reset 
def reset_ball():
    #global ball_x, ball_y, ball_vx, ball_vy, launched, clay_cracked, ball_trail
    global ball_x, ball_y, ball_vx, ball_vy, launched, clay_cracked, ball_trail, CANNON_Y
    CANNON_Y = sy(480) if not liquid_mode else sy(380)
    ball_x   = float(CANNON_X)
    ball_x   = float(CANNON_X)
    ball_y   = float(CANNON_Y)
    ball_vx  = 0.0
    ball_vy  = 0.0
    launched = False
    clay_cracked = False
    ball_trail = []

def handle_keys(key):
    global current_ball, current_liquid, current_planet, launch_speed_kmh, running, game_state

    if key == pygame.K_ESCAPE:
        running = False
        return  

    SFX["click"].play()

    if key == pygame.K_ESCAPE: 
        SFX["escape"].play()
        pygame.time.delay(1000)
        running = False
    if key == pygame.K_r:      reset_ball()
    if key == pygame.K_m:
        game_state = "menu"
        reset_ball()

    if key == pygame.K_1: current_planet = "Earth"
    if key == pygame.K_2: current_planet = "Moon"
    if key == pygame.K_3: current_planet = "Jupiter"
    if key == pygame.K_4: current_planet = "Sun"
    if key == pygame.K_5: current_planet = "Pluto"

    if key == pygame.K_UP:   launch_speed_kmh = min(100, launch_speed_kmh + 5)
    if key == pygame.K_DOWN: launch_speed_kmh = max(1,   launch_speed_kmh - 5)

    if key == pygame.K_b:
        ball_list = list(BALL_TYPES.keys())
        current_ball = ball_list[(ball_list.index(current_ball) + 1) % len(ball_list)]

    if key == pygame.K_l:
        liquid_list = list(LIQUIDS.keys())
        current_liquid = liquid_list[(liquid_list.index(current_liquid) + 1) % len(liquid_list)]

game_state = "menu"
prev_game_state = None
liquid_mode = True
#  Game loop 
running = True
while running:
    clock.tick(FPS)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_x = sx(90)
                btn_w, btn_h = sx(260), sy(55)

                btn1_y = sy(320)
                if btn_x < mouse_x < btn_x + btn_w and btn1_y < mouse_y < btn1_y + btn_h:
                    SFX["click"].play()
                    liquid_mode = True
                    game_state = "play"

                btn2_y = sy(395)
                if btn_x < mouse_x < btn_x + btn_w and btn2_y < mouse_y < btn2_y + btn_h:
                    SFX["click"].play()
                    liquid_mode = False
                    game_state = "play"

        elif game_state == "play":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not launched and not clay_cracked:
                    SFX["cannon"].play()
                    speed_px = kmh_to_pixels(launch_speed_kmh)
                    angle    = math.atan2(mouse_y - CANNON_Y, mouse_x - CANNON_X)
                    ball_vx  = math.cos(angle) * speed_px
                    ball_vy  = math.sin(angle) * speed_px
                    ball_x   = float(CANNON_X)
                    ball_y   = float(CANNON_Y)
                    launched = True

            if event.type == pygame.KEYDOWN:
                handle_keys(event.key)

    #if game_state == "menu":
        #draw_menu(mouse_x, mouse_y)

    if game_state == "menu":
        if prev_game_state != "menu":
            SFX["menu"].play()
        draw_menu(mouse_x, mouse_y)

    elif game_state == "play":

        # ── Physics ───────────────────────────────────────────────
        if launched or clay_cracked:
            drag = BALL_TYPES[current_ball]["drag"]
            ball_vx *= (1 - drag)
            ball_vy *= (1 - drag)

            ball_bottom = ball_y + ball_r
            if liquid_mode:
                in_liquid = (POOL_X < ball_x < POOL_X + POOL_WIDTH and
                            POOL_Y < ball_bottom < POOL_Y + POOL_HEIGHT)
            else:
                in_liquid = False

            if in_liquid and not was_in_liquid:
                SFX["splash"].play()
                # Spawn 8 splash particles on entry
                for _ in range(8):
                    particles.append({
                        "x": ball_x + random.randint(-ball_r, ball_r),
                        "y": POOL_Y,
                        "vx": random.uniform(-1.5, 1.5),
                        "vy": random.uniform(-3, -1.5),
                        "life": 20
                    })
            was_in_liquid = in_liquid
            
            if in_liquid:
                liquid = LIQUIDS[current_liquid]
                ball_vx *= (1 - liquid["drag"])
                ball_vy *= (1 - liquid["drag"])
                ball_density = BALL_DENSITY[current_ball]
                net_accel = get_g() * (ball_density - liquid["density"]) / ball_density
                ball_vy += net_accel * (1/60)
            else:
                ball_vy += get_g() * (1/60)

            ball_x += ball_vx
            ball_y += ball_vy

            if launched:
                ball_trail.append((int(ball_x), int(ball_y)))

            for p in particles:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.2  # gravity
                p["life"] -= 1
            particles[:] = [p for p in particles if p["life"] > 0]

            if not clay_cracked:
                PAD = 16  
                for block in blocks:
                    if (ball_x + ball_r > block.x + PAD and
                        ball_x - ball_r < block.x + block.w - PAD and
                        ball_y + ball_r > block.y + PAD and
                        ball_y - ball_r < block.y + block.h - PAD):
                        speed  = math.sqrt(ball_vx**2 + ball_vy**2)
                        block.health -= get_ball_mass() * speed
                        if BALL_TYPES[current_ball]["shatter"]:
                            SFX["shatter"].play()
                            clay_cracked = True
                            ball_vx = 0.0
                            ball_vy = 0.0
                        else:
                            SFX["block_hit"].play()
                            e = get_ball_bounce()
                            if ball_x < block.x or ball_x > block.x + block.w:
                                ball_vx *= -e
                            else:
                                ball_vy *= -e

            blocks[:] = [b for b in blocks if b.health > 0]
            if len(blocks) < 2:
                spawn_blocks()

            if ball_y >= GROUND_Y - ball_r:
                ball_y = float(GROUND_Y - ball_r)
                if BALL_TYPES[current_ball]["shatter"]:
                    SFX["shatter"].play()
                    clay_cracked = True
                    ball_vx = 0.0
                    ball_vy = 0.0
                else:
                    if abs(ball_vy) > 0.8:      
                        SFX["thud"].play()
                    ball_vy = -ball_vy * get_ball_bounce()
                    ball_vx *= 0.85
                if abs(ball_vy) < 0.8:
                    ball_vy = 0.0

            if ball_x <= ball_r:
                ball_x  = float(ball_r)
                ball_vx = -ball_vx * 0.6
                SFX["wall"].play()
            if ball_x >= SIDEBAR_X - ball_r:
                ball_x  = float(SIDEBAR_X - ball_r)
                ball_vx = -ball_vx * 0.6
                SFX["wall"].play()

        draw_scene(mouse_x, mouse_y)
    prev_game_state = game_state
pygame.quit()