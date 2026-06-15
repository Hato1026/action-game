import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("アクションゲーム")
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (40, 40))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

player_x = 100
player_y = 400
player_w = 40
player_h = 40
player_speed = 5
player_hp = 5
player_invincible = 0
game_over = False
facing_right = True

velocity_y = 0
is_jumping = False
GRAVITY = 0.5
JUMP_POWER = -12
GROUND_Y = 500

enemy_x = 600
enemy_y = 500
enemy_w = 40
enemy_h = 40
enemy_hp = 3
enemy_alive = True
enemy_invincible = 0
enemy_speed = 2

is_attacking = False
attack_timer = 0
ATTACK_DURATION = 15

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                velocity_y = JUMP_POWER
                is_jumping = True
            if event.key == pygame.K_z and not is_attacking and not game_over:
                is_attacking = True
                attack_timer = ATTACK_DURATION
            if event.key == pygame.K_r and game_over:
                player_hp = 5
                player_x = 100
                player_y = 400
                enemy_hp = 3
                enemy_x = 600
                enemy_y = 500
                enemy_alive = True
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            facing_right = True
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            facing_right = False

        velocity_y += GRAVITY
        player_y += velocity_y

        if player_y >= GROUND_Y:
            player_y = GROUND_Y
            velocity_y = 0
            is_jumping = False

        if is_attacking:
            attack_timer -= 1
            if attack_timer <= 0:
                is_attacking = False

        if is_attacking and enemy_alive and enemy_invincible <= 0:
            if facing_right:
                attack_rect = pygame.Rect(player_x + 40, player_y + 10, 40, 20)
            else:
                attack_rect = pygame.Rect(player_x - 40, player_y + 10, 40, 20)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
            if attack_rect.colliderect(enemy_rect):
                enemy_hp -= 1
                enemy_invincible = 30
                if enemy_hp <= 0:
                    enemy_alive = False

        if enemy_invincible > 0:
            enemy_invincible -= 1
        if player_invincible > 0:
            player_invincible -= 1

        if enemy_alive and player_invincible <= 0:
            player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
            if player_rect.colliderect(enemy_rect):
                player_hp -= 1
                player_invincible = 60
                if player_hp <= 0:
                    game_over = True

        if enemy_alive:
            if enemy_x < player_x:
                enemy_x += enemy_speed
            elif enemy_x > player_x:
                enemy_x -= enemy_speed

    # 描画
    screen.fill((100, 150, 255))
    pygame.draw.rect(screen, (50, 150, 50), (0, GROUND_Y + 40, 800, 60))

    screen.blit(player_img, (player_x, player_y))

    if enemy_alive:
        screen.blit(enemy_img, (enemy_x, enemy_y))

    if is_attacking:
        if facing_right:
            pygame.draw.rect(screen, (255, 100, 0), (player_x + 40, player_y + 10, 40, 20))
        else:
            pygame.draw.rect(screen, (255, 100, 0), (player_x - 40, player_y + 10, 40, 20))

    font = pygame.font.SysFont("msmincho", 30)
    text = font.render("プレイヤーHP：" + str(player_hp), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render("敵HP：" + str(enemy_hp), True, (255, 100, 100))
    screen.blit(text, (10, 50))

    pygame.draw.rect(screen, (150, 0, 0), (10, 80, 100, 15))
    pygame.draw.rect(screen, (0, 255, 0), (10, 80, 100 * player_hp // 5, 15))
    pygame.draw.rect(screen, (150, 0, 0), (10, 100, 100, 15))
    pygame.draw.rect(screen, (255, 100, 0), (10, 100, 100 * enemy_hp // 3, 15))

    if game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("msmincho", 60)
        text = font.render("ゲームオーバー", True, (255, 0, 0))
        screen.blit(text, (200, 250))
        font2 = pygame.font.SysFont("msmincho", 30)
        text2 = font2.render("Rキーで再スタート", True, (255, 255, 255))
        screen.blit(text2, (300, 350))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()