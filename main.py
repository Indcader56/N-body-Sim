# Imports
import pygame
import sys
import random
import math

# Import physics.py
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
text_font = pygame.font.SysFont(None, 50)
small_text_font = pygame.font.SysFont(None, 35)

# Button images
button_one = pygame.transform.scale(pygame.image.load("assents/Buttons/Button_one.png"), (55,55))
button_two = pygame.transform.scale(pygame.image.load("assents/Buttons/Button_two.png"), (55,55))
button_three = pygame.transform.scale(pygame.image.load("assents/Buttons/Button_three.png"), (55,55))

# Alt button images
alt_button_one = pygame.transform.scale(pygame.image.load("assents/Buttons/Alt-Button_one.png"), (55,55))
alt_button_two = pygame.transform.scale(pygame.image.load("assents/Buttons/Alt-Button_two.png"), (55,55))
alt_button_three = pygame.transform.scale(pygame.image.load("assents/Buttons/Alt-Button_three.png"), (55,55))

# Sub Button images
orbit_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_0.png"), (55,25))
shoot_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_2.png"), (55,25))
delete_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_4.png"), (55,25))
clear_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_6.png"), (55,25))

# Alt Sub Button images
alt_orbit_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_1.png"), (55,25))
alt_shoot_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_3.png"), (55,25))
alt_delete_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_5.png"), (55,25))
alt_clear_sub_button = pygame.transform.scale(pygame.image.load("assents/Sub_Buttons/sprite_7.png"), (55,25))

# Night sky image
sky = pygame.transform.scale(pygame.image.load("assents/Extras/sky.jpg"), (960,720))

# Body class
class Body:
    # Initalizes variables needed for a given body
    def __init__(self, x_pos, y_pos, speed_x, speed_y, mass, color, trail_list):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mass = mass
        self.color = color
        self.trail_list = trail_list
    
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
        if other.mass > self.mass:
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
        radius = math.sqrt(self.mass)*(player_zoom/100)
        if radius < 1:
            radius = 1

        pygame.draw.circle(screen, self.color, (((self.x_pos-player_x)*(player_zoom/100))+window_size_x/2,((self.y_pos+player_y)*(player_zoom/100))+window_size_y/2), radius)

    # Draws a trail of where the body was based on its past positions
    def draw_trail(self):
        for i in range(len(self.trail_list)):
            if i != len(self.trail_list)-1:
                pygame.draw.line(screen, self.color, (((self.trail_list[i][0]-player_x)*(player_zoom/100))+window_size_x/2,((self.trail_list[i][1]+player_y)*(player_zoom/100))+window_size_y/2),(((self.trail_list[i+1][0]-player_x)*(player_zoom/100))+window_size_x/2,((self.trail_list[i+1][1]+player_y)*(player_zoom/100))+window_size_y/2), 1)
                

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

# Sub buttons which only appear when the user selects one of the buttons
class Sub_Button():
    def __init__(self, x,y, image):
        self.x = x
        self.y = y
        self.image = image

    # Draws the sub button on the screen
    def draw_button(self):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_x > self.x and mouse_x < self.x + 55 and mouse_y > self.y and mouse_y < self.y + 25:
            if self.image == orbit_sub_button:
                screen.blit(alt_orbit_sub_button, (self.x, self.y))
            elif self.image == shoot_sub_button:
                screen.blit(alt_shoot_sub_button, (self.x, self.y))
            elif self.image == delete_sub_button:
                screen.blit(alt_delete_sub_button, (self.x, self.y))
            elif self.image == clear_sub_button:
                screen.blit(alt_clear_sub_button, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

# A function that deals with variables that can be modified by typing an input
def typer(variable, input, type, limit):
    global frame
    # Backspace gets rid of the last character of input
    if event.key == pygame.K_BACKSPACE:
        input = input[:-1]
        frame = 60
    # Return sets the final variable to the intger of input
    elif event.key == pygame.K_RETURN:
        if len(input) == 0:
            variable = 0
        else:
            variable = int(input)
        input = ""
        type = False
    else:
        # Allows the user to type numbers and under a certain character limit
        if event.unicode.isdigit():
            if len(input) < limit:
                input += event.unicode
                frame = 60

    return variable, input, type

# The buttons list hosts the button objects that can be clicked on find sub_buttons
buttons = [Button(window_size_x-165, 0, button_one), Button(window_size_x-110, 0, button_two), Button(window_size_x-55, 0, button_three)]

# The sub buttons for the creation button
add_sub_buttons = [Sub_Button(window_size_x-110, 55, orbit_sub_button), Sub_Button(window_size_x-110, 80, shoot_sub_button)]

# The sub buttons for the deletion button 
deletion_sub_buttons = [Sub_Button(window_size_x-55, 55, delete_sub_button), Sub_Button(window_size_x-55, 80, clear_sub_button)]

# The list where the body objects are held
bodies = []

# Variable to determine the desired mass of the body
select_mass = 1

# Clock for fps
clock = pygame.time.Clock()

# Variables for user

# Past_mouse_x and y track the last position of the mouse
past_mouse_x = 0
past_mouse_y = 0

"""
The mode key variable determines what options opens up to the user

1 - Nothing, everything is disabled so that the user can watch
2 - Allows the user to select sub buttons that allow the user to create bodies in orbit or at a certain velocity
3 - Allows the user to select sub buttons that allow the user to either delete certain bodies or clear the entire play area

"""

mode_key = 1

"""
The sub mode key variable determines how the user can modify, add, or delete bodies.
Sub modes can only be accessed by clicking on the main buttons

1 - Allows the user to place bodies in orbit around a parent body, if theres not parent body then the body just gets placed with 0 velocity
2 - Allows the user to place bodies or shoot them if they drag out the mouse

3 - Allows the user to delete certain bodies if they click on them
4 - Allows the user to delete every body in the play area
"""

sub_mode_key = 0

# Shows and hides excess menus 
view_mode = 0

# Shows and hides trails
view_trails = 0

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

# Time determines the simulation speed. Past time is just a varibale that tracks what was the past time when pausing or playing
time = 0
past_time = 0

# Frame is a variable that tracks how many frames happen in a second. Only used for the cursor that pops in when typing
frame = 0

# Input variables that independently keep track of what the user is typing into the respective variables
mass_input = ""
time_input = ""

# Determines whether or not the user is typing out the value of the respective variable
mass_type = False
time_type = False

# Used to determine the parent body of a orbit when in orbit sub mode
max_body = 0

# Enables and disables the background
background = 0


# Main Game Loop
while True:

    # Delta time to maintain a fixed simulation speed
    dt = clock.tick(60) / 1000
    # Gets the mouse x and y to be used for placement code
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]

    # Empties deleted_bodies so then it can take new bodies
    deleted_bodies = []

    # To get seconds for typing
    if mass_type == True or time_type == True:
        frame += 1
        if frame > 120:
            frame = 0
    else:
        frame = 60

    # Checks for user input
    for event in pygame.event.get():
        # Quits the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Goes through the button list and checks if the mouse is hovering over the buttons and checks if a click happens. If it does, it updates the mode_key variable
        hovering_list = []
        for button in buttons:
            if event.type == pygame.MOUSEBUTTONDOWN and view_mode == 0:
                if mouse_x > button.x and mouse_x < button.x + 55 and mouse_y > button.y and mouse_y < button.y + 55:
                    if button.image == button_one:
                        mode_key = 1
                    elif button.image == button_two:
                        mode_key = 2
                    elif button.image == button_three:
                        mode_key = 3

            # Checks if a user is hovering over a button
            if mouse_x > button.x and mouse_x < button.x + 55 and mouse_y > button.y and mouse_y < button.y + 55 and view_mode == 0:
                hovering_list.append(True)
            else:
                hovering_list.append(False)
        """
        Appends to the hovering list when hovering over a sub button and updates the sub_mode_key variable when a sub button is pressed
        Note: There are two loops for the addtion list and deletion list for the sub buttons. However they basically do the same thing
        """
        for sub_button in add_sub_buttons:
            if event.type == pygame.MOUSEBUTTONDOWN and view_mode == 0:
                if mouse_x > sub_button.x and mouse_x < sub_button.x + 55 and mouse_y > sub_button.y and mouse_y < sub_button.y + 25:
                    if sub_button.image == orbit_sub_button:
                        sub_mode_key = 1
                    elif sub_button.image == shoot_sub_button:
                        sub_mode_key = 2

            # Checks if a user is hovering over a button
            if mouse_x > sub_button.x and mouse_x < sub_button.x + 55 and mouse_y > sub_button.y and mouse_y < sub_button.y + 25 and view_mode == 0:
                hovering_list.append(True)
            else:
                hovering_list.append(False)

        for sub_button in deletion_sub_buttons:
            if event.type == pygame.MOUSEBUTTONDOWN and view_mode == 0:
                if mouse_x > sub_button.x and mouse_x < sub_button.x + 55 and mouse_y > sub_button.y and mouse_y < sub_button.y + 25:
                    if sub_button.image == delete_sub_button:
                        sub_mode_key = 3
                    elif sub_button.image == clear_sub_button:
                        sub_mode_key = 4

            # Checks if a user is hovering over a button
            if mouse_x > sub_button.x and mouse_x < sub_button.x + 55 and mouse_y > sub_button.y and mouse_y < sub_button.y + 25 and view_mode == 0:
                hovering_list.append(True)
            else:
                hovering_list.append(False)


        # Adds True values to the hovering_list if its over the mass text or the zoom text
        if mouse_x > window_size_x-125 and mouse_y > window_size_y-45 and view_mode == 0:
            hovering_list.append(True)
        if mouse_x < 175 and mouse_y < 75 and mode_key == 2 and view_mode == 0:
            hovering_list.append(True)

        # Logic for Orbit mode of Creation mode
        if mode_key == 2 and not True in hovering_list and view_mode == 0 and sub_mode_key == 1:
            # Finds the body exerting the greatest gravitational pull towards the body selected at the possible position it could be placed in
            max_force = 0
            max_body = 0
            for body in bodies:
                if player_zoom/100 != 0:
                    # Finds the distance between the possible parent body and the world position of the mouse
                    distance = physics.find_distance(body.x_pos, body.y_pos, (((mouse_x-window_size_x/2)/(player_zoom/100))+player_x),(((mouse_y-window_size_y/2)/(player_zoom/100))-player_y))

                    # Finds the gravitational pull of the two bodies
                    force = physics.find_force_gravity(body.mass, select_mass, distance)

                    # Compares the previous maximum force and the current force just computed to find the greatest one
                    if force > max_force:
                        max_force = float(force)
                        max_body = body

            # If the user places a body and theres a parent body it finds the velocity x and y and accounts for the parent's velocity
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and max_body != 0:

                # Finds the orbital velocity of the child body using the formula V = sqrt((G(M1 +M2))/D)
                start_force_x, start_force_y = physics.find_orbital_components((((mouse_x-window_size_x/2)/(player_zoom/100))+player_x), (((mouse_y-window_size_y/2)/(player_zoom/100))-player_y),select_mass, max_body.x_pos, max_body.y_pos,max_body.mass)

                # Adds on the velocity of the parent body in order for the child body to correctly orbit around it relative to the parent body
                start_force_x,start_force_y = start_force_x+max_body.speed_x, start_force_y+max_body.speed_y

                # Adds the body to the bodies list and change the color to be random next time
                bodies.append(Body((((mouse_x-window_size_x/2)/(player_zoom/100))+player_x),(((mouse_y-window_size_y/2)/(player_zoom/100))-player_y),start_force_x,start_force_y,select_mass, random_color, []))
                
                random_color = (random.randint(15,255),random.randint(15,255),random.randint(15,255))

            # Otherwise it just places a body at a velocity of 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and max_body == 0:
                bodies.append(Body((((mouse_x-window_size_x/2)/(player_zoom/100))+player_x),(((mouse_y-window_size_y/2)/(player_zoom/100))-player_y),0,0,select_mass, random_color, []))
                                
                random_color = (random.randint(15,255),random.randint(15,255),random.randint(15,255))
            
    
        # Logic for when in Shooting sub mode of the creation mode
        if mode_key == 2 and not True in hovering_list and view_mode == 0 and sub_mode_key == 2:
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

                # Finds the force x and y based off the distance from the body about to be created and the mouse
                start_force_x, start_force_y = physics.find_distance_componets(past_mouse_x, past_mouse_y, mouse_x, mouse_y, select_mass, player_zoom)
                
                bodies.append(Body((((past_mouse_x-window_size_x/2)/(player_zoom/100))+player_x),(((past_mouse_y-window_size_y/2)/(player_zoom/100))-player_y),start_force_x,start_force_y,select_mass, random_color, []))
                
                random_color = (random.randint(15,255),random.randint(15,255),random.randint(15,255))

                left_hold = False

        # Logic for deletion mode logic when in DELETE mode (sub_mode_key = 3)
        if mode_key == 3 and not True in hovering_list and view_mode == 0 and sub_mode_key == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for body in bodies:
                        if physics.find_distance(((body.x_pos-player_x)*(player_zoom/100))+(window_size_x/2), ((body.y_pos+player_y)*(player_zoom/100))+(window_size_y/2), mouse_x, mouse_y) <= math.sqrt(body.mass)*(player_zoom/100):
                            deleted_bodies.append(body)

        # Logic for deletion mode logic when in CLEAR mode (sub_mode_key = 4)
        if mode_key == 3 and sub_mode_key == 4 and not True in hovering_list and view_mode == 0:
            for body in bodies:
                deleted_bodies.append(body)
            # Resets sub_mode_key because its a action not a mode that can be stayed in
            sub_mode_key = 0


        # Independent Logic

        # Activates typing mode when the text is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # FOR MASS
                if mouse_x < 175 and mouse_y < 75 and mode_key == 2 and view_mode == 0 and time_type == False:
                    mass_type = True
                # FOR TIME
                elif mouse_x > window_size_x-125 and mouse_y > window_size_y-45 and view_mode == 0 and mass_type == False:
                    time_type = True

        # Allows the user to type in input for the time and mass variables
        if event.type == pygame.KEYDOWN:
            if mass_type == True:
                select_mass, mass_input, mass_type = typer(select_mass, mass_input, mass_type, 4)            

            if time_type == True:
                time, time_input, time_type = typer(time, time_input, time_type, 3)
        
        # Changes zoom via mousewheel
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                player_zoom += 10
            if event.y < 0:
                player_zoom -= 10
        
        # Adds a bunch of random bodies when the space key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bodies = []
                for i in range(50):
                    rnd_x = random.uniform(-1000,1000)
                    rnd_y = random.uniform(-1000,1000)

                    rnd_clr = (random.uniform(10,255),random.uniform(10,255),random.uniform(10,255))

                    rnd_mass = random.uniform(100,1000)

                    bodies.append(Body(rnd_x,rnd_y,0,0,rnd_mass, rnd_clr, []))

            # Clears out the entire play area 
            if event.key == pygame.K_p:
                for body in bodies:
                    deleted_bodies.append(body)

            # Pauses and plays time and keeps track of the past time using the past_time variable
            if event.key == pygame.K_q:
                if time > 0:
                    past_time = int(time)
                    time = 0
                else:
                    time = int(past_time)
                    past_time = 0

            # Enables and disables the view mode variable which gets rid of excess menus and variables for viewing pleasure
            if event.key == pygame.K_v:
                if view_mode == 0:
                    view_mode = 1
                else:
                    view_mode = 0
            # Enables and disables the trail mode which allows the user to see trails
            if event.key == pygame.K_t:
                if view_trails == 0:
                    view_trails = 1
                else:
                    view_trails = 0

            if event.key == pygame.K_b:
                if background == 0:
                    background = 1
                else:
                    background = 0

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

    # Makes sure the select_mass variable never goes below 0 or above 9,999
    if select_mass < 1:
        select_mass = 1
    if select_mass > 9999:
        select_mass = 9999

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

    # Draws a night sky
    if background == 1:
        screen.blit(sky, (0,0))

    # Updates the position of the bodies
    for body in bodies:
        for t in range(time):
            body.update_pos()

        if time > 0:
            # Adds points to the trail_list of every body
            body.trail_list.append((body.x_pos, body.y_pos))
            # Gets rid of points in order to conserve memory. The 1000 offset is to give each trail a sizable amount of length
            if len(body.trail_list) > body.mass+1000:
                body.trail_list.pop(0)

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

    # Draws trails
    if view_trails == 1:
        for body in bodies:
            body.draw_trail()

    # Draws the bodies on the screen
    for body in bodies:
        # Displays the body only if its within the screen limits
        if ((body.x_pos - player_x)-math.sqrt(body.mass))*(player_zoom/100) < window_size_x/2 and ((body.x_pos - player_x)+math.sqrt(body.mass))*(player_zoom/100) > -(window_size_x/2) and ((body.y_pos + player_y)-math.sqrt(body.mass))*(player_zoom/100) < window_size_y/2 and ((body.y_pos + player_y)+math.sqrt(body.mass))*(player_zoom/100) > -(window_size_y/2):
            body.display()

        # If the mouse hovers over a body, and the mode for the user is 3 (delete), then a box will be drawn over the selected body
        if mode_key == 3 and sub_mode_key == 3 and view_mode == 0:
            if physics.find_distance(((body.x_pos-player_x)*(player_zoom/100))+(window_size_x/2), ((body.y_pos+player_y)*(player_zoom/100))+(window_size_y/2), mouse_x, mouse_y) <= math.sqrt(body.mass)*(player_zoom/100):
                pygame.draw.rect(screen,red, ((((body.x_pos-player_x)-math.sqrt(body.mass))*(player_zoom/100)) + window_size_x/2, (((body.y_pos+player_y)-math.sqrt(body.mass))*(player_zoom/100))+window_size_y/2, (math.sqrt(body.mass)*2)*(player_zoom / 100),(math.sqrt(body.mass)*2)*(player_zoom / 100)), 1)
        # If the user is in orbit mode and theres a parent body it will draw a circle symbolizing its possible path in said orbit
        if max_body == body and mode_key == 2 and sub_mode_key == 1 and view_mode == 0:
            pygame.draw.circle(screen, line_color, (((body.x_pos-player_x)*(player_zoom/100))+(window_size_x/2), ((body.y_pos+player_y)*(player_zoom/100))+(window_size_y/2)),(physics.find_distance(((body.x_pos-player_x)*(player_zoom/100))+(window_size_x/2), ((body.y_pos+player_y)*(player_zoom/100))+(window_size_y/2), mouse_x, mouse_y)), 1)


    # Draws a circle to show the user what body will be placed and shows a line to show which direction and how fast will it go
    if mode_key == 2 and not True in hovering_list and view_mode == 0:
        if left_hold == True:
            pygame.draw.line(screen, line_color, (past_mouse_x,past_mouse_y), (mouse_x, mouse_y), 1)
            pygame.draw.circle(screen, random_color, (past_mouse_x,past_mouse_y), math.sqrt(select_mass)*(player_zoom/100))
        else:
            pygame.draw.circle(screen, random_color, (mouse_x,mouse_y), math.sqrt(select_mass)*(player_zoom/100))

    # Draws the circle if its hovering over the mass slider so that the user can see a satisfiying increase in size of the mouse's body
    if mode_key == 2 and hovering_list[-1] == True and view_mode == 0:
        pygame.draw.circle(screen, random_color, (mouse_x,mouse_y), math.sqrt(select_mass)*(player_zoom/100))

    # Creates the select_mass surface and changes the message depending on if the user is typing
    if mass_type == True:
        if sub_mode_key == 2 or sub_mode_key == 1:
            if frame//60 == 1:
                mass_surface = text_font.render(f"Mass: {mass_input}|", True, text_color)
            else:
                mass_surface = text_font.render(f"Mass: {mass_input}", True, text_color)
    else:
        mass_surface = text_font.render(f"Mass: {select_mass}", True, text_color)

    # Creates the time surface and changes the message depending on if the user is typing
    if time_type == True:
        if frame//60 == 1:
            time_surface = small_text_font.render(f"time: {time_input}|", True, text_color)
        else:
            time_surface = small_text_font.render(f"time: {time_input}", True, text_color)
    else:
        time_surface = small_text_font.render(f"time: {time}", True, text_color)

    # Creates the x and y surfaces
    x_surface = small_text_font.render(f"x: {player_x}", True, text_color)
    y_surface = small_text_font.render(f"y: {player_y}", True, text_color)

    # Creates the zoom surface
    zoom_surface = small_text_font.render(f"zoom: {player_zoom}", True, text_color)

    if view_mode == 0:
        # Draws the mass variable if the user is in creation mode (mode_key == 2)
        if mode_key == 2:
            if sub_mode_key == 2 or sub_mode_key == 1:
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

        # Draws the addition sub buttons and the deletion sub buttons
        if mode_key == 2:
            for a_sub_button in add_sub_buttons:
                a_sub_button.draw_button()
        if mode_key == 3:
            for d_sub_button in deletion_sub_buttons:
                d_sub_button.draw_button()
    pygame.display.flip()

