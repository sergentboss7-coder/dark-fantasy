#!/usr/bin/env python3
"""
The Dark Fantasy World
A text-based adventure game set in a grim, dark fantasy realm.
"""

import random
import time
import sys
from enum import Enum


class Color:
    """ANSI color codes for terminal output."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class EntityType(Enum):
    """Types of entities in the game."""
    PLAYER = "Player"
    ENEMY = "Enemy"
    NPC = "NPC"


class Player:
    """Represents the player character."""
    
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.defense = 10
        self.gold = 0
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.level = 1
        self.experience = 0
        self.experience_to_level = 50
        self.location = "Village of Shadowmere"
        self.visited_locations = set()
        self.choices = {}
    
    def add_item(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        print(f"{Color.GREEN}You picked up: {item.name}{Color.RESET}")
    
    def use_item(self, item_index):
        """Use an item from the inventory."""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory.pop(item_index)
            if item.type == "Health Potion":
                heal_amount = 30
                self.health = min(self.health + heal_amount, self.max_health)
                print(f"{Color.GREEN}You used a {item.name} and restored {heal_amount} health!{Color.RESET}")
            elif item.type == "Strength Potion":
                self.attack += 5
                print(f"{Color.GREEN}You used a {item.name} and increased your attack by 5!{Color.RESET}")
            elif item.type == "Defense Potion":
                self.defense += 5
                print(f"{Color.GREEN}You used a {item.name} and increased your defense by 5!{Color.RESET}")
            return True
        return False
    
    def equip(self, item_index):
        """Equip a weapon or armor from the inventory."""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item.type == "Weapon":
                if self.equipped_weapon:
                    self.inventory.append(self.equipped_weapon)
                self.equipped_weapon = self.inventory.pop(item_index)
                self.attack += self.equipped_weapon.value
                print(f"{Color.GREEN}You equipped: {self.equipped_weapon.name} (Attack +{self.equipped_weapon.value}){Color.RESET}")
            elif item.type == "Armor":
                if self.equipped_armor:
                    self.inventory.append(self.equipped_armor)
                self.equipped_armor = self.inventory.pop(item_index)
                self.defense += self.equipped_armor.value
                print(f"{Color.GREEN}You equipped: {self.equipped_armor.name} (Defense +{self.equipped_armor.value}){Color.RESET}")
            return True
        return False
    
    def add_experience(self, amount):
        """Add experience points to the player."""
        self.experience += amount
        print(f"{Color.CYAN}You gained {amount} experience points!{Color.RESET}")
        if self.experience >= self.experience_to_level:
            self.level_up()
    
    def level_up(self):
        """Level up the player."""
        self.level += 1
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.5)
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.defense += 5
        print(f"{Color.YELLOW}{Color.BOLD}LEVEL UP! You are now level {self.level}!{Color.RESET}")
        print(f"{Color.CYAN}Stats increased: Health +20, Attack +5, Defense +5{Color.RESET}")
    
    def take_damage(self, amount):
        """Reduce the player's health by the given amount."""
        damage = max(1, amount - self.defense)
        self.health -= damage
        print(f"{Color.RED}You took {damage} damage!{Color.RESET}")
        if self.health <= 0:
            print(f"{Color.RED}{Color.BOLD}You have been defeated...{Color.RESET}")
            return True
        return False
    
    def heal(self, amount):
        """Increase the player's health by the given amount."""
        self.health = min(self.health + amount, self.max_health)
        print(f"{Color.GREEN}You healed {amount} health!{Color.RESET}")
    
    def show_stats(self):
        """Display the player's current stats."""
        print(f"\n{Color.BOLD}{Color.YELLOW}=== {self.name} ==={Color.RESET}")
        print(f"{Color.WHITE}Level: {self.level}{Color.RESET}")
        print(f"{Color.RED}Health: {self.health}/{self.max_health}{Color.RESET}")
        print(f"{Color.CYAN}Attack: {self.attack}{Color.RESET}")
        print(f"{Color.BLUE}Defense: {self.defense}{Color.RESET}")
        print(f"{Color.YELLOW}Gold: {self.gold}{Color.RESET}")
        print(f"{Color.MAGENTA}Experience: {self.experience}/{self.experience_to_level}{Color.RESET}")
        print(f"{Color.WHITE}Location: {self.location}{Color.RESET}")
        if self.equipped_weapon:
            print(f"{Color.WHITE}Weapon: {self.equipped_weapon.name} (+{self.equipped_weapon.value} Attack){Color.RESET}")
        if self.equipped_armor:
            print(f"{Color.WHITE}Armor: {self.equipped_armor.name} (+{self.equipped_armor.value} Defense){Color.RESET}")


class Item:
    """Represents an item in the game."""
    
    def __init__(self, name, type, value=0, description=""):
        self.name = name
        self.type = type
        self.value = value
        self.description = description


class Enemy:
    """Represents an enemy in the game."""
    
    def __init__(self, name, health, attack, defense, gold_reward, exp_reward, description=""):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward
        self.description = description
    
    def take_damage(self, amount):
        """Reduce the enemy's health by the given amount."""
        damage = max(1, amount - self.defense)
        self.health -= damage
        return damage
    
    def is_defeated(self):
        """Check if the enemy is defeated."""
        return self.health <= 0


class NPC:
    """Represents a non-player character in the game."""
    
    def __init__(self, name, dialogue, quest=None):
        self.name = name
        self.dialogue = dialogue
        self.quest = quest


class Game:
    """Main game class to manage the game state and flow."""
    
    def __init__(self):
        self.player = None
        self.locations = {}
        self.enemies = {}
        self.items = {}
        self.npcs = {}
        self.game_over = False
        self.victory = False
        self.setup_game()
    
    def setup_game(self):
        """Initialize the game world, items, enemies, and locations."""
        # Items
        self.items = {
            "health_potion": Item("Health Potion", "Health Potion", 30, "Restores 30 health."),
            "strength_potion": Item("Strength Potion", "Strength Potion", 5, "Increases attack by 5."),
            "defense_potion": Item("Defense Potion", "Defense Potion", 5, "Increases defense by 5."),
            "rusty_sword": Item("Rusty Sword", "Weapon", 5, "A basic sword."),
            "iron_sword": Item("Iron Sword", "Weapon", 10, "A sturdy sword."),
            "steel_sword": Item("Steel Sword", "Weapon", 15, "A sharp sword."),
            "leather_armor": Item("Leather Armor", "Armor", 5, "Basic protection."),
            "chainmail": Item("Chainmail", "Armor", 10, "Heavy protection."),
            "plate_armor": Item("Plate Armor", "Armor", 15, "Strong protection."),
        }
        
        # Enemies
        self.enemies = {
            "goblin": Enemy("Goblin", 30, 10, 2, 10, 20, "A small, green-skinned creature."),
            "skeleton": Enemy("Skeleton", 40, 12, 5, 15, 25, "A reanimated corpse with a sword."),
            "zombie": Enemy("Zombie", 50, 15, 3, 20, 30, "A decaying, flesh-eating monster."),
            "dark_knight": Enemy("Dark Knight", 80, 20, 10, 50, 60, "A knight corrupted by dark magic."),
            "shadow_beast": Enemy("Shadow Beast", 100, 25, 8, 75, 80, "A creature made of pure shadow."),
            "ancient_dragon": Enemy("Ancient Dragon", 200, 30, 15, 200, 150, "A massive dragon with ancient power."),
        }
        
        # NPCs
        self.npcs = {
            "old_man": NPC(
                "Old Man",
                "The world is dark, traveler. Beware the shadows...",
                "Find the Amulet of Light"
            ),
            "blacksmith": NPC(
                "Blacksmith",
                "I can forge weapons and armor for you, if you have the gold.",
                "Buy a weapon or armor"
            ),
            "witch": NPC(
                "Witch",
                "The forest is cursed. Only the brave dare enter.",
                "Survive the Cursed Forest"
            ),
            "king": NPC(
                "King",
                "The kingdom is under siege. Defeat the Dark Knight to save us!",
                "Defeat the Dark Knight"
            ),
        }
        
        # Locations
        self.locations = {
            "Village of Shadowmere": {
                "description": "A small village shrouded in perpetual twilight. The air is thick with fear.",
                "enemies": ["goblin", "skeleton"],
                "items": ["health_potion", "rusty_sword", "leather_armor"],
                "npcs": ["old_man", "blacksmith"],
                "connections": {
                    "north": "Cursed Forest",
                    "east": "Ruined Castle",
                },
            },
            "Cursed Forest": {
                "description": "A dark forest filled with whispers and shadows. The trees seem to watch you.",
                "enemies": ["skeleton", "zombie", "shadow_beast"],
                "items": ["health_potion", "strength_potion", "iron_sword"],
                "npcs": ["witch"],
                "connections": {
                    "south": "Village of Shadowmere",
                    "east": "Abyssal Cavern",
                },
            },
            "Ruined Castle": {
                "description": "A once-great castle now in ruins. The walls are stained with blood.",
                "enemies": ["zombie", "dark_knight"],
                "items": ["health_potion", "defense_potion", "chainmail"],
                "npcs": ["king"],
                "connections": {
                    "west": "Village of Shadowmere",
                    "north": "Abyssal Cavern",
                },
            },
            "Abyssal Cavern": {
                "description": "A deep cavern filled with the stench of death. The air is thick with darkness.",
                "enemies": ["shadow_beast", "ancient_dragon"],
                "items": ["health_potion", "steel_sword", "plate_armor"],
                "npcs": [],
                "connections": {
                    "south": "Ruined Castle",
                    "west": "Cursed Forest",
                },
            },
        }
    
    def start(self):
        """Start the game."""
        print(f"{Color.BOLD}{Color.RED}\n=== THE DARK FANTASY WORLD ==={Color.RESET}")
        print(f"{Color.WHITE}Welcome to a world of darkness, danger, and ancient evils.{Color.RESET}")
        print(f"{Color.WHITE}Your choices will determine your fate...{Color.RESET}\n")
        
        # Get player name
        name = input(f"{Color.YELLOW}Enter your name, traveler: {Color.RESET}").strip()
        if not name:
            name = "Hero"
        self.player = Player(name)
        
        # Intro story
        self.print_slow(
            f"{Color.CYAN}In the land of {Color.BOLD}Dark Fantasy{Color.RESET}{Color.CYAN}, "
            f"an ancient evil stirs. The once-peaceful kingdom of Shadowmere "
            f"has fallen into darkness. Monsters roam the land, and the people "
            f"live in fear. You, {self.player.name}, have been chosen by fate to "
            f"restore the light... or succumb to the darkness.{Color.RESET}\n"
        )
        
        # Main game loop
        while not self.game_over and not self.victory:
            self.display_location()
            self.show_actions()
            action = input(f"{Color.YELLOW}What will you do? {Color.RESET}").strip().lower()
            self.handle_action(action)
        
        # Game over or victory
        if self.victory:
            print(f"\n{Color.BOLD}{Color.GREEN}=== VICTORY ==={Color.RESET}")
            print(f"{Color.GREEN}You have saved the kingdom of Shadowmere from the darkness!{Color.RESET}")
            print(f"{Color.GREEN}Your name will be remembered in legend...{Color.RESET}")
        else:
            print(f"\n{Color.BOLD}{Color.RED}=== GAME OVER ==={Color.RESET}")
            print(f"{Color.RED}Your journey ends here, {self.player.name}.{Color.RESET}")
    
    def display_location(self):
        """Display the current location and its description."""
        location = self.locations[self.player.location]
        print(f"\n{Color.BOLD}{Color.MAGENTA}=== {self.player.location} ==={Color.RESET}")
        print(f"{Color.WHITE}{location['description']}{Color.RESET}")
        
        # Show NPCs in the location
        if location["npcs"]:
            print(f"\n{Color.BOLD}{Color.CYAN}NPCs:{Color.RESET}")
            for npc_key in location["npcs"]:
                npc = self.npcs[npc_key]
                print(f"{Color.CYAN}- {npc.name}: {npc.dialogue}{Color.RESET}")
        
        # Show items in the location
        if location["items"]:
            print(f"\n{Color.BOLD}{Color.YELLOW}Items here:{Color.RESET}")
            for item_key in location["items"]:
                item = self.items[item_key]
                print(f"{Color.YELLOW}- {item.name}: {item.description}{Color.RESET}")
        
        # Show connections
        connections = location["connections"]
        if connections:
            print(f"\n{Color.BOLD}{Color.WHITE}Paths:{Color.RESET}")
            for direction, connected_location in connections.items():
                print(f"{Color.WHITE}- {direction.capitalize()}: {connected_location}{Color.RESET}")
    
    def show_actions(self):
        """Display available actions to the player."""
        print(f"\n{Color.BOLD}{Color.WHITE}=== Actions ==={Color.RESET}")
        print(f"{Color.WHITE}- move <direction>: Move to another location (e.g., 'move north'){Color.RESET}")
        print(f"{Color.WHITE}- explore: Search for items or enemies{Color.RESET}")
        print(f"{Color.WHITE}- inventory: View your inventory{Color.RESET}")
        print(f"{Color.WHITE}- use <index>: Use an item from your inventory{Color.RESET}")
        print(f"{Color.WHITE}- equip <index>: Equip a weapon or armor{Color.RESET}")
        print(f"{Color.WHITE}- stats: View your stats{Color.RESET}")
        print(f"{Color.WHITE}- rest: Rest and restore some health{Color.RESET}")
        print(f"{Color.WHITE}- quit: Quit the game{Color.RESET}")
    
    def handle_action(self, action):
        """Handle the player's action."""
        if action.startswith("move "):
            direction = action[5:].strip().lower()
            self.move(direction)
        elif action == "explore":
            self.explore()
        elif action == "inventory":
            self.show_inventory()
        elif action.startswith("use "):
            try:
                index = int(action[4:].strip())
                self.player.use_item(index)
            except ValueError:
                print(f"{Color.RED}Invalid item index.{Color.RESET}")
        elif action.startswith("equip "):
            try:
                index = int(action[6:].strip())
                self.player.equip(index)
            except ValueError:
                print(f"{Color.RED}Invalid item index.{Color.RESET}")
        elif action == "stats":
            self.player.show_stats()
        elif action == "rest":
            self.rest()
        elif action == "quit":
            self.game_over = True
            print(f"{Color.YELLOW}You have quit the game.{Color.RESET}")
        else:
            print(f"{Color.RED}Invalid action. Try again.{Color.RESET}")
    
    def move(self, direction):
        """Move the player to a new location."""
        location = self.locations[self.player.location]
        connections = location["connections"]
        
        if direction in connections:
            new_location = connections[direction]
            self.player.location = new_location
            print(f"{Color.GREEN}You moved {direction} to {new_location}.{Color.RESET}")
            
            # Add to visited locations
            self.player.visited_locations.add(new_location)
            
            # Random encounter chance
            if random.random() < 0.3:  # 30% chance of encounter
                self.random_encounter()
        else:
            print(f"{Color.RED}You cannot go that way.{Color.RESET}")
    
    def explore(self):
        """Explore the current location for items or enemies."""
        location = self.locations[self.player.location]
        
        # Check for items
        if location["items"]:
            item_key = random.choice(location["items"])
            item = self.items[item_key]
            self.player.add_item(item)
            location["items"].remove(item_key)
        
        # Check for enemies
        if location["enemies"]:
            if random.random() < 0.5:  # 50% chance of enemy encounter
                enemy_key = random.choice(location["enemies"])
                enemy = self.enemies[enemy_key]
                print(f"\n{Color.RED}{Color.BOLD}=== ENCOUNTER ==={Color.RESET}")
                print(f"{Color.RED}A wild {enemy.name} appears!{Color.RESET}")
                print(f"{Color.WHITE}{enemy.description}{Color.RESET}")
                self.combat(enemy)
            else:
                print(f"{Color.GREEN}You found nothing of interest.{Color.RESET}")
        else:
            print(f"{Color.GREEN}You found nothing of interest.{Color.RESET}")
    
    def random_encounter(self):
        """Trigger a random encounter while moving."""
        location = self.locations[self.player.location]
        if location["enemies"]:
            enemy_key = random.choice(location["enemies"])
            enemy = self.enemies[enemy_key]
            print(f"\n{Color.RED}{Color.BOLD}=== RANDOM ENCOUNTER ==={Color.RESET}")
            print(f"{Color.RED}A {enemy.name} ambushes you!{Color.RESET}")
            print(f"{Color.WHITE}{enemy.description}{Color.RESET}")
            self.combat(enemy)
    
    def combat(self, enemy):
        """Handle combat between the player and an enemy."""
        while True:
            print(f"\n{Color.BOLD}{Color.RED}=== COMBAT ==={Color.RESET}")
            print(f"{Color.RED}{enemy.name}: {enemy.health}/{enemy.max_health} HP{Color.RESET}")
            print(f"{Color.GREEN}{self.player.name}: {self.player.health}/{self.player.max_health} HP{Color.RESET}")
            print(f"\n{Color.WHITE}1. Attack{Color.RESET}")
            print(f"{Color.WHITE}2. Use Item{Color.RESET}")
            print(f"{Color.WHITE}3. Flee{Color.RESET}")
            
            choice = input(f"{Color.YELLOW}Choose an action: {Color.RESET}").strip()
            
            if choice == "1":
                # Player attacks
                damage = self.player.attack
                enemy_damage = enemy.take_damage(damage)
                print(f"{Color.GREEN}You attack the {enemy.name} for {enemy_damage} damage!{Color.RESET}")
                
                if enemy.is_defeated():
                    print(f"{Color.GREEN}{Color.BOLD}You defeated the {enemy.name}!{Color.RESET}")
                    self.player.gold += enemy.gold_reward
                    self.player.add_experience(enemy.exp_reward)
                    print(f"{Color.YELLOW}You found {enemy.gold_reward} gold!{Color.RESET}")
                    
                    # Check for victory condition
                    if enemy.name == "Ancient Dragon":
                        self.victory = True
                    break
                
                # Enemy attacks
                damage = enemy.attack
                player_defeated = self.player.take_damage(damage)
                if player_defeated:
                    self.game_over = True
                    break
            
            elif choice == "2":
                self.show_inventory()
                if self.player.inventory:
                    try:
                        item_index = int(input(f"{Color.YELLOW}Enter item index to use: {Color.RESET}").strip())
                        self.player.use_item(item_index)
                    except ValueError:
                        print(f"{Color.RED}Invalid item index.{Color.RESET}")
                
                # Enemy attacks
                damage = enemy.attack
                player_defeated = self.player.take_damage(damage)
                if player_defeated:
                    self.game_over = True
                    break
            
            elif choice == "3":
                # Flee
                if random.random() < 0.5:  # 50% chance to flee
                    print(f"{Color.GREEN}You successfully fled from the {enemy.name}!{Color.RESET}")
                    break
                else:
                    print(f"{Color.RED}You failed to flee!{Color.RESET}")
                    # Enemy attacks
                    damage = enemy.attack
                    player_defeated = self.player.take_damage(damage)
                    if player_defeated:
                        self.game_over = True
                        break
            
            else:
                print(f"{Color.RED}Invalid choice. Try again.{Color.RESET}")
    
    def show_inventory(self):
        """Display the player's inventory."""
        if not self.player.inventory:
            print(f"{Color.YELLOW}Your inventory is empty.{Color.RESET}")
            return
        
        print(f"\n{Color.BOLD}{Color.YELLOW}=== Inventory ==={Color.RESET}")
        for i, item in enumerate(self.player.inventory):
            print(f"{Color.YELLOW}{i}. {item.name} ({item.type}){Color.RESET}")
    
    def rest(self):
        """Rest and restore some health."""
        heal_amount = 20
        self.player.heal(heal_amount)
        print(f"{Color.GREEN}You rest for a while and restore {heal_amount} health.{Color.RESET}")
    
    def print_slow(self, text, delay=0.03):
        """Print text with a delay for dramatic effect."""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()


if __name__ == "__main__":
    game = Game()
    game.start()
