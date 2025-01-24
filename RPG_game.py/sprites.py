
from config import *
import pygame
import sys
import math
import random

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert() #loads image faster 

    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height)) #third parameter creates cutout of the multple sprites
        sprite.set_colorkey(BLACK)
        return sprite
    
class  Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y,name,level,health,strength,defense,inventory,move_list,xp):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = name
        self.level = level
        self._health = health
        self._strength = strength
        self._inventory = inventory
        self._defense = defense
        self.move_list = move_list
        self.xp = xp 
        print(self.name)

        #times all the x and y values by the tile size which is 32x32
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        #gets image from return value of sprite
        self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
        #sprites need a rectangle
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
    def __str__(self):
     return f"{self.name} (Level: {self.level}, Health: {self._health})"

    def attack(self,move):
        #move will have a default amount of damage that it can do, however depending on the strength, it will multiply that move 
        if move in self.move_list:
            damage = self.move_list[move]
            if self._strength <= 3:
                damage = damage * 1
            elif self._strength <= 6:
                damage = damage * 1.15
            else:
                damage = damage *1.25
        #print(f'{damage}')
            return round(damage) 
        
    def take_damage(self, amount):
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        if amount == 0:
            print("No damage to process.")
            return self._health
        if self._defense < 3:
            amount = round(amount * 1)
        elif self._defense > 3 and self._defense < 7:
            amount = round(amount * 0.90)
        else:
            amount = round(amount * 0.85)
        self._health = max(0, self._health - amount)
        return self._health
    
    def level_up(self):
        #use level then distribute to strength and defenese
        self.level += 1
        self.level = min(self.level,10)
        self._health = self._health + 10
        self._health = min(self._health, 100)
        if self.level % 2 == 0:
            self._defense += 1
            self._strength += 1
        elif self.level % 2 == 1:
            rand = random.randint(1,2)
            if rand == 1:
                self._defense +=1
            else:
                self._strength += 1
        #print(f"Returning: {self.level, self._defense, self._strength}")
        return self.level
    

    def return_name(self):
        return self.name
    def return_inventory(self):
        return self._inventory
    def return_level(self):
        return self.level
    def return_strength(self):
        return self._strength
    def return_defense(self):
        return self._defense
    def return_moves(self):
        return self.move_list
    

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0


    def movement(self):
    
        if self.game.state != 'normal':
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED #changes all other sprites on opposite direction
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED #changes all other sprites on opposite direction
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED#changes all other sprites on opposite direction
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED#changes all other sprites on opposite direction
            self.y_change += PLAYER_SPEED
            self.facing = 'down'


    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            for enemy in hits:
                enemy.grid_pos = (enemy.x//TILESIZE, enemy.y // TILESIZE)
                self.game.defeated_enemies.append(enemy.grid_pos)
                print(self.game.defeated_enemies)
                print(f"Collided with enemy at grid position: {enemy.grid_pos}")
                player = self.return_name()
                print(player)
                self.game.battle_screen(enemy)
        #this will be the place where it puts into a game screen and then will do the rpg battle

    def collide_blocks(self, direction):
       ui = self.game.main_screen_health
       xp_bar = self.game.xp_bar
       if direction == 'x':                                           #checks if you want to delete it it collides
           hits = pygame.sprite.spritecollide(self, self.game.blocks, False) #checks if the rect of one sprite is in the rect of another sprite
           if hits:
               if self.x_change > 0: #changes right
                   self.rect.x = hits[0].rect.left - self.rect.width
                   for sprite in self.game.all_sprites: #if colliding moves camera opposite direction
                       sprite.rect.x += PLAYER_SPEED
                   ui.rect.x -= PLAYER_SPEED
                   xp_bar.rect.x -= PLAYER_SPEED
               if self.x_change < 0: #changes left
                   self.rect.x = hits[0].rect.right
                   for sprite in self.game.all_sprites:
                       sprite.rect.x -= PLAYER_SPEED
                   ui.rect.x += PLAYER_SPEED
                   xp_bar.rect.x += PLAYER_SPEED
       if direction == 'y':
           hits = pygame.sprite.spritecollide(self, self.game.blocks, False) #checks if the rect of one sprite is in the rect of another sprite
           if hits:
               if self.y_change > 0: #changes right
                   self.rect.y = hits[0].rect.top - self.rect.height
                   for sprite in self.game.all_sprites:
                       sprite.rect.y += PLAYER_SPEED
                   ui.rect.y -= PLAYER_SPEED
                   xp_bar.rect.y -= PLAYER_SPEED
               if self.y_change < 0: #changes left
                   self.rect.y = hits[0].rect.bottom
                   for sprite in self.game.all_sprites:
                       sprite.rect.y -= PLAYER_SPEED
                   ui.rect.y += PLAYER_SPEED
                   xp_bar.rect.y += PLAYER_SPEED

                    

    def animate(self):
        
         if self.facing == 'down':
             if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
             else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #changes every 10 frames
                if self.animation_loop >= 3:
                    self.animation_loop = 1

         if self.facing == 'up':
              if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
              else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
         if self.facing == 'left':
              if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
              else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
         if self.facing == 'right':
              if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
              else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self,game, x, y, name, level, health, strength, defense, move_list, loot):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        
        self.name = name
        self.level = level
        self._health = health
        self._strength = strength
        self._defense = defense
        self.move_list = move_list
        self.loot = loot
    
        #times all the x and y values by the tile size which is 32x32
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        
        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7,30)

        #dont need for now
        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]
        #dont need for now
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
    


        self.image = self.game.enemy_spritesheet.get_sprite(3,2, self.width, self.height)
        self.image.set_colorkey(BLACK)
        #sprites need a rectangle
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def __str__(self):
     return f"{self.name} (Level: {self.level}, Health: {self._health})"
    
    def return_name(self):
        return self.name
    def attack(self,move):
        #move will have a default amount of damage that it can do, however depending on the strength, it will multiply that move 
        if move in self.move_list:
            damage = self.move_list[move]
            if self._strength <= 3:
                damage = damage * 1
            elif self._strength <= 6:
                damage = damage * 1.15
            else:
                damage = damage *1.25
        #print(f'{damage}')
            return round(damage) 
        
    def take_damage(self, amount):
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        if amount == 0:
            print("No damage to process.")
            return self._health
        if self._defense < 3:
            amount = round(amount * 1)
        elif self._defense > 3 and self._defense < 7:
            amount = round(amount * 0.90)
        else:
            amount = round(amount * 0.85)
        self._health = max(0, self._health - amount)
        return self._health
    
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
            if self.game.state != 'normal':
                return
            if self.facing == 'left':
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel: #every frame take away from the x change if if its below the negative value of max travel change direction
                    self.facing = 'right'
            if self.facing == 'right':
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel: 
                    self.facing = 'left'
    
    def animate(self):
         
         #dont need for now
         if self.facing == 'down':
             if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
             else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #changes every 10 frames
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            #dont need for now
         if self.facing == 'up':
              if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
              else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
         if self.facing == 'left':
              if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
              else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
         if self.facing == 'right':
              if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
              else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        




class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = 1
        self.groups = self.game.all_sprites
        #calling init method of sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
       
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64,352,self.width,self.height) #uses get_sprite method from the spreadsheet class and then gets it
        #create rectangle boundary from the image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, color, character, type='health'):
        self.game = game
        self._layer = HEALTH_BAR_LAYER
        self.groups = self.game.all_sprites
        #calling init method of sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self. height = height
        self.color = color
        self.character = character
        self.type = type

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
         
        self.font = pygame.font.Font('Hawthorne Vintage.otf', 20)

    def movement(self):
        if self.game.state != 'normal':
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED 
        
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED 

        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
            
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

    

    def update(self):
        self.movement()
        if self.type == 'health':
            current_width = int((self.character._health/100) * self.width)
            self.image.fill(GREY)
            pygame.draw.rect(self.image, self.color , (0,0,current_width, self.height))

            health_text = self.font.render(f"{self.character._health}/100", True, WHITE)
            text_rect = health_text.get_rect(center=(self.width // 2, self.height // 2))
            text_y = self.y - 50
            self.image.blit(health_text, text_rect)
        elif self.type == 'xp':
            current_width = int((self.character.xp/100) * self.width)
            self.image.fill(GREY)
            pygame.draw.rect(self.image, self.color , (0,0,current_width, self.height))

            text = self.font.render(f"{self.character.xp}/100", True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            text_y = self.y - 50
            self.image.blit(text, text_rect)

        pygame.display.update()

class Button:
    def __init__(self, x, y , width, height, fg, bg, content, fontsize, center = True):
        self.font = pygame.font.Font('Hawthorne Vintage.otf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        if center == True:
            self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        else:
            self.text_rect = self.text.get_rect(topleft=(5, self.height / 2 - self.text.get_height() / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    def __repr__(self):
        return self.content

class UI(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, color, character=None):
        self.game = game
        self._layer = UI_LAYER
        self.groups = self.game.all_sprites
        #calling init method of sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
       

        self.x = x
        self.y = y
        self.width = width
        self. height = height
        self.color = color
        self.character = character
       
        self.buttons = []
        self.current_log = "" 

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.main_font = pygame.font.Font('Hawthorne Vintage.otf', 18)
        self.sub_font = pygame.font.Font('Hawthorne Vintage.otf', 13)
    
    
    def add_log(self, message):
        self.current_log = message
    
    def add_buttons(self,var):
        self.buttons = []
        button_width = 100
        button_height = 20

        if isinstance(var, dict):
            for i, (name, move) in enumerate(var.items()):
                button_x = self.x   
                button_y = self.y + 50 + i *  (button_height)  
                pair = f"{name}: {move}"
                button = Button(button_x, button_y, button_width, button_height, WHITE, GREY, pair, 15, center= False)
                self.buttons.append(button)

        elif isinstance(var, list):
            for i, item in enumerate(var):
                button_x = self.x   
                button_y = self.y + 50 + i *  (button_height) 
                string = f"{item}" 
                button = Button(button_x, button_y, button_width, button_height, WHITE, GREY, string, 15, center= False)
                self.buttons.append(button)


                   
        
    def update(self):
        self.image.fill(self.color)
        
        if self.character is not None:
            self.image.fill(GREY)
            pygame.draw.rect(self.image, self.color , (0,0, self.width, self.height))
            player_stats = f"{self.character.name} Level: {self.character.level}"
            player_text = self.main_font.render(player_stats, True, WHITE)
            self.image.blit(player_text, (10, 10)) 

        log_surface = self.sub_font.render(self.current_log, True, WHITE)
        self.image.blit(log_surface, (10, 35))

        for button in self.buttons:
            self.image.blit(button.image,(button.rect.x - self.rect.x, button.rect.y - self.rect.y))


class Item:
   def __init__(self,weapon=None,armor=None,potion=None):
       self._weapon = weapon
       self._armor = armor
       self._potion = potion

   def __str__(self):
       if self._weapon:
           return self._weapon
       elif self._armor:
           return self._armor
       elif self._potion:
           return self._potion
       return "Unknown Item"

   def __repr__(self):
       return self.__str__()
  
   def use(self, target):
       if self._weapon:
           target._strength += 3
       elif self._armor:
           target._defense += 3
       elif self._potion:
           target._health = min(100, target._health +20)
   def ran_out(self, target):
       if self._weapon:
           target._strength -= 3
       elif self._armor:
           target._defense -= 3













