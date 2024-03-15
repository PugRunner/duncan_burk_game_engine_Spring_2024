# This filed created by: Duncan Burk
# Github is now listening
# Imports pygame as pg and imports settings code

'''
change player
projectiles
killing player
'''

import pygame as pg 
from settings import *
from sprite import *
from random import randint
from os import path
import sys

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
class Game:
    # Allows us to assign properties to the class
    def __init__(self):
        self.current_level = 1
        #  initilaize pygame
        pg.init()
        # When run, create a screen with the widths from settings and height from settings and called "Title" from settings.
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting Game Clock
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
       self.game_folder = path.dirname(__file__)
       self.map_data = []
       with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    def test_method(self):
        print("I can be called from Sprites...")
    # added level change method
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
                if tile == 'C':
                    Gem(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'p':
                    PowerUp(self, col, row)
        self.shield = Shield(self, RESPAWN_X, RESPAWN_Y)
        if lvl == LEVEL2:
            # self.playing = False
            self.current_level += 1


    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gems = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.fake_walls = pg.sprite.Group()
        self.teleports = pg.sprite.Group()
        self.dones = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shield = Shield(self, RESPAWN_X, RESPAWN_Y)

        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                # if tile == 'P':
                #     print("A player at", row, col)
                #     self.player1 = Player(self, col, row)
                if tile == 'G':
                    Gem(self, col, row)
                if tile == 's':
                    Shield(self, col, row)
                if tile == 'p':
                    PowerUp(self, col, row)
                if tile == 'F':
                    FakeWall(self, col, row)
                if tile == 't':
                    Teleport(self, col, row)
                if tile == 'd':
                    Done(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
                
    # def run
    def run(self):
        self.playing= True
        while self.playing:
            # Set fps
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()
    
    def update(self):
        self.all_sprites.update()
        if self.shield.gem == 2:
                if self.current_level == 1:
                    self.change_level(LEVEL2)
                else:
                    # Handle end of the game or additional levels
                    self.playing = False
        
    # Draws lines to form a grid
    def draw_grid(self):
        #  for x in range(0, WIDTH, TILESIZE):
        #       pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        #  for y in range(0, HEIGHT, TILESIZE):
        #       pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        pass
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            if self.shield.death == 1:
                self.draw_text(self.screen, "Imaging Dying " + str(self.shield.death) + " Time On Level " + str(self.current_level), 32, WHITE, 11, 1)
            if self.shield.death > 1:
                self.draw_text(self.screen, "Imaging Dying " + str(self.shield.death) + " Times On Level " + str(self.current_level), 32, WHITE, 11, 1)
            if self.shield.life == 1:
                self.draw_text(self.screen, str(self.shield.life) + " Life left", 32, WHITE, 1, 1)
            if self.shield.life > 1:
                self.draw_text(self.screen, str(self.shield.life) + " Lives Left", 32, WHITE, 1, 1)
            pg.display.flip()
    def show_start_screen(self):
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "Press ANY button to start", 64, WHITE, 7, 10)
            pg.display.flip()
            self.wait_for_key()

    def show_death_screen(self):
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "Press ANY button to start AGAIN", 64, WHITE, 7, 10)
            pg.display.flip()
            self.wait_for_key()

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
    # Lets you do events of movement/quiting
        # dx+1 is down
        # dx-1 is up
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
# def g as game
g = Game()
# use run method to start things
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()