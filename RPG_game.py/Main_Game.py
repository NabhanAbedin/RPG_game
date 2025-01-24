
from config import *
import pygame
import sys
import math
import random
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Hawthorne Vintage.otf', 32)
        self.running = True
        self.defeated_enemies = []
        self.gold_sword = Item(weapon='Gold Sword')
        self.iron_armor = Item(armor="Iron Armor")
        self.healing_potion = Item(potion="Healing Potion")
        #creates the variables for the character animations and terrain but doesnt draw them here
        self.character_spritesheet = Spritesheet('/Users/nabhanabedin/Desktop/img/character.png')
        self.terrain_spritesheet = Spritesheet('/Users/nabhanabedin/Desktop/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('/Users/nabhanabedin/Desktop/img/enemy.png')
        self.intro_background = pygame.image.load('/Users/nabhanabedin/Documents/pixelated_blue_background.png')
        self.go_background = pygame.image.load('/Users/nabhanabedin/Desktop/img/gameover.png')
        self.state = 'normal'
        self.turn = True
    def createTilemap(self,normal_map):
        #sees based on the tilemap that if it is b from the enumarate it will get position and place it there
        for i, row in enumerate(normal_map):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == 'B':
                    Block(self,j,i)
                if column == 'P':
                    self.bob =Character(self, j,i, 'bob',1,100,1,1,[],{'Strike': 50,'Bash': 20,'Pierce': 17, 'Run': 'run'},0)
                    #print(f'current xp: {self.bob.xp}')
                   
                    
                    
                   
                if column == 'E':
                   if (j, i) not in self.defeated_enemies:
                    #print(f"Spawning enemy at grid position: ({j}, {i})")
                    #print(f"Enemy pixel position: x = {j * TILESIZE}, y = {i * TILESIZE}")
                    Enemy(self, j, i, "Madara", 1, 100, 1, 1, {"Strike": 15, "Bash": 20}, ["Gold"])
                
                 
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap(tilemap)

        self.main_screen_health = HealthBar(self, 430, 440, 200, 20, RED, self.bob)
        self.xp_bar = HealthBar(self,430, 400, 200, 20, BLUE, self.bob, 'xp' )
        


    
    def events(self):
        #game loop events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    def update(self):
        self.all_sprites.update()

    def draw(self):
       self.screen.fill(BLACK)
       self.all_sprites.draw(self.screen) #refers to the all.sprites method and calls draw method
  
       self.clock.tick(FPS)
       pygame.display.update()


    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.state == 'battle':
                self.battle_update()
            
    

        self.running = False
    def game_over(self):
        loop = True
        text = self.font.render('Game Over', True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        restart_button = Button(10, 10, 120,50, WHITE, BLACK, 'Restart', 32 )

        for sprite in self.all_sprites:
            sprite.kill()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    loop = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

        
    def intro_screen(self):
        intro = True
        title = self.font.render('Sigma Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 70, 100, 50, WHITE, BLACK, 'Play', 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    intro = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
    
    def clear_screen(self):
        for sprite in self.all_sprites:
            sprite.kill()

        self.all_sprites = pygame.sprite.LayeredUpdates()
    # Clear other specific groups if needed
        self.blocks.empty()
        self.enemies.empty()
        self.attacks.empty()

    def battle_screen(self, enemy):
        self.state = 'battle'

        current_health = self.bob._health
        current_level = self.bob.level
        current_xp = self.bob.xp


        self.clear_screen()

        self.createTilemap(battle_map)
        player_health_bar = HealthBar(self, 50, 250, 200, 20, GREEN, self.bob)
        enemy_health_bar = HealthBar(self, 370, 250, 200, 20, RED, enemy)
        self.player_ui = UI(self, 50, 275, 215,200, GREY, character=self.bob)
        self.log_ui = UI(self, 370, 275, 200,50,GREY)

        self.current_enemy = enemy

        self.bob._health = current_health
        self.bob.level = current_level
        self.bob.xp = current_xp
        
        #log_ui.add_log('hello')
       
    def battle_update(self):
        self.events()
        count = 0
        used_items = []
        
        items = self.bob._inventory
        moves = self.bob.move_list
        enemy_moves = self.current_enemy.move_list
        selected_move = None
        if not items:
            items.append(self.gold_sword)
            items.append(self.iron_armor)
            items.append(self.healing_potion)
            print(items)
      
        self.log_ui.add_log("select your move")
        self.player_ui.add_buttons(moves)
       
              
        # Handle input and button logic

       
        
        move_name = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                 pygame.event.clear() 
                 #print('click')
                 mouse_pos = pygame.mouse.get_pos()
                 mouse_pressed = pygame.mouse.get_pressed()
                

                 for button in self.player_ui.buttons:
                    if button.is_pressed(mouse_pos, mouse_pressed):
                        selected_move = button.content
                        move_name , damage = selected_move.split(':')
                        print(f"Button {button.content} pressed!")
                        print()
                        print(f"move name: {move_name}")
                        self.log_ui.add_log(f"You used {move_name}!")

                        if move_name == 'Run':
                            self.log_ui.add_log(f"{self.bob.name} ran away!")
                            last_cords = self.defeated_enemies[-1]
                            self.defeated_enemies.remove(last_cords)
                            print(f"removing {last_cords}")

                            current_health = self.bob._health
                            current_level = self.bob.level

                            self.state = 'normal'
                            self.clear_screen()
                            self.new()

                            self.bob._health = current_health
                            self.bob.level = current_level
                            print(current_health)

                            self.main()  # Return to overworld
                            return

                        # Player's turn
                        if move_name in self.bob.move_list:
                            damage = self.bob.attack(move_name)
                            print(f"current health: {self.current_enemy._health}")
                            print(f"you have done {damage}")
                            self.current_enemy.take_damage(damage)
                            self.log_ui.add_log(f"{self.bob.name} used {selected_move} and dealt {damage} damage!")
                            

                            # Check if the enemy is defeated
                            if self.current_enemy._health <= 0:
                                self.log_ui.add_log(f"{self.current_enemy.name} has been defeated!")
                                self.state = 'normal'
                                winner = self.bob
                                loser = self.current_enemy
                                current_xp = self.give_xp(winner,loser)
                                current_health = self.bob._health
                                current_level = self.bob.level

                                self.clear_screen()
                                self.new()

                                self.bob._health = current_health
                                self.bob.level = current_level
                                self.bob.xp = current_xp

                                self.main()  # End battle
                                return 

                            # Enemy's turn
                            enemy_move = random.choice(list(enemy_moves.keys()))
                            enemy_damage = self.current_enemy.attack(enemy_move)
                            self.bob.take_damage(enemy_damage)
                            self.log_ui.add_log(f"{self.current_enemy.name} used {enemy_move} and dealt {enemy_damage} damage!")

                            # Check if the player is defeated
                            if self.bob._health <= 0:
                                self.log_ui.add_log(f"{self.bob.name} has been defeated!")
                                self.state = 'normal'
                                self.defeated_enemies.clear()
                                self.clear_screen()
                                self.game_over()  # End game or return to overworld
                                return  
                        
                

        self.all_sprites.update()
        

    def give_xp(self, winner, loser):
                    if loser.level < 3:
                        winner.xp += 15
                    elif loser.level < 6:
                        winner.xp += 25
                    elif loser.level < 10:
                        winner.xp += 30
                    
                    if winner.xp > 100:
                        winner.level_up()
                        winner.xp = 0

                    return winner.xp


g = Game()
g.intro_screen()
g.new()
while g.running: 
    g.main()

g.game_over()
pygame.quit()
sys.exit()
