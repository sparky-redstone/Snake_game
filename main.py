import pygame
import random
import os
from pygame import mixer

# initializing the modules
pygame.init()
# color
white = (255, 255, 255)
black = (0, 0, 0)
amber_yellow = (255, 191, 0)
aero_blue = (201, 255, 229)
red = (225, 0, 0)
blue = (0, 0, 255)
green = (0, 128, 0)
# game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake Game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
title = pygame.font.SysFont('comicsansms', 45)
font = pygame.font.SysFont('comicsansms', 30)
clock = pygame.time.Clock()
back = pygame.image.load('background.png')
gameover = pygame.image.load('gameover.png')
bgm = mixer.Sound('snake_bgm.mp3')
bgm.play(-1)


def text_screen(text, color, x, y):
    show_text = font.render(text, True, color)
    screen.blit(show_text, (x, y))


def title_screen(text, color, x, y):
    show_text = title.render(text, True, color)
    screen.blit(show_text, (x, y))


def plot_snake(screen, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.circle(screen, color, [x, y], snake_size)


def welcome():
    exit_game = True
    while exit_game:
        screen.fill(black)
        screen.blit(back, (-20, 0))
        title_screen("WELCOME TO SNAKES", white, 280, 420)
        text_screen("(Press 'any key' to enter the game)", blue, 280, 480)
        text_screen("(Press 'SPACE' to pause/continue the game)",
                    blue, 160, 520)
        text_screen(
            "(RULE)-Don't run into yourself or the edges...", red, 100, 10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.QUIT:
                    pass
                else:
                    gameloop()
        clock.tick(30)
        pygame.display.update()


def pause():
    paused = True
    title_screen("GAME PAUSED", green, 260, 20)
    text_screen("(Press 'SPACE' to continue...)", blue, 220, 520)
    bgm.stop()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    bgm.play(-1)
        clock.tick(30)
        pygame.display.update()


# game loop
def gameloop():
    # game variables
    game_over = True
    exit_game = True
    snake_x = 45
    snake_y = 45
    snake_size = 10
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    food_x = random.randrange(20, 790, 5)
    food_y = random.randrange(20, 590, 5)
    fps = 60
    score = 0
    snake_list = []
    snake_len = 1
    if not os.path.exists('hiscore.txt'):
        with open('hiscore.txt', 'w') as f:
            f.write('0')
    with open('hiscore.txt', 'r') as f:
        hiscore = f.read()
    while exit_game:
        if not game_over:
            screen.fill(white)
            screen.blit(gameover, (0, -100))
            title_screen("GAME OVER", red, 280, 380)
            text_screen("(Press 'ENTER' to Play again...)", green, 200, 440)
            text_screen(f" SCORE: {score}", blue, 10, 10)
            bgm.stop()
            # text_screen(f"HIGHSCORE: {hiscore}", blue, 510, 10)
            with open('hiscore.txt', 'w') as f:
                f.write(str(hiscore))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        bgm.play(-1)
                        gameloop()
        else:
            screen.fill(amber_yellow)
            plot_snake(screen, black, snake_list, snake_size)
            pygame.draw.circle(screen, red, [food_x, food_y], snake_size)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_SPACE:
                        pause()
            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 5
                # print(score)
                beep = mixer.Sound('beep.wav')
                beep.play()
                food_x = random.randrange(5, 795, 5)
                food_y = random.randrange(5, 595, 5)
                snake_len += 5
                if score % 50 == 0:
                    init_velocity += 1
                if score > int(hiscore):
                    hiscore = score
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            text_screen(f"SCORE: {score}", blue, 10, 10)
            text_screen(f"HIGHSCORE: {hiscore}", blue, 510, 10)
            if len(snake_list) > snake_len:
                del snake_list[0]
            if head in snake_list[:-1]:
                game_over = False
                pygame.mixer.music.load('explosion.wav')
                pygame.mixer.music.play()
            # border
            if snake_x < 0 or snake_y < 0 or snake_x > 800 or snake_y > 600:
                game_over = False
                pygame.mixer.music.load('explosion.wav')
                pygame.mixer.music.play()
                # print('Game over')
            # classic
            # if snake_x < 5:
            #     snake_x = 795
            # if snake_x > 795:
            #     snake_x = 5
            # if snake_y < 5:
            #     snake_y = 595
            # if snake_y > 595:
            #     snake_y = 5
        clock.tick(fps)
        pygame.display.update()
    pygame.quit()
    quit()


welcome()
