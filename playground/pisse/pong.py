import pygame
import sys

# Window settings
WIDTH, HEIGHT = 700, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_RADIUS = 12

PADDLE_SPEED = 7
BALL_X_SPEED_INIT = 5
BALL_Y_SPEED_INIT = 4
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
FONT = pygame.font.SysFont(None, 48)



def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, paddles[0])
    pygame.draw.rect(win, WHITE, paddles[1])
    pygame.draw.ellipse(win, WHITE, ball)
    pygame.draw.aaline(win, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    left_text = FONT.render(str(left_score), 1, WHITE)
    right_text = FONT.render(str(right_score), 1, WHITE)
    win.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    win.blit(right_text, (3*WIDTH//4 - right_text.get_width()//2, 20))
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    run = True
    left_paddle = pygame.Rect(20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
    ball_x_vel = BALL_X_SPEED_INIT * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
    ball_y_vel = BALL_Y_SPEED_INIT * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
    left_score, right_score = 0, 0

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Ball movement
        ball.x += ball_x_vel
        ball.y += ball_y_vel

        # Collision with top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_y_vel *= -1

        # Collision with paddles
        if ball.colliderect(left_paddle):
            ball.left = left_paddle.right + 1
            ball_x_vel *= -1
        if ball.colliderect(right_paddle):
            ball.right = right_paddle.left - 1
            ball_x_vel *= -1

        # Out of bounds
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_x_vel, ball_y_vel = BALL_X_SPEED_INIT, BALL_Y_SPEED_INIT
            if pygame.time.get_ticks() % 2 == 0:
                ball_x_vel *= -1
            if pygame.time.get_ticks() % 2 == 1:
                ball_y_vel *= -1
            pygame.time.wait(500)
        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_x_vel, ball_y_vel = -BALL_X_SPEED_INIT, BALL_Y_SPEED_INIT
            if pygame.time.get_ticks() % 2 == 0:
                ball_y_vel *= -1
            pygame.time.wait(500)

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    main()
