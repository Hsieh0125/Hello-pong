import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打磚塊遊戲")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)


clock = pygame.time.Clock()
FPS = 60


font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 48)


paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 15)
paddle_speed = 8


ball_radius = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-4, 4])
ball_dy = -4


lives = 3


BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 60
BRICK_OFFSET_LEFT = 35


bricks = []

for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
        y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)

        # 不同排數有不同血量
        hits = 3 - row // 2
        color = RED if hits == 3 else YELLOW if hits == 2 else GREEN

        brick = {
            "rect": pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT),
            "hits": hits,
            "color": color
        }
        bricks.append(brick)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


running = True
game_over = False
win = False

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # 擋板控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # 球移動
        ball_x += ball_dx
        ball_y += ball_dy

        # 牆壁反彈
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
            ball_dx = -1
        if ball_y - ball_radius <= 0:
            ball_dy= -1

        # 掉落
        if ball_y > HEIGHT:
            lives -= 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = random.choice([-4, 4])
            ball_dy = -4
            if lives == 0:
                game_over = True

        # 擋板碰撞
        ball_rect = pygame.Rect(
            ball_x - ball_radius,
            ball_y - ball_radius,
            ball_radius * 2,
            ball_radius * 2
        )

        if ball_rect.colliderect(paddle):
            ball_dy = -1
            ball_y = paddle.top - ball_radius

        # 磚塊碰撞
        for brick in bricks[:]:
            if ball_rect.colliderect(brick["rect"]):
                ball_dy= -1
                brick["hits"] -= 1
                if brick["hits"] == 2:
                    brick["color"] = YELLOW
                elif brick["hits"] == 1:
                    brick["color"] = GREEN
                else:
                    bricks.remove(brick)
                break

        if not bricks:
            win = True
            game_over = True
#繪製磚塊
    for brick in bricks:
        pygame.draw.rect(screen, brick["color"], brick["rect"])

    # 繪製擋板與球
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # 顯示生命
    draw_text(f"Lives: {lives}", font, WHITE, 10, 10)

    # 結束畫面
    if game_over:
        if win:
            draw_text("YOU WIN!", big_font, GREEN, WIDTH//2 - 120, HEIGHT//2 - 40)
        else:
            draw_text("GAME OVER", big_font, RED, WIDTH//2 - 150, HEIGHT//2 - 40)

    pygame.display.flip()
