import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("アクションゲーム")
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (40, 40))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

# プレイヤー
player_x = 100
player_y = 400
player_w = 40
player_h = 40
player_speed = 5
player_hp = 5
player_invincible = 0
facing_right = True

# ジャンプ
velocity_y = 0
is_jumping = False
GRAVITY = 0.5
JUMP_POWER = -12
GROUND_Y = 500

# 攻撃
is_attacking = False
attack_timer = 0
attack_type = 0
ATTACK_DURATION = 15
STRONG_ATTACK_DURATION = 25

# パリィ
is_parrying = False
parry_timer = 0
PARRY_DURATION = 10
parry_cooldown = 0
PARRY_COOLDOWN = 60

# 敵
enemy_x = 600
enemy_y = 500
enemy_w = 40
enemy_h = 40
enemy_hp = 6
enemy_alive = True
enemy_invincible = 0
enemy_speed = 2
enemy_attack_timer = 0
ENEMY_ATTACK_INTERVAL = 120
enemy_bullet_x = 0
enemy_bullet_y = 0
enemy_bullet_active = False
enemy_bullet_dir = -1  # 弾の方向（-1:左 1:右）
enemy_velocity_y = 0
enemy_is_jumping = False

# ゲーム状態
game_over = False
game_clear = False
title_screen = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and title_screen:
                title_screen = False
            if not game_over and not game_clear and not title_screen:
                if event.key == pygame.K_SPACE and not is_jumping:
                    velocity_y = JUMP_POWER
                    is_jumping = True
                if event.key == pygame.K_z and not is_attacking:
                    is_attacking = True
                    attack_timer = ATTACK_DURATION
                    attack_type = 0
                if event.key == pygame.K_x and not is_attacking:
                    is_attacking = True
                    attack_timer = STRONG_ATTACK_DURATION
                    attack_type = 1
                if event.key == pygame.K_c and is_jumping and not is_attacking:
                    is_attacking = True
                    attack_timer = ATTACK_DURATION
                    attack_type = 2
                if event.key == pygame.K_v and not is_parrying and parry_cooldown <= 0:
                    is_parrying = True
                    parry_timer = PARRY_DURATION
                    parry_cooldown = PARRY_COOLDOWN
            if event.key == pygame.K_r and (game_over or game_clear):
                player_x = 100
                player_y = 400
                player_hp = 5
                player_invincible = 0
                velocity_y = 0
                is_jumping = False
                is_attacking = False
                is_parrying = False
                parry_cooldown = 0
                enemy_x = 600
                enemy_y = 500
                enemy_hp = 6
                enemy_alive = True
                enemy_invincible = 0
                enemy_bullet_active = False
                enemy_attack_timer = 0
                game_over = False
                game_clear = False

    if not game_over and not game_clear and not title_screen:
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
        if player_y >= GROUND_Y:
            player_y = GROUND_Y
            velocity_y = 0
            is_jumping = False

        # 攻撃タイマー
        if is_attacking:
            attack_timer -= 1
            if attack_timer <= 0:
                is_attacking = False

        # パリィタイマー
        if is_parrying:
            parry_timer -= 1
            if parry_timer <= 0:
                is_parrying = False
        if parry_cooldown > 0:
            parry_cooldown -= 1

        # 攻撃が敵に当たったか
        if is_attacking and enemy_alive and enemy_invincible <= 0:
            if facing_right:
                attack_rect = pygame.Rect(player_x + 40, player_y + 10, 40, 20)
            else:
                attack_rect = pygame.Rect(player_x - 40, player_y + 10, 40, 20)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
            if attack_rect.colliderect(enemy_rect):
                if attack_type == 0:
                    damage = 1
                elif attack_type == 1:
                    damage = 3
                elif attack_type == 2:
                    damage = 2
                enemy_hp -= damage
                enemy_invincible = 30
                print("ヒット！ダメージ：" + str(damage) + " 敵HP：" + str(enemy_hp))
                if enemy_hp <= 0:
                    enemy_alive = False
                    game_clear = True

        # 無敵タイマー
        if enemy_invincible > 0:
            enemy_invincible -= 1
        if player_invincible > 0:
            player_invincible -= 1

        # 敵の飛び道具
        if enemy_alive:
            enemy_attack_timer += 1
            if enemy_attack_timer >= ENEMY_ATTACK_INTERVAL:
                enemy_attack_timer = 0
                enemy_bullet_active = True
                enemy_bullet_x = enemy_x
                enemy_bullet_y = enemy_y + 20
                # 発射時にプレイヤーの方向を決定して固定する
                if enemy_x > player_x:
                    enemy_bullet_dir = -1
                else:
                    enemy_bullet_dir = 1

        if enemy_bullet_active:
            enemy_bullet_x += 5 * enemy_bullet_dir  # 固定方向に飛ぶ

            # パリィで弾を跳ね返す
            if is_parrying:
                bullet_rect = pygame.Rect(enemy_bullet_x, enemy_bullet_y, 10, 10)
                if facing_right:
                    parry_rect = pygame.Rect(player_x + 40, player_y, 20, 40)
                else:
                    parry_rect = pygame.Rect(player_x - 20, player_y, 20, 40)
                if bullet_rect.colliderect(parry_rect):
                    enemy_bullet_active = False
                    enemy_hp -= 2
                    print("パリィ成功！カウンター！")
                    if enemy_hp <= 0:
                        enemy_alive = False
                        game_clear = True

            # 弾がプレイヤーに当たる
            elif player_invincible <= 0:
                bullet_rect = pygame.Rect(enemy_bullet_x, enemy_bullet_y, 10, 10)
                player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
                if bullet_rect.colliderect(player_rect):
                    enemy_bullet_active = False
                    player_hp -= 1
                    player_invincible = 60
                    if player_hp <= 0:
                        game_over = True

            if enemy_bullet_x < 0 or enemy_bullet_x > 800:
                enemy_bullet_active = False

        # 敵の体当たり
        if enemy_alive and player_invincible <= 0:
            player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
            if player_rect.colliderect(enemy_rect):
                player_hp -= 1
                player_invincible = 60
                if player_hp <= 0:
                    game_over = True

       # 敵の追跡（左右のみ）
        if enemy_alive:
            if enemy_x < player_x:
                enemy_x += enemy_speed
            elif enemy_x > player_x:
                enemy_x -= enemy_speed

            # 敵にも重力をかける
            enemy_velocity_y += GRAVITY
            enemy_y += enemy_velocity_y
            if enemy_y >= GROUND_Y:
                enemy_y = GROUND_Y
                enemy_velocity_y = 0
                enemy_is_jumping = False

    # 描画
    screen.fill((100, 150, 255))
    pygame.draw.rect(screen, (50, 150, 50), (0, GROUND_Y + 40, 800, 60))

    screen.blit(player_img, (player_x, player_y))

    if enemy_alive:
        screen.blit(enemy_img, (enemy_x, enemy_y))

    # 攻撃エフェクト
    if is_attacking:
        color = (255, 100, 0) if attack_type == 0 else (255, 0, 0) if attack_type == 1 else (0, 100, 255)
        if facing_right:
            pygame.draw.rect(screen, color, (player_x + 40, player_y + 10, 40, 20))
        else:
            pygame.draw.rect(screen, color, (player_x - 40, player_y + 10, 40, 20))

    # パリィエフェクト
    if is_parrying:
        if facing_right:
            pygame.draw.rect(screen, (0, 255, 255), (player_x + 40, player_y, 10, 40))
        else:
            pygame.draw.rect(screen, (0, 255, 255), (player_x - 10, player_y, 10, 40))

    # 弾を描画
    if enemy_bullet_active:
        pygame.draw.circle(screen, (255, 50, 50), (enemy_bullet_x, enemy_bullet_y), 8)

    # HP表示
    font = pygame.font.SysFont("msmincho", 30)
    text = font.render("プレイヤーHP：" + str(player_hp), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render("敵HP：" + str(enemy_hp), True, (255, 100, 100))
    screen.blit(text, (10, 50))

    pygame.draw.rect(screen, (150, 0, 0), (10, 80, 100, 15))
    pygame.draw.rect(screen, (0, 255, 0), (10, 80, 100 * player_hp // 5, 15))
    pygame.draw.rect(screen, (150, 0, 0), (10, 100, 100, 15))
    pygame.draw.rect(screen, (255, 100, 0), (10, 100, 100 * enemy_hp // 6, 15))

    # 操作説明
    font2 = pygame.font.SysFont("msmincho", 20)
    text = font2.render("Z:通常攻撃 X:強攻撃 C:ジャンプ攻撃 V:パリィ", True, (255, 255, 255))
    screen.blit(text, (200, 570))

    if game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("msmincho", 60)
        text = font.render("ゲームオーバー", True, (255, 0, 0))
        screen.blit(text, (200, 250))
        font2 = pygame.font.SysFont("msmincho", 30)
        text2 = font2.render("Rキーで再スタート", True, (255, 255, 255))
        screen.blit(text2, (300, 350))

    if game_clear:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("msmincho", 60)
        text = font.render("クリア！", True, (255, 215, 0))
        screen.blit(text, (300, 250))
        font2 = pygame.font.SysFont("msmincho", 30)
        text2 = font2.render("Rキーで再スタート", True, (255, 255, 255))
        screen.blit(text2, (300, 350))

    if title_screen:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("msmincho", 60)
        text = font.render("アクションゲーム", True, (255, 215, 0))
        screen.blit(text, (180, 200))
        font2 = pygame.font.SysFont("msmincho", 30)
        text2 = font2.render("Enterキーでスタート", True, (255, 255, 255))
        screen.blit(text2, (280, 320))
        text3 = font2.render("Z:通常 X:強攻撃 C:ジャンプ攻撃 V:パリィ", True, (200, 200, 200))
        screen.blit(text3, (150, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()