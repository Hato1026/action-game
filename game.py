import pygame
import random

class Player:
    def __init__(self):
        self.hp = 100
        self.attack = 10
        self.defense = 0
        self.level = 1
        self.exp = 0
        self.potion = 3

    def attack_enemy(self, enemy):
        damage = self.attack
        enemy.hp -= damage

    def use_potion(self):
        if self.potion > 0:
            self.hp += 30
            if self.hp > 100:
                self.hp = 100
            self.potion -= 1
            return True
        return False

class Enemy:
    def __init__(self, name, hp, attack, exp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.exp = exp

    def attack_player(self, player):
        damage = max(0, self.attack - player.defense)
        player.hp -= damage

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPGゲーム")
clock = pygame.time.Clock()

# 画像読み込み
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

player = Player()

enemy_data = [
    {"name": "スライム", "hp": 30, "attack": 5, "exp": 10},
    {"name": "ゴブリン", "hp": 50, "attack": 15, "exp": 25},
    {"name": "ドラゴン", "hp": 100, "attack": 30, "exp": 50},
]

enemy = Enemy("スライム", 30, 5, 10)

player_x = 400
player_y = 300
player_speed = 5
in_battle = False

enemy_x = 600
enemy_y = 300

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_battle and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.attack_enemy(enemy)
                enemy.attack_player(player)
                if enemy.hp <= 0:
                    player.exp += enemy.exp
                    print("敵を倒した！経験値+" + str(enemy.exp))
                    in_battle = False
                    data = random.choice(enemy_data)
                    enemy = Enemy(data["name"], data["hp"], data["attack"], data["exp"])
                if player.hp <= 0:
                    print("ゲームオーバー")
                    running = False
            elif event.key == pygame.K_2:
                player.use_potion()
            elif event.key == pygame.K_3:
                in_battle = False

    if not in_battle:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        if (abs(player_x - enemy_x) < 40 and abs(player_y - enemy_y) < 40):
            in_battle = True

    screen.fill((0, 0, 0))

    if in_battle:
        screen.fill((20, 20, 40))
        font = pygame.font.SysFont("msmincho", 36)

        # 敵画像を大きく表示
        enemy_battle_img = pygame.transform.scale(enemy_img, (100, 100))
        screen.blit(enemy_battle_img, (550, 100))

        # 勇者画像を表示
        player_battle_img = pygame.transform.scale(player_img, (100, 100))
        screen.blit(player_battle_img, (150, 350))

        text = font.render(enemy.name + "  HP：" + str(enemy.hp), True, (255, 100, 100))
        screen.blit(text, (100, 100))

        text = font.render("勇者  HP：" + str(player.hp) + "  ポーション：" + str(player.potion) + "個", True, (100, 200, 255))
        screen.blit(text, (100, 450))

        text = font.render("1: こうげき  2: ポーション  3: にげる", True, (255, 255, 255))
        screen.blit(text, (100, 520))

    else:
        screen.blit(player_img, (player_x, player_y))
        screen.blit(enemy_img, (enemy_x, enemy_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()