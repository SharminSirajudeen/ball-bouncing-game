#!/usr/bin/env python3
"""
Bird Hunter - Strategic Shooting Game

A challenging slingshot-based bird hunting game with strategic gameplay mechanics.

Features:
  - Limited ammo system - make every shot count!
  - Multiple bird types with different behaviors and rewards
  - Moving obstacles (clouds) that block shots
  - Wind effects that alter ball trajectory
  - Power-ups with strategic timing
  - Combo system for skilled consecutive shots
  - Wave-based difficulty progression
  - Miss streak penalties
  - Perfect shot bonuses for precision hits

Author: AegisX
Usage: python3 bouncing_ball.py
Controls:
  - ESC/Q: Quit
  - R: Reset game
  - SPACE: Pause/Unpause
  - Drag Ball: Slingshot mode
  - Shoot the birds strategically!
"""

import math
import random
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

import pygame


# Constants
class PhysicsConstants:
    """Physics simulation constants."""
    GRAVITY: float = 800.0  # pixels/s²
    BOUNCE_DAMPENING: float = 0.85  # Energy loss factor (0-1)
    AIR_FRICTION: float = 0.998  # Air resistance coefficient
    MIN_VELOCITY: float = 5.0  # Minimum velocity threshold
    MAX_DELTA_TIME: float = 1/30.0  # Maximum frame time to prevent physics explosions
    
    # Ball-to-ball collision constants
    COLLISION_DAMPENING: float = 0.92  # Energy loss during ball collisions
    COLLISION_SEPARATION_FORCE: float = 0.5  # Force to separate overlapping balls
    MIN_COLLISION_DISTANCE: float = 2.0  # Minimum separation distance


class DisplayConstants:
    """Display and UI constants optimized for minimalism."""
    DEFAULT_WIDTH: int = 800
    DEFAULT_HEIGHT: int = 600
    TARGET_FPS: int = 60
    
    # Minimalist UI constants
    UI_MARGIN: int = 20
    SCORE_FONT_SIZE: int = 48        # Large, prominent score
    HIGH_SCORE_FONT_SIZE: int = 24   # Smaller, subtle high score
    GROUND_THICKNESS: int = 2        # Thin ground line
    BALL_SHADOW_OFFSET: int = 2      # Subtle shadow
    SHADOW_OFFSET: int = 3           # Ball shadow offset for effects
    
    # Layout positions
    SCORE_Y: int = 40                # Top center score position
    HIGH_SCORE_Y: int = 70           # Below main score
    BALL_COUNT_X: int = 20           # Bottom left ball count
    BALL_COUNT_Y: int = 550          # Bottom area


class BallConstants:
    """Ball-related constants."""
    DEFAULT_RADIUS: int = 25
    HIGHLIGHT_DIVISOR: int = 3
    PUSH_FORCE: float = -500.0
    MAX_RANDOM_VELOCITY_X: float = 300.0
    MAX_RANDOM_VELOCITY_Y: float = 200.0
    CLICK_PUSH_RANGE_X: Tuple[float, float] = (-200.0, 200.0)
    SLINGSHOT_MAX_FORCE: float = 3500.0  # Strong force for powerful launches
    SLINGSHOT_MAX_DRAG_DISTANCE: float = 200.0  # Increased drag distance for more power
    SQUISH_FACTOR: float = 0.8

    # Resource scarcity settings (addiction mechanic)
    MAX_AMMO: int = 8  # Cap on maximum ammo to create scarcity
    MAX_BALLS_ON_SCREEN: int = 3  # Limit simultaneous balls for strategic timing


class BirdConstants:
    """Bird animation constants."""
    BIRD_WIDTH: int = 60  # Regular birds
    BIRD_HEIGHT: int = 45  # Regular birds
    COLLISION_RADIUS: int = 25  # Collision detection radius
    WING_ANIMATION_SPEED: float = 8.0  # frames per second
    FLIGHT_HEIGHT_MIN: int = 80  # minimum flight height from top
    FLIGHT_HEIGHT_MAX: int = 300  # maximum flight height from top
    SINE_AMPLITUDE: float = 15.0  # vertical sine wave amplitude
    SINE_FREQUENCY: float = 2.0  # sine wave frequency
    
    # Regular brown birds
    REGULAR_SPEED: float = 100.0  # pixels per second
    REGULAR_POINTS: int = 1
    REGULAR_BALLS_REWARD: int = 0  # No ammo - creates scarcity!
    
    # Golden birds (yellow)
    GOLDEN_SPEED: float = 150.0  # faster
    GOLDEN_POINTS: int = 5
    GOLDEN_BALLS_REWARD: int = 1  # Valuable ammo reward
    
    # Red angry birds
    ANGRY_SPEED: float = 120.0
    ANGRY_POINTS: int = 3
    ANGRY_BALLS_REWARD: int = 0  # No ammo - just points
    ANGRY_ZIGZAG_AMPLITUDE: float = 30.0  # zigzag pattern
    ANGRY_ZIGZAG_FREQUENCY: float = 4.0
    
    # Blue rare birds
    RARE_SPEED: float = 200.0  # very fast
    RARE_POINTS: int = 10
    RARE_BALLS_REWARD: int = 2  # Jackpot ammo reward!
    RARE_DODGE_DISTANCE: float = 80.0  # dodge when ball gets close
    
    # Spawn rates (probabilities out of 100)
    REGULAR_SPAWN_RATE: int = 60
    GOLDEN_SPAWN_RATE: int = 20
    ANGRY_SPAWN_RATE: int = 15
    RARE_SPAWN_RATE: int = 5
    
    SPAWN_INTERVAL_MIN: float = 1.0
    SPAWN_INTERVAL_MAX: float = 3.0


class ScoringConstants:
    """Scoring system constants."""
    # Bird Strike Bonuses
    BIRD_STRIKE_BASE: int = 500
    BIRD_STRIKE_PEAK: int = 1000
    
    # Collision Combo System
    COLLISION_BASE_POINTS: int = 10
    COMBO_WINDOW: float = 1.0  # seconds to chain combos
    COMBO_MULTIPLIER: float = 2.0  # exponential growth
    
    # Air Time Bonuses
    AIR_TIME_POINTS_PER_TICK: int = 1
    AIR_TIME_TICK_INTERVAL: float = 0.1  # seconds
    AIR_TIME_BONUS_THRESHOLD: float = 2.0  # seconds for bonus
    AIR_TIME_HEIGHT_THRESHOLD: int = 100  # pixels above ground
    
    # Pipe Target Bonuses
    PIPE_ENTRY_POINTS: int = 100
    PIPE_DIRECT_SHOT_BONUS: int = 300
    
    # Speed Achievements
    SPEED_TIER_1: float = 500.0  # px/s
    SPEED_TIER_1_POINTS: int = 25
    SPEED_TIER_2: float = 750.0
    SPEED_TIER_2_POINTS: int = 50
    SPEED_TIER_3: float = 1000.0
    SPEED_TIER_3_POINTS: int = 100
    
    # Trick Shot Bonuses
    FLOOR_IS_LAVA_TIME: float = 5.0  # seconds
    FLOOR_IS_LAVA_POINTS: int = 200
    WALL_RIDER_POINTS: int = 50
    ORBIT_POINTS: int = 150
    
    # Slingshot Mastery
    PERFECT_LAUNCH_POINTS: int = 50  # exactly 100% power
    GENTLE_TOUCH_POINTS: int = 30    # under 20% power that scores
    SNIPER_POINTS: int = 100         # hit another ball directly
    
    # Zone Multipliers
    CLOUD_ZONE_MULTIPLIER: float = 2.0
    HILL_ZONE_MULTIPLIER: float = 1.0
    GROUND_ZONE_MULTIPLIER: float = 0.5
    CLOUD_ZONE_HEIGHT: int = 150  # pixels from top
    GROUND_ZONE_HEIGHT: int = 100  # pixels from bottom
    
    # Visual Feedback
    FLOATING_TEXT_DURATION: float = 2.0  # seconds
    FLOATING_TEXT_RISE_SPEED: float = 50.0  # pixels per second
    PARTICLE_DURATION: float = 1.0  # seconds
    SCREEN_SHAKE_INTENSITY: int = 5  # pixels
    SCREEN_SHAKE_DURATION: float = 0.2  # seconds


class Colors:
    """Color constants for Mario-themed game."""
    # Basic colors
    BLACK: Tuple[int, int, int] = (32, 33, 36)
    WHITE: Tuple[int, int, int] = (248, 249, 250)
    GRAY: Tuple[int, int, int] = (95, 99, 104)
    
    # Accent colors
    ACCENT: Tuple[int, int, int] = (66, 133, 244)
    
    # Colorful ball colors
    RED: Tuple[int, int, int] = (255, 85, 85)
    BLUE: Tuple[int, int, int] = (85, 85, 255)
    GREEN: Tuple[int, int, int] = (85, 255, 85)
    ORANGE: Tuple[int, int, int] = (255, 165, 0)
    PURPLE: Tuple[int, int, int] = (255, 85, 255)
    CYAN: Tuple[int, int, int] = (85, 255, 255)
    YELLOW: Tuple[int, int, int] = (255, 255, 85)
    GOLD: Tuple[int, int, int] = (255, 215, 0)  # For rewards and bonuses

    # Mario background colors
    SKY_BLUE_LIGHT: Tuple[int, int, int] = (135, 206, 250)
    SKY_BLUE_DARK: Tuple[int, int, int] = (70, 130, 180)
    CLOUD_WHITE: Tuple[int, int, int] = (255, 255, 255)
    HILL_GREEN: Tuple[int, int, int] = (34, 139, 34)
    HILL_DARK_GREEN: Tuple[int, int, int] = (0, 100, 0)
    BUSH_GREEN: Tuple[int, int, int] = (0, 128, 0)
    PIPE_GREEN: Tuple[int, int, int] = (0, 200, 0)
    PIPE_DARK_GREEN: Tuple[int, int, int] = (0, 150, 0)
    
    # Bird colors - different types
    BIRD_BODY: Tuple[int, int, int] = (139, 69, 19)          # Brown (default)
    BIRD_REGULAR_BODY: Tuple[int, int, int] = (139, 69, 19)  # Brown
    BIRD_GOLDEN_BODY: Tuple[int, int, int] = (255, 215, 0)   # Gold
    BIRD_ANGRY_BODY: Tuple[int, int, int] = (220, 20, 20)    # Red
    BIRD_RARE_BODY: Tuple[int, int, int] = (0, 100, 255)     # Blue
    BIRD_WING: Tuple[int, int, int] = (101, 67, 33)
    BIRD_BEAK: Tuple[int, int, int] = (255, 165, 0)
    BIRD_EYE: Tuple[int, int, int] = (255, 255, 255)
    
    # Power-up colors
    POWERUP_MULTIBALL: Tuple[int, int, int] = (255, 100, 255)  # Magenta
    POWERUP_SLOWMO: Tuple[int, int, int] = (100, 255, 100)     # Green
    POWERUP_BIGBALL: Tuple[int, int, int] = (255, 100, 100)    # Red
    POWERUP_MAGNET: Tuple[int, int, int] = (100, 100, 255)     # Blue
    
    # Warning colors
    WARNING_RED: Tuple[int, int, int] = (255, 50, 50)
    COMBO_FIRE: Tuple[int, int, int] = (255, 150, 0)
    
    # Ground line
    GROUND_COLOR: Tuple[int, int, int] = BLACK
    SHADOW_COLOR: Tuple[int, int, int] = (30, 30, 30)  # Dark shadow for balls
    
    # UI colors
    SCORE_TEXT: Tuple[int, int, int] = BLACK
    HIGH_SCORE_TEXT: Tuple[int, int, int] = GRAY
    ACHIEVEMENT_TEXT: Tuple[int, int, int] = ORANGE
    
    # Slingshot
    SLINGSHOT_LINE: Tuple[int, int, int] = GRAY
    TRAJECTORY_LINE: Tuple[int, int, int] = ACCENT
    POWER_METER_BACKGROUND: Tuple[int, int, int] = (200, 200, 200)
    POWER_METER_FILL: Tuple[int, int, int] = GREEN


class BallState(Enum):
    """Ball state for interaction."""
    NORMAL = "normal"
    GRABBED = "grabbed"
    LAUNCHING = "launching"


class BirdType(Enum):
    """Different types of birds with unique behaviors."""
    REGULAR = "regular"
    GOLDEN = "golden"
    ANGRY = "angry"
    RARE = "rare"


class PowerUpType(Enum):
    """Different power-up types."""
    MULTIBALL = "multiball"
    SLOWMO = "slowmo"
    BIGBALL = "bigball"
    MAGNET = "magnet"


@dataclass
class Bird:
    """Bird data class for animated flying bird."""
    x: float
    y: float
    direction: int  # 1 for right, -1 for left
    base_y: float  # base flight height for sine wave
    start_time: float  # when the bird started flying
    bird_type: BirdType  # type of bird
    wing_frame: int = 0  # current wing animation frame
    dodging: bool = False  # for rare birds dodging mechanic
    dodge_start_time: float = 0.0
    
    @property  
    def is_active(self) -> bool:
        """Check if bird is still on screen."""
        # Birds should stay active longer, accounting for their size
        buffer = BirdConstants.BIRD_WIDTH + 100
        return -buffer <= self.x <= 1920 + buffer  # Support wider screens
    
    @property
    def speed(self) -> float:
        """Get speed based on bird type."""
        if self.bird_type == BirdType.REGULAR:
            return BirdConstants.REGULAR_SPEED
        elif self.bird_type == BirdType.GOLDEN:
            return BirdConstants.GOLDEN_SPEED
        elif self.bird_type == BirdType.ANGRY:
            return BirdConstants.ANGRY_SPEED
        elif self.bird_type == BirdType.RARE:
            return BirdConstants.RARE_SPEED
        return BirdConstants.REGULAR_SPEED
    
    @property
    def color(self) -> Tuple[int, int, int]:
        """Get color based on bird type."""
        if self.bird_type == BirdType.REGULAR:
            return Colors.BIRD_REGULAR_BODY
        elif self.bird_type == BirdType.GOLDEN:
            return Colors.BIRD_GOLDEN_BODY
        elif self.bird_type == BirdType.ANGRY:
            return Colors.BIRD_ANGRY_BODY
        elif self.bird_type == BirdType.RARE:
            return Colors.BIRD_RARE_BODY
        return Colors.BIRD_REGULAR_BODY
    
    @property
    def points(self) -> int:
        """Get points awarded for hitting this bird."""
        if self.bird_type == BirdType.REGULAR:
            return BirdConstants.REGULAR_POINTS
        elif self.bird_type == BirdType.GOLDEN:
            return BirdConstants.GOLDEN_POINTS
        elif self.bird_type == BirdType.ANGRY:
            return BirdConstants.ANGRY_POINTS
        elif self.bird_type == BirdType.RARE:
            return BirdConstants.RARE_POINTS
        return BirdConstants.REGULAR_POINTS
    
    @property
    def balls_reward(self) -> int:
        """Get ball reward for hitting this bird."""
        if self.bird_type == BirdType.REGULAR:
            return BirdConstants.REGULAR_BALLS_REWARD
        elif self.bird_type == BirdType.GOLDEN:
            return BirdConstants.GOLDEN_BALLS_REWARD
        elif self.bird_type == BirdType.ANGRY:
            return BirdConstants.ANGRY_BALLS_REWARD
        elif self.bird_type == BirdType.RARE:
            return BirdConstants.RARE_BALLS_REWARD
        return BirdConstants.REGULAR_BALLS_REWARD


@dataclass
class FloatingText:
    """Floating score text for visual feedback."""
    x: float
    y: float
    text: str
    color: Tuple[int, int, int]
    font_size: int
    duration: float
    start_time: float
    
    @property
    def alpha(self) -> float:
        """Calculate alpha based on remaining time."""
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        return min(1.0, remaining / (self.duration * 0.3))
    
    @property
    def is_alive(self) -> bool:
        """Check if text should still be displayed."""
        return (time.time() - self.start_time) < self.duration


@dataclass
class Particle:
    """Particle for visual effects."""
    x: float
    y: float
    vx: float
    vy: float
    color: Tuple[int, int, int]
    size: int
    life: float
    start_life: float
    
    @property
    def alpha(self) -> float:
        """Calculate alpha based on remaining life."""
        return max(0, self.life / self.start_life)
    
    @property
    def is_alive(self) -> bool:
        """Check if particle should still be displayed."""
        return self.life > 0


@dataclass
class Cloud:
    """Moving cloud obstacle that blocks shots."""
    x: float
    y: float
    width: float
    height: float
    vx: float  # horizontal velocity
    
    def update(self, dt: float, screen_width: int) -> None:
        """Update cloud position."""
        self.x += self.vx * dt
        # Wrap around screen
        if self.x + self.width < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = -self.width


@dataclass
class PowerUp:
    """Power-up that appears temporarily."""
    x: float
    y: float
    power_type: PowerUpType
    spawn_time: float
    duration: float = 5.0  # appears for 5 seconds
    collected: bool = False
    
    @property
    def is_active(self) -> bool:
        """Check if power-up is still available."""
        return not self.collected and (time.time() - self.spawn_time) < self.duration
    
    @property
    def alpha(self) -> float:
        """Calculate alpha for fading effect."""
        elapsed = time.time() - self.spawn_time
        if elapsed > self.duration * 0.8:  # Start fading in last 20%
            remaining = self.duration - elapsed
            return max(0.2, remaining / (self.duration * 0.2))
        return 1.0


@dataclass
class GameState:
    """Main game state tracking all mechanics."""
    # Ammo system
    ammo_count: int = 3
    balls_in_flight: int = 0
    
    # Scoring
    score: int = 0
    high_score: int = 0
    
    # Combo system
    combo_count: int = 0
    combo_timer: float = 0.0
    last_hit_time: float = 0.0
    max_combo: int = 0
    combo_window: float = 3.0  # seconds to maintain combo
    
    # Miss streak
    miss_count: int = 0
    shots_fired: int = 0
    
    # Wave system
    current_wave: int = 1
    wave_start_time: float = 0.0
    wave_duration: float = 30.0  # 30 seconds per wave
    
    # Power-ups active
    multiball_active: bool = False
    slowmo_active: bool = False
    slowmo_end_time: float = 0.0
    bigball_active: bool = False
    magnet_active: bool = False
    
    # Wind system
    wind_strength: float = 0.0
    wind_direction: float = 0.0  # angle in radians
    wind_change_timer: float = 0.0
    
    # Visual effects
    screen_shake_timer: float = 0.0
    screen_shake_intensity: float = 0.0
    
    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.ammo_count = 3
        self.balls_in_flight = 0
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.combo_count = 0
        self.combo_timer = 0.0
        self.miss_count = 0
        self.shots_fired = 0
        self.current_wave = 1
        self.wave_start_time = time.time()
        self.multiball_active = False
        self.slowmo_active = False
        self.bigball_active = False
        self.magnet_active = False
        self.wind_strength = 0.0
        self.screen_shake_timer = 0.0
    
    @property
    def is_game_over(self) -> bool:
        """Check if game is over (no ammo and no balls in flight)."""
        return self.ammo_count <= 0 and self.balls_in_flight <= 0


@dataclass
class Ball:
    """Ball data class with position, velocity, and rendering properties."""
    x: float
    y: float
    vx: float
    vy: float
    radius: int
    color: Tuple[int, int, int]
    state: BallState = BallState.NORMAL
    squish_factor: float = 1.0
    
    # Scoring tracking
    last_ground_touch: float = 0.0
    consecutive_wall_bounces: int = 0
    launch_power: float = 0.0  # Track launch power for achievements
    
    # Track maximum velocities to determine if ball has been launched
    max_vx: float = 0.0
    max_vy: float = 0.0
    has_been_launched: bool = False  # Track if ball was ever launched
    
    @property
    def speed(self) -> float:
        """Calculate current speed magnitude."""
        return math.sqrt(self.vx**2 + self.vy**2)
    
    @property
    def position(self) -> Tuple[float, float]:
        """Get position as tuple."""
        return (self.x, self.y)
    
    @property
    def velocity(self) -> Tuple[float, float]:
        """Get velocity as tuple."""
        return (self.vx, self.vy)
    
    def distance_to_point(self, x: float, y: float) -> float:
        """Calculate distance from ball center to a point."""
        return math.sqrt((x - self.x)**2 + (y - self.y)**2)
    
    def distance_to_ball(self, other: 'Ball') -> float:
        """Calculate distance between ball centers."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is inside the ball."""
        return self.distance_to_point(x, y) <= self.radius
    
    def is_colliding_with(self, other: 'Ball') -> bool:
        """Check if this ball is colliding with another ball."""
        distance = self.distance_to_ball(other)
        return distance < (self.radius + other.radius)


class BouncingBallSimulation:
    """Professional bouncing ball physics simulation."""
    
    def __init__(self, width: int = DisplayConstants.DEFAULT_WIDTH, 
                 height: int = DisplayConstants.DEFAULT_HEIGHT) -> None:
        """Initialize the simulation.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        self._initialize_pygame()
        self._setup_display(width, height)
        self._initialize_state()
        self._setup_fonts()
        
        # Don't add initial ball - let player click to create balls
        print("Strategic Bird Hunter initialized!")
        print("Click anywhere to create a ball, then drag to shoot!")
    
    def _initialize_clouds(self) -> None:
        """Initialize moving cloud obstacles."""
        for i in range(3):
            cloud = Cloud(
                x=random.uniform(100, self.width - 200),
                y=random.uniform(50, 200),
                width=random.uniform(80, 120),
                height=random.uniform(40, 60),
                vx=random.uniform(-50, 50)
            )
            self.clouds.append(cloud)
    
    def _load_high_score(self) -> None:
        """Load high score from file."""
        try:
            with open('bird_hunter_highscore.txt', 'r') as f:
                self.game_state.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.game_state.high_score = 0
    
    def _save_high_score(self) -> None:
        """Save high score to file."""
        try:
            with open('bird_hunter_highscore.txt', 'w') as f:
                f.write(str(self.game_state.high_score))
        except Exception as e:
            print(f"Could not save high score: {e}")
    
    def _initialize_pygame(self) -> None:
        """Initialize pygame subsystems."""
        if not pygame.get_init():
            pygame.init()
        
        # Bird rendering mode: 'sprite', 'emoji', or 'geometric'
        self.bird_mode = 'sprite'  # Start with sprite birds for wing animation
        
        # Try to load bird sprites
        try:
            self.bird_sprite_right = pygame.image.load('bird_sprite.png')
            self.bird_sprite_left = pygame.image.load('bird_sprite_left.png')
            # Scale sprites to desired size
            self.bird_sprite_right = pygame.transform.scale(self.bird_sprite_right, (100, 70))
            self.bird_sprite_left = pygame.transform.scale(self.bird_sprite_left, (100, 70))
            print("Bird sprites loaded successfully")
        except:
            self.bird_sprite_right = None
            self.bird_sprite_left = None
            print("Bird sprites not found, using emoji mode")
        
        # Emoji font for bird rendering
        try:
            # Try to use a font that supports emoji
            self.emoji_font = pygame.font.Font(None, 80)
        except:
            self.emoji_font = None
    
    def _setup_display(self, width: int, height: int) -> None:
        """Setup display window and properties."""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), 
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Ricochet - Bird Hunter")
    
    def _initialize_state(self) -> None:
        """Initialize simulation state."""
        self.balls: List[Ball] = []
        self.paused = False
        self.clock = pygame.time.Clock()
        
        # New comprehensive game state
        self.game_state = GameState()
        self.game_state.wave_start_time = time.time()
        
        # Performance tracking
        self._frame_count = 0
        self._last_fps_update = 0.0
        self._current_fps = 0.0
        
        # Slingshot mechanics
        self.dragging_ball: Optional[Ball] = None
        self.drag_start_pos: Optional[Tuple[float, float]] = None
        self.mouse_pos: Tuple[float, float] = (0, 0)
        
        # Collision tracking
        self.collision_flashes: List[Tuple[float, float, float]] = []  # (x, y, time_remaining)
        
        # Bird system
        self.birds: List[Bird] = []
        self.last_bird_spawn: float = 0.0
        self.next_bird_spawn_delay: float = 2.0
        
        # Cloud obstacles
        self.clouds: List[Cloud] = []
        self._initialize_clouds()  # Now draws fluffy clouds, not gray rectangles
        
        # Power-ups
        self.power_ups: List[PowerUp] = []
        self.last_powerup_spawn: float = 0.0
        
        # Visual effects
        self.particles: List[Particle] = []
        self.floating_texts: List[FloatingText] = []
        
        # Screen shake
        self.screen_shake_offset: Tuple[float, float] = (0.0, 0.0)
        
        # Load high score from file if exists
        self._load_high_score()
    
    def _setup_fonts(self) -> None:
        """Setup fonts for UI rendering."""
        try:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            self.big_font = pygame.font.Font(None, 72)
            self.score_font = pygame.font.Font(None, 48)
        except pygame.error:
            # Fallback to default font if custom font fails
            self.font = pygame.font.get_default_font()
            self.small_font = pygame.font.get_default_font()
            self.big_font = pygame.font.get_default_font()
            self.score_font = pygame.font.get_default_font()
        
    def create_ball_for_shooting(self, x: Optional[float] = None, y: Optional[float] = None) -> Optional[Ball]:
        """Create a ball for slingshot shooting if ammo available.

        Args:
            x: Optional X position for the ball (defaults to center)
            y: Optional Y position for the ball (defaults to mid-screen)

        Returns:
            Ball if ammo available, None otherwise
        """
        if self.game_state.ammo_count <= 0:
            return None

        # Enforce max balls on screen (addiction mechanic: strategic timing)
        if self.game_state.balls_in_flight >= BallConstants.MAX_BALLS_ON_SCREEN:
            self._add_floating_text(self.width // 2, 200, "Wait for ball to land!", Colors.RED, 28)
            return None

        # Create ball at specified position or default
        radius = BallConstants.DEFAULT_RADIUS
        if self.game_state.bigball_active:
            radius *= 2

        # Use provided position or defaults
        if x is None:
            x = self.width * 0.5
        if y is None:
            y = self.height * 0.65  # About 2/3 down the screen
        
        # Assign random colorful ball color
        ball_colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.ORANGE, Colors.PURPLE, Colors.CYAN]
        ball_color = random.choice(ball_colors)
        
        ball = Ball(
            x=float(x),
            y=float(y),
            vx=0.0,
            vy=0.0,
            radius=radius,
            color=ball_color,
            max_vx=0.0,  # Explicitly set to 0 so ball won't be removed
            max_vy=0.0   # until it's actually launched
        )
        
        return ball
    
    def fire_ball(self, ball: Ball, force_multiplier: float) -> None:
        """Fire a ball and consume ammo."""
        self.game_state.ammo_count -= 1
        self.game_state.balls_in_flight += 1
        self.game_state.shots_fired += 1
        ball.launch_power = force_multiplier
        
        # Add multiball effect if active
        if self.game_state.multiball_active:
            self._create_multiball_shots(ball)
            self.game_state.multiball_active = False
    
    def reset_game(self) -> None:
        """Reset complete game state."""
        self.balls.clear()
        self.birds.clear()
        self.particles.clear()
        self.floating_texts.clear()
        self.power_ups.clear()
        
        # Update high score if needed
        if self.game_state.score > self.game_state.high_score:
            self.game_state.high_score = self.game_state.score
            self._save_high_score()
        
        # Reset game state
        self.game_state.reset_game()
        
        # Reset clouds
        self.clouds.clear()
        self._initialize_clouds()
        
        # Don't add initial ball - let player click to create balls
        print(f"Game reset! Starting new game with 3 shots!")
    
    def update_physics(self, dt: float) -> None:
        """Update ball positions with realistic physics and handle collisions.
        
        Args:
            dt: Delta time in seconds
        """
        if self.paused or dt <= 0:
            return
        
        # Cap delta time to prevent physics instability
        dt = min(dt, PhysicsConstants.MAX_DELTA_TIME)
        
        # Update game state timers
        self._update_game_state(dt)
        
        # Update balls
        for ball in self.balls:
            # Skip physics updates for balls being dragged
            if ball.state == BallState.GRABBED:
                continue
                
            self._apply_forces(ball, dt)
            self._apply_wind_effects(ball, dt)
            self._apply_magnet_effects(ball, dt)
            self._update_position(ball, dt)
            self._handle_wall_collisions(ball)
            self._check_ball_out_of_bounds(ball)
        
        # Handle ball-to-ball collisions after all positions are updated
        self._handle_ball_collisions()
        
        # Update obstacles
        self._update_clouds(dt)
        
        # Update bird system with new mechanics
        self._update_wind_system(dt)
        self._spawn_birds_if_needed()
        self._update_birds(dt)
        self._check_bird_dodging()
        
        # Check for collisions
        self._check_bird_strikes()
        self._check_cloud_collisions()  # Re-enabled with fluffy clouds
        self._check_powerup_collection()
        
        # Spawn power-ups with improved visuals
        self._spawn_powerups_if_needed()
        
        # Update visual effects
        self._update_collision_effects(dt)
        self._update_particles(dt)
        self._update_floating_texts(dt)
        self._update_screen_shake(dt)
        
        # Check game over
        if self.game_state.is_game_over:
            print(f"GAME OVER! Final score: {self.game_state.score}")
            if self.game_state.score > self.game_state.high_score:
                print("NEW HIGH SCORE!")
    
    def _apply_forces(self, ball: Ball, dt: float) -> None:
        """Apply physics forces to a ball.
        
        Args:
            ball: Ball to update
            dt: Delta time in seconds
        """
        # Apply gravity to vertical velocity
        ball.vy += PhysicsConstants.GRAVITY * dt
        
        # Apply air resistance
        ball.vx *= PhysicsConstants.AIR_FRICTION
        ball.vy *= PhysicsConstants.AIR_FRICTION
        
        # Only track max velocities after ball has been launched (state changes from GRABBED)
        # Don't count gravity-induced velocity for stationary balls on ground
        if ball.state == BallState.NORMAL and (abs(ball.vx) > 50 or abs(ball.vy) > 100):
            ball.max_vx = max(abs(ball.max_vx), abs(ball.vx))
            ball.max_vy = max(abs(ball.max_vy), abs(ball.vy))
    
    def _update_position(self, ball: Ball, dt: float) -> None:
        """Update ball position based on velocity.
        
        Args:
            ball: Ball to update
            dt: Delta time in seconds
        """
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
    
    def _handle_wall_collisions(self, ball: Ball) -> None:
        """Handle boundary collisions with proper physics.
        
        Args:
            ball: Ball to check for collisions
        """
        radius = ball.radius
        
        # Floor collision (bottom) - ball stops here in strategic game
        if ball.y + radius >= self.height:
            ball.y = self.height - radius
            ball.vy = 0
            ball.vx *= 0.7  # Slow down on ground
        
        # Ceiling collision (top)
        elif ball.y - radius <= 0:
            ball.y = radius
            ball.vy = abs(ball.vy) * PhysicsConstants.BOUNCE_DAMPENING
        
        # Left wall collision
        if ball.x - radius <= 0:
            ball.x = radius
            ball.vx = abs(ball.vx) * PhysicsConstants.BOUNCE_DAMPENING
            ball.consecutive_wall_bounces += 1
        
        # Right wall collision
        elif ball.x + radius >= self.width:
            ball.x = self.width - radius
            ball.vx = -abs(ball.vx) * PhysicsConstants.BOUNCE_DAMPENING
            ball.consecutive_wall_bounces += 1
        else:
            # Reset wall bounce counter if not hitting walls
            ball.consecutive_wall_bounces = 0
    
    def _handle_ball_collisions(self) -> None:
        """Handle ball-to-ball collisions using elastic collision physics."""
        # Check all pairs of balls for collisions
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                ball1, ball2 = self.balls[i], self.balls[j]
                
                # Skip collision if either ball is being dragged
                if (ball1.state == BallState.GRABBED or 
                    ball2.state == BallState.GRABBED):
                    continue
                
                if ball1.is_colliding_with(ball2):
                    self._resolve_ball_collision(ball1, ball2)
    
    def _resolve_ball_collision(self, ball1: Ball, ball2: Ball) -> None:
        """Resolve collision between two balls using elastic collision physics.
        
        Args:
            ball1: First ball in collision
            ball2: Second ball in collision
        """
        # Calculate collision normal (vector from ball1 to ball2)
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Prevent division by zero
        if distance == 0:
            # Balls are at exact same position, separate them randomly
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)
            distance = 1.0
        
        # Normalize collision normal
        nx = dx / distance
        ny = dy / distance
        
        # Separate overlapping balls
        overlap = (ball1.radius + ball2.radius) - distance
        if overlap > 0:
            # Move balls apart by half the overlap each (plus minimum separation)
            separation = (overlap + PhysicsConstants.MIN_COLLISION_DISTANCE) * 0.5
            ball1.x -= nx * separation
            ball1.y -= ny * separation
            ball2.x += nx * separation
            ball2.y += ny * separation
        
        # Calculate relative velocity
        dvx = ball2.vx - ball1.vx
        dvy = ball2.vy - ball1.vy
        
        # Calculate relative velocity in collision normal direction
        dvn = dvx * nx + dvy * ny
        
        # Do not resolve if velocities are separating
        if dvn > 0:
            return
        
        # Apply elastic collision with dampening
        # Assuming equal mass for simplicity: m1 = m2 = 1
        # For equal masses: impulse = 2 * dvn
        impulse = 2 * dvn * PhysicsConstants.COLLISION_DAMPENING
        
        # Apply impulse to velocities
        ball1.vx += impulse * nx
        ball1.vy += impulse * ny
        ball2.vx -= impulse * nx
        ball2.vy -= impulse * ny
        
        # No scoring for ball collisions in strategic bird game
        pass
    
    def _check_ball_out_of_bounds(self, ball: Ball) -> None:
        """Check if ball is out of bounds and should be removed."""
        # Only remove balls that have been launched
        if not ball.has_been_launched:
            return  # Never remove balls that haven't been launched
        
        # Remove balls that are stationary on ground after being launched
        if (ball.y + ball.radius >= self.height and 
            abs(ball.vx) < 10 and abs(ball.vy) < 10):
            # Ball is stationary on ground after being launched, consider it done
            if ball in self.balls:
                self.balls.remove(ball)
                self.game_state.balls_in_flight -= 1
                # Check if this was a miss (no bird hits in this trajectory)
                current_time = time.time()
                if current_time - self.game_state.last_hit_time > 2.0:
                    self._handle_miss()
    
    def _handle_miss(self) -> None:
        """Handle when player misses a shot (addiction mechanic: punishment)."""
        self.game_state.miss_count += 1

        # Warning feedback after 2 misses
        if self.game_state.miss_count == 2:
            self._add_floating_text(self.width // 2, self.height // 2 - 50,
                                  "⚠️ ONE MORE MISS = -1 AMMO!", Colors.ORANGE, 36)

        # Miss streak penalty: lose ammo after 3 consecutive misses (was 5)
        # This creates tension and makes each shot matter more
        if self.game_state.miss_count >= 3:
            self.game_state.ammo_count = max(0, self.game_state.ammo_count - 1)
            self.game_state.miss_count = 0
            self._add_floating_text(self.width // 2, self.height // 2,
                                  "MISS STREAK! -1 AMMO 💔", Colors.WARNING_RED, 48)
            self._trigger_screen_shake(10)
    
    def _update_game_state(self, dt: float) -> None:
        """Update game state timers and mechanics."""
        current_time = time.time()
        
        # Update combo timer
        if self.game_state.combo_count > 0:
            self.game_state.combo_timer -= dt
            if self.game_state.combo_timer <= 0:
                # Combo expired
                self.game_state.combo_count = 0
        
        # Update power-up timers
        if self.game_state.slowmo_active and current_time > self.game_state.slowmo_end_time:
            self.game_state.slowmo_active = False
        
        # Update wave system
        wave_elapsed = current_time - self.game_state.wave_start_time
        if wave_elapsed > self.game_state.wave_duration:
            self.game_state.current_wave += 1
            self.game_state.wave_start_time = current_time
            self._add_floating_text(self.width // 2, 100, 
                                  f"WAVE {self.game_state.current_wave}", Colors.COMBO_FIRE, 60)
    
    def _apply_wind_effects(self, ball: Ball, dt: float) -> None:
        """Apply wind effects to ball trajectory."""
        if self.game_state.wind_strength > 0:
            wind_force_x = math.cos(self.game_state.wind_direction) * self.game_state.wind_strength
            wind_force_y = math.sin(self.game_state.wind_direction) * self.game_state.wind_strength
            
            ball.vx += wind_force_x * dt
            ball.vy += wind_force_y * dt
    
    def _apply_magnet_effects(self, ball: Ball, dt: float) -> None:
        """Apply magnet power-up effects."""
        if not self.game_state.magnet_active:
            return
            
        # Find closest bird and attract ball slightly
        closest_bird = None
        closest_dist = float('inf')
        
        for bird in self.birds:
            dist = math.sqrt((bird.x - ball.x)**2 + (bird.y - ball.y)**2)
            if dist < closest_dist:
                closest_dist = dist
                closest_bird = bird
        
        if closest_bird and closest_dist < 150:  # Only attract if reasonably close
            # Gentle attraction force
            force_factor = 50.0
            dx = closest_bird.x - ball.x
            dy = closest_bird.y - ball.y
            if closest_dist > 0:
                ball.vx += (dx / closest_dist) * force_factor * dt
                ball.vy += (dy / closest_dist) * force_factor * dt
    
    def _update_clouds(self, dt: float) -> None:
        """Update cloud obstacle positions."""
        for cloud in self.clouds:
            cloud.update(dt, self.width)
    
    def _update_wind_system(self, dt: float) -> None:
        """Update wind system with changing effects."""
        self.game_state.wind_change_timer += dt
        
        # Change wind every 5-10 seconds
        if self.game_state.wind_change_timer > random.uniform(5, 10):
            self.game_state.wind_change_timer = 0
            self.game_state.wind_strength = random.uniform(0, 100)
            self.game_state.wind_direction = random.uniform(0, 2 * math.pi)
    
    def _check_cloud_collisions(self) -> None:
        """Check if balls collide with cloud obstacles."""
        for ball in self.balls[:]:
            for cloud in self.clouds:
                if (cloud.x <= ball.x <= cloud.x + cloud.width and
                    cloud.y <= ball.y <= cloud.y + cloud.height):
                    # Ball passes through cloud with air resistance, not sticky collision
                    # Apply gentle dampening instead of harsh reduction
                    ball.vx *= 0.85  # Much gentler than 0.3
                    ball.vy *= 0.9   # Even less vertical dampening to maintain trajectory
                    # Add cloud particle effects
                    self._add_cloud_particles(ball.x, ball.y)
    
    def _check_bird_dodging(self) -> None:
        """Make rare birds dodge when balls get close."""
        current_time = time.time()
        
        for bird in self.birds:
            if bird.bird_type != BirdType.RARE or bird.dodging:
                continue
                
            # Check if any ball is close
            for ball in self.balls:
                distance = math.sqrt((ball.x - bird.x)**2 + (ball.y - bird.y)**2)
                if distance < BirdConstants.RARE_DODGE_DISTANCE:
                    # Start dodging
                    bird.dodging = True
                    bird.dodge_start_time = current_time
                    # Change bird's trajectory
                    bird.y += random.uniform(-40, 40)
                    bird.y = max(50, min(bird.y, self.height - 200))
                    break
    
    def _spawn_powerups_if_needed(self) -> None:
        """Spawn power-ups occasionally."""
        current_time = time.time()
        
        # Spawn power-up every 15-25 seconds
        if current_time - self.last_powerup_spawn > random.uniform(15, 25):
            self.last_powerup_spawn = current_time
            
            # Random power-up type
            power_type = random.choice(list(PowerUpType))
            
            # Random position in upper area
            x = random.uniform(100, self.width - 100)
            y = random.uniform(100, 250)
            
            powerup = PowerUp(x, y, power_type, current_time)
            self.power_ups.append(powerup)
    
    def _check_powerup_collection(self) -> None:
        """Check if balls collect power-ups."""
        for ball in self.balls:
            for powerup in self.power_ups[:]:
                if not powerup.is_active:
                    continue
                    
                distance = math.sqrt((ball.x - powerup.x)**2 + (ball.y - powerup.y)**2)
                if distance < ball.radius + 20:  # Collection radius
                    # Collect power-up
                    powerup.collected = True
                    self._activate_powerup(powerup.power_type)
                    self.power_ups.remove(powerup)
                    self._add_floating_text(powerup.x, powerup.y, 
                                          f"{powerup.power_type.value.upper()} POWER!", 
                                          Colors.COMBO_FIRE, 32)
                    break
    
    def _activate_powerup(self, power_type: PowerUpType) -> None:
        """Activate a collected power-up."""
        current_time = time.time()
        
        if power_type == PowerUpType.MULTIBALL:
            self.game_state.multiball_active = True
        elif power_type == PowerUpType.SLOWMO:
            self.game_state.slowmo_active = True
            self.game_state.slowmo_end_time = current_time + 10.0  # 10 seconds
        elif power_type == PowerUpType.BIGBALL:
            self.game_state.bigball_active = True
        elif power_type == PowerUpType.MAGNET:
            self.game_state.magnet_active = True
    
    def _create_multiball_shots(self, original_ball: Ball) -> None:
        """Create additional balls for multiball power-up."""
        for i in range(2):  # Create 2 additional balls
            angle_offset = (-0.5 + i) * 0.3  # Spread shots
            new_ball = Ball(
                x=original_ball.x,
                y=original_ball.y,
                vx=original_ball.vx + math.cos(angle_offset) * 100,
                vy=original_ball.vy + math.sin(angle_offset) * 100,
                radius=original_ball.radius,
                color=original_ball.color,
                has_been_launched=True  # Mark as launched so they can be removed when done
            )
            self.balls.append(new_ball)
            self.game_state.balls_in_flight += 1
    
    def _add_cloud_particles(self, x: float, y: float) -> None:
        """Add cloud collision particles."""
        for _ in range(8):
            particle = Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                vx=random.uniform(-100, 100),
                vy=random.uniform(-50, 50),
                color=Colors.CLOUD_WHITE,
                size=random.randint(3, 6),
                life=random.uniform(0.5, 1.0),
                start_life=1.0
            )
            self.particles.append(particle)
    
    def _trigger_screen_shake(self, intensity: float) -> None:
        """Trigger screen shake effect."""
        self.game_state.screen_shake_timer = 0.3
        self.game_state.screen_shake_intensity = intensity
    
    def _update_collision_effects(self, dt: float) -> None:
        """Update visual collision effects.
        
        Args:
            dt: Delta time in seconds
        """
        # Update collision flashes
        self.collision_flashes = [
            (x, y, time_remaining - dt) 
            for x, y, time_remaining in self.collision_flashes 
            if time_remaining - dt > 0
        ]
    
    def _update_particles(self, dt: float) -> None:
        """Update feather particle effects.
        
        Args:
            dt: Delta time in seconds
        """
        active_particles = []
        for particle in self.particles:
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            particle.vy += 100 * dt  # Gravity for feathers
            particle.vx *= 0.98  # Air resistance
            particle.life -= dt
            
            if particle.is_alive:
                active_particles.append(particle)
        self.particles = active_particles
    
    def _update_floating_texts(self, dt: float) -> None:
        """Update floating text effects.
        
        Args:
            dt: Delta time in seconds
        """
        # Update positions and remove expired texts
        active_texts = []
        for text in self.floating_texts:
            text.y -= ScoringConstants.FLOATING_TEXT_RISE_SPEED * dt
            if text.is_alive:
                active_texts.append(text)
        self.floating_texts = active_texts
    
    
    
    def _add_floating_text(self, x: float, y: float, text: str, 
                          color: Tuple[int, int, int], font_size: int = 36) -> None:
        """Add floating text for visual feedback."""
        floating_text = FloatingText(
            x=x, y=y, text=text, color=color, font_size=font_size,
            duration=2.0, start_time=time.time()
        )
        self.floating_texts.append(floating_text)
    
    def _add_feather_particles(self, x: float, y: float, count: int = 12) -> None:
        """Add feather particles when bird is hit.
        
        Args:
            x: X position
            y: Y position  
            count: Number of feathers to spawn
        """
        feather_colors = [Colors.WHITE, (245, 245, 220), (255, 248, 220), (250, 235, 215)]
        
        for _ in range(count):
            # Random velocity for feathers
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - random.uniform(30, 80)  # Slight upward bias
            
            feather = Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                vx=vx,
                vy=vy,
                color=random.choice(feather_colors),
                size=random.randint(2, 4),
                life=random.uniform(1.5, 2.5),
                start_life=2.0
            )
            self.particles.append(feather)
    
    def _update_screen_shake(self, dt: float) -> None:
        """Update screen shake effect."""
        if self.game_state.screen_shake_timer > 0:
            self.game_state.screen_shake_timer -= dt
            if self.game_state.screen_shake_timer > 0:
                intensity = self.game_state.screen_shake_intensity * (self.game_state.screen_shake_timer / 0.3)
                self.screen_shake_offset = (
                    random.uniform(-intensity, intensity),
                    random.uniform(-intensity, intensity)
                )
            else:
                self.screen_shake_offset = (0.0, 0.0)
    
    
    def _get_zone_multiplier(self, y: float) -> float:
        """Get scoring multiplier based on Y position.
        
        Args:
            y: Y position
            
        Returns:
            Multiplier value
        """
        if y <= ScoringConstants.CLOUD_ZONE_HEIGHT:
            return ScoringConstants.CLOUD_ZONE_MULTIPLIER
        elif y >= self.height - ScoringConstants.GROUND_ZONE_HEIGHT:
            return ScoringConstants.GROUND_ZONE_MULTIPLIER
        else:
            return ScoringConstants.HILL_ZONE_MULTIPLIER
    
    
    
    
    
    
    def _check_bird_strikes(self) -> None:
        """Check for ball-bird collisions and award points."""
        current_time = time.time()
        
        for ball in self.balls:
            # Only count hits if ball is moving fast (was shot, not just bouncing)
            ball_speed = math.sqrt(ball.vx**2 + ball.vy**2)
            if ball_speed < 100:  # Ignore slow-moving balls
                continue
                
            for bird in self.birds[:]:
                # Collision detection
                distance = math.sqrt((ball.x - bird.x)**2 + (ball.y - bird.y)**2)
                collision_distance = ball.radius + BirdConstants.COLLISION_RADIUS
                
                if distance < collision_distance:
                    # Bird hit! Calculate scoring
                    base_points = bird.points
                    
                    # Check for perfect shot (head shot) - closer to bird center
                    is_perfect_shot = distance < collision_distance * 0.5
                    if is_perfect_shot:
                        base_points *= 2
                        self._add_floating_text(bird.x, bird.y - 30, "PERFECT!", Colors.COMBO_FIRE, 48)
                        self._trigger_screen_shake(8)
                    
                    # Apply combo multiplier
                    if self.game_state.combo_count > 0:
                        multiplier = 1 + (self.game_state.combo_count * 0.5)
                        base_points = int(base_points * multiplier)
                    
                    # Award points
                    self.game_state.score += base_points

                    # Award ammo with strategic rewards
                    ammo_reward = bird.balls_reward

                    # Bonus ammo for perfect shots (center hits)
                    distance_from_center = math.sqrt((ball.x - bird.x)**2 + (ball.y - bird.y)**2)
                    if distance_from_center < BirdConstants.COLLISION_RADIUS * 0.3:  # Within 30% of center
                        ammo_reward += 1
                        self._add_floating_text(bird.x, bird.y - 50, "+1 AMMO BONUS!", Colors.GOLD, 24)

                    # Bonus ammo for combo streaks (every 5 hits)
                    if self.game_state.combo_count > 0 and self.game_state.combo_count % 5 == 0:
                        ammo_reward += 1
                        self._add_floating_text(bird.x, bird.y + 50, "STREAK BONUS +1!", Colors.GOLD, 24)

                    # Add ammo with cap enforcement (addiction mechanic: scarcity)
                    if ammo_reward > 0:
                        old_ammo = self.game_state.ammo_count
                        self.game_state.ammo_count = min(self.game_state.ammo_count + ammo_reward, BallConstants.MAX_AMMO)
                        actual_gained = self.game_state.ammo_count - old_ammo
                        if actual_gained > 0:
                            self._add_floating_text(bird.x, bird.y - 70, f"+{actual_gained} AMMO", Colors.BLUE, 28)
                        if self.game_state.ammo_count >= BallConstants.MAX_AMMO:
                            self._add_floating_text(self.width // 2, 150, "MAX AMMO!", Colors.RED, 32)

                    # Update combo system
                    self.game_state.combo_count += 1
                    self.game_state.max_combo = max(self.game_state.max_combo, self.game_state.combo_count)
                    self.game_state.combo_timer = self.game_state.combo_window
                    self.game_state.last_hit_time = current_time
                    self.game_state.miss_count = 0  # Reset miss streak
                    
                    # Visual feedback
                    self._add_floating_text(bird.x, bird.y, f"+{base_points}", Colors.COMBO_FIRE, 36)
                    if self.game_state.combo_count > 1:
                        self._add_floating_text(bird.x, bird.y + 30, 
                                              f"COMBO x{self.game_state.combo_count}!", Colors.COMBO_FIRE, 28)
                    
                    # Remove the bird
                    self.birds.remove(bird)
                    
                    # Add feather particle effect  
                    self._add_feather_particles(bird.x, bird.y)
                    
                    # Screen shake for impact
                    self._trigger_screen_shake(5)
                    
                    # Slow down the ball after hit
                    ball.vx *= 0.6
                    ball.vy *= 0.6
                    break
    
    def _check_pipe_entry(self, ball: Ball) -> None:
        """Check if ball enters the Mario pipe.
        
        Args:
            ball: Ball to check
        """
        pipe_x = self.width - 100
        pipe_y = self.height - 120
        pipe_width = 60
        pipe_top_y = pipe_y
        
        # Check if ball is within pipe opening area
        if (pipe_x <= ball.x <= pipe_x + pipe_width and 
            pipe_top_y <= ball.y <= pipe_top_y + 30):  # Top opening area
            
            # Check if it's a direct shot (no bounces recently)
            direct_shot = ball.consecutive_wall_bounces == 0
            
            points = (ScoringConstants.PIPE_DIRECT_SHOT_BONUS if direct_shot 
                     else ScoringConstants.PIPE_ENTRY_POINTS)
            
            pipe_text = "PIPE ENTRY!" + (" DIRECT SHOT!" if direct_shot else "")
            self._add_floating_text(ball.x, ball.y - 30, pipe_text, 
                                  Colors.ACHIEVEMENT_TEXT, 48)
            
            # "Swallow" the ball by removing it
            if ball in self.balls:
                self.balls.remove(ball)
    
    def _check_slingshot_mastery(self, ball: Ball) -> None:
        """Check for slingshot mastery achievements.
        
        Args:
            ball: Ball that was launched
        """
        launch_power = ball.launch_power
        
        # Perfect Launch: exactly 100% power
        if abs(launch_power - 1.0) < 0.05:  # 5% tolerance
            self._add_floating_text(ball.x, ball.y - 30, "PERFECT LAUNCH!", 
                                  Colors.ACHIEVEMENT_TEXT, 36)
        
        # Gentle Touch: under 20% power that still scores
        elif launch_power < 0.2:
            self._add_floating_text(ball.x, ball.y - 30, "GENTLE TOUCH!", 
                                  Colors.ACHIEVEMENT_TEXT, 36)
    
    def _check_sniper_shot(self, ball1: Ball, ball2: Ball, collision_x: float, collision_y: float) -> None:
        """Check if collision is a sniper shot (direct from launch).
        
        Args:
            ball1: First ball in collision
            ball2: Second ball in collision 
            collision_x: Collision X position
            collision_y: Collision Y position
        """
        current_time = time.time()
        
        # Check if either ball was recently launched and has high speed
        for ball in [ball1, ball2]:
            if (hasattr(ball, 'launch_power') and ball.launch_power > 0.5 and 
                ball.speed > 300 and ball.consecutive_wall_bounces == 0):
                # This looks like a direct sniper shot
                self._add_floating_text(collision_x, collision_y - 40, "SNIPER SHOT!", 
                                      Colors.ACHIEVEMENT_TEXT, 48)
                # Reset launch power to prevent multiple awards
                ball.launch_power = 0
                break
    
    def handle_resize(self, new_width: int, new_height: int) -> None:
        """Handle window resize events.
        
        Args:
            new_width: New window width
            new_height: New window height
        """
        self.width = max(100, new_width)  # Minimum window size
        self.height = max(100, new_height)
        
        # Keep balls in bounds after resize
        for ball in self.balls:
            radius = ball.radius
            ball.x = max(radius, min(ball.x, self.width - radius))
            ball.y = max(radius, min(ball.y, self.height - radius))
    
    def draw(self) -> None:
        """Draw all elements with strategic game visuals."""
        # Apply screen shake offset if active
        screen_offset_x, screen_offset_y = self.screen_shake_offset
        
        # Draw Mario-style background
        self._draw_mario_background()
        
        # Draw fluffy clouds (not gray rectangles anymore)
        self._draw_clouds()
        
        # Draw power-ups with improved visuals (no letters)
        self._draw_powerups()
        
        # Draw birds with different colors based on type
        self._draw_birds()
        
        # Draw wind particles if strong wind
        if self.game_state.wind_strength > 50:
            self._draw_wind_particles()
        
        # Draw feather particles
        self._draw_particles()
        
        # Draw floating text
        self._draw_floating_texts()
        
        # Draw balls with colors and effects
        for ball in self.balls:
            self._draw_ball_with_effects(ball)
        
        # Draw slingshot mechanics
        self._draw_slingshot()
        
        # Draw strategic UI elements
        self._draw_strategic_ui()
        
        pygame.display.flip()
    
    def _draw_clouds(self) -> None:
        """Draw fluffy cloud obstacles."""
        for cloud in self.clouds:
            # Draw fluffy cloud using multiple overlapping circles
            cloud_color = (255, 255, 255)  # Pure white
            shadow_color = (220, 220, 220)  # Light gray for depth
            
            # Cloud is made of multiple circles
            cx = int(cloud.x + cloud.width // 2)
            cy = int(cloud.y + cloud.height // 2)
            
            # Draw shadow circles first (slightly offset)
            shadow_offset = 3
            pygame.draw.circle(self.screen, shadow_color, 
                             (cx - 25 + shadow_offset, cy + shadow_offset), 25)
            pygame.draw.circle(self.screen, shadow_color, 
                             (cx + shadow_offset, cy - 10 + shadow_offset), 30)
            pygame.draw.circle(self.screen, shadow_color, 
                             (cx + 25 + shadow_offset, cy + shadow_offset), 25)
            pygame.draw.circle(self.screen, shadow_color, 
                             (cx - 15 + shadow_offset, cy + 10 + shadow_offset), 20)
            pygame.draw.circle(self.screen, shadow_color, 
                             (cx + 15 + shadow_offset, cy + 10 + shadow_offset), 20)
            
            # Draw main cloud circles
            pygame.draw.circle(self.screen, cloud_color, (cx - 25, cy), 25)
            pygame.draw.circle(self.screen, cloud_color, (cx, cy - 10), 30)
            pygame.draw.circle(self.screen, cloud_color, (cx + 25, cy), 25)
            pygame.draw.circle(self.screen, cloud_color, (cx - 15, cy + 10), 20)
            pygame.draw.circle(self.screen, cloud_color, (cx + 15, cy + 10), 20)
            
            # Add some smaller circles for extra fluffiness
            pygame.draw.circle(self.screen, cloud_color, (cx - 35, cy + 5), 15)
            pygame.draw.circle(self.screen, cloud_color, (cx + 35, cy + 5), 15)
    
    def _draw_powerups(self) -> None:
        """Draw power-ups with distinct visual designs."""
        import math
        
        for powerup in self.power_ups:
            if not powerup.is_active:
                continue
                
            alpha = int(powerup.alpha * 255)
            x, y = int(powerup.x), int(powerup.y)
            
            # Create surface with per-pixel alpha
            powerup_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            
            if powerup.power_type == PowerUpType.MULTIBALL:
                # Three overlapping circles design (magenta)
                color = Colors.POWERUP_MULTIBALL
                # Outer glow
                pygame.draw.circle(powerup_surface, (*color, alpha//3), (25, 25), 22)
                # Main background circle
                pygame.draw.circle(powerup_surface, (*color, alpha//2), (25, 25), 18)
                # Three smaller circles representing multiple balls
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha), (20, 20), 6)
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha), (30, 20), 6)
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha), (25, 28), 6)
                # Small highlights on the balls
                pygame.draw.circle(powerup_surface, (255, 255, 255, min(255, alpha + 50)), (22, 18), 2)
                pygame.draw.circle(powerup_surface, (255, 255, 255, min(255, alpha + 50)), (32, 18), 2)
                pygame.draw.circle(powerup_surface, (255, 255, 255, min(255, alpha + 50)), (27, 26), 2)
                
            elif powerup.power_type == PowerUpType.SLOWMO:
                # Clock design with radiating lines (green)
                color = Colors.POWERUP_SLOWMO
                # Outer glow
                pygame.draw.circle(powerup_surface, (*color, alpha//3), (25, 25), 22)
                # Main circle
                pygame.draw.circle(powerup_surface, (*color, alpha//2), (25, 25), 18)
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha), (25, 25), 14, 2)
                
                # Clock tick marks (8 marks around the circle)
                for i in range(8):
                    angle = i * (2 * math.pi / 8)
                    start_x = 25 + 10 * math.cos(angle)
                    start_y = 25 + 10 * math.sin(angle)
                    end_x = 25 + 13 * math.cos(angle)
                    end_y = 25 + 13 * math.sin(angle)
                    pygame.draw.line(powerup_surface, (255, 255, 255, alpha), 
                                   (start_x, start_y), (end_x, end_y), 2)
                
                # Clock hands
                pygame.draw.line(powerup_surface, (255, 255, 255, alpha), 
                               (25, 25), (25, 15), 3)  # Hour hand
                pygame.draw.line(powerup_surface, (255, 255, 255, alpha), 
                               (25, 25), (30, 20), 2)  # Minute hand
                # Center dot
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha), (25, 25), 3)
                
            elif powerup.power_type == PowerUpType.BIGBALL:
                # Pulsing large circle with inner rings (red)
                color = Colors.POWERUP_BIGBALL
                # Animated pulse effect using time
                pulse = 1.0 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
                radius = int(18 * pulse)
                
                # Outer glow with pulse
                pygame.draw.circle(powerup_surface, (*color, alpha//4), (25, 25), radius + 4)
                # Main circle
                pygame.draw.circle(powerup_surface, (*color, alpha//2), (25, 25), radius)
                # Inner rings for depth
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha//3), (25, 25), radius - 4, 2)
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha//2), (25, 25), radius - 8, 1)
                # Bright center highlight
                pygame.draw.circle(powerup_surface, (255, 255, 255, min(255, alpha + 100)), (23, 22), 4)
                
            elif powerup.power_type == PowerUpType.MAGNET:
                # Magnetic field lines design (blue)
                color = Colors.POWERUP_MAGNET
                # Outer glow
                pygame.draw.circle(powerup_surface, (*color, alpha//3), (25, 25), 22)
                # Main circle
                pygame.draw.circle(powerup_surface, (*color, alpha//2), (25, 25), 18)
                
                # Magnetic field lines radiating outward
                for i in range(12):
                    angle = i * (2 * math.pi / 12)
                    # Inner point
                    inner_x = 25 + 8 * math.cos(angle)
                    inner_y = 25 + 8 * math.sin(angle)
                    # Outer point
                    outer_x = 25 + 15 * math.cos(angle)
                    outer_y = 25 + 15 * math.sin(angle)
                    # Draw line with varying thickness
                    thickness = 3 if i % 3 == 0 else 2
                    pygame.draw.line(powerup_surface, (255, 255, 255, alpha//2), 
                                   (inner_x, inner_y), (outer_x, outer_y), thickness)
                
                # Central magnet core
                pygame.draw.circle(powerup_surface, (255, 255, 255, alpha), (25, 25), 8)
                pygame.draw.circle(powerup_surface, (*color, alpha), (25, 25), 6)
                # North/South poles
                pygame.draw.circle(powerup_surface, (255, 100, 100, alpha), (25, 20), 3)  # North (red)
                pygame.draw.circle(powerup_surface, (100, 100, 255, alpha), (25, 30), 3)  # South (blue)
                
            else:
                # Fallback design
                color = Colors.WHITE
                pygame.draw.circle(powerup_surface, (*color, alpha//2), (25, 25), 18)
                pygame.draw.circle(powerup_surface, (*color, alpha), (25, 25), 15, 3)
            
            # Blit the surface to screen
            self.screen.blit(powerup_surface, (x - 25, y - 25))
    
    def _draw_wind_particles(self) -> None:
        """Draw wind effect particles."""
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height // 2)
            
            # Calculate wind particle movement
            wind_x = math.cos(self.game_state.wind_direction) * 3
            wind_y = math.sin(self.game_state.wind_direction) * 3
            
            # Draw small moving dots
            pygame.draw.circle(self.screen, (200, 200, 255), (int(x + wind_x), int(y + wind_y)), 1)
    
    
    
    
    
    def _draw_strategic_ui(self) -> None:
        """Draw strategic bird hunter UI with all game info."""
        # Score (top center)
        score_text = f"Score: {self.game_state.score}"
        score_font = pygame.font.Font(None, 48)
        score_surface = score_font.render(score_text, True, Colors.SCORE_TEXT)
        score_rect = score_surface.get_rect(center=(self.width // 2, 40))
        self.screen.blit(score_surface, score_rect)
        
        # High score
        if self.game_state.high_score > 0:
            high_score_text = f"Best: {self.game_state.high_score}"
            high_score_font = pygame.font.Font(None, 24)
            high_score_surface = high_score_font.render(high_score_text, True, Colors.HIGH_SCORE_TEXT)
            high_score_rect = high_score_surface.get_rect(center=(self.width // 2, 70))
            self.screen.blit(high_score_surface, high_score_rect)
        
        # Ammo count (prominent, with warning if low)
        ammo_color = Colors.WARNING_RED if self.game_state.ammo_count <= 1 else Colors.SCORE_TEXT
        ammo_text = f"AMMO: {self.game_state.ammo_count}"
        ammo_font = pygame.font.Font(None, 36)
        ammo_surface = ammo_font.render(ammo_text, True, ammo_color)
        self.screen.blit(ammo_surface, (20, 20))
        
        # Flash warning if low on ammo
        if self.game_state.ammo_count <= 1:
            flash_time = time.time() % 1.0
            if flash_time < 0.5:  # Flash every half second
                warning_surface = ammo_font.render("LOW AMMO!", True, Colors.WARNING_RED)
                self.screen.blit(warning_surface, (20, 60))
        
        # Combo counter with fire effect
        if self.game_state.combo_count > 1:
            combo_text = f"COMBO x{self.game_state.combo_count}!"
            combo_font = pygame.font.Font(None, 32)
            combo_surface = combo_font.render(combo_text, True, Colors.COMBO_FIRE)
            self.screen.blit(combo_surface, (20, 100))
        
        # Wave info (top right)
        wave_text = f"Wave {self.game_state.current_wave}"
        wave_font = pygame.font.Font(None, 28)
        wave_surface = wave_font.render(wave_text, True, Colors.ACHIEVEMENT_TEXT)
        self.screen.blit(wave_surface, (self.width - 120, 20))
        
        # Wave timer
        wave_elapsed = time.time() - self.game_state.wave_start_time
        wave_remaining = max(0, self.game_state.wave_duration - wave_elapsed)
        timer_text = f"Next: {int(wave_remaining)}s"
        timer_font = pygame.font.Font(None, 20)
        timer_surface = timer_font.render(timer_text, True, Colors.GRAY)
        self.screen.blit(timer_surface, (self.width - 120, 50))
        
        # Active power-ups (bottom right)
        powerup_y = self.height - 100
        if self.game_state.slowmo_active:
            slowmo_text = "SLOW-MO ACTIVE"
            slowmo_surface = self.font.render(slowmo_text, True, Colors.POWERUP_SLOWMO)
            self.screen.blit(slowmo_surface, (self.width - 180, powerup_y))
            powerup_y -= 25
        
        if self.game_state.multiball_active:
            multi_text = "MULTIBALL READY"
            multi_surface = self.font.render(multi_text, True, Colors.POWERUP_MULTIBALL)
            self.screen.blit(multi_surface, (self.width - 180, powerup_y))
            powerup_y -= 25
            
        if self.game_state.bigball_active:
            big_text = "BIG BALL READY"
            big_surface = self.font.render(big_text, True, Colors.POWERUP_BIGBALL)
            self.screen.blit(big_surface, (self.width - 180, powerup_y))
            powerup_y -= 25
            
        if self.game_state.magnet_active:
            magnet_text = "MAGNET ACTIVE"
            magnet_surface = self.font.render(magnet_text, True, Colors.POWERUP_MAGNET)
            self.screen.blit(magnet_surface, (self.width - 180, powerup_y))
        
        # Wind indicator
        if self.game_state.wind_strength > 30:
            wind_text = f"Wind: {int(self.game_state.wind_strength)}"
            wind_surface = self.small_font.render(wind_text, True, Colors.GRAY)
            self.screen.blit(wind_surface, (20, self.height - 40))
        
        # Game over screen
        if self.game_state.is_game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = "GAME OVER"
            game_over_font = pygame.font.Font(None, 72)
            game_over_surface = game_over_font.render(game_over_text, True, Colors.WARNING_RED)
            game_over_rect = game_over_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(game_over_surface, game_over_rect)
            
            # Final score
            final_score_text = f"Final Score: {self.game_state.score}"
            final_score_surface = self.font.render(final_score_text, True, Colors.WHITE)
            final_score_rect = final_score_surface.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(final_score_surface, final_score_rect)
            
            # Restart instruction
            restart_text = "Press R to restart"
            restart_surface = self.small_font.render(restart_text, True, Colors.GRAY)
            restart_rect = restart_surface.get_rect(center=(self.width // 2, self.height // 2 + 30))
            self.screen.blit(restart_surface, restart_rect)
        
        # Instructions (bottom left)
        if not self.game_state.is_game_over:
            instruction_text = "Click to aim and shoot!"
            instruction_font = pygame.font.Font(None, 24)
            instruction_surface = instruction_font.render(instruction_text, True, Colors.ACHIEVEMENT_TEXT)
            self.screen.blit(instruction_surface, (20, self.height - 80))
        
        # Pause indicator (only when paused)
        if self.paused:
            pause_font = pygame.font.Font(None, 48)
            pause_surface = pause_font.render("PAUSED", True, Colors.ACCENT)
            pause_rect = pause_surface.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(pause_surface, pause_rect)
    
    def _draw_mario_background(self) -> None:
        """Draw Mario-style pixelated background."""
        # Sky gradient
        for y in range(self.height):
            gradient_factor = y / self.height
            r = int(Colors.SKY_BLUE_LIGHT[0] + (Colors.SKY_BLUE_DARK[0] - Colors.SKY_BLUE_LIGHT[0]) * gradient_factor)
            g = int(Colors.SKY_BLUE_LIGHT[1] + (Colors.SKY_BLUE_DARK[1] - Colors.SKY_BLUE_LIGHT[1]) * gradient_factor)
            b = int(Colors.SKY_BLUE_LIGHT[2] + (Colors.SKY_BLUE_DARK[2] - Colors.SKY_BLUE_LIGHT[2]) * gradient_factor)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
        
        # Pixelated clouds
        self._draw_pixelated_clouds()
        
        # Hills
        self._draw_pixelated_hills()
        
        # Ground/floor
        floor_y = self.height - 40
        pygame.draw.rect(self.screen, Colors.HILL_GREEN, (0, floor_y, self.width, 40))
        
        # Pixelated bushes
        self._draw_pixelated_bushes()
        
        # Mario pipes
        self._draw_mario_pipes()
    
    def _draw_pixelated_clouds(self) -> None:
        """Draw fluffy background clouds."""
        cloud_positions = [(100, 80), (300, 60), (600, 90), (450, 100)]
        
        for x, y in cloud_positions:
            # Draw fluffy clouds using circles
            cloud_color = (255, 255, 255, 200)  # White with some transparency
            shadow_color = (230, 230, 230)
            
            # Create a surface for the cloud with alpha
            cloud_surface = pygame.Surface((120, 60), pygame.SRCALPHA)
            
            # Draw shadow circles
            pygame.draw.circle(cloud_surface, shadow_color, (25, 35), 18)
            pygame.draw.circle(cloud_surface, shadow_color, (50, 30), 22)
            pygame.draw.circle(cloud_surface, shadow_color, (75, 35), 18)
            pygame.draw.circle(cloud_surface, shadow_color, (40, 40), 15)
            pygame.draw.circle(cloud_surface, shadow_color, (60, 40), 15)
            
            # Draw main cloud circles
            pygame.draw.circle(cloud_surface, cloud_color, (25, 32), 18)
            pygame.draw.circle(cloud_surface, cloud_color, (50, 27), 22)
            pygame.draw.circle(cloud_surface, cloud_color, (75, 32), 18)
            pygame.draw.circle(cloud_surface, cloud_color, (40, 37), 15)
            pygame.draw.circle(cloud_surface, cloud_color, (60, 37), 15)
            
            # Extra fluffy bits
            pygame.draw.circle(cloud_surface, cloud_color, (15, 35), 12)
            pygame.draw.circle(cloud_surface, cloud_color, (85, 35), 12)
            
            # Blit the cloud to the screen
            self.screen.blit(cloud_surface, (x, y))
    
    def _draw_pixelated_hills(self) -> None:
        """Draw Mario-style hills."""
        # Simple hill shape in the background
        hill_y = self.height - 120
        hill_points = [
            (50, self.height - 40),
            (100, hill_y),
            (200, hill_y),
            (250, self.height - 40)
        ]
        if len(hill_points) > 2:
            pygame.draw.polygon(self.screen, Colors.HILL_GREEN, hill_points)
        
        # Second hill
        hill2_points = [
            (400, self.height - 40),
            (450, hill_y + 20),
            (550, hill_y + 20),
            (600, self.height - 40)
        ]
        if len(hill2_points) > 2:
            pygame.draw.polygon(self.screen, Colors.HILL_DARK_GREEN, hill2_points)
    
    def _draw_pixelated_bushes(self) -> None:
        """Draw simple pixelated bushes."""
        bush_positions = [(150, self.height - 60), (450, self.height - 55)]
        for x, y in bush_positions:
            # Simple bush pixels
            bush_pixels = [
                (0, 2), (1, 2), (2, 2),
                (0, 1), (1, 1), (2, 1),
                (1, 0)
            ]
            for px, py in bush_pixels:
                pixel_size = 6
                pygame.draw.rect(self.screen, Colors.BUSH_GREEN,
                               (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
    
    def _draw_mario_pipes(self) -> None:
        """Draw Mario-style pipes."""
        pipe_x = self.width - 100
        pipe_y = self.height - 120
        pipe_width = 60
        pipe_height = 80
        
        # Main pipe body
        pygame.draw.rect(self.screen, Colors.PIPE_GREEN,
                        (pipe_x, pipe_y, pipe_width, pipe_height))
        
        # Pipe top (wider)
        pygame.draw.rect(self.screen, Colors.PIPE_DARK_GREEN,
                        (pipe_x - 8, pipe_y, pipe_width + 16, 20))
        
        # Pipe highlights for 3D effect
        pygame.draw.rect(self.screen, Colors.WHITE,
                        (pipe_x + 5, pipe_y + 20, 4, pipe_height - 20))
        
        # Draw pipe scoring zone indicator
        scoring_zone_rect = pygame.Rect(pipe_x, pipe_y, pipe_width, 30)
        # Removed scoring zone indicator for minimal design
        
        # Pipe is functional for gameplay scoring
    
    def _draw_ball_with_effects(self, ball: Ball) -> None:
        """Draw a ball with shadow, 3D highlight effects, and squish factor.
        
        Args:
            ball: Ball to render
        """
        x, y = int(ball.x), int(ball.y)
        radius = int(ball.radius * ball.squish_factor)
        
        # Draw shadow for depth
        shadow_pos = (x + DisplayConstants.SHADOW_OFFSET, 
                     y + DisplayConstants.SHADOW_OFFSET)
        pygame.draw.circle(self.screen, Colors.SHADOW_COLOR, shadow_pos, radius)
        
        # Draw main ball with potential squish effect
        if ball.state == BallState.GRABBED:
            # Draw squished ball (ellipse)
            squish_radius = int(radius * BallConstants.SQUISH_FACTOR)
            pygame.draw.ellipse(self.screen, ball.color,
                              (x - radius, y - squish_radius, radius * 2, squish_radius * 2))
        else:
            pygame.draw.circle(self.screen, ball.color, (x, y), radius)
        
        # Add highlight for 3D effect
        highlight_color = self._calculate_highlight_color(ball.color)
        highlight_radius = radius // BallConstants.HIGHLIGHT_DIVISOR
        highlight_pos = (x - highlight_radius, y - highlight_radius)
        pygame.draw.circle(self.screen, highlight_color, highlight_pos, highlight_radius)
    
    def _calculate_highlight_color(self, base_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Calculate highlight color for 3D effect.
        
        Args:
            base_color: Base color RGB tuple
            
        Returns:
            Highlight color RGB tuple
        """
        return tuple(min(255, c + 80) for c in base_color)
    
    
    def _update_fps(self) -> None:
        """Update FPS calculation."""
        self._frame_count += 1
        current_time = pygame.time.get_ticks() / 1000.0
        
        if current_time - self._last_fps_update >= 1.0:
            self._current_fps = self._frame_count
            self._frame_count = 0
            self._last_fps_update = current_time
    
    
    
    
    
    def handle_events(self) -> bool:
        """Handle pygame events.
        
        Returns:
            False if should quit, True otherwise
        """
        for event in pygame.event.get():
            if not self._handle_event(event):
                return False
        return True
    
    def _handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a single pygame event.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            False if should quit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False
        
        elif event.type == pygame.KEYDOWN:
            return self._handle_keydown(event)
        
        elif event.type == pygame.VIDEORESIZE:
            self._handle_resize_event(event)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up(event)
        
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        
        return True
    
    def _handle_keydown(self, event: pygame.event.Event) -> bool:
        """Handle keyboard input events.
        
        Args:
            event: Keyboard event
            
        Returns:
            False if should quit, True otherwise
        """
        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            return False
        elif event.key == pygame.K_r:
            self.reset_game()
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key == pygame.K_b:
            # Toggle between sprite and emoji birds only
            if self.bird_mode == 'emoji':
                self.bird_mode = 'sprite'
            else:
                self.bird_mode = 'emoji'
            print(f"Bird mode switched to: {self.bird_mode}")
        
        return True
    
    def _handle_resize_event(self, event: pygame.event.Event) -> None:
        """Handle window resize events.
        
        Args:
            event: Resize event
        """
        self.handle_resize(event.w, event.h)
        self.screen = pygame.display.set_mode(
            (event.w, event.h), pygame.RESIZABLE
        )
    
    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        """Handle mouse button down events.
        
        Args:
            event: Mouse button down event
        """
        if event.button != 1:  # Only handle left clicks
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)
        
        # Check if game is over
        if self.game_state.is_game_over:
            return
        
        # Check if clicking on existing ball for slingshot
        clicked_ball = self._find_ball_at_position(mouse_x, mouse_y)
        if clicked_ball:
            self._start_slingshot(clicked_ball, mouse_x, mouse_y)
        else:
            # Try to create a new ball at mouse position if ammo available
            if self.game_state.ammo_count > 0 and not self.dragging_ball:
                new_ball = self.create_ball_for_shooting(mouse_x, mouse_y)
                if new_ball:
                    self.balls.append(new_ball)
                    self._start_slingshot(new_ball, mouse_x, mouse_y)
    
    def _handle_mouse_up(self, event: pygame.event.Event) -> None:
        """Handle mouse button up events.
        
        Args:
            event: Mouse button up event
        """
        if event.button != 1:  # Only handle left clicks
            return
        
        if self.dragging_ball:
            self._release_slingshot()
    
    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Handle mouse motion events.
        
        Args:
            event: Mouse motion event
        """
        self.mouse_pos = pygame.mouse.get_pos()
        
        # Check if mouse button is still held down
        mouse_buttons = pygame.mouse.get_pressed()
        if not mouse_buttons[0]:  # Left mouse button not pressed
            if self.dragging_ball:
                self._release_slingshot()
        elif self.dragging_ball and self.drag_start_pos:
            self._update_slingshot_drag()
    
    def _find_ball_at_position(self, x: float, y: float) -> Optional[Ball]:
        """Find ball at given position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Ball at position or None
        """
        for ball in self.balls:
            if ball.contains_point(x, y):
                return ball
        return None
    
    def _start_slingshot(self, ball: Ball, mouse_x: float, mouse_y: float) -> None:
        """Start slingshot interaction with a ball.
        
        Args:
            ball: Ball to grab
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
        """
        self.dragging_ball = ball
        # Store the MOUSE position as the slingshot anchor point for better ground launches
        # This allows upward shots even when ball is on ground
        self.drag_start_pos = (mouse_x, mouse_y)
        ball.state = BallState.GRABBED
        ball.vx = 0  # Stop ball motion while dragging
        ball.vy = 0
    
    def _update_slingshot_drag(self) -> None:
        """Update ball position during slingshot drag."""
        if not self.dragging_ball or not self.drag_start_pos:
            return
        
        # Get current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)
        
        # Ball follows mouse directly
        self.dragging_ball.x = mouse_x
        self.dragging_ball.y = mouse_y
        
        # Constrain to screen bounds
        radius = self.dragging_ball.radius
        self.dragging_ball.x = max(radius, min(self.dragging_ball.x, self.width - radius))
        self.dragging_ball.y = max(radius, min(self.dragging_ball.y, self.height - radius))
        
        # Update squish factor based on drag distance
        start_x, start_y = self.drag_start_pos
        drag_distance = math.sqrt((mouse_x - start_x)**2 + (mouse_y - start_y)**2)
        squish = max(0.7, 1.0 - (drag_distance / BallConstants.SLINGSHOT_MAX_DRAG_DISTANCE) * 0.3)
        self.dragging_ball.squish_factor = squish
    
    def _release_slingshot(self) -> None:
        """Release the slingshot and launch the ball."""
        if not self.dragging_ball or not self.drag_start_pos:
            return
        
        # Get starting position (where we clicked initially)
        start_x, start_y = self.drag_start_pos
        
        # Get current mouse position for launch calculation
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate launch velocity based on mouse drag, not ball position
        # This allows proper upward shots even when ball is on ground
        dx = start_x - mouse_x
        dy = start_y - mouse_y
        
        # Debug print
        print(f"Launch: start=({start_x:.0f},{start_y:.0f}) current=({mouse_x:.0f},{mouse_y:.0f}) velocity=({dx:.0f},{dy:.0f})")
        
        drag_distance = math.sqrt(dx**2 + dy**2)
        
        # Only fire if there's enough drag (prevent accidental shots)
        if drag_distance < 10:
            # Not enough drag, just reset without firing
            self.dragging_ball.state = BallState.NORMAL
            self.dragging_ball.squish_factor = 1.0
            self.dragging_ball = None
            self.drag_start_pos = None
            return
        
        # Apply velocity based on drag distance
        force_multiplier = min(drag_distance / BallConstants.SLINGSHOT_MAX_DRAG_DISTANCE, 1.0)
        launch_force = force_multiplier * BallConstants.SLINGSHOT_MAX_FORCE
        
        if drag_distance > 0:
            # Normalize and apply force
            self.dragging_ball.vx = (dx / drag_distance) * launch_force
            self.dragging_ball.vy = (dy / drag_distance) * launch_force
        
        # Fire the ball (consumes ammo)
        self.fire_ball(self.dragging_ball, force_multiplier)
        
        # Mark ball as launched so it can be removed later when it stops
        self.dragging_ball.has_been_launched = True
        
        # Reset ball state
        self.dragging_ball.state = BallState.NORMAL
        self.dragging_ball.squish_factor = 1.0
        
        # Clear slingshot state
        self.dragging_ball = None
        self.drag_start_pos = None
    
    def _draw_slingshot(self) -> None:
        """Draw slingshot mechanics visual feedback."""
        if not self.dragging_ball or not self.drag_start_pos:
            return
        
        start_x, start_y = self.drag_start_pos
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ball_x, ball_y = self.dragging_ball.x, self.dragging_ball.y
        
        # Draw slingshot line from start to current ball position
        pygame.draw.line(self.screen, Colors.SLINGSHOT_LINE,
                        (int(start_x), int(start_y)), (int(ball_x), int(ball_y)), 3)
        
        # Draw trajectory prediction based on mouse position for accurate preview
        self._draw_trajectory_prediction(start_x, start_y, mouse_x, mouse_y)
        
        # Draw power meter based on mouse drag distance
        self._draw_power_meter(start_x, start_y, mouse_x, mouse_y)
    
    def _draw_trajectory_prediction(self, start_x: float, start_y: float, 
                                  current_x: float, current_y: float) -> None:
        """Draw predicted trajectory line.
        
        Args:
            start_x: Slingshot start X position (initial click)
            start_y: Slingshot start Y position (initial click)
            current_x: Current mouse X position
            current_y: Current mouse Y position
        """
        # Calculate predicted velocity based on mouse position
        dx = start_x - current_x
        dy = start_y - current_y
        drag_distance = math.sqrt(dx**2 + dy**2)
        
        if drag_distance == 0:
            return
        
        force_multiplier = min(drag_distance / BallConstants.SLINGSHOT_MAX_DRAG_DISTANCE, 1.0)
        launch_force = force_multiplier * BallConstants.SLINGSHOT_MAX_FORCE
        
        pred_vx = (dx / drag_distance) * launch_force
        pred_vy = (dy / drag_distance) * launch_force
        
        # Draw dotted trajectory from ball's actual position
        points = []
        dt = 0.05  # Time step for prediction
        # Start from the ball's current position for accurate trajectory
        if self.dragging_ball:
            x, y = self.dragging_ball.x, self.dragging_ball.y
        else:
            x, y = start_x, start_y
        vx, vy = pred_vx, pred_vy
        
        for i in range(20):  # Predict 20 points ahead
            points.append((int(x), int(y)))
            
            # Simple physics prediction
            vx *= PhysicsConstants.AIR_FRICTION
            vy = vy * PhysicsConstants.AIR_FRICTION + PhysicsConstants.GRAVITY * dt
            x += vx * dt
            y += vy * dt
            
            # Stop if hit boundaries
            if x < 0 or x > self.width or y > self.height:
                break
        
        # Draw dotted line
        for i in range(0, len(points) - 1, 2):  # Skip every other point for dotted effect
            if i + 1 < len(points):
                pygame.draw.line(self.screen, Colors.TRAJECTORY_LINE, points[i], points[i + 1], 2)
    
    def _draw_collision_effects(self) -> None:
        """Draw visual effects for ball collisions."""
        for x, y, time_remaining in self.collision_flashes:
            # Calculate flash intensity based on remaining time
            intensity = min(1.0, time_remaining / 0.1)  # Fade over 0.1 seconds
            alpha = int(255 * intensity)
            
            # Create a temporary surface for the flash effect
            flash_radius = int(15 * (1.0 + (0.3 - time_remaining) * 2))  # Expanding circle
            
            # Draw expanding ring effect
            if flash_radius > 0 and alpha > 0:
                # Create color with fade effect
                flash_color = (min(255, 255), min(255, 200), min(255, 100))  # Yellow-white
                
                # Draw multiple rings for better effect
                for ring in range(3):
                    ring_radius = flash_radius - ring * 3
                    if ring_radius > 0:
                        ring_alpha = alpha // (ring + 1)
                        if ring_alpha > 20:  # Only draw if visible enough
                            pygame.draw.circle(self.screen, flash_color, 
                                             (int(x), int(y)), ring_radius, 2)
    
    def _draw_power_meter(self, start_x: float, start_y: float, 
                         current_x: float, current_y: float) -> None:
        """Draw power meter showing launch force.
        
        Args:
            start_x: Slingshot start X position (initial click)
            start_y: Slingshot start Y position (initial click)
            current_x: Current mouse X position
            current_y: Current mouse Y position
        """
        drag_distance = math.sqrt((start_x - current_x)**2 + (start_y - current_y)**2)
        power_ratio = min(drag_distance / BallConstants.SLINGSHOT_MAX_DRAG_DISTANCE, 1.0)
        
        # Power meter dimensions
        meter_x = 10
        meter_y = self.height - 50
        meter_width = 200
        meter_height = 20
        
        # Background
        pygame.draw.rect(self.screen, Colors.POWER_METER_BACKGROUND,
                        (meter_x, meter_y, meter_width, meter_height))
        
        # Power fill
        fill_width = int(meter_width * power_ratio)
        pygame.draw.rect(self.screen, Colors.POWER_METER_FILL,
                        (meter_x, meter_y, fill_width, meter_height))
        
        # Border
        pygame.draw.rect(self.screen, Colors.WHITE,
                        (meter_x, meter_y, meter_width, meter_height), 2)
        
        # Power text
        power_text = f"Power: {int(power_ratio * 100)}%"
        text_surface = self.small_font.render(power_text, True, Colors.WHITE)
        self.screen.blit(text_surface, (meter_x, meter_y - 25))
    
    def _spawn_birds_if_needed(self) -> None:
        """Spawn birds at random intervals."""
        current_time = time.time()
        if current_time - self.last_bird_spawn >= self.next_bird_spawn_delay:
            self._spawn_bird()
            self.last_bird_spawn = current_time
            self.next_bird_spawn_delay = random.uniform(
                BirdConstants.SPAWN_INTERVAL_MIN, 
                BirdConstants.SPAWN_INTERVAL_MAX
            )
    
    def _spawn_bird(self) -> None:
        """Spawn a new bird with strategic type selection."""
        # Determine bird type based on spawn rates and current wave
        rand = random.randint(1, 100)
        
        # Increase rare bird spawn rate with higher waves
        wave_bonus = min(self.game_state.current_wave * 2, 20)
        
        if rand <= BirdConstants.REGULAR_SPAWN_RATE:
            bird_type = BirdType.REGULAR
        elif rand <= BirdConstants.REGULAR_SPAWN_RATE + BirdConstants.GOLDEN_SPAWN_RATE:
            bird_type = BirdType.GOLDEN
        elif rand <= BirdConstants.REGULAR_SPAWN_RATE + BirdConstants.GOLDEN_SPAWN_RATE + BirdConstants.ANGRY_SPAWN_RATE:
            bird_type = BirdType.ANGRY
        else:
            bird_type = BirdType.RARE
            
        # Apply wave bonus to rare birds
        if rand > (100 - wave_bonus) and self.game_state.current_wave > 2:
            bird_type = BirdType.RARE
        
        # Random direction (left to right or right to left)
        direction = random.choice([1, -1])
        
        # Start position based on direction
        if direction == 1:  # Flying left to right
            start_x = -BirdConstants.BIRD_WIDTH
        else:  # Flying right to left
            start_x = self.width + BirdConstants.BIRD_WIDTH
        
        # Random height in upper portion of screen
        flight_height = random.randint(
            BirdConstants.FLIGHT_HEIGHT_MIN,
            min(BirdConstants.FLIGHT_HEIGHT_MAX, self.height // 3)
        )
        
        # Adjust flight height for different bird types
        if bird_type == BirdType.RARE:
            flight_height = max(50, flight_height - 50)  # Rare birds fly higher
        elif bird_type == BirdType.ANGRY:
            flight_height = min(self.height // 2, flight_height + 30)  # Angry birds fly lower
            
        bird = Bird(
            x=float(start_x),
            y=float(flight_height),
            direction=direction,
            base_y=float(flight_height),
            start_time=time.time(),
            bird_type=bird_type
        )
        
        self.birds.append(bird)
        
        # Apply slowmo effect if active
        if self.game_state.slowmo_active:
            # Birds move at half speed during slowmo
            pass  # Handled in bird update method
    
    def _update_birds(self, dt: float) -> None:
        """Update bird positions and animations with type-specific behaviors.
        
        Args:
            dt: Delta time in seconds
        """
        current_time = time.time()
        
        # Apply slowmo effect
        effective_dt = dt * 0.5 if self.game_state.slowmo_active else dt
        
        # Update each bird
        for bird in self.birds[:]:
            # Get speed for this bird type
            speed = bird.speed
            
            # Update position based on type
            if bird.bird_type == BirdType.ANGRY:
                # Zigzag pattern for angry birds
                flight_time = current_time - bird.start_time
                zigzag_offset = math.sin(flight_time * BirdConstants.ANGRY_ZIGZAG_FREQUENCY) * BirdConstants.ANGRY_ZIGZAG_AMPLITUDE
                bird.x += bird.direction * speed * effective_dt
                bird.y = bird.base_y + zigzag_offset
                
            elif bird.bird_type == BirdType.RARE and bird.dodging:
                # Dodging behavior for rare birds
                dodge_time = current_time - bird.dodge_start_time
                if dodge_time < 1.0:  # Dodge for 1 second
                    # Erratic movement
                    dodge_x = math.sin(dodge_time * 10) * 20
                    dodge_y = math.cos(dodge_time * 8) * 15
                    bird.x += bird.direction * speed * effective_dt * 0.7 + dodge_x * effective_dt
                    bird.y = bird.base_y + dodge_y
                else:
                    # Stop dodging
                    bird.dodging = False
                    bird.x += bird.direction * speed * effective_dt
                    
            else:
                # Regular movement
                bird.x += bird.direction * speed * effective_dt
                
                # Add subtle sine wave motion for regular and golden birds
                flight_time = current_time - bird.start_time
                sine_amplitude = BirdConstants.SINE_AMPLITUDE
                if bird.bird_type == BirdType.GOLDEN:
                    sine_amplitude *= 1.5  # Golden birds have more pronounced wave
                    
                sine_offset = math.sin(flight_time * BirdConstants.SINE_FREQUENCY) * sine_amplitude
                bird.y = bird.base_y + sine_offset
            
            # Update wing animation
            wing_frame_duration = 1.0 / BirdConstants.WING_ANIMATION_SPEED
            flight_time = current_time - bird.start_time
            bird.wing_frame = int((flight_time / wing_frame_duration) % 3)
        
        # Remove birds that have flown off screen
        self.birds = [bird for bird in self.birds if bird.is_active]
    
    def _draw_birds(self) -> None:
        """Draw all active birds."""
        for bird in self.birds:
            self._draw_bird(bird)
    
    def _get_rainbow_color(self, offset: float = 0) -> Tuple[int, int, int]:
        """Generate rainbow colors based on time.
        
        Args:
            offset: Phase offset for creating different colors
            
        Returns:
            RGB color tuple
        """
        import time
        import math
        
        # Use time to animate through rainbow
        t = time.time() * 2 + offset  # Speed of color change
        
        # Generate RGB values using sine waves
        r = int((math.sin(t) + 1) * 127.5)
        g = int((math.sin(t + 2.094) + 1) * 127.5)  # 2.094 = 2π/3
        b = int((math.sin(t + 4.189) + 1) * 127.5)  # 4.189 = 4π/3
        
        return (r, g, b)
    
    def _draw_bird(self, bird: Bird) -> None:
        """Draw a bird using the selected rendering mode with rainbow colors.
        
        Args:
            bird: Bird to draw
        """
        x, y = int(bird.x), int(bird.y)
        
        # Get rainbow color for this bird (use bird.x as offset for variety)
        rainbow_color = self._get_rainbow_color(bird.x * 0.01)
        
        # Mode 1: Sprite-based birds with animated wings
        if self.bird_mode == 'sprite' and self.bird_sprite_right:
            # Draw bird body from sprite
            sprite = self.bird_sprite_right if bird.direction == 1 else self.bird_sprite_left
            
            # Animate wings by drawing them separately
            # Bird body with rainbow color
            body_rect = pygame.Rect(x - 40, y - 20, 80, 40)
            pygame.draw.ellipse(self.screen, rainbow_color, body_rect)
            # Darker outline for contrast
            outline_color = tuple(max(0, c - 50) for c in rainbow_color)
            pygame.draw.ellipse(self.screen, outline_color, body_rect, 2)
            
            # Animated wings based on bird.wing_frame
            wing_offset = [-10, 0, 10][bird.wing_frame]  # Up, middle, down
            
            # Left wing with complementary rainbow color
            wing_color = self._get_rainbow_color(bird.x * 0.01 + 1.57)  # Phase shift for contrast
            left_wing = pygame.Rect(x - 50, y - 10 + wing_offset, 35, 20)
            pygame.draw.ellipse(self.screen, wing_color, left_wing)
            
            # Right wing
            right_wing = pygame.Rect(x + 15, y - 10 + wing_offset, 35, 20)
            pygame.draw.ellipse(self.screen, wing_color, right_wing)
            
            # Head with same rainbow color as body
            pygame.draw.circle(self.screen, rainbow_color, 
                             (x + 20 if bird.direction == 1 else x - 20, y - 5), 15)
            
            # Beak
            if bird.direction == 1:
                beak_points = [(x + 35, y), (x + 50, y - 3), (x + 50, y + 3)]
            else:
                beak_points = [(x - 35, y), (x - 50, y - 3), (x - 50, y + 3)]
            pygame.draw.polygon(self.screen, Colors.BIRD_BEAK, beak_points)
            
            # Eye
            eye_x = x + 25 if bird.direction == 1 else x - 25
            pygame.draw.circle(self.screen, Colors.WHITE, (eye_x, y - 5), 6)
            pygame.draw.circle(self.screen, Colors.BLACK, (eye_x + 2 if bird.direction == 1 else eye_x - 2, y - 5), 3)
            
            return
        
        # Mode 2: Emoji birds (fun and simple)
        if self.bird_mode == 'emoji' and self.emoji_font:
            # Different bird emojis to choose from
            bird_emojis = ['🦅', '🦆', '🐦', '🦜', '🦢', '🕊️']
            # Use eagle for now
            emoji = bird_emojis[0]  # Eagle emoji
            
            # Render the emoji
            bird_surface = self.emoji_font.render(emoji, True, (0, 0, 0))
            
            # Flip if flying left
            if bird.direction == -1:
                bird_surface = pygame.transform.flip(bird_surface, True, False)
            
            # Center the emoji on the bird position
            bird_rect = bird_surface.get_rect(center=(x, y))
            self.screen.blit(bird_surface, bird_rect)
            return
        
        # Mode 3: Fallback to geometric birds
        # Bird dimensions
        body_width = 60
        body_height = 40
        wing_width = 30
        wing_height = 20
        
        # Draw bird body (oval shape) with rainbow color
        body_rect = pygame.Rect(x - body_width//2, y - body_height//2, body_width, body_height)
        pygame.draw.ellipse(self.screen, rainbow_color, body_rect)
        # Darker outline for contrast
        outline_color = tuple(max(0, c - 50) for c in rainbow_color)
        pygame.draw.ellipse(self.screen, outline_color, body_rect, 3)
        
        # Draw wings based on animation
        wing_offset = 8 * (bird.wing_frame - 1)  # -8, 0, or 8 pixels
        
        # Left wing with complementary rainbow color
        wing_color = self._get_rainbow_color(bird.x * 0.01 + 1.57)  # Phase shift
        left_wing = pygame.Rect(x - body_width//2 - 15, y - 10 + wing_offset, wing_width, wing_height)
        pygame.draw.ellipse(self.screen, wing_color, left_wing)
        
        # Right wing with same complementary color
        right_wing = pygame.Rect(x + body_width//2 - 15, y - 10 + wing_offset, wing_width, wing_height)
        pygame.draw.ellipse(self.screen, wing_color, right_wing)
        
        # Draw head circle with rainbow color
        head_radius = 18
        pygame.draw.circle(self.screen, rainbow_color, 
                          (x + 15 if bird.direction == 1 else x - 15, y - 10), head_radius)
        
        # Draw beak (triangle)
        if bird.direction == 1:  # Flying right
            beak_points = [(x + body_width//2, y),
                          (x + body_width//2 + 20, y - 5),
                          (x + body_width//2 + 20, y + 5)]
        else:  # Flying left
            beak_points = [(x - body_width//2, y),
                          (x - body_width//2 - 20, y - 5),
                          (x - body_width//2 - 20, y + 5)]
        pygame.draw.polygon(self.screen, Colors.BIRD_BEAK, beak_points)
        
        # Draw eye (white circle with black pupil)
        eye_x = x + 20 if bird.direction == 1 else x - 20
        eye_y = y - 10
        pygame.draw.circle(self.screen, Colors.WHITE, (eye_x, eye_y), 8)
        pygame.draw.circle(self.screen, Colors.BLACK, (eye_x + 2 if bird.direction == 1 else eye_x - 2, eye_y), 4)
        
        # Draw tail feathers
        tail_x = x - 25 if bird.direction == 1 else x + 25
        for i in range(3):
            tail_points = [(tail_x - 5 + i*5, y),
                          (tail_x - 10 + i*5, y + 15),
                          (tail_x + i*5, y + 10)]
            pygame.draw.polygon(self.screen, Colors.BIRD_WING, tail_points)
    
    def _draw_floating_texts(self) -> None:
        """Draw floating score texts."""
        for text in self.floating_texts:
            alpha = int(text.alpha * 255)
            if alpha > 0:
                try:
                    # Create font surface
                    if text.font_size <= 24:
                        font = self.small_font
                    elif text.font_size <= 36:
                        font = self.font
                    elif text.font_size <= 48:
                        font = self.score_font
                    else:
                        font = self.big_font
                    
                    text_surface = font.render(text.text, True, text.color)
                    
                    # Apply alpha if supported
                    if alpha < 255:
                        text_surface.set_alpha(alpha)
                    
                    # Center the text
                    text_rect = text_surface.get_rect(center=(int(text.x), int(text.y)))
                    self.screen.blit(text_surface, text_rect)
                except Exception:
                    # Fallback for font issues
                    pass
    
    def _draw_particles(self) -> None:
        """Draw feather particle effects."""
        for particle in self.particles:
            alpha = int(particle.alpha * 255)
            if alpha > 0:
                try:
                    # Draw feather as small ellipse
                    size = max(1, int(particle.size * particle.alpha))
                    pygame.draw.ellipse(self.screen, particle.color, 
                                       (int(particle.x - size), int(particle.y - size//2), 
                                        size * 2, size))
                except Exception:
                    # Fallback - draw as circle
                    pygame.draw.circle(self.screen, particle.color, 
                                     (int(particle.x), int(particle.y)), max(1, particle.size))
    
    
    
    def run(self) -> None:
        """Main simulation loop."""
        print("🎯 RICOCHET HUNTER - Make Every Shot Count! 🎯")
        print("=" * 50)
        print("📢 GAME MECHANICS (BALANCED FOR ADDICTIVE GAMEPLAY!):")
        print("   • Ammo System: Start with 3 shots, MAX 8 ammo (resource scarcity!)")
        print("   • Max 3 balls on screen - timing matters!")
        print("   • Bird Rewards: Brown(0 ammo), Gold(+1), Red(0), Blue(+2) - hunt gold!")
        print("   • Skill Bonuses: Perfect center shot (+1 ammo), 5-hit streak (+1)")
        print("   • Combos: Chain hits for multiplier bonuses")
        print("   • Miss Penalty: 3 misses in a row = LOSE 1 ammo! ⚠️")
        print("   • Perfect Shots: Hit bird center for 2x points + bonus ammo")
        print("📢 CONTROLS:")
        print("   • Click & Drag: Aim and shoot")
        print("   • R: Reset game  • SPACE: Pause  • ESC/Q: Quit")
        print("=" * 50)
        print("🚀 Starting game... Good luck, hunter!")
        
        try:
            self._main_loop()
        except Exception as e:
            print(f"❌ Game error: {e}")
            raise
        finally:
            self._cleanup()
    
    def _main_loop(self) -> None:
        """Execute the main simulation loop."""
        running = True
        last_time = pygame.time.get_ticks() / 1000.0
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Calculate frame delta time
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - last_time
            last_time = current_time
            
            # Update simulation
            self.update_physics(dt)
            
            # Update slingshot drag if active
            if self.dragging_ball:
                # Check if mouse button is still held down
                mouse_buttons = pygame.mouse.get_pressed()
                if not mouse_buttons[0]:  # Left mouse button not pressed
                    self._release_slingshot()
                else:
                    self._update_slingshot_drag()
            
            # Render frame
            self.draw()
            
            # Maintain target framerate
            self.clock.tick(DisplayConstants.TARGET_FPS)
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        pygame.quit()
        print(f"🎯 GAME FINISHED!")
        print(f"📊 Final Score: {self.game_state.score}")
        print(f"🏆 High Score: {self.game_state.high_score}")
        if self.game_state.max_combo > 1:
            print(f"🔥 Best Combo: {self.game_state.max_combo}x")
        print("Thanks for playing Strategic Bird Hunter!")


def test_collision_detection() -> None:
    """Test ball collision detection and physics."""
    print("Testing collision detection...")
    
    # Create test balls - overlapping for collision test
    ball1 = Ball(x=100, y=100, vx=50, vy=0, radius=25, color=Colors.RED)
    ball2 = Ball(x=140, y=100, vx=-50, vy=0, radius=25, color=Colors.BLUE)  # 40px apart, radii sum to 50
    ball3 = Ball(x=200, y=200, vx=0, vy=0, radius=25, color=Colors.GREEN)
    
    # Test collision detection
    assert ball1.is_colliding_with(ball2), "Balls should be colliding (40px apart, combined radius 50px)"
    assert not ball1.is_colliding_with(ball3), "Balls should not be colliding"
    
    # Test distance calculation
    distance = ball1.distance_to_ball(ball2)
    assert abs(distance - 40) < 0.1, f"Distance should be 40, got {distance}"
    
    distance_far = ball1.distance_to_ball(ball3)
    expected_distance = math.sqrt((200-100)**2 + (200-100)**2)  # ~141.42
    assert abs(distance_far - expected_distance) < 0.1, f"Distance should be ~141.42, got {distance_far}"
    
    print("✓ All collision detection tests passed!")


def main() -> None:
    """Main function to run the bouncing ball simulation."""
    # Run tests if --test argument is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_collision_detection()
        return
        
    try:
        simulation = BouncingBallSimulation()
        simulation.run()
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure pygame is installed: pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()