"""
Religion Project: By Chenyu (Eric) Lu
Teacher: Ms.Ferraro
Made with Pygame

"""


#importing modules
from math import sin, cos, radians
import pygame
from pygame import K_LEFT, K_RIGHT
import random
#_________________________________________#


pygame.init()


# Setting up screen, color, and variables
# Setting up screen, color, and variables
WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)
time = 0  # Game time for day/night cycle
GRASS_Y = HEIGHT - 80  # Y position of the grass
DAY_COLOR = (0, 255, 255)  # Cyan for day
NIGHT_COLOR = (0, 0, 128)  # Dark blue for night
WINDOW_DAY_COLOR = (173, 216, 230)  # Cyan window color for day
WINDOW_NIGHT_COLOR = (255, 255, 100)  # Yellow window color for night
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
white = (255, 255, 255)  # Color values for quick access
character_y = GRASS_Y  # Character initially starts on the ground
character_x = WIDTH / 2  # Centered horizontally
jump_speed = 15
is_jumping = False
move_speed = 5


#^ I will make the window and sky color change as time in the game goes on.
#------------------------
# Sun parameters
center_of_rotation_x = WIDTH / 2
center_of_rotation_y = HEIGHT / 2 + 180
radius = 400
sunangle = radians(45)
moonangle = radians(225)
omega = 0.03
sun_radius = 40


#------------------------
#setting up text
pygame.display.set_caption('RELIGION PRAYER') #set title for game
font = pygame.font.Font('freesansbold.ttf', 15)
text = font.render('Left and right arrow keys', True, (0, 0, 0), white)
textRect = text.get_rect()
textRect.center = (470, HEIGHT-40)
text3 = font.render('WASD to control character', True, (0, 0, 0), white)
textRect = text.get_rect()
textRect.center = (470, HEIGHT-40)
textRect3 = text3.get_rect()
textRect3.center = (260, HEIGHT-40)

# Snow/rain parameters
rain_count = 100
raindrops = []
for _ in range(rain_count):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(2, 5)
    raindrops.append([x, y, speed])

# Initialize global variables
running = True
while running:
    #get keys pressed variable
    keys = pygame.key.get_pressed()
    #render texts
    text2 = font.render(f'Time : {time}', True, (0, 0, 0), white)
    textRect2 = text2.get_rect()
    textRect2.center = (90, HEIGHT - 40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
#keys pressing
    # Updated Jump Logic in the  Main Loop
    if keys[pygame.K_w] and not is_jumping:
        is_jumping = True
        jump_speed = 15

    if is_jumping:
        character_y -= jump_speed
        jump_speed -= 1
        if jump_speed < -15:
            is_jumping = False
            jump_speed = 15
            character_y = GRASS_Y  # Return to ground level

    # Horizontal movement with 'A' and 'D' keys
    if keys[pygame.K_a]:
        character_x -= move_speed
    if keys[pygame.K_d]:
        character_x += move_speed

    # Screen wrapping for character
    if character_x > WIDTH:
        character_x = -30  # Wrap to the left
    elif character_x < -30:
        character_x = WIDTH  # Wrap to the right

    if keys[K_LEFT]:
        sunangle += omega
        moonangle += omega
        time -= 23
    elif keys[K_RIGHT]:
        sunangle -= omega
        moonangle -= omega
        time += 23

    # Calculate sun and moon positions
    sun_x = center_of_rotation_x + radius * cos(sunangle)
    sun_y = center_of_rotation_y - radius * sin(sunangle)
    moon_x = center_of_rotation_x + radius * cos(moonangle)
    moon_y = center_of_rotation_y - radius * sin(moonangle)
    #set time so 3600 ticks in a day. If we go over, we set it to zero
    if time > 3600:
        time = 0
    if time < 0:
        time = 3600
    if character_x > WIDTH+30:
        characterx = -30
    # Calculate blend ratio for background and window colors
    if sun_y < GRASS_Y:
        blend_ratio = min(1, max(0, (GRASS_Y - sun_y) / (GRASS_Y - (center_of_rotation_y - radius))))
        background_color = (
            int(NIGHT_COLOR[0] * (1 - blend_ratio) + DAY_COLOR[0] * blend_ratio),
            int(NIGHT_COLOR[1] * (1 - blend_ratio) + DAY_COLOR[1] * blend_ratio),
            int(NIGHT_COLOR[2] * (1 - blend_ratio) + DAY_COLOR[2] * blend_ratio)
        )
        window_color = (
            int(WINDOW_NIGHT_COLOR[0] * (1 - blend_ratio) + WINDOW_DAY_COLOR[0] * blend_ratio),
            int(WINDOW_NIGHT_COLOR[1] * (1 - blend_ratio) + WINDOW_DAY_COLOR[1] * blend_ratio),
            int(WINDOW_NIGHT_COLOR[2] * (1 - blend_ratio) + WINDOW_DAY_COLOR[2] * blend_ratio)
        )

    # draw background, sun, moon, and grass
    screen.fill(background_color)
    pygame.draw.circle(screen, (255, 255, 0), (int(sun_x), int(sun_y)), sun_radius)
    pygame.draw.circle(screen, (255, 255, 225), (int(moon_x), int(moon_y)), sun_radius)

    pygame.draw.rect(screen, (255, 255, 255), (0, GRASS_Y, WIDTH, HEIGHT - GRASS_Y))

    # draw my buildings and windows
    myrect = pygame.draw.rect(screen, (128, 0, 0), (HEIGHT - 323, 191, 376 - 157, 209))
    pygame.draw.rect(screen, (128, 0, 0), (376, 282, 495 - 377, HEIGHT - 80 - 282))
    pygame.draw.polygon(screen, (0, 0, 0), [(156, 193), (262, 116), (372, 190)])
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    # windows with changing color
    for i in range(3):
        pygame.draw.rect(screen, window_color, (120 + 60 * (i + 1), 214, 50, 50))
    pygame.draw.rect(screen, window_color, (300, 280, 50, 50))
    pygame.draw.rect(screen, (79, 32, 15), (180, 300, 70, 100))#door
    pygame.draw.circle(screen, (255, 255, 0), (233, 350), 8)
    pygame.draw.circle(screen, (255, 255, 255), (584, GRASS_Y- 70 - 30), 30) #Snowman!
    pygame.draw.circle(screen, (255, 255, 255), (584, GRASS_Y - 40), 40)
    pygame.draw.polygon(screen, (128, 128, 128), [(381, 310), (381, 400), (473, 400), (473, 310)])
    # draw garage
    pygame.draw.polygon(screen, (79, 32, 15), [(551, 340), (531, 334), (530, 320), (524, 321), (524, 337), (513, 337), (513, 344), (530, 343), (547, 348) ])
    pygame.draw.polygon(screen, (79, 32, 15), ([(620, 341), (639, 331), (639, 341), (621, 348)]))
    pygame.draw.polygon(screen, (255, 165, 0), ([(574, 299), (574, 306), (535, 302)]))
    pygame.draw.circle(screen, (0, 0, 0), (567, 288), 3)
    pygame.draw.circle(screen, (0, 0 , 0), (580, 288), 3)
    for i in range(3):
        pygame.draw.circle(screen, (0, 0, 0), (579, 335 + 20 * i), 3)
    for i in range(9):
        pygame.draw.rect(screen, (0, 0, 0), (381, 400 - 9 * (i + 1), 474 - 381, 2))
    pygame.draw.rect(screen, (0, 0, 0), (character_x, character_y-70, 30, 20))#draw head
    pygame.draw.rect(screen, (0, 0, 255), (character_x, character_y-50, 30, 50)) #draw body
    # Draw raindrops
    for drop in raindrops:
        drop[1] += drop[2]  # move drop down by its speed
        if drop[1] > GRASS_Y:  # reset to the top if it reaches the ground
            drop[0] = random.randint(0, WIDTH)
            drop[1] = random.randint(-20, 0)
            drop[2] = random.uniform(2, 5)
        pygame.draw.line(screen, (173, 216, 230), (drop[0], drop[1]), (drop[0], drop[1] + 5), 1)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
