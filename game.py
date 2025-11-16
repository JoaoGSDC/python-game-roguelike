"""
Roguelike game using PgZero.
A top-down roguelike with sprite animations, enemies, and sound effects.
"""

import math
import random
from pygame import Rect

# Window configuration (PgZero uses WIDTH, HEIGHT)
WIDTH = 800
HEIGHT = 600

# Grid and sizes
CELL_SIZE = 40
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Directions (constants)
DIRECTION_DOWN = 0
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3

# Image names for sprite animations
# Each direction needs multiple frames that cycle continuously
# This is REAL sprite animation - multiple images changing cyclically
SPRITE_HERO_IDLE_DOWN = [
    "hero_idle_right",
    "hero_idle_right",
    "hero_idle_right",
]
SPRITE_HERO_IDLE_LEFT = [
    "hero_idle_left",
    "hero_idle_left",
    "hero_idle_left",
]
SPRITE_HERO_IDLE_RIGHT = [
    "hero_idle_right",
    "hero_idle_right",
    "hero_idle_right",
]
SPRITE_HERO_IDLE_UP = [
    "hero_idle_right",
    "hero_idle_right",
    "hero_idle_right",
]
SPRITE_HERO_MOVING_DOWN = [
    "hero_move_1",
    "hero_move_2",
    "hero_move_3",
    "hero_move_4",
]
SPRITE_HERO_MOVING_LEFT = [
    "hero_move_left_1",
    "hero_move_left_2",
    "hero_move_left_3",
    "hero_move_left_4",
]
SPRITE_HERO_MOVING_RIGHT = [
    "hero_move_1",
    "hero_move_2",
    "hero_move_3",
    "hero_move_4",
]
SPRITE_HERO_MOVING_UP = [
    "hero_move_1",
    "hero_move_2",
    "hero_move_3",
    "hero_move_4",
]

SPRITE_ENEMY_IDLE_DOWN = [
    "enemy_idle_right",
    "enemy_idle_right",
    "enemy_idle_right",
]
SPRITE_ENEMY_IDLE_LEFT = [
    "enemy_idle_left",
    "enemy_idle_left",
    "enemy_idle_left",
]
SPRITE_ENEMY_IDLE_RIGHT = [
    "enemy_idle_right",
    "enemy_idle_right",
    "enemy_idle_right",
]
SPRITE_ENEMY_IDLE_UP = [
    "enemy_idle_right",
    "enemy_idle_right",
    "enemy_idle_right",
]
SPRITE_ENEMY_MOVING_DOWN = [
    "enemy_move_1",
    "enemy_move_2",
    "enemy_move_3",
    "enemy_move_4",
]
SPRITE_ENEMY_MOVING_LEFT = [
    "enemy_move_left_1",
    "enemy_move_left_2",
    "enemy_move_left_3",
    "enemy_move_left_4",
]
SPRITE_ENEMY_MOVING_RIGHT = [
    "enemy_move_1",
    "enemy_move_2",
    "enemy_move_3",
    "enemy_move_4",
]
SPRITE_ENEMY_MOVING_UP = [
    "enemy_move_1",
    "enemy_move_2",
    "enemy_move_3",
    "enemy_move_4",
]

# Game states (constants)
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Global game variables (lowercase per PEP8)
game_state = STATE_MENU
game_grid = []
game_hero = None
game_enemies = []
music_enabled = True
sounds_enabled = True
# Global volume multiplier (0.0 to 1.0). Set to 0.5 to reduce overall sound by half.
GLOBAL_VOLUME = 0.25
# Coin on the map (grid coordinates) or None
game_coin = None


def play_sound(name):
    """Play sound effect safely (doesn't break if missing)."""
    if not sounds_enabled:
        return
    try:
        snd = getattr(sounds, name, None)
        if snd:
            try:
                snd.set_volume(GLOBAL_VOLUME)
            except Exception:
                pass
            snd.play()
    except Exception:
        pass


def play_music(name):
    """Play background music safely."""
    if not music_enabled:
        return
    try:
        try:
            music.set_volume(GLOBAL_VOLUME)
        except Exception:
            pass
        music.play(name)
    except Exception:
        pass


def stop_music():
    """Stop background music safely."""
    try:
        music.stop()
    except Exception:
        pass


class Animation:
    """Handles sprite animation with multiple frames cycling continuously."""

    def __init__(self, frames, speed=0.18):
        self.frames = frames or []
        self.speed = speed
        self.time = 0.0
        self.index = 0

    def update(self, dt):
        """Update animation frame based on elapsed time."""
        if len(self.frames) < 2:
            return
        self.time += dt
        while self.time >= self.speed:
            self.time -= self.speed
            self.index = (self.index + 1) % len(self.frames)

    def current_frame(self):
        """Get current frame image name."""
        if not self.frames:
            return None
        return self.frames[self.index]


class Character:
    """Base class for all game characters."""

    def __init__(
        self,
        grid_x,
        grid_y,
        idle_frames_by_direction,
        moving_frames_by_direction,
        speed=3.0,
    ):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = grid_y * CELL_SIZE + CELL_SIZE // 2
        self.target_x = self.x
        self.target_y = self.y
        self.speed = speed
        self.is_moving = False
        self.direction = DIRECTION_DOWN

        # Create animations for each direction
        # Each direction has its own animation with multiple frames
        self.idle_animations = {
            DIRECTION_DOWN: Animation(
                idle_frames_by_direction[DIRECTION_DOWN], speed=0.4
            ),
            DIRECTION_LEFT: Animation(
                idle_frames_by_direction[DIRECTION_LEFT], speed=0.4
            ),
            DIRECTION_RIGHT: Animation(
                idle_frames_by_direction[DIRECTION_RIGHT], speed=0.4
            ),
            DIRECTION_UP: Animation(idle_frames_by_direction[DIRECTION_UP], speed=0.4),
        }
        self.moving_animations = {
            DIRECTION_DOWN: Animation(
                moving_frames_by_direction[DIRECTION_DOWN], speed=0.12
            ),
            DIRECTION_LEFT: Animation(
                moving_frames_by_direction[DIRECTION_LEFT], speed=0.12
            ),
            DIRECTION_RIGHT: Animation(
                moving_frames_by_direction[DIRECTION_RIGHT], speed=0.12
            ),
            DIRECTION_UP: Animation(
                moving_frames_by_direction[DIRECTION_UP], speed=0.12
            ),
        }

    def move_to_cell(self, new_x, new_y):
        """Move character to a new grid cell."""
        if not self.is_moving:
            self.grid_x = new_x
            self.grid_y = new_y
            self.target_x = new_x * CELL_SIZE + CELL_SIZE // 2
            self.target_y = new_y * CELL_SIZE + CELL_SIZE // 2
            self.is_moving = True

    def update_position(self, dt):
        """Update character position and animation."""
        # Update animation for current direction
        anim_dict = self.moving_animations if self.is_moving else self.idle_animations
        current_anim = anim_dict.get(self.direction)
        if current_anim:
            current_anim.update(dt)

        # Smooth movement interpolation
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.is_moving = False
            return
        if dist <= self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw_on_screen(self):
        """Draw character on screen with sprite animation."""
        # Get current animation for direction
        anim_dict = self.moving_animations if self.is_moving else self.idle_animations
        current_anim = anim_dict.get(self.direction)
        frame_name = None
        if current_anim:
            frame_name = current_anim.current_frame()

        # Try to draw using Actor if image exists
        if frame_name:
            try:
                Actor(frame_name, (self.x, self.y)).draw()
                return
            except Exception:
                pass

        # Fallback: draw simple animated shape
        radius = int(CELL_SIZE / 2.6)
        frame_idx = current_anim.index if current_anim else 0
        # Animate size based on frame (real animation effect)
        size_variation = (frame_idx % 3) * 2
        radius_animated = radius + size_variation
        screen.draw.filled_circle(
            (int(self.x), int(self.y)), radius_animated, (200, 200, 200)
        )
        # Animated eyes
        eye_offset = (frame_idx % 2) * 2 - 1
        screen.draw.filled_circle(
            (int(self.x - 6 + eye_offset), int(self.y - 6)), 3, "white"
        )
        screen.draw.filled_circle(
            (int(self.x + 6 + eye_offset), int(self.y - 6)), 3, "white"
        )


class Hero(Character):
    """Player-controlled hero character."""

    def __init__(self, grid_x, grid_y):
        idle_frames = [
            SPRITE_HERO_IDLE_DOWN,
            SPRITE_HERO_IDLE_LEFT,
            SPRITE_HERO_IDLE_RIGHT,
            SPRITE_HERO_IDLE_UP,
        ]
        moving_frames = [
            SPRITE_HERO_MOVING_DOWN,
            SPRITE_HERO_MOVING_LEFT,
            SPRITE_HERO_MOVING_RIGHT,
            SPRITE_HERO_MOVING_UP,
        ]
        super().__init__(grid_x, grid_y, idle_frames, moving_frames, speed=4.0)
        self.health = 100
        # Collected coins count
        self.coins = 0
        # Damage cooldown timer (seconds). When >0 hero is invulnerable to further hits
        self.damage_timer = 0.0
        # Minimal delay between enemy damages (seconds)
        self.damage_cooldown = 0.45

    def process_input(self, grid):
        """Process player input for movement."""
        if self.is_moving:
            return

        new_x, new_y = self.grid_x, self.grid_y
        if keyboard.up or keyboard.w:
            new_y = max(0, self.grid_y - 1)
            self.direction = DIRECTION_UP
        elif keyboard.down or keyboard.s:
            new_y = min(ROWS - 1, self.grid_y + 1)
            self.direction = DIRECTION_DOWN
        elif keyboard.left or keyboard.a:
            new_x = max(0, self.grid_x - 1)
            self.direction = DIRECTION_LEFT
        elif keyboard.right or keyboard.d:
            new_x = min(COLUMNS - 1, self.grid_x + 1)
            self.direction = DIRECTION_RIGHT

        # Move if position changed and cell is not obstacle
        if (new_x, new_y) != (self.grid_x, self.grid_y) and not grid[new_y][new_x]:
            self.move_to_cell(new_x, new_y)
            play_sound("step")


class Enemy(Character):
    """Enemy character with simple AI."""

    def __init__(self, grid_x, grid_y, radius=3):
        idle_frames = [
            SPRITE_ENEMY_IDLE_DOWN,
            SPRITE_ENEMY_IDLE_LEFT,
            SPRITE_ENEMY_IDLE_RIGHT,
            SPRITE_ENEMY_IDLE_UP,
        ]
        moving_frames = [
            SPRITE_ENEMY_MOVING_DOWN,
            SPRITE_ENEMY_MOVING_LEFT,
            SPRITE_ENEMY_MOVING_RIGHT,
            SPRITE_ENEMY_MOVING_UP,
        ]
        super().__init__(grid_x, grid_y, idle_frames, moving_frames, speed=2.0)
        self.start_position = (grid_x, grid_y)
        self.radius = radius
        self.timer = 0.0

    def update_ai(self, dt, grid, hero):
        """Update enemy AI and movement."""
        self.timer += dt
        # If hero is nearby, try to approach
        distance = abs(self.grid_x - hero.grid_x) + abs(self.grid_y - hero.grid_y)
        if distance <= self.radius and not self.is_moving:
            dx = hero.grid_x - self.grid_x
            dy = hero.grid_y - self.grid_y
            if abs(dx) > abs(dy):
                new_x = self.grid_x + (1 if dx > 0 else -1)
                new_y = self.grid_y
                self.direction = DIRECTION_RIGHT if dx > 0 else DIRECTION_LEFT
            else:
                new_x = self.grid_x
                new_y = self.grid_y + (1 if dy > 0 else -1)
                self.direction = DIRECTION_DOWN if dy > 0 else DIRECTION_UP
            if 0 <= new_x < COLUMNS and 0 <= new_y < ROWS and not grid[new_y][new_x]:
                self.move_to_cell(new_x, new_y)
            return

        # Random patrol within territory
        if self.timer >= 1.0 and not self.is_moving:
            self.timer = 0.0
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = self.grid_x + dx
                new_y = self.grid_y + dy
                dist_from_start = abs(new_x - self.start_position[0]) + abs(
                    new_y - self.start_position[1]
                )
                if (
                    0 <= new_x < COLUMNS
                    and 0 <= new_y < ROWS
                    and not grid[new_y][new_x]
                    and dist_from_start <= self.radius
                ):
                    # Set direction based on movement
                    if dx > 0:
                        self.direction = DIRECTION_RIGHT
                    elif dx < 0:
                        self.direction = DIRECTION_LEFT
                    elif dy > 0:
                        self.direction = DIRECTION_DOWN
                    elif dy < 0:
                        self.direction = DIRECTION_UP
                    self.move_to_cell(new_x, new_y)
                    break


def create_grid():
    """Create game grid with random obstacles."""
    g = [[False for _ in range(COLUMNS)] for _ in range(ROWS)]
    # Create some random obstacles
    for _ in range(25):
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)
        g[y][x] = True
    return g


def spawn_coin(grid, exclude_positions=None):
    """Spawn a coin on a random free cell not in exclude_positions.

    exclude_positions: iterable of (x,y) tuples to avoid (hero/enemies).
    Returns (x,y) or None if no free cell found.
    """
    if exclude_positions is None:
        exclude_positions = set()
    else:
        exclude_positions = set(exclude_positions)

    free_cells = []
    for y in range(ROWS):
        for x in range(COLUMNS):
            if not grid[y][x] and (x, y) not in exclude_positions:
                free_cells.append((x, y))
    if not free_cells:
        return None
    return random.choice(free_cells)


def start_game():
    """Start a new game."""
    global game_state, game_grid, game_hero, game_enemies
    game_state = STATE_PLAYING
    game_grid = create_grid()
    # Create hero in free position
    hero_x, hero_y = 2, 2
    while game_grid[hero_y][hero_x]:
        hero_x = random.randint(0, COLUMNS - 1)
        hero_y = random.randint(0, ROWS - 1)
    game_hero = Hero(hero_x, hero_y)
    # Create enemies
    game_enemies = []
    for _ in range(4):
        enemy_x = random.randint(5, COLUMNS - 1)
        enemy_y = random.randint(5, ROWS - 1)
        while game_grid[enemy_y][enemy_x]:
            enemy_x = random.randint(5, COLUMNS - 1)
            enemy_y = random.randint(5, ROWS - 1)
        game_enemies.append(Enemy(enemy_x, enemy_y, radius=4))
    # Spawn a coin somewhere not occupied by hero or enemies
    global game_coin
    exclude = {(game_hero.grid_x, game_hero.grid_y)}
    for e in game_enemies:
        exclude.add((e.grid_x, e.grid_y))
    game_coin = spawn_coin(game_grid, exclude_positions=exclude)
    # Play music if enabled
    if music_enabled:
        play_music("background")


def update(dt):
    """PgZero update function called each frame."""
    global game_state
    if game_state == STATE_MENU:
        return
    if game_state == STATE_PLAYING:
        # Update hero
        if game_hero:
            # decrement damage timer
            if getattr(game_hero, "damage_timer", 0.0) > 0.0:
                game_hero.damage_timer = max(0.0, game_hero.damage_timer - dt)
            game_hero.process_input(game_grid)
            game_hero.update_position(dt)
            # Check coin pickup
            global game_coin
            if game_coin and (game_hero.grid_x, game_hero.grid_y) == game_coin:
                game_hero.coins = getattr(game_hero, "coins", 0) + 1
                play_sound("coin")
                # Respawn coin avoiding hero and enemies
                exclude = {(game_hero.grid_x, game_hero.grid_y)}
                for e in game_enemies:
                    exclude.add((e.grid_x, e.grid_y))
                game_coin = spawn_coin(game_grid, exclude_positions=exclude)
        # Update enemies
        for enemy in game_enemies:
            enemy.update_ai(dt, game_grid, game_hero)
            enemy.update_position(dt)
            # Simple collision: same grid cell causes damage
            if enemy.grid_x == game_hero.grid_x and enemy.grid_y == game_hero.grid_y:
                # Only apply damage if cooldown expired
                if getattr(game_hero, "damage_timer", 0.0) <= 0.0:
                    game_hero.health -= 5
                    game_hero.damage_timer = getattr(game_hero, "damage_cooldown", 0.45)
                    play_sound("hit")
                    if game_hero.health <= 0:
                        game_hero.health = 0
                        game_state = STATE_GAME_OVER
                        play_sound("game_over")
    elif game_state == STATE_GAME_OVER:
        # Return to menu with space key
        if keyboard.space:
            game_state = STATE_MENU
            stop_music()


def draw():
    """PgZero draw function called each frame."""
    screen.fill((25, 30, 45))
    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_PLAYING:
        draw_game()
    else:
        draw_game()
        draw_game_over()


def draw_grid():
    """Draw the game grid."""
    for y in range(ROWS):
        for x in range(COLUMNS):
            r = Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if game_grid[y][x]:
                screen.draw.filled_rect(r, (60, 60, 70))
            else:
                screen.draw.rect(r, (45, 45, 60))


def draw_game():
    """Draw the game screen."""
    # Draw grid
    draw_grid()
    # Draw coin on the map
    if game_coin:
        cx, cy = game_coin
        px = cx * CELL_SIZE + CELL_SIZE // 2
        py = cy * CELL_SIZE + CELL_SIZE // 2
        try:
            Actor("coin", (px, py)).draw()
        except Exception:
            # fallback: simple yellow circle
            screen.draw.filled_circle((px, py), CELL_SIZE // 4, (220, 200, 40))
    # Draw characters
    if game_hero:
        game_hero.draw_on_screen()
    for enemy in game_enemies:
        enemy.draw_on_screen()
    # Draw HUD
    if game_hero:
        screen.draw.text(
            f"HEALTH: {game_hero.health}  COINS: {getattr(game_hero, 'coins', 0)}",
            (10, 10),
            fontsize=28,
            color="white",
        )


def draw_menu():
    """Draw the main menu."""
    screen.draw.text(
        "SIMPLE ROGUELIKE",
        center=(WIDTH / 2, 120),
        fontsize=56,
        color="white",
    )
    # Buttons: start, music/sounds, exit
    top = 240
    width = 260
    height = 56
    left = WIDTH // 2 - width // 2

    # Start button
    btn_start = Rect(left, top, width, height)
    screen.draw.filled_rect(btn_start, (70, 130, 70))
    screen.draw.text(
        "START GAME",
        center=btn_start.center,
        fontsize=34,
        color="white",
    )

    # Music/Sounds toggle button
    btn_music = Rect(left, top + 90, width, height)
    music_color = (120, 100, 60) if music_enabled else (80, 80, 80)
    screen.draw.filled_rect(btn_music, music_color)
    music_text = "MUSIC/SOUNDS: ON" if music_enabled else "MUSIC/SOUNDS: OFF"
    screen.draw.text(music_text, center=btn_music.center, fontsize=24, color="white")

    # Exit button
    btn_exit = Rect(left, top + 180, width, height)
    screen.draw.filled_rect(btn_exit, (150, 50, 50))
    screen.draw.text("EXIT", center=btn_exit.center, fontsize=34, color="white")


def draw_game_over():
    """Draw the game over screen."""
    # Dark overlay
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 120))
    screen.draw.text(
        "GAME OVER",
        center=(WIDTH / 2, HEIGHT // 2 - 30),
        fontsize=56,
        color="red",
    )
    screen.draw.text(
        "Press SPACE to return to menu",
        center=(WIDTH / 2, HEIGHT // 2 + 30),
        fontsize=22,
        color="white",
    )


def on_mouse_down(pos):
    """Handle mouse clicks on menu."""
    global music_enabled, sounds_enabled
    if game_state != STATE_MENU:
        return
    top = 240
    width = 260
    height = 56
    left = WIDTH // 2 - width // 2
    # Start button
    if Rect(left, top, width, height).collidepoint(pos):
        play_sound("button_click")
        start_game()
    # Music/Sounds toggle button
    elif Rect(left, top + 90, width, height).collidepoint(pos):
        music_enabled = not music_enabled
        sounds_enabled = music_enabled
        if music_enabled:
            play_music("background")
        else:
            stop_music()
        play_sound("button_click")
    # Exit button
    elif Rect(left, top + 180, width, height).collidepoint(pos):
        play_sound("button_click")
        exit()


# Initialize game grid
game_grid = create_grid()
