import random

class Player:
    def __init__(self):
        self.hp = 100
        self.attack = 10
        self.defense = 0
        self.speed = 10
        self.level = 1
        self.exp = 0
        self.potion = 3

    def attack_enemy(self, enemy):
        damage = self.attack
        enemy.hp -= damage
        print("勇者の攻撃！" + str(damage) + "ダメージ！")
        print(enemy.name + "のHP：" + str(enemy.hp))

    def use_potion(self):
        if self.potion > 0:
            self.hp += 30
            if self.hp > 100:
                self.hp = 100
            self.potion -= 1
            print("ポーションを使った！HPが30回復！")
            print("勇者のHP：" + str(self.hp) + "  残りポーション：" + str(self.potion) + "個")
        else:
            print("ポーションがない！")

    def level_up(self):
        if self.exp >= self.level * 30:
            self.level += 1
            self.exp = 0
            print("\nレベルアップ！レベル" + str(self.level) + "になった！")
            print("どのステータスを上げますか？")
            print("1: 攻撃力  2: 防御力  3: 速度")
            choice = input("選んでください：")
            if choice == "1":
                self.attack += 5
                print("攻撃力が" + str(self.attack) + "になった！")
            elif choice == "2":
                self.defense += 5
                print("防御力が" + str(self.defense) + "になった！")
            elif choice == "3":
                self.speed += 5
                print("速度が" + str(self.speed) + "になった！")

class Enemy:
    def __init__(self, name, hp, attack, exp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.exp = exp

    def attack_player(self, player):
        damage = max(0, self.attack - player.defense)
        player.hp -= damage
        print(self.name + "の反撃！" + str(damage) + "ダメージ！")
        print("勇者のHP：" + str(player.hp))

enemy_data = [
    {"name": "スライム", "hp": 30, "attack": 5, "exp": 10},
    {"name": "ゴブリン", "hp": 50, "attack": 15, "exp": 25},
    {"name": "ドラゴン", "hp": 100, "attack": 30, "exp": 50},
]

player = Player()
print("=== ゲーム開始 ===")

while player.hp > 0:
    data = random.choice(enemy_data)
    enemy = Enemy(data["name"], data["hp"], data["attack"], data["exp"])

    print("\n" + enemy.name + "があらわれた！")
    print("勇者のHP：" + str(player.hp))
    print(enemy.name + "のHP：" + str(enemy.hp))

    while enemy.hp > 0 and player.hp > 0:
        print("\n--- ターン ---")
        print("勇者のHP：" + str(player.hp) + "  ポーション：" + str(player.potion) + "個")
        print("1: こうげき  2: ポーション  3: にげる")
        action = input("行動を選んでください：")

        if action == "1":
            player.attack_enemy(enemy)
            if enemy.hp > 0:
                enemy.attack_player(player)
            if player.hp <= 0:
                print("勇者は倒れた...")

        elif action == "2":
            player.use_potion()

        elif action == "3":
            print("勇者は逃げ出した！")
            break

    if enemy.hp <= 0:
        player.exp += enemy.exp
        print("\n" + enemy.name + "を倒した！経験値+" + str(enemy.exp) + "！（合計：" + str(player.exp) + "）")
        player.level_up()

print("\n=== ゲームオーバー ===")
print("レベル" + str(player.level) + "まで到達しました！")