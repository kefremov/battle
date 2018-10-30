import random
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

print("\n\n")

fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 60, 200, "black")
quake = Spell("Quake", 14, 140, "black")

cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully Restores HP and MP of one party member", 9999)
megaelixir = Item("Mega Elixir", "elixir", "Fully Restores party's HP and MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2}, {"item": elixir, "quantity": 2},
                {"item": megaelixir, "quantity": 1}, {"item": grenade, "quantity": 3}]

player1 = Person("Valos:", 3260, 195, 60, 34, player_spells, player_items)
player2 = Person("Nicko: ", 4160, 165, 60, 34, player_spells, player_items)
player3 = Person("Robon:", 3089, 235, 60, 34, player_spells, player_items)

enemy2 = Person("Imp    ", 1250, 130, 260, 325, enemy_spells, [])
enemy1 = Person("Magus", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp    ", 1250, 130, 260, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "ENEMIES ATTACK!" + bcolors.ENDC)

while running:
    print("==================================================================")
    print("NAME              HP                                 MP")

    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    print("==================================================================")

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attack " + enemies[enemy].name.replace(" ", "") + " for", dmg, "damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue

            current_mp = player.get_mp()

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP!\n" + bcolors.ENDC)
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

            player.reduce_mp(spell.cost)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item:")) - 1

            if item_choice == -1:
                continue

            item = player_items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "No more left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restored party's HP and MP" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restored HP and MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    defeated_enemies = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "YOU WON!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "YOU DIED!" + bcolors.ENDC)
        running = False

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 2)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(
                bcolors.FAIL + "\n" + enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(":", "")
                + " for", enemy_dmg, "damage!" + bcolors.ENDC)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " heals " +
                      enemy.name.replace(" ", "") + " for", str(magic_dmg), "HP." + bcolors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, 2)
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg),
                      "damage to " + players[target].name.replace(":", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
