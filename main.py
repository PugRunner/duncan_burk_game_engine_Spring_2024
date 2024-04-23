import pygame as pg
from settings import *  # Make sure all required constants are defined in settings.py
from sprite import *  # Assuming sprite.py contains the sprite classes
from os import path
import sys


'''

Realease virson idea, 
get coins form beating levels and be able to use those coins to gamable

'''


# Import mixer module for playing sounds
from pygame import mixer

# defines levels
LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
LEVEL3 = "level3.txt"
LEVEL4 = "level4.txt"

# heart beat done by Chapt GPT
mixer.init()
heartbeat_sound = mixer.Sound(path.join('sounds', 'heartbeat.wav'))

class Timer:
    def __init__(self):
        self.start_time = pg.time.get_ticks() / 1000  # Store the start time
        self.remaining_time = 60  # Set the initial remaining time to 60 seconds

    def ticking(self):
        elapsed_time = pg.time.get_ticks() / 1000 - self.start_time  # Calculate elapsed time
        self.remaining_time = max(0, self.remaining_time - elapsed_time)  # Calculate remaining time

    def start_timer(self, duration):
        self.remaining_time = duration
        self.start_time = pg.time.get_ticks() / 1000  # Reset the start time

    def is_finished(self):
        return self.remaining_time <= 0

class Game:
    # Allows us to assign properties to the class
    def __init__(self):
        # makes it so that first level is 1 so that code easier to keep track of level
        self.current_level = 1
        # initialize the last update time
        self.last_update = pg.time.get_ticks()
        #  initialize pygame
        pg.init()
        # When run, create a screen with the widths from settings and height from settings and called "Title" from settings.
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting Game Clock
        self.clock = pg.time.Clock()
        # game clock
        self.timer = Timer()
        self.shield_duration = 0  
        self.shield_active = False
        self.life_duration = 1800  # 60 is about 2 second
        self.life_timer = Timer()
        self.life = 0
        # loads data
        self.load_data()
        # defines data for leel 1 file
        self.last_update = pg.time.get_ticks()  # Initialize last_update here

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        #    actually sprites
        self.mob_img = pg.image.load(path.join(self.img_folder, 'red_triangle.png.ico')).convert_alpha()
        self.circle_img = pg.image.load(path.join(self.img_folder, 'red_circle.png')).convert_alpha()
        self.map_data = []
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # def way to change level
    def change_level(self, lvl):
        for s in self.all_sprites:
            s.kill()
        self.map_data = []
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                self.map_data.append(line.strip())
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'd':
                    Done(self, col, row)
                if tile == 'G':
                    Gem(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    Sideway(self, col, row)
        # Reset the timer when changing levels
        self.timer.start_timer(LEVEL_DURATION)
        # Check if the current level is level 3
        self.shield = Shield(self, RESPAWN_X, RESPAWN_Y)
        # Incrementing the current level should come after setting the spawn point
        self.current_level += 1

    # Create run method which runs the whole GAME
    def new(self):
        # loads all sprites
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gems = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.fake_walls = pg.sprite.Group()
        self.teleports = pg.sprite.Group()
        self.dones = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.sideways = pg.sprite.Group()
        # gives player a spawn point
        self.shield = Shield(self, RESPAWN_X, RESPAWN_Y)
        # player timer
        self.timer.start_timer(60)  # Start the timer at 60 seconds
        self.shield_active = True
        # life timer
        self.life_timer.start_timer(self.life_duration)
        # Set self.life after shield initialization
        self.life = self.shield.life
        # load classes
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'G':
                    Gem(self, col, row)
                if tile == 's':
                    Shield(self, col, row)
                if tile == 'F':
                    FakeWall(self, col, row)
                if tile == 't':
                    Teleport(self, col, row)
                if tile == 'd':
                    Done(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
                if tile == "U":
                    Sideway(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            # Calculate elapsed time since the last update
            current_time = pg.time.get_ticks()
            elapsed_time = (current_time - self.last_update) / 1000  # Convert to seconds

            # Update the last update time
            self.last_update = current_time

            # Set fps
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            self.reder_screen()

            # Decrease display timer by elapsed time
            self.timer.remaining_time -= elapsed_time

            # Check if the display timer has reached 0
            if self.timer.remaining_time <= 0:
                self.timer.remaining_time = 0  # Ensure the timer doesn't go negative
                # Handle any actions when the timer reaches 0

            # Play heartbeat sound
            heartbeat_sound.set_volume(0.5)  # Adjust the volume as needed
            heartbeat_rate = max(0.5, 1.0 - self.timer.remaining_time / 60.0)  # Heartbeat rate increases as time decreases
            heartbeat_sound.set_rate(heartbeat_rate)
            heartbeat_sound.play()

    # def quit so you can quit
    def quit(self):
        pg.quit()
        sys.exit()

    # def updates in game 
    def update(self):
        # Calculate the elapsed time since the last update call
        elapsed_time = pg.time.get_ticks() - self.last_update
        self.last_update = pg.time.get_ticks()

        self.all_sprites.update()
        if self.shield.gem == 2:
            if self.current_level == 1:
                self.change_level(LEVEL2)
            elif self.current_level == 2:
                self.change_level(LEVEL3)
            elif self.current_level == 3:
                self.change_level(LEVEL4)
            else:
                # Handle end of the game or additional levels
                self.playing = False
        if self.shield.life == 0:
            self.show_death_screen()
        if self.shield.end == 1:
            self.show_end_screen()
        if self.shield_active:
            self.timer.ticking()
            if self.timer.is_finished():
                self.shield_active = False
                # Start life timer when shield expires
                self.life_timer.start_timer(self.life_duration)
        else:
            self.life_timer.ticking()
            if self.life_timer.is_finished():
                self.shield.life -= 10
                # Restart life timer and shield timer when a life is lost
                self.life_timer.start_timer(self.life_duration)
                self.timer.start_timer(LEVEL_DURATION)

    # Draws lines to form a grid
    def draw_grid(self):
        pass

    # def text font
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    # makes screen render when player dies
    def reder_screen(self):
        global BGCOLOR
        BGCOLOR = (0 + 15*self.shield.death, 0, 0)

    # def draw for different events
    # def draw for different events
    def draw(self):
        self.screen.fill(BGCOLOR)
        # Draw countdown timer in the top left corner
        # Removed display of timer
        self.all_sprites.draw(self.screen)
        if self.shield.death == 1:
            self.draw_text(self.screen, "Imagine Dying " + str(self.shield.death) + " Time On Level " + str(self.current_level), 32, WHITE, 11, 1)
        if self.shield.death > 1:
            self.draw_text(self.screen, "Imagine Dying " + str(self.shield.death) + " Times On Level " + str(self.current_level), 32, WHITE, 11, 1)
        if self.shield.life == 1:
            self.draw_text(self.screen, str(self.shield.life) + " Life left", 32, WHITE, 1, 1)
        if self.shield.life > 1:
            self.draw_text(self.screen, str(self.shield.life) + " Lives Left", 32, WHITE, 1, 1)
        if self.shield_active:
            # Draw shield UI or anything related to an active shield
            pass
        pg.display.flip()

    # lets start screen stay up till button pressed
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press ANY button to start", 64, WHITE, 7, 10)
        pg.display.flip()
        self.wait_for_key()

    # same for start screen just for death screen
    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press ANY button to start AGAIN", 64, WHITE, 4.5, 10)
        pg.display.flip()
        self.wait_for_key_death()

    # same as those above
    def show_end_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "good job you beat this game", 64, WHITE, 6, 8)
        self.draw_text(self.screen, "Press ANY button to start again", 64, RED, 5, 10)
        pg.display.flip()
        self.wait_for_key_death()

    # def what wait for key is and what actions to take
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.draw_text(self.screen, "Clicking is NOT pressing a BUTTON", 64, RED, 3, 13)
                    pg.display.flip()

    # def what wait for key is and what actions to take
    def wait_for_key_death(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN:
                    waiting = False
                    self.change_level(LEVEL1)
                    self.current_level = 1
                    self.new()  # Start a new game
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.draw_text(self.screen, "Clicking is NOT pressing a BUTTON", 64, RED, 3, 13)
                    pg.display.flip()
                
    # Lets you do events of movement/quitting
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

# Define the duration of each level (in seconds)
LEVEL_DURATION = 300  # 5 minutes

# def g as game
g = Game()
# use run method to start things
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
