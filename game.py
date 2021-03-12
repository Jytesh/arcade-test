# Basic arcade shooter

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Platformer"
SCALING = 2.0

PLAYER_SCALING = 0.4
TILE_SCALING = 2

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
JUMP_SPEED = 25
class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds
    """

    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it
        """

        # Move the sprite
        super().update()

        # Remove if off the screen
        if self.right < 0:
            self.remove_from_sprite_lists()


class Platformer(arcade.Window):
    def __init__(self, width, height, title):
        """Initialize the game
        """
        super().__init__(width, height, title)
        self.start_game()
    def start_game(self):
        game_view = gameView()
        self.show_view(game_view)

class gameView(arcade.View):
    def on_show(self):
        self.setup()
    def on_draw(self):
        arcade.start_render()
        self.tile_list.draw()
        self.platform_list.draw()
        self.sprites.draw()

    def setup(self):
        """Get the game ready to play
        """
        self.paused = False
        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)


        # Set up the empty sprite lists
        self.sprites = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Set up the player
        self.player = arcade.Sprite('images/geometry.png', PLAYER_SCALING)
        self.player.center_y = self.window.height / 2 - 76
        self.player.center_x = self.player.width * PLAYER_SCALING + 20
        self.sprites.append(self.player)
        self.previous_left = self.player.left

        self.visible_tiles = 0
        self.draw_tiles(0)
        for x in range(0, 64 * 10, 64):
            platform = arcade.SpriteSolidColor(64, 64, arcade.color.SKY_BLUE)
            platform.center_x = x
            platform.center_y = self.window.height / 2 - 76 - 64
            self.platform_list.append(platform)
        self.viewed_levels = 0
        self.last_level_x = 640
        self.last_level_y = 0
        (self.last_level_x, self.last_level_y) = self.generate_level(self.last_level_x, self.last_level_y, 128)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_list, GRAVITY)

    def on_key_press(self, key, modifiers):
        if self.physics_engine.can_jump():
            self.player.change_y = JUMP_SPEED
    
    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.paused:
            return

        self.player.change_x = PLAYER_MOVEMENT_SPEED
        # Move the player with the physics engine
        self.physics_engine.update()

        if self.player.left == self.previous_left:
            self.end()
            return 
        else:
            self.previous_left = self.player.left 
        if not self.physics_engine.can_jump():
            self.player.angle -= 2.2
        else:
            self.player.angle = self.player.angle - self.player.angle % 90
        if self.player.bottom <= 100:
            self.end()

        self.view_left +=  PLAYER_MOVEMENT_SPEED

        self.visible_tiles += PLAYER_MOVEMENT_SPEED
        self.viewed_levels += PLAYER_MOVEMENT_SPEED
        if self.visible_tiles > 64 * 1000:
            self.visible_tiles = 0
            self.draw_tiles(self.view_left)
        if self.viewed_levels > 128 * 64:
            self.viewed_levels = 0
            (self.last_level_x, self.last_level_y) = self.generate_level(self.last_level_x, self.last_level_y, 128)

        self.window.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)

    def draw_tiles(self, start):
        for x in range(start, 64 * 1000 + start, 64):
            tile = arcade.Sprite("images/tiles/hex.jpeg", TILE_SCALING)
            tile.center_x = x
            tile.center_y = self.window.height / 2
            self.tile_list.append(tile)     

    def generate_level(self, start, lastLevel, iters):
        start_y = lastLevel
        last_level_x = start
        for i in range(0, iters):
            x = random.randint(2,6) * 64 # Calculate length of platform
            y = start_y + random.randint(-1,1)
            platform = arcade.SpriteSolidColor(x, 64, arcade.color.SKY_BLUE)
            platform.left = start
            platform.bottom = 194 + y * 64
            start += x
            last_level_y = y
            last_level_x += x
            self.platform_list.append(platform)
        return (last_level_x, last_level_y)

    def end(self):
        self.window.show_view(endView())
class endView(arcade.View):
    def __init__(self):
        super().__init__()
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.RED_DEVIL)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Game ended!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press any button to restart!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_key_press(self, key, mods):
        self.window.start_game()


if __name__ == "__main__":
    app = Platformer(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
