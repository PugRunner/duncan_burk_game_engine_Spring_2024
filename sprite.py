# This file was created by: Duncan Burk
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from random import randint
from math import floor
from pygame.sprite import Sprite
from os import path
import random


dir = path.dirname(__file__)
img_dir = path.join(dir,'images')
SPRITESHEET = "theBell.png"


# def Spritesheet to use for animations
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
    
# player shield class
class Shield(pg.sprite.Sprite):
    def __init__(self, game, x, y):
            super().__init__()
            self.groups = game.all_sprites
            # init super class
            pg.sprite.Sprite.__init__(self, self.groups)
            # def atrobutes about shield
            self.game = game
            global SheildSize
            SheildSize = self.image = pg.Surface((SHEILDX, SHEILDY))
            self.rect = self.image.get_rect()
            self.vy = 0
            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.moneybag = 0
            self.speed = PLAYER_SPEED
            self.hitpoints = 10
            self.gem = 1
            self.death = 0
            self.life = 10
            self.end = 0
            self.coins = 0
            self.max_life = 10  # Initial maximum life
            self.life = self.max_life  # Set current life to maximum initially
            self.invincible = False  # Flag to indicate if the player is invincible
            self.invincible_timer = 0  # Timer to track the duration of invincibility

    def update_speed(self):
        self.speed = PLAYER_SPEED

    
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
                

    
    # def player size and Speed
    def update(self):
        self.get_keys()
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
            self.coins += 10
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
            pass
        if self.collide_with_group(self.game.sideways, True):
            pass
        if self.life > self.max_life:
            self.life = self.max_life
        if self.collide_with_group(self.game.mobs, True):  # Check collision with mobs
            if not self.invincible:  # If not invincible, lose a life and become invincible
                self.life -= 1
                self.death += 1
                self.invincible = True  # Set invincible to True
                self.invincible_timer = pg.time.get_ticks()  # Set the start time of invincibility

        # Check if invincibility timer has expired
        if self.invincible and pg.time.get_ticks() - self.invincible_timer > INVINCIBLE_DURATION:
            self.invincible = False  # Reset invincibility after the duration expires
        

                    


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
        self.vy = ENEMY_SPEED

    def update(self):
        self.rect.y += self.vy
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1
            self.image = pg.transform.rotate(self.image, -180)

    def update_speed(self):
        self.vy = ENEMY_SPEED


    
# Up down mob
class Sideway(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.sideways)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, -90)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx = ENEMY_SPEED

    def update(self):
        self.rect.x += self.vx
        if self.rect.right <= 0 or self.rect.left >= WIDTH:
            self.vx *= -1
            self.image = pg.transform.rotate(self.image, 180)

    def update_speed(self):
        self.vx = ENEMY_SPEED

class Timer():
    # sets all properties to zero when instantiated...
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
    # resets event time to zero - cooldown reset
    def get_countdown(self):
        return floor(self.cd)
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt
    # def event_reset(self):
    #     self.event_time = floor((self.game.clock.)/1000)
    # sets current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

class ShieldTimer(Timer):
    def __init__(self):
        super().__init__()


class Shop:
    def __init__(self, game):
        self.game = game
        self.shield = game.shield
        self.mob = game.mobs
        self.available_potions = []

    def random_potions(self):
        potion_types = ["life_increase", "life_duration_increase", "mob_speed_potion", "player_speed_potion"]
        # Randomly select three potions
        self.available_potions = random.sample(potion_types, 3)

    def show_shop_screen(self):
        self.random_potions()  # Regenerate available potions
        self.game.screen.fill(BGCOLOR)
        # Drawing the shop title
        self.game.draw_text(self.game.screen, "Shop", 64, WHITE, 32, 2)
        
        # Vertical position offset for the potions
        start_y = 2
        line_height = 2  # Height between each line of text

        for i, potion in enumerate(self.available_potions):
            self.game.draw_text(self.game.screen, f"{i+1}. {potion.replace('_', ' ').title()}", 32, WHITE, 2, start_y + i * line_height)

        # Instructions for the player
        self.game.draw_text(self.game.screen, "Press 1, 2, or 3 to buy a potion pair, or any key to exit", 32, WHITE, 32, start_y + (len(self.available_potions) + 1) * line_height)

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_1, pg.K_2, pg.K_3]:
                        potion_index = event.key - pg.K_1
                        if potion_index < len(self.available_potions):
                            self.handle_purchase(potion_index)
                            waiting = False
                    else:
                        waiting = False

    def handle_purchase(self, index):
        potion = self.available_potions[index]
        if self.game.purchase_item(potion):
            print(f"Bought {potion}")
            self.available_potions.pop(index)  # Remove the purchased potion from the list
        # After purchasing, transition back to the game
        self.show_shop_screen = False

    def purchase_item(self, item):
        if item == "life_increase":
            if self.game.shield.coins >= 10: 
                self.game.shield.max_life += 1
                self.game.shield.life += 1 
                self.game.shield.coins -= 10
                self.game.save_player_data()
                return True
            else:
                return False
        elif item == "life_duration_increase":
            if self.game.shield.coins >= 10:
                self.game.life_duration += 10000
                self.game.shield.coins -= 10
                return True
        elif item == "mob_speed_potion":
            if self.game.shield.coins >= 10:
                global ENEMY_SPEED
                ENEMY_SPEED += 750
                self.game.shield.coins -= 10
                self.mob.update_speed()
                return True
        elif item == "player_speed_potion":
            if self.game.shield.coins >= 10:
                global PLAYER_SPEED
                PLAYER_SPEED += 6000
                self.game.shield.coins -= 10
                self.shield.update_speed()
                return True
            else:
                return False
        else:
            return False