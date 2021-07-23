import pygame, sys, time, random

#initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480

#Parameters for Snake
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
snake_rect = []
direction = 'RIGHT'
change_to = direction

#Parameters for food
food_pos = [0,0]
food_spawn = False

score = 0


# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

food_rect = pygame.Rect(0,0,10,10)
food_rect.centerx = food_pos[0]
food_rect.centery = food_pos[1]

for i in range(0,len(snake_body)):
    snake_rect.append(pygame.Rect(0,0,10,10))
    snake_rect[i].centerx = snake_body[i][0]
    snake_rect[i].centery = snake_body[i][1]
    pygame.draw.rect(game_window, (255,255,0), snake_rect[i])

pygame.display.update()



# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()


def check_for_events():
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    global change_to
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
        return



def update_snake():
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    # Code for making the snake move in the expected direction
    
    global direction, change_to, snake_rect, snake_body, snake_pos, score, food_spawn

    if (((change_to == 'RIGHT') or (change_to == 'LEFT')) and ((direction == 'UP') or (direction == 'DOWN'))) or (((change_to == 'UP') or (change_to == 'DOWN')) and ((direction == 'RIGHT') or (direction == 'LEFT'))):
        direction = change_to

    temp_pos_1 = [0,0]
    temp_pos_2 = [0,0]

    temp_pos_1[0] = snake_pos[0]
    temp_pos_1[1] = snake_pos[1]
    temp_pos_2[0] = temp_pos_1[0]
    temp_pos_2[1] = temp_pos_1[1]

    #Head Moves
    if direction == 'RIGHT':
        snake_rect[0].centerx += 10
        snake_body[0][0] += 10
        snake_pos[0] += 10
    if direction == 'LEFT':
        snake_rect[0].centerx -= 10
        snake_body[0][0] -= 10
        snake_pos[0] -= 10
    if direction == 'DOWN':
        snake_rect[0].centery += 10
        snake_body[0][1] += 10
        snake_pos[1] += 10
    if direction == 'UP':
        snake_rect[0].centery -= 10
        snake_body[0][1] -= 10
        snake_pos[1] -= 10
    

    for i in range(1, len(snake_body)):
        temp_pos_2[0] = snake_body[i][0]
        temp_pos_2[1] = snake_body[i][1]

        snake_rect[i].centerx = temp_pos_1[0]
        snake_rect[i].centery = temp_pos_1[1]

        snake_body[i][0] = temp_pos_1[0]
        snake_body[i][1] = temp_pos_1[1]

        temp_pos_1[0] = temp_pos_2[0]
        temp_pos_1[1] = temp_pos_2[1]

    if food_caught():
        score += 1
        snake_body.append(temp_pos_1)
        snake_rect.append(pygame.Rect(0, 0, 10, 10))
        snake_rect[len(snake_body) - 1].centerx = temp_pos_1[0]
        snake_rect[len(snake_body) - 1].centery = temp_pos_1[1]
        pygame.draw.rect(game_window, (255,255,0), snake_rect[len(snake_body) - 1])
        show_score((50,30),(240,240,240),None, 30)

        food_spawn = False
        create_food()

    pygame.display.update()

    if collision_occurred():
        game_over()

    update_screen()


    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions 
    # since we have not made snake and food as a specific sprite or surface.
    

    # End the game if the snake collides with the wall or with itself. 
    
def food_caught():
    global snake_pos, food_pos

    if abs(snake_pos[0] - food_pos[0]) < 10 and abs(snake_pos[1] - food_pos[1]) < 10:
        return True
    else:
        return False


def collision_occurred():
    global snake_pos, snake_body

    for i in range(1, len(snake_body)):
        if abs(snake_pos[0] - snake_body[i][0]) < 10 and abs(snake_pos[1] - snake_body[i][1]) < 10:
            return True
    if snake_pos[0] not in range(0, frame_size_x) or snake_pos[1] not in range(0, frame_size_y):
        return True
    return False


def create_food():
    """ 
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global food_spawn, food_rect

    if not food_spawn:
        food_rect.centerx = food_pos[0] = 10 + 10*random.randrange(0, frame_size_x/10 - 4)
        food_rect.centery = food_pos[1] = 10 + 10*random.randrange(0, frame_size_y/10 - 4)

        pygame.draw.rect(game_window, (255, 255, 255), food_rect)

        food_spawn = True

        pygame.display.update()


def show_score(pos, color, font, size):
    """
    It takes in the above arguements and shows the score at the given pos according to the color, font and size.
    """
    global score

    score_text = "Score = %d" % score
    score_img = pygame.font.SysFont(font,size).render(score_text, True, color)
    score_rect = score_img.get_rect()
    score_rect.center = pos
    game_window.blit(score_img, score_rect)
    pygame.display.update()


def update_screen():
    """
    Draw the snake, food, background, score on the screen
    """
    global snake_rect, food_rect

    game_window.fill((0,0,0))

    show_score((50,30),(240,240,240),None, 30)

    for i in range(0, len(snake_rect)):
        pygame.draw.rect(game_window, (255,255,0), snake_rect[i])

    pygame.draw.rect(game_window, (255, 255, 255), food_rect)

    pygame.display.update()


def game_over():
    """ 
    Write the function to call in the end. 
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    gameover_img = pygame.font.SysFont(None,48).render("GAME OVER",True,(240,240,240))
    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = frame_size_x/2
    gameover_rect.top = 50
    game_window.blit(gameover_img, gameover_rect)
    pygame.display.update()
    time.sleep(3)
    sys.exit()


# Main loop
while True:
    # Make appropriate calls to the above functions so that the game could finally run
    show_score((50,30),(240,240,240),None, 30)
    create_food()
    check_for_events()
    update_snake()
    

    # To set the speed of the screen
    fps_controller.tick(25)