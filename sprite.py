# This file was created by: Duncan Burk
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *

# defines plapyer class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
            self.groups = game.all_sprites
            # init super class
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            global PlayerSize
            PlayerSize = self.image = pg.Surface((TILESIZE, TILESIZE))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.vx, self.vy = 0, 0
            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.moneybag = 0
            self.spedd = 300
            self.hitpoints = 100
    
    # def key presses for movement and player speed
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        # make dialong speed slower
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # # Def ways to move
    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False

        # Def new collision, hit box in top right
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
                
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Done":
                self.quit()
            if str(hits[0].__class__.__name__) == "PowerUp":
                    global PlayerSize 
                    PlayerSize = self.image = pg.Surface((BIGTILESIZE, BIGTILESIZE))
                    self.image.fill(GREEN)
                    self.rect = self.image.get_rect()
                    # self.vx, self.vy = 0, 0
                    # self.x * BIGTILESIZE
                    # self.y * BIGTILESIZE
            if str(hits[0].__class__.__name__) == "Teleport":
                    self.x =525
                    self.y =50
                    
                
            
    def update(self):
            self.get_keys()
            self.rect.y = self.y
            # collision 
            self.collide_with_walls('y')
            self.collide_with_group(self.game.coins, True)
            self.collide_with_group(self.game.power_ups, True)
            # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
            # if coin_hits:
            #     print("I got a coin")

    
    # def player size
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        #collision
        # walls 
        self.collide_with_walls('x')
        self.rect.y = self.y  
        self.collide_with_walls('y')  
        # gold coins
        if self.collide_with_group(self.game.fake_walls, True):
            pass
        if self.collide_with_group(self.game.dones, True):
            # quits game
            self.quit()
        if self.collide_with_group(self.game.teleports, True):
            # moves player to 525, 50
            self.x =525
            self.y =50
        if self.collide_with_group(self.game.coins, True):
            # gives player more gold
            self.gold += 1
        if self.collide_with_group(self.game.power_ups, True):
                    # makes player bigger
                    global PlayerSize
                    PlayerSize = self.image = pg.Surface((BIGTILESIZE, BIGTILESIZE))
                    self.image.fill(GREEN)
                    self.rect = self.image.get_rect()
                    # self.vx, self.vy = 0, 0
                    # self.x *BIGTILESIZE
                    # self.y *BIGTILESIZE
                    


# def wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class SWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.swalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class NWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.nwalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# def coin class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Done(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.dones
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class FakeWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.fake_walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(FAKEBLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# def power up class
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKRED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        

