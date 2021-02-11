import random

DICE_Min = 1
DICE_MAX = 6


class Unit:
    def __init__(self, name, attack, defense, health):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.maxHealth = health
        self.kills = 0
        self.healAmount = .05

    def print_stats(self):
        print("Name: " + self.name
                + "\nHealth: " + str(self.health)
                + "\nAttack: " + str(self.attack)
                + "\nDefense: " + str(self.defense))

    def dead(self) -> bool:
        """

        :rtype: Boolean
        """
        return self.health <= 0

    def killed_unit(self, enemy):
        self.kills += 1
        self.maxHealth += int(enemy.maxHealth/10)
        self.health += int(enemy.health/10)
        self.attack += int(enemy.attack/10)
        self.defense += int(enemy.defense/10)
        self.restore_health()

    def turn(self, enemy):
        x = int(0)
        if self.name == "Monster" and self.health != self.maxHealth:
            x = random.randint(1, 4)
        elif self.name == "Monster":
            x = random.randint(1, 3)
        while x < 1 or x > 4:
            enemy.print_stats()
            try:
                selection = input("1: Attack for " + str(self.attack)
                              + "\n2: Boost Attack"
                              + "\n3: Boost Defense"
                              + "\n4: Restore " + str(self.health * self.healAmount) + " Health\n")
                x = int(selection)
            except ValueError:
                print("Not an option")
        if x == 1:
            print(self.name + " attacks " + enemy.name + " for " + str(int(enemy.make_defend(self.make_attack()))) + " damage")
        elif x == 2:
            self.increase_attack()
            print(self.name + " increases attack!")
        elif x == 3:
            self.increase_def()
            print(self.name + " increases defense!")
        elif x == 4:
            self.restore_health()
            print(self.name + " restores health!")

    def make_attack(self) -> int:
        power = []
        for i in range(self.attack):
            power.append(random.randint(DICE_Min, DICE_MAX))
        return int(sum(power))

    def make_defend(self, x) -> int:
        evade = []
        for i in range(self.defense):
            evade.append(random.randint(DICE_Min, DICE_MAX))
        damage_mitigation = sum(evade)
        damage_to_take = (x - damage_mitigation)
        if damage_to_take < 0:
            damage_to_take = 0
        self.health -= damage_to_take
        return damage_to_take

    def increase_attack(self):
        self.attack += 1

    def increase_def(self):
        self.defense += 1

    def restore_health(self):
        self.health += int(self.health * self.healAmount)
        if self.health > self.maxHealth:
            self.health = self.maxHealth


if __name__ == '__main__':
    player = Unit("Player", 5, 5, 50)
    monster = Unit("Monster", 3, 3, 10)
    x = 3
    y = 3
    z = 10
    while player.health > 0:
        if monster.health <= 0:
            print("A NEW MONSTER APPEARS")
            x += random.randint(1, x)
            y += random.randint(1, y)
            z += random.randint(1, z)
            monster = Unit("Monster", x, y, z)
            player.killed_unit(monster)
        player.print_stats()
        player.turn(monster)
        monster.turn(player)

    print("Game Over\nMonsters Killed: " + str(player.kills))