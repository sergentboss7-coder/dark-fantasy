# The Dark Fantasy World

A **text-based dark fantasy adventure game** written in Python. Explore a grim world, battle monsters, collect items, and uncover the secrets of the kingdom of Shadowmere.

---

## 📖 Story
In the land of **Dark Fantasy**, an ancient evil stirs. The once-peaceful kingdom of **Shadowmere** has fallen into darkness. Monsters roam the land, and the people live in fear. You, the player, have been chosen by fate to restore the light... or succumb to the darkness.

---

## 🎮 Features
- **Exploration**: Travel through multiple locations, each with unique descriptions, enemies, and items.
- **Combat**: Turn-based battles against goblins, skeletons, zombies, dark knights, and even an ancient dragon.
- **Inventory System**: Collect and use health potions, strength potions, weapons, and armor.
- **Progression**: Gain experience, level up, and increase your stats (health, attack, defense).
- **NPCs**: Interact with characters like the Old Man, Blacksmith, Witch, and King for lore and quests.
- **Random Encounters**: Chance encounters while moving between locations.
- **Multiple Endings**: Defeat the Ancient Dragon to save the kingdom and achieve victory.

---

## 🌍 Locations
1. **Village of Shadowmere**: A small village shrouded in perpetual twilight.
2. **Cursed Forest**: A dark forest filled with whispers and shadows.
3. **Ruined Castle**: A once-great castle now in ruins.
4. **Abyssal Cavern**: A deep cavern filled with the stench of death.

---

## 👾 Enemies
| Enemy          | Health | Attack | Defense | Gold Reward | EXP Reward |
|----------------|--------|--------|---------|-------------|-------------|
| Goblin         | 30     | 10     | 2       | 10          | 20          |
| Skeleton       | 40     | 12     | 5       | 15          | 25          |
| Zombie         | 50     | 15     | 3       | 20          | 30          |
| Dark Knight    | 80     | 20     | 10      | 50          | 60          |
| Shadow Beast   | 100    | 25     | 8       | 75          | 80          |
| Ancient Dragon | 200    | 30     | 15      | 200         | 150         |

---

## ⚔️ Items
### Weapons
- **Rusty Sword**: +5 Attack
- **Iron Sword**: +10 Attack
- **Steel Sword**: +15 Attack

### Armor
- **Leather Armor**: +5 Defense
- **Chainmail**: +10 Defense
- **Plate Armor**: +15 Defense

### Potions
- **Health Potion**: Restores 30 health.
- **Strength Potion**: +5 Attack.
- **Defense Potion**: +5 Defense.

---

## 🎯 How to Play
### Controls
| Command               | Description                                      |
|-----------------------|--------------------------------------------------|
| `move <direction>`    | Move to another location (e.g., `move north`).   |
| `explore`             | Search for items or enemies.                     |
| `inventory`           | View your inventory.                              |
| `use <index>`         | Use an item from your inventory.                 |
| `equip <index>`       | Equip a weapon or armor.                          |
| `stats`               | View your stats.                                 |
| `rest`                | Rest and restore 20 health.                       |
| `quit`                | Quit the game.                                   |

### Combat
When you encounter an enemy, you can:
1. **Attack**: Deal damage to the enemy.
2. **Use Item**: Use a potion or other item from your inventory.
3. **Flee**: Attempt to escape from combat (50% chance).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher.

### Installation
1. Clone this repository or download the `main.py` file.
2. Navigate to the game directory:
   ```bash
   cd the_dark_fantasy_world
   ```
3. Run the game:
   ```bash
   python3 main.py
   ```

---

## 📦 Project Structure
```
the_dark_fantasy_world/
├── main.py          # Main game script
└── README.md        # This file
```

---

## 🎨 Customization
You can easily customize the game by editing the `main.py` file:
- **Add New Locations**: Modify the `self.locations` dictionary in the `setup_game` method.
- **Add New Enemies**: Add entries to the `self.enemies` dictionary.
- **Add New Items**: Add entries to the `self.items` dictionary.
- **Add New NPCs**: Add entries to the `self.npcs` dictionary.

---

## 🐛 Bugs and Issues
If you encounter any bugs or have suggestions, feel free to open an issue on the [GitHub repository](https://github.com/sergentboss7-coder/dark-fantasy).

---

## 📜 License
This project is open-source and free to use. Feel free to modify, distribute, or use it as a base for your own projects.

---

## 🎉 Victory Condition
Defeat the **Ancient Dragon** in the **Abyssal Cavern** to save the kingdom of Shadowmere and achieve victory!

---

**Enjoy your adventure in the Dark Fantasy World!** 🏰🔥
