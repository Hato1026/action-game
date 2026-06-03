import random

enemies = [
    {"name": "スライム", "hp": 30, "attack": 5, "exp": 10},
    {"name": "ゴブリン", "hp": 50, "attack": 15, "exp": 25},
    {"name": "ドラゴン", "hp": 100, "attack": 30, "exp": 50},
]

player_hp = 100
player_attack = 10
player_defense = 0
player_speed = 10
player_level = 1
player_exp = 0
potion = 3

print("=== ゲーム開始 ===")

while player_hp > 0:
    enemy = random.choice(enemies)
    enemy_hp = enemy["hp"]

    print("\n" + enemy["name"] + "があらわれた！")
    print("勇者のHP：" + str(player_hp))
    print(enemy["name"] + "のHP：" + str(enemy_hp))

    while enemy_hp > 0 and player_hp > 0:
        print("\n--- ターン ---")
        print("勇者のHP：" + str(player_hp) + "  ポーション：" + str(potion) + "個")
        print("1: こうげき  2: ポーション  3: にげる")
        action = input("行動を選んでください：")

        if action == "1":
            enemy_hp -= player_attack
            print("勇者の攻撃！" + str(player_attack) + "ダメージ！")
            print(enemy["name"] + "のHP：" + str(enemy_hp))

            if enemy_hp > 0:
                damage = max(0, enemy["attack"] - player_defense)
                player_hp -= damage
                print(enemy["name"] + "の反撃！" + str(damage) + "ダメージ！")
                print("勇者のHP：" + str(player_hp))

            if player_hp <= 0:
                print("勇者は倒れた...")

        elif action == "2":
            if potion > 0:
                player_hp += 30
                if player_hp > 100:
                    player_hp = 100
                potion -= 1
                print("ポーションを使った！HPが30回復！")
                print("勇者のHP：" + str(player_hp) + "  残りポーション：" + str(potion) + "個")
            else:
                print("ポーションがない！")

        elif action == "3":
            print("勇者は逃げ出した！")
            break

    if enemy_hp <= 0:
        player_exp += enemy["exp"]
        print("\n" + enemy["name"] + "を倒した！経験値+" + str(enemy["exp"]) + "！（合計：" + str(player_exp) + "）")

        if player_exp >= player_level * 30:
            player_level += 1
            player_exp = 0
            print("\nレベルアップ！レベル" + str(player_level) + "になった！")
            print("どのステータスを上げますか？")
            print("1: 攻撃力  2: 防御力  3: 速度")
            choice = input("選んでください：")

            if choice == "1":
                player_attack += 5
                print("攻撃力が" + str(player_attack) + "になった！")
            elif choice == "2":
                player_defense += 5
                print("防御力が" + str(player_defense) + "になった！")
            elif choice == "3":
                player_speed += 5
                print("速度が" + str(player_speed) + "になった！")

print("\n=== ゲームオーバー ===")
print("レベル" + str(player_level) + "まで到達しました！")