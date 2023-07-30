import pygame

screen_width = 500
screen_height = 500
mov_speed = 15

white = (255, 255, 255)


class Player:

    def __init__(self):
        self.colour = (255, 255, 255)

        self.x_pos = 10
        self.y_pos = 10

        self.x_size = 30
        self.y_size = 80

        self.up = None
        self.down = None

        self.score = 0

        self.hitbox = (self.x_pos, self.y_pos, self.x_size, self.y_size)

    def hitbox_update(self):
        self.hitbox = (self.x_pos, self.y_pos, self.x_size, self.y_size)


class Ball:
    def __init__(self):
        self.x_vel = 0
        self.y_vel = 0

        self.x_pos = 250
        self.y_pos = 250

        self.mov_speed = 10

        self.colour = (255, 255, 255)

        self.radius = 15

        self.hitbox = (self.x_pos - self.radius, self.y_pos - self.radius, 30, 30)

    def tick(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def reset(self):
        self.x_vel = 0
        self.y_vel = 0

        self.x_pos = 250
        self.y_pos = 250

    def draw_hitbox(self):
        self.hitbox = (self.x_pos - self.radius, self.y_pos - self.radius, 30, 30)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def serve_to_right(self):
        self.x_vel += self.mov_speed

    def serve_to_left(self):
        self.x_vel += -self.mov_speed


play = True
debug = False
match = False
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.mixer.init()
effect = pygame.mixer.Sound('bounce.wav')

pygame.display.set_caption("Christoper's Pong Game", "Pong")

pygame.font.init()
pygame.mixer.init()
font = pygame.font.SysFont('Arial', 30)
text = font.render('Hello World', 1, white)

ball = Ball()

# Initializes player 1.
player_1 = Player()
player_1.up, player_1.down = pygame.K_w, pygame.K_s  # Sets up and down keys for player 1
player_1.x_pos, player_1.y_pos = 10, 10  # Sets starting position for player 1

# Initializes player 2.
player_2 = Player()
player_2.up, player_2.down = pygame.K_i, pygame.K_k  # Sets up and down keys for player 2
player_2.x_pos, player_2.y_pos = 455, 10  # Sets starting position for player 2

# Serve prompt.
ServePrompt = 'Press SPACEBAR to serve!'
ServeSurface = font.render(ServePrompt, True, white)


# Serve the ball
def serve():
    if player_1.score > player_2.score or player_1.score == player_2.score:
        ball.serve_to_left()
    else:
        ball.serve_to_right()


# Function to blit the debugging stats.
def blit_debug(x_vel, y_vel, x_pos, y_pos):
    debug_surface = font.render('ball x vel {}'.format(x_vel), True, white)
    screen.blit(debug_surface, (160, 10))
    debug_surface = font.render('ball y vel {}'.format(y_vel), True, white)
    screen.blit(debug_surface, (160, 30))
    debug_surface = font.render('ball x pos {}'.format(x_pos), True, white)
    screen.blit(debug_surface, (300, 10))
    debug_surface = font.render('ball y pos {}'.format(y_pos), True, white)
    screen.blit(debug_surface, (300, 30))


# Function to blit the score.
def blit_score(player_1_score, player_2_score):
    score_surface = font.render('{} - {}'.format(player_1_score, player_2_score), True, white)
    screen.blit(score_surface, (230, 400))


# Function for when the ball collides with a paddle.
def paddle_collide(play_ball, paddle_hitbox):
    paddle_x_bound = range(paddle_hitbox[0], paddle_hitbox[0] + paddle_hitbox[2])
    paddle_y_bound = range(paddle_hitbox[1], paddle_hitbox[1] + paddle_hitbox[3])
    paddle_midpoint = paddle_hitbox[0] + (paddle_hitbox[2] // 2), paddle_hitbox[1] + (paddle_hitbox[3] // 2)
    distance_from_mid = play_ball.x_pos - paddle_midpoint[0], play_ball.y_pos - paddle_midpoint[1]

    # If the ball overlaps with any players:
    if ((play_ball.x_pos in paddle_x_bound) or (play_ball.x_pos + play_ball.radius in paddle_x_bound)) and \
            ((play_ball.y_pos in paddle_y_bound) or play_ball.y_pos + play_ball.radius in paddle_y_bound):

        # Changes the x_vel of the ball accordingly.
        play_ball.x_vel = -play_ball.x_vel

        # Changes the y_vel of the ball accordingly.
        if (distance_from_mid[1]) == 0:
            play_ball.y_vel = 0
        if 0 < (distance_from_mid[1]) <= 8:
            play_ball.y_vel = 1
        if 8 < (distance_from_mid[1]) <= 16:
            play_ball.y_vel = 2
        if 16 < (distance_from_mid[1]) <= 24:
            play_ball.y_vel = 3
        if 24 < (distance_from_mid[1]) <= 32:
            play_ball.y_vel = 4
        if 32 < distance_from_mid[1] <= 40:
            play_ball.y_vel = 5

        if 0 > (distance_from_mid[1]) >= -8:
            play_ball.y_vel = -1
        if -8 > (distance_from_mid[1]) >= -16:
            play_ball.y_vel = -2
        if -16 > (distance_from_mid[1]) >= -24:
            play_ball.y_vel = -3
        if -24 > (distance_from_mid[1]) >= -32:
            play_ball.y_vel = -4
        if -32 > distance_from_mid[1] >= -40:
            play_ball.y_vel = -5

        effect.play()  # Plays sound effect upon collision.


while play:

    # Updates hitbox.
    player_1.hitbox_update()
    player_2.hitbox_update()

    screen.fill((0, 0, 0))
    blit_score(player_1.score, player_2.score)

    # Blits prompt to serve ball until ball is served.
    if match is False:
        screen.blit(ServeSurface, (130, 200))

    # Blits debug stats onto screen when toggled.
    if debug is True:
        blit_debug(ball.x_vel, ball.y_vel, ball.x_pos, ball.y_pos)
        pygame.draw.rect(screen, (255, 0, 0), player_1.hitbox, 2)
        pygame.draw.rect(screen, (255, 0, 0), player_2.hitbox, 2)
        ball.draw_hitbox()

    # When ball collides with a hitbox (wall or paddle):
    # When ball collides with wall:
    if ball.y_pos < 0:
        ball.y_vel = -ball.y_vel
        effect.play()
    if ball.y_pos > screen_height - ball.radius:
        ball.y_vel = -ball.y_vel
        effect.play()

    # Checks whether ball collides with paddle and adjusts accordingly.
    paddle_collide(ball, player_1.hitbox)
    paddle_collide(ball, player_2.hitbox)

    # When ball goes out-of-bounds and either player scores a point.
    if ball.x_pos > screen_width:
        player_1.score += 1
        match = False
        ball.reset()
    if ball.x_pos < 0:
        player_2.score += 1
        match = False
        ball.reset()

    ball.tick()

    for event in pygame.event.get():

        # Allows the user to exit game when window is closed.
        if event.type == pygame.QUIT:
            play = False

        # If a key has been pressed down:
        if event.type == pygame.KEYDOWN:

            # Serves the ball.
            if event.key == pygame.K_SPACE and match is False:
                serve()
                match = True

            # Toggles debug stats
            if event.key == pygame.K_BACKSPACE:
                if debug is True:
                    debug = False
                else:
                    debug = True

            # If player 1 presses a key.
            if event.key == player_1.up:
                player_1.y_pos -= mov_speed
            if event.key == player_1.down:
                player_1.y_pos += mov_speed

            # If player 2 presses a key.
            if event.key == player_2.up:
                player_2.y_pos -= mov_speed
            if event.key == player_2.down:
                player_2.y_pos += mov_speed

            # Out-of-bounds conditions:
            # Prevents out-of-bounds for player 1.
            if player_1.y_pos < 0:
                player_1.y_pos = 0
            if player_1.y_pos > screen_height - player_1.y_size:
                player_1.y_pos = screen_height - player_1.y_size

            # Prevents out-of-bounds for player 2.
            if player_2.y_pos < 0:
                player_2.y_pos = 0
            if player_2.y_pos > screen_height - player_2.y_size:
                player_2.y_pos = screen_height - player_2.y_size

        # Prints out position of mouse for debugging.
        if event.type == pygame.MOUSEBUTTONDOWN and debug is True:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(mouse_pos[0], mouse_pos[1], 30, 30))

    # Draw player 1
    pygame.draw.rect(screen, player_1.colour, pygame.Rect(player_1.x_pos,
                                                          player_1.y_pos,
                                                          player_1.x_size,
                                                          player_1.y_size))

    # Draw player 2
    pygame.draw.rect(screen, player_2.colour, pygame.Rect(player_2.x_pos,
                                                          player_2.y_pos,
                                                          player_2.x_size,
                                                          player_2.y_size))

    # Draw ball
    pygame.draw.circle(screen, ball.colour, (ball.x_pos, ball.y_pos), ball.radius)

    pygame.display.flip()
    clock.tick(30)
