import pygame
import math
import random
import time
from pygame import mixer


def distance(c1, c2):
    return math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))


def reset():
    global ball_center
    global rect1, rect2
    global ball_x_change, ball_y_change
    global ball_state
    ball_x_change = -(
            (random.random() * ((ball_speed / math.sqrt(2)) - (ball_speed * math.sqrt(3) / 2))) + (
            ball_speed * math.sqrt(3) / 2))
    ball_y_change = (math.sqrt((ball_speed ** 2) - (ball_x_change ** 2))) * (
            (-1) ** (int(random.random() * 2) + 1))
    rect1.topleft = (5, (HEIGHT - bar_height) / 2)
    rect2.topleft = (WIDTH - bar_width - 5, (HEIGHT - bar_height) / 2)
    ball_center = [(rect2.left - ball_radius - 5), rect2.center[1]]


pygame.init()

WIDTH, HEIGHT = 800, 700
bar_width = 20
bar_height = 100
ball_radius = 10
bar_speed = 4
ball_speed = (((math.sqrt((HEIGHT ** 2) + (WIDTH ** 2))) / (HEIGHT - bar_height)) * bar_speed) * 1.5
upper_boundary = 100
lower_boundary = HEIGHT - 5


# Don't change anything beyond this point
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Sound
collide_sound = mixer.Sound("wall_collision.wav")
beep_sound = mixer.Sound("beep.wav")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")

result = pygame.Surface((WIDTH, upper_boundary + 5))
score1 = 0
score2 = 0
pygame.draw.rect(result, white, (5, 5, WIDTH - 10, upper_boundary - 5), 1)
font = pygame.font.Font("freesansbold.ttf", 32)
score_text11 = font.render("PLAYER", True, white)
score_text12 = font.render(f"SCORE: {score1}", True, white)
score_text21 = font.render("AI", True, white)
score_text22 = font.render(f"SCORE: {score2}", True, white)

result.blit(score_text11, (50, 13))
result.blit(score_text12, (50, 55))
result.blit(score_text21, (WIDTH - 200, 13))
result.blit(score_text22, (WIDTH - 200, 55))

player1 = pygame.Surface((bar_width, bar_height))
player2 = pygame.Surface((bar_width, bar_height))
player1.fill(red)
player2.fill(red)
rect1 = player1.get_rect()
rect2 = player2.get_rect()
rect1.topleft = (5, (HEIGHT - bar_height)/2)
rect2.topleft = (WIDTH - bar_width - 5, (HEIGHT - bar_height)/2)
y1_change = 0
y2_change = 0

ball_center = [(rect2.left - ball_radius - 5), rect2.center[1]]

ball_state = "rest"
ball_x_change = 0
ball_y_change = 0
collision_state = False
collision_time_count = 0

font2 = pygame.font.Font("freesansbold.ttf", 16)
text = font2.render("Press any key to continue", True, white)
text_rect = text.get_rect()
text_rect.center = (WIDTH / 2, (HEIGHT + upper_boundary) / 2)

clock = pygame.time.Clock()

first = True
while True:

    screen.fill(black)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
        if events.type == pygame.KEYDOWN:

            # Not sure
            if ball_state == "rest":
                ball_state = "motion"
                reset()

            if events.key == pygame.K_UP:
                y1_change = -bar_speed
            if events.key == pygame.K_DOWN:
                y1_change = bar_speed
        if events.type == pygame.KEYUP:
            if (events.key == pygame.K_UP) or (events.key == pygame.K_DOWN):
                y1_change = 0
    result.fill(black)
    pygame.draw.rect(result, white, (5, 5, WIDTH - 10, upper_boundary - 5), 1)
    score_text11 = font.render("PLAYER", True, white)
    score_text12 = font.render(f"SCORE: {score1}", True, white)
    score_text21 = font.render("AI", True, white)
    score_text22 = font.render(f"SCORE: {score2}", True, white)

    result.blit(score_text11, (50, 13))
    result.blit(score_text12, (50, 55))
    result.blit(score_text21, (WIDTH - 200, 13))
    result.blit(score_text22, (WIDTH - 200, 55))
    screen.blit(result, (0, 0))

    if ball_state == "rest":
        screen.blit(text, text_rect)
    # if collision_state:
    #     if collision_time_count >= 0:
    #         collision_state = False
    #     else:
    #         collision_time_count += 1

    # Score recording
    if ball_center[0] < -(ball_radius / 2):
        score2 += 1
        ball_state = "rest"
        mixer.stop()
        beep_sound.play()
        time.sleep(0.2)
        reset()
    elif ball_center[0] > WIDTH + (ball_radius / 2):
        score1 += 1
        ball_state = "rest"
        mixer.stop()
        beep_sound.play()
        time.sleep(0.2)
        reset()

    # Setting boundaries:
    if rect1.top < upper_boundary:
        rect1.top = upper_boundary
    if rect1.bottom > lower_boundary:
        rect1.bottom = lower_boundary
    if rect2.top < upper_boundary:
        rect2.top = upper_boundary
    if rect2.bottom > lower_boundary:
        rect2.bottom = lower_boundary

    screen.blit(player1, rect1)
    screen.blit(player2, rect2)

    # Ball mechanism
    pygame.draw.circle(screen, blue, ball_center, ball_radius)

    if first:
        first = False
        ball_state = "rest"
        reset()
    # if ball_state == "rest":
    #     ball_state = "motion"
    #     ball_x_change = -((random.random()*((ball_speed / math.sqrt(2)) - (ball_speed * math.sqrt(3) / 2))) + (ball_speed * math.sqrt(3) / 2))
    #     ball_y_change = (math.sqrt((ball_speed ** 2) - (ball_x_change ** 2))) * ((-1) ** (int(random.random() * 2) + 1))

    # Ball boundaries
    if ball_state == "motion":
        # Bouncing from upper and lower boundaries
        if abs(ball_center[1] - upper_boundary) <= ball_radius:
            ball_y_change *= (-1)

            # Not sure
            ball_center[0] += ball_x_change
            ball_center[1] += ball_y_change

            collision_state = True
            collision_time_count = 0

            mixer.stop()
            collide_sound.play()
        if abs(ball_center[1] - lower_boundary) <= ball_radius:
            ball_y_change *= (-1)

            # Not sure
            ball_center[0] += ball_x_change
            ball_center[1] += ball_y_change

            collision_state = True
            collision_time_count = 0

            mixer.stop()
            collide_sound.play()

        # Bouncing from sides of rect1
        if (ball_center[1] >= rect1.top) and (ball_center[1] <= rect1.bottom):
            if abs(ball_center[0] - rect1.right) <= ball_radius:
                ball_x_change *= (-1)

                # Not sure
                ball_center[0] += ball_x_change
                ball_center[1] += ball_y_change

                collision_state = True
                collision_time_count = 0

                mixer.stop()
                collide_sound.play()
        # Bouncing from sides of rect2
        if (ball_center[1] >= rect2.top) and (ball_center[1] <= rect2.bottom):
            if abs(ball_center[0] - rect2.left) <= ball_radius:
                ball_x_change *= (-1)

                # Not sure
                ball_center[0] += ball_x_change
                ball_center[1] += ball_y_change

                collision_state = True
                collision_time_count = 0

                mixer.stop()
                collide_sound.play()

        # Bouncing from corners of rect1
        if ball_center[1] < rect1.top:
            if ball_center[0] > rect1.right:
                if distance(ball_center, rect1.topright) <= ball_radius:
                    ball_x_change *= (-1)
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()
            # Bouncing from upper side of rect1:
            elif ball_center[0] < rect1.right:
                if (abs(ball_center[1] - rect1.top) <= ball_radius) or \
                        (distance(ball_center, rect1.topleft) <= ball_radius):
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()

        if ball_center[1] > rect1.bottom:
            if ball_center[0] > rect1.right:
                if distance(ball_center, rect1.bottomright) <= ball_radius:
                    ball_x_change *= (-1)
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()
            # Bouncing from lower side of rect1
            elif ball_center[0] < rect1.right:
                if (abs(ball_center[1] - rect1.bottom) <= ball_radius) or \
                        (distance(ball_center, rect1.bottomleft) <= ball_radius):
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()

        # Bouncing from corners of rect2
        if ball_center[1] < rect2.top:
            if ball_center[0] < rect2.left:
                if distance(ball_center, rect2.topleft) <= ball_radius:
                    ball_x_change *= (-1)
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()
            # Bouncing from upper side of rect2:
            elif ball_center[0] > rect2.left:
                if (abs(ball_center[1] - rect2.top) <= ball_radius) or \
                        (distance(ball_center, rect1.topright) <= ball_radius):
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()

        if ball_center[1] > rect2.bottom:
            if ball_center[0] < rect2.left:
                if distance(ball_center, rect2.bottomleft) <= ball_radius:
                    ball_x_change *= (-1)
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()
            # Bouncing from lower side of rect2
            elif ball_center[0] > rect2.left:
                if (abs(ball_center[1] - rect2.bottom) <= ball_radius) or \
                        (distance(ball_center, rect1.bottomright) <= ball_radius):
                    ball_y_change *= (-1)

                    # Not sure
                    ball_center[0] += ball_x_change
                    ball_center[1] += ball_y_change

                    collision_state = True
                    collision_time_count = 0

                    mixer.stop()
                    collide_sound.play()
    if ball_state == "motion":
        ball_center[0] += ball_x_change
        ball_center[1] += ball_y_change

    # Updating Coordinates of AI
    if ball_state == "motion":
        if ball_center[1] > rect2.center[1]:
            y2_change = bar_speed
        if ball_center[1] < rect2.center[1]:
            y2_change = -bar_speed
        if ball_center[1] == rect2.center[1]:
            y2_change = 0

    # Updating coordinates of Player
    # if not collision_state:
    #     rect1.top += y1_change
    # if not collision_state:
    #     rect2.top += y2_change
        rect1.top += y1_change
        rect2.top += y2_change

    pygame.display.flip()
    clock.tick(60)
