import os
import json
import pygame as pg
from settings import *
from os import path
import sys
from sprite import *
print("Current working directory:", os.getcwd())



# Import mixer module for playing sounds
from pygame import mixer

# Define level filenames as constants
LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
LEVEL3 = "level3.txt"
LEVEL4 = "level4.txt"


class Timer:
    def __init__(self, duration_ms=60000):
        self.duration = duration_ms
        self.start_time = None

    def start_timer(self):
        self.start_time = pg.time.get_ticks()

    def ticking(self):
        if self.start_time is not None:
            elapsed_time = pg.time.get_ticks() - self.start_time
            self.remaining_time = max(0, self.duration - elapsed_time)

    def is_finished(self):
        return self.remaining_time <= 0

class Game:
    def __init__(self):
        self.current_level = 1
        self.last_update = pg.time.get_ticks()  # Initialize last_update with current time
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.timer = Timer(LEVEL_DURATION * 1000)
        self.shield_duration = 0  
        self.shield_active = False
        self.life_duration = 20000
        self.life_timer = Timer()
        self.life = 0
        self.shield = None  # Initialize shield attribute
        global max_life
        max_life = 10  # Adjust starting max life to 10
        self.player_data_file = "player_data.json"
        self.load_player_data()  # Call load_player_data after shield is initialized
        self.load_data()  # Move load_data method call to after load_player_data

    def load_player_data(self):
        try:
            with open(self.player_data_file, "r") as f:
                player_data = json.load(f)
                if self.shield is not None:  # Check if shield exists
                    self.shield.max_life = player_data.get("max_life", 10)  # Default max life is 10
        except FileNotFoundError:
            print(f"Player data file '{self.player_data_file}' not found.")

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        mixer.init()
        self.snd_folder = path.join(self.game_folder, 'sounds')
        global heartbeat_sound
        heartbeat_sound = mixer.Sound(path.join(self.snd_folder, 'heartbeat.wav'))
        self.mob_img = pg.image.load(path.join(self.img_folder, 'red_triangle.png.ico')).convert_alpha()
        self.circle_img = pg.image.load(path.join(self.img_folder, 'red_circle.png')).convert_alpha()
        self.map_data = []
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gems = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.fake_walls = pg.sprite.Group()
        self.teleports = pg.sprite.Group()
        self.dones = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.sideways = pg.sprite.Group()
        self.shield = Shield(self, RESPAWN_X, RESPAWN_Y)
        self.timer.start_timer()
        self.shield_active = True
        self.life_timer.start_timer()
        self.life = self.shield.life
        self.shop = Shop(self)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
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
            current_time = pg.time.get_ticks()
            elapsed_time = (current_time - self.last_update) / 1000
            self.last_update = current_time
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            self.reder_screen()
            self.timer.ticking()
            if self.timer.is_finished():
                self.timer.remaining_time = 0
            heartbeat_sound.set_volume(0.5)
            heartbeat_rate = max(60, 1.0 - self.timer.remaining_time)
            heartbeat_sound.set_volume(heartbeat_rate)
            heartbeat_sound.play()
            
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
        self.timer.start_timer()
        self.shield = Shield(self, RESPAWN_X, RESPAWN_Y)
        self.current_level += 1

    def after_level_complete(self):
        self.shield.coins += 1
        self.shop.show_shop_screen()

    def purchase_item(self, item):
        # Logic for purchasing items...
        if item == "life_increase":
            if self.shield.coins >= 10: 
                self.shield.max_life += 1
                self.shield.life += 1 
                self.shield.coins -= 10
                # Save player data after increasing maximum life
                self.save_player_data()
                return True  # Return True if item was successfully purchased
            else:
                return False  # Return False if max life is already reached or coins are insufficient
        elif item == "life_duration_increase":
            # Implement logic for increasing life duration
            self.life_duration += 10000  # Increase life duration by 10 seconds
            return True  # Return True if item was successfully purchased
        elif item == "mob_speed_potation":
            self.increase_mob_speed_potation()  # Call the method to increase mob speed
            return True
        elif item == "player_speed_potation":
            self.increase_player_speed_potation()  # Call the method to increase player speed
            return True
        else:
            # Handle other items or invalid item names
            return False  # Return False if item purchase failed or invalid item named


        
        
    def increase_mob_speed_potation(self):
        # Implement the second random event here
        global ENEMY_SPEED
        ENEMY_SPEED = 250

    def increase_player_speed_potation(self):
        # Implement the second random event here
        global PLAYER_SPEED
        PLAYER_SPEED = 2500


    def save_player_data(self):
        player_data = {"max_life": self.shield.max_life}
        with open(self.player_data_file, "w") as f:
            json.dump(player_data, f)


    


    def update(self):
        elapsed_time = pg.time.get_ticks() - self.last_update
        self.last_update = pg.time.get_ticks()
        self.all_sprites.update()
        if self.shield.gem == 2:
            if self.current_level == 1:
                self.change_level(LEVEL2)
                self.after_level_complete()
            elif self.current_level == 2:
                self.change_level(LEVEL3)
                self.after_level_complete()
            elif self.current_level == 3:
                self.change_level(LEVEL4)
                self.after_level_complete()
            else:
                self.playing = False
        if self.shield.life == 0:
            self.show_death_screen()
        if self.shield.end == 1:
            self.show_end_screen()
        if self.shield_active:
            self.timer.ticking()
            if self.timer.is_finished():
                self.shield_active = False
                self.life_timer.start_timer(self.life_duration)
        else:
            self.life_timer.ticking()
            if self.life_timer.is_finished():
                self.shield.life -= 10
                self.life_timer.start_timer(self.life_duration)
                self.timer.start_timer(LEVEL_DURATION)
        if self.purchase_item("life_increase"):
            # Check if player hasn't reached the max life already
            self.shield.life += 1
            if self.shield.life > self.shield.max_life:  # Access max_life from Shield object
                self.shield.life = self.shield.max_life
        if self.purchase_item("life_duration_increase"):
            self.life_duration += 10000
        if self.purchase_item("mob_speed_potation"):
            global ENEMY_SPEED
            ENEMY_SPEED = 250
        if self.purchase_item("player_speed_potation"):
            global PLAYER_SPEED
            PLAYER_SPEED = 2500


    def draw_grid(self):
        pass

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def reder_screen(self):
        global BGCOLOR
        BGCOLOR = (0 + 15*self.shield.death, 0, 0)

    def draw(self):
        self.screen.fill(BGCOLOR)
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
            pass
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press ANY button to start", 64, WHITE, 7, 10)
        pg.display.flip()
        self.wait_for_key()

    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press ANY button to start AGAIN", 64, WHITE, 4.5, 10)
        pg.display.flip()
        self.wait_for_key_death()

    def show_end_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "good job you beat this game", 64, WHITE, 6, 8)
        self.draw_text(self.screen, "Press ANY button to start again", 64, RED, 5, 10)
        pg.display.flip()
        self.wait_for_key_death()

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
                    self.new()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.draw_text(self.screen, "Clicking is NOT pressing a BUTTON", 64, RED, 3, 13)
                    pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

# Define the duration of each level (in seconds)
LEVEL_DURATION = 300  # 5 minutes

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
