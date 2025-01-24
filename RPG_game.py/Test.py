from classes import *
import pygame
from sprites import *

if __name__ == '__main__':
   #level 1 test
   health = 100
   defense = 1
   strength = 1
   
   def normal_test():
      bob = Player('bob',1,100,1,1,[],{'Strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'})
      print(f'bob did {bob.attack('Strike')}')
      #level >3 test
      bob = Player('bob',1,100,4,1,[],{'Strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'})
      print(f'bob did {bob.attack('Strike')}')

      #take damage test
      bob = Player('bob',1,100,1,1,[],{'strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'})
      villian = Player('Villian',1,100,7,1,[],{'strike': 15,'Bash': 20,'Pierce': 17, 'Sneeze': 10})
      damage = villian.attack('Bash')
      remaining_health = bob.take_damage(damage)
      print(f"Remaining health: {remaining_health}")

      #level up test
      for i in range(5):
         new_level = bob.level_up()
         print(f"Bob's new level is {new_level}") 
    
   def test_battle():
     bob = Player('bob',1,100,1,1,[],{'Strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'},0)
     villain = Villain("Madara", 1, 100, 1, 1, {"Strike": 15, "Bash": 20}, ["Gold"])
     print(f"{villain.name} has entered a battle with {bob.name}")
     battle = Battle(bob,villain)
     winner , loser, condition = battle.start_battle()
     #print(winner, loser, condition)
     if condition == True:
        current_xp = battle.give_xp(winner)
        print(f"{winner}'s current xp is now {current_xp} and his level is {bob.return_level()}")
   
   #test_battle()
   def test_xp():
      bob = Player('bob',1,100,1,1,[],{'Strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'},0)
      villain = Villain("Madara", 1, 100, 1, 1, {"Strike": 15, "Bash": 20}, ["Gold"])
      battle = Battle(bob,villain)
      condition = True
      winner = bob
      if condition == True:
        for i in range(7):
         current_xp = battle.give_xp(winner)
         print(f"{winner}'s current xp is now {current_xp} and his level is {bob.return_level()}")
      
   #test_xp()
   
   def test_items():
      bob = Player('bob',1,100,1,1,[],{'Strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'},0)
      gold_sword = Item(weapon='Gold Sword')
      iron_armor = Item(armor="Iron Armor")
      healing_potion = Item(potion="Healing Potion")
      bob_inventory = bob.return_inventory()
      bob_inventory.append(gold_sword)
      bob_inventory.append(iron_armor)
      bob_inventory.append(healing_potion)
      print(bob_inventory)

   #test_items()
   def test_battle_with_items():
      bob = Player('bob',1,100,1,1,[],{'Strike': 15,'Bash': 20,'Pierce': 17, 'Run': 'Run'},0)
      gold_sword = Item(weapon='Gold Sword')
      iron_armor = Item(armor="Iron Armor")
      healing_potion = Item(potion="Healing Potion")
      bob_inventory = bob.return_inventory()
      bob_inventory.append(gold_sword)
      bob_inventory.append(iron_armor)
      bob_inventory.append(healing_potion)
      
      villain = Villain("Madara", 1, 100, 1, 1, {"Strike": 15, "Bash": 20}, ["Gold"])
      battle = Battle(bob,villain)
      winner , loser, condition = battle.start_battle()
      print(winner, loser, condition)

def test_strings():
   list = ['a','b','c','d']
   empty_string = ''
   for letter in list:
      empty_string += f"{letter}\n"
   print(empty_string)

