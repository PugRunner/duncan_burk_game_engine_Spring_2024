# This file was created by: Duncan Burk
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from random import randint
import math
from pygame.sprite import Sprite
from os import path


dir = path.dirname(__file__)
img_dir = path.join('images')
SPRITESHEET = "theBell.png"

# player shield class
class Shield(pg.sprite.Sprite):
    def __init__(self, game, x, y):
            self.groups = game.all_sprites
            # init super class
            Sprite.__init__(self)
            self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
            self.load_images()
            self.image = self.standing_frames[0]
            self.game = game
            global SheildSize
            SheildSize = self.image = pg.Surface((SHEILDX, SHEILDY))
            self.image.fill(LIGHTBLUE)
            self.rect = self.image.get_rect()
            self.vx = 0
            self.vy = 0
            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.jumping = False
            self.walking = False
            self.current_frame = 0
            self.last_update = 0
            self.moneybag = 0
            self.speed = 200
            self.hitpoints = 100
            self.gem = 1
            self.death = 0
            self.life = 10
            self.end = 0
    
    def respawn(self):
        # Set player's position to a respawn point
        self.rect.x = RESPAWN_X
        self.rect.y = RESPAWN_Y 
    
    # def key presses for movement and player speed
    def get_keys(self):
        self.vx = 0 
        self.vy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED

        # Set the shield size and fill color outside of the key checks
        ShieldSize = pg.Surface((SHEILDX, SHEILDY))
        ShieldSize.fill(LIGHTBLUE)

        # Update the player image and rect based on shield size
        if self.vx < 0:
            self.image = pg.transform.flip(ShieldSize, True, False)
        elif self.vx > 0:
            self.image = ShieldSize
        elif self.vy < 0:
            self.image = pg.transform.rotate(ShieldSize, 90)
        elif self.vy > 0:
            self.image = pg.transform.rotate(ShieldSize, -90)
    
        # make dialong speed slower
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0
            self.vy *= 0
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

    # ddef what happens when things collides
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Gem":
                self.gem += 1
            if str(hits[0].__class__.__name__) == "Done":
                self.end += 1
            if str(hits[0].__class__.__name__) == "Mob":
                self.life -= 1
                self.death += 1
                self.x = RESPAWN_X * TILESIZE
                self.y = RESPAWN_Y * TILESIZE
            if str(hits[0].__class__.__name__) == "Sideway":
                self.life -= 1
                self.death += 1
                self.x = RESPAWN_X * TILESIZE
                self.y = RESPAWN_Y * TILESIZE
            if str(hits[0].__class__.__name__) == "PowerUp":
                    global SheildSize 
                    SheildSize = self.image = pg.Surface((BIGTILESIZE, BIGTILESIZE))
                    self.image.fill(GREEN)
                    self.rect = self.image.get_rect()
            if str(hits[0].__class__.__name__) == "Teleport":
                    self.x =525
                    self.y =50

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
                              self.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
        self.jump_frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
                    
                

    
    # def player size and Speed
    def update(self):
        self.get_keys()
        self.animate()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        #defines collision with walls
        self.collide_with_walls('x') 
        self.collide_with_walls('y')
        # Does collision for everything 
        self.rect.y = self.y
        self.rect.x = self.x 
        # def collision for up happens for everything
        if self.collide_with_group(self.game.fake_walls, True):
            pass
        if self.collide_with_group(self.game.dones, True):
            # quits game
            self.quit()
        if self.collide_with_group(self.game.teleports, True):
            # moves player to 525, 50
            self.x =525
            self.y =50
        if self.collide_with_group(self.game.gems, True):
            # gives player more gem
            self.gem += 1
        if self.collide_with_group(self.game.power_ups, True):
                    # makes player bigger
                    global PlayerSize
                    PlayerSize = self.image = pg.Surface((BIGTILESIZE, BIGTILESIZE))
                    self.image.fill(GREEN)
                    self.rect = self.image.get_rect()
                    # self.vx, self.vy = 0, 0
                    # self.x *BIGTILESIZE
                    # self.y *BIGTILESIZE
        if self.collide_with_group(self.game.mobs, True):
            self.quit
        if self.collide_with_group(self.game.sideways, True):
            self.quit

                    


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

# def coin class
class Gem(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.gems
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# def a done game class
class Done(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.dones
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# break able walls
class FakeWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.fake_walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# teleport block
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

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.mobs)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, -180)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vy = 15

    def update(self):
        self.rect.y += self.vy
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1
            self.image = pg.transform.rotate(self.image, -180)


    
# Up down mob
            # Thx chatgpt for making hitbox a circle
class Sideway(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.sideways)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, -90)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx = 15

    def update(self):
        self.rect.x += self.vx
        if self.rect.right <= 0 or self.rect.left >= WIDTH:
            self.vx *= -1
            self.image = pg.transform.rotate(self.image, 180)

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image
    