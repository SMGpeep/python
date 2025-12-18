import pygame
import random as rand

#consts

# Window settings
WIDTH, HEIGHT = 900, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pöng")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BALL_X_INIT = WIDTH / 2 
BALL_Y_INIT = HEIGHT / 2 
BALL_X_SPEED_INIT_MAX = 14
BALL_Y_SPEED_INIT_MAX = 14

#classes

def Randy():
    return pygame.time.get_ticks() % 2 == 0

class Ball:
    
    RADIUS = 10
    COLOR= WHITE
    
    def __init__(self,x,y,x_v = 0, y_v = 0, ) -> None:
        self.pos_x = x
        self.pos_y = y
        self.vel_x = x_v
        self.vel_y = y_v
    
    def setVelocity(self, x_v,y_v):
        self.vel_x = x_v
        self.vel_y = y_v
 
    def update(self, screen_width, screen_height):
        #keep in mind if we scored or not
        scored = False
        direction = self.vel_x
        # Use velocity as pixels per frame (not times dt)
        newX = self.pos_x + self.vel_x

        # If ball goes out left/right, reset its position and give a new random velocity
        if newX <= self.RADIUS or newX + self.RADIUS >= screen_width:
            # Reset position to center
            self.pos_x = BALL_X_INIT
            self.pos_y = BALL_Y_INIT
            # Assign new velocity, randomize direction
            self.vel_x = ( (-1 if Randy() else 1)) *  rand.randint(BALL_X_SPEED_INIT_MAX//2, BALL_X_SPEED_INIT_MAX)
            self.vel_y = ( (-1 if Randy() else 1)) *  rand.randint(BALL_Y_SPEED_INIT_MAX//2, BALL_Y_SPEED_INIT_MAX)
            scored = True
        else:
            self.pos_x = newX

        newY = self.pos_y + self.vel_y

        # Bounce off top/bottom
        if newY <= self.RADIUS or newY + self.RADIUS >= screen_height:
            self.vel_y = -self.vel_y
        self.pos_y += self.vel_y
        return (scored, direction if scored else None)

    def render(self, screen):
        pygame.draw.circle(screen, self.COLOR, (int(self.pos_x), int(self.pos_y)), self.RADIUS)
        # Remove pygame.display.update() from here

class Racket:
    HEIGHT = 100
    WIDTH = 10
    COLOR = BLACK
    score = 0
    
    def __init__(self, x, y, v_y, serving) -> None:
        self.pos_x = x
        self.pos_y = y
        self.velocity_y = v_y
        self.hasServe = serving
        self.win = False

    def update(self, screen_width, screen_height):
        newY = self.pos_y + self.velocity_y
        if newY <= 0:
            self.pos_y = 0
        elif newY + self.HEIGHT >= screen_height:
            self.pos_y = screen_height - self.HEIGHT
        else:
            self.pos_y = newY

    def get_rect(self):
        return pygame.Rect(int(self.pos_x), int(self.pos_y), self.WIDTH, self.HEIGHT)

    def render(self, screen):
        pygame.draw.rect(screen, self.COLOR, (int(self.pos_x), int(self.pos_y), self.WIDTH, self.HEIGHT))
        # Remove pygame.display.update() from here
  
    def serve(self, ball):
        if not self.hasServe: 
            return
        speed_x = ( (1 if self.pos_x <= WIDTH//2 else -1)) *  rand.randint(BALL_X_SPEED_INIT_MAX//2, BALL_X_SPEED_INIT_MAX)
        speed_y = ( (-1 if Randy() else 1)) *  rand.randint(BALL_Y_SPEED_INIT_MAX//2, BALL_Y_SPEED_INIT_MAX)
        ball.setVelocity(speed_x,speed_y)       
         
    def setServe(self, serve = True):
        self.hasServe = serve
       
    def IncScore(self):
        self.score+=1
        if self.score >= 10:
            self.win = True

def ShowWinScreen(playerId, window):
    """
    Display a simple win screen for the winning player.
    playerId: 0 for left player, 1 for right player
    """
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 60)
    small_font = pygame.font.SysFont('Comic Sans MS', 30)
    window.fill("black")
    if playerId == 0:
        text = font.render("Left Player Wins!", True, (255, 255, 0))
    else:
        text = font.render("Right Player Wins!", True, (255, 255, 0))
    instr = small_font.render("Press Q or ESC to quit", True, (200, 200, 200))
    window.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 50))
    window.blit(instr, ((WIDTH - instr.get_width()) // 2, HEIGHT // 2 + 40))
    pygame.display.flip()

    # Wait for user to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    waiting = False


def main():
    pygame.init()
    ball = Ball(BALL_X_INIT, BALL_Y_INIT, 0, 0)
    #get randy to "randomize" first serve
    thisRandy = Randy()
    lRacket = Racket(40, HEIGHT // 2 - Racket.HEIGHT // 2, 0, thisRandy)
    rRacket = Racket(WIDTH - 40 - Racket.WIDTH, HEIGHT // 2 - Racket.HEIGHT // 2, 0,not thisRandy)
    
    clock = pygame.time.Clock()

    pygame.font.init() # you have to call this at the start, 
                    # if you want to use this module.
    font = pygame.font.SysFont('Comic Sans MS', 30)

    serving = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(60)
        window.fill("blue")
        points_left = font.render(str(lRacket.score), True, "red")
        window.blit(points_left, (WIDTH //10, 0))


        points_right = font.render(str(rRacket.score), True, "red")
        window.blit(points_right, (WIDTH -100, 0))


        # Racket movement controls ('w'/'s' for left, up/down for right paddle)
        keys = pygame.key.get_pressed()
        lRacket.velocity_y = 0
        rRacket.velocity_y = 0
        if keys[pygame.K_w]:
            lRacket.velocity_y = -8
        elif keys[pygame.K_s]:
            lRacket.velocity_y = 8
        if keys[pygame.K_UP]:
            rRacket.velocity_y = -8
        elif keys[pygame.K_DOWN]:
            rRacket.velocity_y = 8
        
        if keys[pygame.K_SPACE] and serving:
            lRacket.serve(ball)
            rRacket.serve(ball)
            serving = False  # Set serving mode to False (serve has been made)

        lRacket.update(WIDTH, HEIGHT)
        rRacket.update(WIDTH, HEIGHT)

        # Adjusted line to use Ball.update's (scored, direction) return value:
        scored, direction = ball.update(WIDTH, HEIGHT)
        if scored:
            ball.setVelocity(0, 0)
            serving = True
        
            # scored == 1 means ball went out on right (left scores), -1 means left out (right scores)
        
            if direction is not None and direction > 0:
                lRacket.IncScore()
                lRacket.setServe()
                rRacket.setServe(False)
        
            elif direction is not None and direction < 0:
                rRacket.IncScore()
                rRacket.setServe()
                lRacket.setServe(False)

            if  lRacket.win:
                ShowWinScreen(0,window)
            elif rRacket.win:
                ShowWinScreen(1,window)
            

        # Collision detection in pygame is optimized for rectangles, not circles, 
        # so we approximate the circular ball using a square that fully contains it.
        # This makes collision checks with paddles (which are also rectangles) much simpler and faster.
        ball_rect = pygame.Rect(
            int(ball.pos_x - ball.RADIUS),
            int(ball.pos_y - ball.RADIUS),
            ball.RADIUS * 2,
            ball.RADIUS * 2
        )
        
        if ball_rect.colliderect(lRacket.get_rect()):
            ball.vel_x = abs(ball.vel_x)
            # Push the ball just out to prevent sticking
            ball.pos_x = lRacket.pos_x + Racket.WIDTH + ball.RADIUS
            
        if ball_rect.colliderect(rRacket.get_rect()):
            ball.vel_x = -abs(ball.vel_x)
            ball.pos_x = rRacket.pos_x - ball.RADIUS

        # Draw game
        lRacket.render(window)
        rRacket.render(window)
        ball.render(window)

        # get input to play/quit game
        if keys[pygame.K_q]:
            break
        if keys[pygame.K_ESCAPE]:
            break

        pygame.display.flip()  # Flip the display at the end of the frame

# Uncomment the following to run the game
main()