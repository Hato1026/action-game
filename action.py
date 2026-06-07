import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("アクションゲーム")
clock = pygame.time.Clock()

# プレイヤーの設定
player_x = 100
player_y = 400
player_w = 40
player_h = 40
player_speed = 5

# ジャンプの設定
velocity_y = 0
is_jumping = False
GRAVITY = 0.5
JUMP_POWER = -12

# 地面の高さ
GROUND_Y = 500

# 敵の設定
enemy_x = 600
enemy_y = 500
enemy_w = 40
enemy_h = 40
enemy_hp = 3
enemy_alive = True
enemy_invincible = 0
enemy_speed = 2  # 敵の移動速度

# 攻撃の設定
is_attacking = False
attack_timer = 0
ATTACK_DURATION = 15
facing_right = True

player_hp = 5
player_invincible = 0  # プレイヤーの無敵時間

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                velocity_y = JUMP_POWER
                is_jumping = True
            if event.key == pygame.K_z and not is_attacking:
                is_attacking = True
                attack_timer = ATTACK_DURATION

    # 左右移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        facing_right = True
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        facing_right = False

    # 重力
    velocity_y += GRAVITY
    player_y += velocity_y

    # 地面に着地
    if player_y >= GROUND_Y:
        player_y = GROUND_Y
        velocity_y = 0
        is_jumping = False

    # 攻撃タイマー
    if is_attacking:
        attack_timer -= 1
        if attack_timer <= 0:
            is_attacking = False

# 攻撃が敵に当たったか
    if is_attacking and enemy_alive and enemy_invincible <= 0:
        if facing_right:
            attack_rect = pygame.Rect(player_x + 40, player_y + 10, 40, 20)
        else:
            attack_rect = pygame.Rect(player_x - 40, player_y + 10, 40, 20)

        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)

        if attack_rect.colliderect(enemy_rect):
            enemy_hp -= 1
            enemy_invincible = 30  # 30フレーム無敵
            print("ヒット！敵のHP：" + str(enemy_hp))
            if enemy_hp <= 0:
                enemy_alive = False
                print("敵を倒した！")

    # 無敵タイマーを減らす
    if enemy_invincible > 0:
        enemy_invincible -= 1

    # 敵がプレイヤーに触れたらダメージ
    if enemy_alive and player_invincible <= 0:
        player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
        if player_rect.colliderect(enemy_rect):
            player_hp -= 1
            player_invincible = 60
            print("ダメージ！プレイヤーHP：" + str(player_hp))
            if player_hp <= 0:
                print("ゲームオーバー！")
                running = False

    # プレイヤーの無敵タイマー
    if player_invincible > 0:
        player_invincible -= 1

    # 敵がプレイヤーを追いかける
    if enemy_alive:
        if enemy_x < player_x:
            enemy_x += enemy_speed
        elif enemy_x > player_x:
            enemy_x -= enemy_speed

    # 描画
    screen.fill((100, 150, 255))

    # HPを画面に表示
    font = pygame.font.SysFont("msmincho", 30)
    text = font.render("プレイヤーHP：" + str(player_hp), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render("敵HP：" + str(enemy_hp), True, (255, 100, 100))
    screen.blit(text, (10, 50))
    
    # プレイヤーHPバー
    pygame.draw.rect(screen, (150, 0, 0), (10, 80, 100, 15))
    pygame.draw.rect(screen, (0, 255, 0), (10, 80, 100 * player_hp // 5, 15))

    # 敵HPバー
    pygame.draw.rect(screen, (150, 0, 0), (10, 100, 100, 15))
    pygame.draw.rect(screen, (255, 100, 0), (10, 100, 100 * enemy_hp // 3, 15))
    
    pygame.draw.rect(screen, (50, 150, 50), (0, GROUND_Y + 40, 800, 60))

    pygame.draw.rect(screen, (255, 200, 0), (player_x, player_y, player_w, player_h))

    if is_attacking:
        if facing_right:
            pygame.draw.rect(screen, (255, 100, 0), (player_x + 40, player_y + 10, 40, 20))
        else:
            pygame.draw.rect(screen, (255, 100, 0), (player_x - 40, player_y + 10, 40, 20))

    if enemy_alive:
        pygame.draw.rect(screen, (255, 0, 0), (enemy_x, enemy_y, enemy_w, enemy_h))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()