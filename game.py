'''
Game Engine
'''

# Imports

import pygame
import random, math
import cv2
import face_recognition

from colors import *
from enemy import returnEnemyList

# Shapes
SQUARE = 0
CIRCLE = 1

# Songs
SONGPATH = './music/'
SONGNAME = 'shapeofyou' # Change song name here

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen Width and Height
screen_width = 600
screen_height = 700
screen_sections = 3
screen = pygame.display.set_mode([screen_width, screen_height])

# Player Position
player_width = 50
player_y = 50
player_height = player_width * math.sqrt(3)/2
player_margin = screen_width // screen_sections // 2 - player_width // 2

# Loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

def returnPlayerCoordinates(x):
    region = x // (webcam_width // webcam_regions)
    if region == webcam_center: region = 1
    elif region < webcam_center: region = 2
    elif region > webcam_center: region = 0
    coordinate1 = [ screen_width // screen_sections // 2 + region * (screen_width // screen_sections) - player_width//2, screen_height - player_y ]
    coordinate2 = [ screen_width // screen_sections // 2 + region * (screen_width // screen_sections), screen_height - (player_y + player_height) ]
    coordinate3 = [ screen_width // screen_sections // 2 + region * (screen_width // screen_sections) + player_width//2, screen_height - player_y ]
    return [coordinate1, coordinate2, coordinate3]

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
player_image = face_recognition.load_image_file("players/player.jpg")
player_face_encoding = face_recognition.face_encodings(player_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

webcam_width = 1280
webcam_height = 720
webcam_regions = 9
webcam_center = webcam_regions // 2

player_location = webcam_width // 2

enemy_radius = 30
enemy_dx = 20
enemiesToCome = returnEnemyList(SONGNAME)
enemiesOnScreen = [] # [ [ x-coordinate, y-coordinate, SHAPE, COLOR] ]

fx = 0.25

# Music
pygame.mixer.music.load(SONGPATH + SONGNAME + '.wav')
pygame.mixer.music.play()

def drawEnemy(x, y, shape, color):
    if shape == CIRCLE:
        pygame.draw.circle(screen, color, [x, y], enemy_radius)

# Game Loop
while not done:
    songTime = pygame.mixer.music.get_pos()
    if songTime > 45000:
        done = not done
    if songTime > enemiesToCome[0][0]:
        time, code = enemiesToCome.pop(0)
        if code == 0:
            xCoordinate = screen_width // screen_sections // 2 + 0 * (screen_width // screen_sections)
            yCoordinate = 0
            shape = CIRCLE
            color = random.choice(COLORS)
            enemiesOnScreen += [ [xCoordinate, yCoordinate, shape, color] ]
        elif code == 1:
            xCoordinate = screen_width // screen_sections // 2 + 1 * (screen_width // screen_sections)
            yCoordinate = 0
            shape = CIRCLE
            color = random.choice(COLORS)
            enemiesOnScreen += [ [xCoordinate, yCoordinate, shape, color] ]
        elif code == 2:
            xCoordinate = screen_width // screen_sections // 2 + 2 * (screen_width // screen_sections)
            yCoordinate = 0
            shape = CIRCLE
            color = random.choice(COLORS)
            enemiesOnScreen += [ [xCoordinate, yCoordinate, shape, color] ]

    # Grab one frame from video_capture
    ret, frame = video_capture.read()

    # Resize frame of video to for faster recognition
    small_frame = cv2.resize(frame, (0, 0), fx=fx, fy=fx)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
    face_names = []
    for index in range(len(face_encodings)):
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([player_face_encoding], face_encodings[index], tolerance=0.8)

        if match[0]:
           player_location = (face_locations[0][1] / fx + face_locations[0][3] / fx) // 2

    # Exit Control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Draw the Background
    screen.fill(PANE2)
    bg1 = pygame.draw.rect(screen, PANE1, [screen_width // screen_sections * 0, screen_height * 0, screen_width // screen_sections * 1, screen_height])
    bg2 = pygame.draw.rect(screen, PANE2, [screen_width // screen_sections * 1, screen_height * 0, screen_width // screen_sections * 2, screen_height])
    bg3 = pygame.draw.rect(screen, PANE3, [screen_width // screen_sections * 2, screen_height * 0, screen_width // screen_sections * 3, screen_height])

    # Draw Player
    pygame.draw.polygon(screen, PLAYER_COLOR, returnPlayerCoordinates(player_location))

    # Draw Enemy
    for index in range(len(enemiesOnScreen)):
        drawEnemy(*enemiesOnScreen[index])
        enemiesOnScreen[index][1] += enemy_dx

    for ind in range(len(enemiesOnScreen)):
        ex, ey = enemiesOnScreen[ind][0], enemiesOnScreen[ind][1]
        cy2 = returnPlayerCoordinates(player_location)[0][1]
        cx, cy = returnPlayerCoordinates(player_location)[1][0], returnPlayerCoordinates(player_location)[1][1]
        if ex == cx and (cy <= ey - enemy_radius <= cy2):
            score -= 20
            enemiesOnScreen.pop(ind)
            break

    print(score)

    # Update Screen
    pygame.display.flip()

    # Increment Score
    score += random.choice([1, 2])

    # Limit to 60 frames per second
    clock.tick(10)

print("Final Score: " + str(score))
pygame.quit()
