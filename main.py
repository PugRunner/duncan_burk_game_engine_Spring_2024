# This filed created by: Duncan Burk
# Github is now listening
# Imports pygame as pg and imports settings code

'''
moving enemies
killing enemies
players and enemies can shot
'''

import pygame as pg 
from settings import *
from sprite import *
from random import randint
from os import path
# created object class of game
class Game():
   # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        # loads map in map.txt
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.fake_walls = pg.sprite.Group()
        self.teleports = pg.sprite.Group()
        self.dones = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):d
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    print("A player at", row, col)
                    self.player1 = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 's':
                    Sheild(self, col, row)
                if tile == 'p':
                    PowerUp(self, col, row)
                if tile == 'F':
                    FakeWall(self, col, row)
                if tile == 't':
                    Teleport(self, col, row)
                if tile == 'd':
                    Done(self, col, row)
    # def run
    def run(self):
    # game lopp
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    # Lets you quit
    def update(self):
        self.all_sprites.update()
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
            self.draw_text(self.screen, str(self.player1.moneybag), 64, WHITE, 1, 1)
            pg.display.flip()
    # Lets you do events of movement/quiting
        # dx+1 is down
        # dx-1 is up
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player1.move(dx=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_d:
            #         self.player1.move(dx=+1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_s:
            #         self.player1.move(dy=+1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_w:
            #         self.player1.move(dy=-1)
# def g as game
g = Game()
# use run method to start things
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()