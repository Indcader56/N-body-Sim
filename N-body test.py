# Imports
import pygame
import sys
import random
import math

import physics

# Initalizing stuff
pygame.init()
pygame.font.init()

window_size_x = 960
window_size_y = 720

window_size = (window_size_x,window_size_y)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("N-body sim")

# Colors used for assents
random_color = (random.randint(15,255),random.randint(15,255),random.randint(15,255))
line_color = (255,255,255)
text_color = (255,255,255)
red = (255,0,0)

# Font for text
text_font = pygame.font.Font(None, 50)

small_text_font = pygame.font.Font(None, 35)

# Button images
button_one = pygame.transform.scale(pygame.image.load("assents/Button_one.png"), (55,55))
button_two = pygame.transform.scale(pygame.image.load("assents/Button_two.png"), (55,55))
button_three = pygame.transform.scale(pygame.image.load("assents/Button_three.png"), (55,55))

# Alt button images
alt_button_one = pygame.transform.scale(pygame.image.load("assents/Alt-Button_one.png"), (55,55))
alt_button_two = pygame.transform.scale(pygame.image.load("assents/Alt-Button_two.png"), (55,55))
alt_button_three = pygame.transform.scale(pygame.image.load("assents/Alt-Button_three.png"), (55,55))

# Body class
class Body:
    # Initalizes variables needed for a given body
    def __init__(self, x_pos, y_pos, speed_x, speed_y, mass, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mass = mass
        self.color = color
    
    # Updates the speed x and y variables to account for another mass
    def update_speed(self, other_x, other_y, other_mass):
        # Finds the fx and fy componets
        force_componets = physics.find_force_componets(self.x_pos, self.y_pos, self.mass, other_x, other_y, other_mass)

        # Changes the speed x and y variables by the forces
        self.speed_x += (force_componets[0] / self.mass) * dt
        self.speed_y += (force_componets[1] / self.mass) * dt

    # Checks if a collision happens between two bodies
    def check_collision(self, other):
        # Takes the distance between two bodies and checks if they have collided
        distance = math.sqrt(((other.x_pos-self.x_pos)**2) + ((other.y_pos-self.y_pos)**2))

        # Determines the winner of the collision
        if other.mass > math.sqrt(self.mass):
            winner = other
            loser = self
        else:
            winner = self
            loser = other

        # Checks if the collision actually happened and returns based on that
        if distance <= math.sqrt(winner.mass) + math.sqrt(loser.mass):
            return winner, loser
        else:
            return False

    # Updates the position of the body based on the body's speed
    def update_pos(self):
        self.x_pos += self.speed_x * dt
        self.y_pos += self.speed_y * dt

    # Displays the body as a circle with its mass being used as the radius
    def display(self):
        pygame.draw.circle(screen, self.color, (((self.x_pos-player_x)*(player_zoom/100))+window_size_x/2,((self.y_pos+player_y)*(player_zoom/100))+window_size_y/2), math.sqrt(self.mass)*(player_zoom/100))

# The class Button which makes allows buttons to be made
class Button():
    def __init__(self, x,y, image):
        self.x = x
        self.y = y
        self.image = image

    # Draws the button on the screen
    def draw_button(self):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_x > self.x and mouse_x < self.x + 55 and mouse_y > self.y and mouse_y < self.y + 55:
            if self.image == button_one:
                screen.blit(alt_button_one, (self.x, self.y))
            elif self.image == button_two:
                screen.blit(alt_button_two, (self.x, self.y))
            elif self.image == button_three:
                screen.blit(alt_button_three, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

# The buttons list hosts the button objects that can be clicked on to change the mode
buttons = [Button(window_size_x-165, 0, button_one), Button(window_size_x-110, 0, button_two), Button(window_size_x-55, 0, button_three)]

# The list where the body objects are held
bodies = []

# Variable to determine the desired mass of the body
select_mass = 1

# Clock for fps
clock = pygame.time.Clock()

# Variables for user
past_mouse_x = 0
past_mouse_y = 0

"""
The mode key variable determines what the user can do 

1 - Nothing, everything is disabled so that the user can watch
2 - Allows the user to add bodies and shoot them
3 - When a user clicks on a body in this mode, it deletes it

"""
mode_key = 1

# Player position
player_x = 0
player_y = 0
player_zoom = 100

# Which movement button is being clicked?
click_w = False
click_s = False
click_a = False
click_d = False

# Various variables to detect clicks
shift_hold = False
left_hold = False
right_click = False

slider_hold = False

time = 0

# Main Game Loop
while True:
    # Delta time for physics calculations
    dt = clock.tick(60) / 1000
    # Gets the mouse x and y to be used for placement code
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]

    # Empties deleted_bodies so then it can take new bodies
    deleted_bodies = []

    # Checks for user input
    for event in pygame.event.get():
        # Quits the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Goes through the button list and checks if the mouse is hovering over the buttons and checks if a click happens. If it does, it updates the mode_key variable
        hovering_list = []
        for button in buttons:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_x > button.x and mouse_x < button.x + 55 and mouse_y > button.y and mouse_y < button.y + 55:
                    if button.image == button_one:
                        mode_key = 1
                    elif button.image == button_two:
                        mode_key = 2
                    elif button.image == button_three:
                        mode_key = 3

            # Checks if a user is hovering over a button
            if mouse_x > button.x and mouse_x < button.x + 55 and mouse_y > button.y and mouse_y < button.y + 55:
                hovering_list.append(True)
            else:
                hovering_list.append(False)

        # Adds True values to the hovering_list if its over the mass text or the zoom text
        if mouse_x > window_size_x-125 and mouse_y > window_size_y-45:
            hovering_list.append(True)
        if mouse_x < 175 and mouse_y < 75 and mode_key == 2:
            hovering_list.append(True)

        # Logic for when in creation mode
        if mode_key == 2 and not True in hovering_list:
            # Stores the past position to allow the user to move their mouse to change the speed and direction of the body
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    past_mouse_x = mouse_x
                    past_mouse_y = mouse_y
                    left_hold = True

                if event.button == 3:
                    right_click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    right_click = False

            # Cancels the placement operation if the player moves
            if click_d == True or click_w == True or click_a == True or click_s == True or shift_hold == True:
                left_hold = False

            # Computates the speed x and y of the body when it is created based on the mouse pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and left_hold == True:
                    
                start_force_x, start_force_y = physics.find_distance_componets(past_mouse_x, past_mouse_y, mouse_x, mouse_y, select_mass, player_zoom)
                
                bodies.append(Body((((past_mouse_x-window_size_x/2)/(player_zoom/100))+player_x),(((past_mouse_y-window_size_y/2)/(player_zoom/100))-player_y),start_force_x,start_force_y,select_mass, random_color))
                
                random_color = (random.randint(15,255),random.randint(15,255),random.randint(15,255))

                left_hold = False

        # Deletion mode logic
        if mode_key == 3 and not True in hovering_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for body in bodies:
                        if physics.find_distance(((body.x_pos-player_x)*(player_zoom/100))+(window_size_x/2), ((body.y_pos+player_y)*(player_zoom/100))+(window_size_y/2), mouse_x, mouse_y) <= math.sqrt(body.mass)*(player_zoom/100):
                            deleted_bodies.append(body)

        # Independent Logic
        
        # Changes the variables based on the mouse's location
        if event.type == pygame.MOUSEWHEEL:
            # If the mouse is near the mass text and the user scrolls, then select mass changes
            if mouse_x < 175 and mouse_y < 75 and mode_key == 2:
                if shift_hold == True:
                    if event.y  > 0:
                        select_mass += 10
                    if event.y < 0:
                        select_mass -= 10
                else:
                    if event.y  > 0:
                        select_mass += 1
                    if event.y < 0:
                        select_mass -= 1
            # If the mouse is near the time text and the user scrolls, then the rate of time changes
            elif mouse_x > window_size_x-125 and mouse_y > window_size_y-45:
                if shift_hold == True:
                    if event.y > 0:
                        time += 10
                    if event.y < 0:
                        time -= 10
                else:
                    if event.y > 0:
                        time += 1
                    if event.y < 0:
                        time -= 1
            # If the mouse is in the normal play area, then the zoom changes
            else:
                if event.y > 0:
                    player_zoom += 10
                if event.y < 0:
                    player_zoom -= 10

        # Pauses and plays time when the time text is clicked and resets the select_mass variable when that text is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mouse_x > window_size_x-125 and mouse_y > window_size_y-45:
                    if time > 0:
                        past_time = int(time)
                        time = 0

                    elif time == 0:
                        time = past_time
                        past_time = 0

                if mouse_x < 175 and mouse_y < 75 and mode_key == 2:
                    if select_mass > 1:
                        past_select_mass = int(select_mass)
                        select_mass = 1

                    elif select_mass == 1:
                        select_mass = past_select_mass
                        past_select_mass = 1
        
        # Adds a bunch of random bodies when the space key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(200):
                    rnd_x = random.uniform(-1000,1000)
                    rnd_y = random.uniform(-1000,1000)

                    rnd_clr = (random.uniform(10,255),random.uniform(10,255),random.uniform(10,255))

                    rnd_mass = random.uniform(2,10)

                    bodies.append(Body(rnd_x,rnd_y,0,0,rnd_mass, rnd_clr))
                
            # Updates the click values to tell if the user is holding down one of these buttons
            if event.key == pygame.K_d:
                click_d = True
            if event.key == pygame.K_a:
                click_a = True
            if event.key == pygame.K_w:
                click_w = True
            if event.key == pygame.K_s:
                click_s = True
            if event.key == pygame.K_LSHIFT:
                shift_hold = True

        # Updates the click values to tell if the user lifts one of these buttons
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                click_d = False
            if event.key == pygame.K_a:
                click_a = False
            if event.key == pygame.K_w:
                click_w = False
            if event.key == pygame.K_s:
                click_s = False
            if event.key == pygame.K_LSHIFT:
                shift_hold = False

    # Changes the player position when one of the buttons are being held
    if click_d == True:
        player_x += 10
    if click_a == True:
        player_x -= 10
    if click_w == True:
        player_y += 10
    if click_s == True:
        player_y -= 10

    # Makes sure the select_mass variable never goes below 0 or above 200
    if select_mass < 1:
        select_mass = 1
    if select_mass > 5000:
        select_mass = 5000

    # Makes sure the time variable never goes below 0 or above 100
    if time < 0:
        time = 0
    if time > 100:
        time = 100
    
    # Makes sure the zoom is always between 10 and 10,000
    if player_zoom < 10:
        player_zoom = 10
    if player_zoom > 10000:
        player_zoom = 10000

   
    # Clears the screen
    screen.fill((0,0,0))

    # Updates the speed of a given body by looping through every other body and checking attraction
    for body in bodies:
        for other_body in bodies:
            if not body == other_body:
                for t in range(time):
                    # Checks if a collision between bodies has happened and if so, the smaller one gets consumed by the bigger one
                    collided = body.check_collision(other_body)
                    if collided != False:
                        winner, loser = collided
                        
                        # Checks if the winner/loser is in the deleted list so that the function doesn't run twice
                        if not winner in deleted_bodies:
                            if not loser in deleted_bodies:
                                deleted_bodies.append(physics.winner_loser_momentum_and_mass(winner, loser))

                    # Updates the speed
                    body.update_speed(other_body.x_pos,other_body.y_pos,other_body.mass)
    
    # Deletes any bodies in the deleted_bodies list
    for body in deleted_bodies:
        if body in bodies:
            bodies.remove(body)
    
    # Updates the position of the bodies and draws them to the screen
    for body in bodies:
        for t in range(time):
            body.update_pos()
        body.display()

        # If the mouse hovers over a body, and the mode for the user is 3 (delete), then a box will be drawn over the selected body
        if mode_key == 3:
            if physics.find_distance(((body.x_pos-player_x)*(player_zoom/100))+(window_size_x/2), ((body.y_pos+player_y)*(player_zoom/100))+(window_size_y/2), mouse_x, mouse_y) <= math.sqrt(body.mass)*(player_zoom/100):
                pygame.draw.rect(screen,red, ((((body.x_pos-player_x)-math.sqrt(body.mass))*(player_zoom/100)) + window_size_x/2, (((body.y_pos+player_y)-math.sqrt(body.mass))*(player_zoom/100))+window_size_y/2, (math.sqrt(body.mass)*2)*(player_zoom / 100),(math.sqrt(body.mass)*2)*(player_zoom / 100)), 1)
    
    # Draws a circle to show the user what body will be placed and shows a line to show which direction and how fast will it go
    if mode_key == 2 and not True in hovering_list:
        if left_hold == True:
            pygame.draw.line(screen, line_color, (past_mouse_x,past_mouse_y), (mouse_x, mouse_y), 1)
            pygame.draw.circle(screen, random_color, (past_mouse_x,past_mouse_y), math.sqrt(select_mass)*(player_zoom/100))
        else:
            pygame.draw.circle(screen, random_color, (mouse_x,mouse_y), math.sqrt(select_mass)*(player_zoom/100))

    # Draws the circle if its hovering over the mass slider so that the user can see a satisfiying increase in size of the mouse's body
    if mode_key == 2 and hovering_list[-1] == True:
        pygame.draw.circle(screen, random_color, (mouse_x,mouse_y), math.sqrt(select_mass)*(player_zoom/100))
    
    # Creates the select_mass surface
    mass_surface = text_font.render(f"Mass: {select_mass}", True, text_color)

    # Creates the x and y surfaces
    x_surface = small_text_font.render(f"x: {player_x}", True, text_color)
    y_surface = small_text_font.render(f"y: {player_y}", True, text_color)

    # Creates the zoom surface
    zoom_surface = small_text_font.render(f"zoom: {player_zoom}", True, text_color)

    # Creates the time surface
    time_surface = small_text_font.render(f"time: {time}", True, text_color)

    # Draws the mass variable if the user is in creation mode (mode_key == 2)
    if mode_key == 2:
        screen.blit(mass_surface, (0,0))

    # Draws the x and y variables
    screen.blit(x_surface, (10,window_size_y-30))
    screen.blit(y_surface, (70+(len(str(player_x))*10),window_size_y-30))   

    # Draws the zoom and time variables
    screen.blit(zoom_surface, (10,window_size_y-60))
    screen.blit(time_surface, (window_size_x-120,window_size_y-30))

    # Draws the buttons on the screen
    for button in buttons:
        button.draw_button()

    pygame.display.flip()

