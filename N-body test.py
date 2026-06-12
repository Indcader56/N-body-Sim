# Imports
import pygame
import sys
import random
import math

# Initalizing stuff
pygame.init()
pygame.font.init()

window_size_x = 960
window_size_y = 720

window_size = (window_size_x,window_size_y)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("N-body sim")

# Colors used for assents
planet_color = (255,255,255)
line_color = (205,205,205)
text_color = (250,250,250)
red = (255,0,0)

# Font for text
text_font = pygame.font.Font(None, 50)

small_text_font = pygame.font.Font(None, 35)

# Button images
button_one = pygame.transform.scale(pygame.image.load("Button_one.png"), (55,55))
button_two = pygame.transform.scale(pygame.image.load("Button_two.png"), (55,55))
button_three = pygame.transform.scale(pygame.image.load("Button_three.png"), (55,55))

# Alt button images
alt_button_one = pygame.transform.scale(pygame.image.load("Alt-Button_one.png"), (55,55))
alt_button_two = pygame.transform.scale(pygame.image.load("Alt-Button_two.png"), (55,55))
alt_button_three = pygame.transform.scale(pygame.image.load("Alt-Button_three.png"), (55,55))

# Figures out the resulting speed and mass of the bigger body (winner) and adds the "losing" body to a list to be deleted
def winner_loser_momentum_and_mass(winner, loser):
    winner.speed_x = ((winner.mass * winner.speed_x) + (loser.mass * loser.speed_x)) / (winner.mass + loser.mass)
    winner.speed_y = ((winner.mass * winner.speed_y) + (loser.mass * loser.speed_y)) / (winner.mass + loser.mass)

    winner.mass += loser.mass

    deleted_bodies.append(loser)

# Finds the distance between two points
def find_distance(other_x, other_y, self_x, self_y):
    return math.sqrt(((other_x-self_x)**2) + ((other_y-self_y)**2))

# Finds the x and y componets of a vector
def final_x_y_componets(magnitude, angle):
    magnitude_x = math.cos(angle) * magnitude
    magnitude_y = math.sin(angle) * magnitude

    return magnitude_x, magnitude_y

# Finds force componets for gravity
def find_force_componets(self_x, self_y, self_mass, other_x, other_y, other_mass):
    # Finds the distance between the other body and the current body
    distance = find_distance(other_x, other_y, self_x, self_y)

    # Finds the resulting force exerted on the current body using the Law of Gravitation (setting the gravitational constant to a basic 1000)
    g = 5000
    try:
        force = g*((other_mass*self_mass)/(distance**2))
    except ZeroDivisionError:
        force = 0

    # Finds the difference in x and y to be used to find the angle of direction for the current body
    x_side = other_x - self_x
    y_side = other_y - self_y

    angle = math.atan2(y_side, x_side)

    # Uses the force length and the angle to find the componets of the force (fx,fy)
    force_x, force_y = final_x_y_componets(force, angle)

    return force_x, force_y

# Finds the distance between two points: used for finding the starting speed of a body when placed
def find_distance_componets(past_x, past_y, current_x, current_y):
    # Finds the distance between the past mouse pos and the current mouse pos
    distance = find_distance(past_x, past_y, current_x, current_y)

    if distance >= select_mass:
        distance -= select_mass
    else:
        return 0,0

    # Finds the difference in x and y to find the angle
    x_side = past_x - current_x
    y_side = past_y - current_y

    angle = math.atan2(y_side, x_side)

    # Finds the start force x and y and uses it to make the new object
    start_force_x, start_force_y = final_x_y_componets(distance, angle)

    return start_force_x, start_force_y


# Body class
class Body:
    # Initalizes variables needed for a given body
    def __init__(self, x_pos, y_pos, speed_x, speed_y, mass):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mass = mass
    
    # Updates the speed x and y variables to account for another mass
    def update_speed(self, other_x, other_y, other_mass):
        # Finds the fx and fy componets
        force_componets = find_force_componets(self.x_pos, self.y_pos, self.mass, other_x, other_y, other_mass)

        # Changes the speed x and y variables by the forces
        self.speed_x += (force_componets[0] / self.mass) * dt
        self.speed_y += (force_componets[1] / self.mass) * dt
    
    # Checks if a collision happens between two bodies
    def check_collision(self, other_x, other_y, other_mass):
        # Takes the distance between two bodies and checks if they have collided
        distance = math.sqrt(((other_x-self.x_pos)**2) + ((other_y-self.y_pos)**2))

        # Determines the winner of the collision
        if other_mass > self.mass:
            winner = other_body
            loser = body
        else:
            winner = body
            loser = other_body

        # Checks if the collision actually happened and returns based on that
        if distance <= winner.mass + loser.mass/3:
            return winner, loser
        else:
            return False

    # Updates the position of the body based on the body's speed
    def update_pos(self):
        self.x_pos += self.speed_x * dt
        self.y_pos += self.speed_y * dt

    # Checks if a body is clicked and returns accordingly
    def check_click(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_x > (self.x_pos-player_x) - (self.mass) and mouse_x < (self.x_pos-player_x) + (self.mass) and mouse_y > (self.y_pos+player_y) - (self.mass) and mouse_y < (self.y_pos+player_y) + (self.mass):
                return True
            
        return False

    # Checks if the mouse is over the body. If True and mode_key is 3, then it draws a rectangle over the body
    def check_hover(self):
        if mouse_x > (self.x_pos-player_x) - (self.mass) and mouse_x < (self.x_pos-player_x) + (self.mass) and mouse_y > (self.y_pos+player_y) - (self.mass) and mouse_y < (self.y_pos+player_y) + (self.mass):
            pygame.draw.rect(screen, red, ((self.x_pos-player_x)-self.mass, (self.y_pos+player_y)-self.mass, self.mass*2,self.mass*2), 1)
            
        return False

    # Displays the body as a circle with its mass being used as the radius
    def display(self):
        pygame.draw.circle(screen, planet_color, ((self.x_pos-player_x),(self.y_pos+player_y)), self.mass)

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

    # If a click happens, it returns a number to be used to change the mode_key variable. Otherwise it returns false
    def check_click(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_x > self.x and mouse_x < self.x + 55 and mouse_y > self.y and mouse_y < self.y + 55:
                if self.image == button_one:
                    return 1
                elif self.image == button_two:
                    return 2
                elif self.image == button_three:
                    return 3
            
        return False
    
    # Checks if the mouse is on the button
    def check_hover(self):
        if mouse_x > self.x and mouse_x < self.x + 55 and mouse_y > self.y and mouse_y < self.y + 55:
            return True
        
        return False

# The buttons list hosts the button objects
buttons = [Button(window_size_x-165, 0, button_one), Button(window_size_x-110, 0, button_two), Button(window_size_x-55, 0, button_three)]

# The list where the body objects are held
bodies = []

# Variable to determine the desired mass of the body
select_mass = 1

# Clock for fps
clock = pygame.time.Clock()

# Variables for user
hold = 0
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

# Which movement button is being clicked?
click_w = False
click_s = False
click_a = False
click_d = False

# Main Game Loop
while True:
    dt = clock.tick(60) / 1000

    # Gets the mouse x and y to be used for placement code
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]

    # Checks for user input
    for event in pygame.event.get():
        
        # Goes through the button list and checks if the mouse is hovering over the buttons and checks if a click happens. If it does, it updates the mode_key variable
        hovering_list = []
        for button in buttons:
            button_click = button.check_click()
            hovering_list.append(button.check_hover())
            if button_click != False:
                mode_key = button_click

        # Quits the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Checks if the create button was pressed and makes sure you can't place bodies when you press the button
        if mode_key == 2 and not True in hovering_list:
            # Stores the past position to allow the user to move their mouse to change the speed and direction of the body
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    past_mouse_x = mouse_x
                    past_mouse_y = mouse_y
                    hold = 1

            # Cancels the placement operation if the player moves
            if click_d == True or click_w == True or click_a == True or click_s == True:
                hold = 0

            # Computates the speed x and y of the body when it is created based on the mouse pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and hold == 1:
                    
                start_force_x, start_force_y = find_distance_componets(past_mouse_x, past_mouse_y, mouse_x, mouse_y)
                
                bodies.append(Body(past_mouse_x+player_x,past_mouse_y-player_y,start_force_x,start_force_y,select_mass))

                hold = 0

            # Changes the select_mass depending on the mousewheel
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    select_mass += 1
                if event.y < 0:
                    select_mass -= 1
        
        # Adds a bunch of random bodies when the space key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bodies = [Body(random.uniform(0,window_size_x), random.uniform(0,window_size_y), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.randint(1, 2)) for i in range(100)]
            
            # Updates the click values to tell if the user is holding down one of these buttons
            if event.key == pygame.K_d:
                click_d = True
            if event.key == pygame.K_a:
                click_a = True
            if event.key == pygame.K_w:
                click_w = True
            if event.key == pygame.K_s:
                click_s = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                click_d = False
            if event.key == pygame.K_a:
                click_a = False
            if event.key == pygame.K_w:
                click_w = False
            if event.key == pygame.K_s:
                click_s = False

    # Changes the player position when one of the buttons are being held
    if click_d == True:
        player_x += 10
    if click_a == True:
        player_x -= 10
    if click_w == True:
        player_y += 10
    if click_s == True:
        player_y -= 10

    # Makes sure the select_mass variable never goes below 0
    if select_mass < 1:
        select_mass = 1
   
    # Clears the screen
    screen.fill((0,0,0))

    deleted_bodies = []
    # Updates the speed of a given body by looping through every other body and updating its speed
    for body in bodies:
        for other_body in bodies:
            if not body == other_body:
                # Checks if a collision between bodies has happened and if so, the smaller one gets consumed by the bigger one
                collided = body.check_collision(other_body.x_pos, other_body.y_pos, other_body.mass)
                if collided != False:
                    winner, loser = collided
                    
                    # Checks if the winner/loser is in the deleted list so that the function doesn't run twice
                    if not winner in deleted_bodies:
                        if not loser in deleted_bodies:
                            winner_loser_momentum_and_mass(winner, loser)

                # Updates the speed
                body.update_speed(other_body.x_pos,other_body.y_pos,other_body.mass)
    
    # Adds bodies to the chopping block (deleted_bodies list) if they were clicked on in deletion mode
    if mode_key == 3 and not True in hovering_list:
        for body in bodies:
            if body.check_click() == True:
                deleted_bodies.append(body)

    # Deletes any bodies in the deleted_bodies list
    for body in deleted_bodies:
        #if body.x_pos < 0-(body.mass) or body.x_pos > window_size_x+(body.mass) or body.y_pos < 0-(body.mass) or body.y_pos > window_size_y+(body.mass):
        if body in bodies:
            bodies.remove(body)

    # Updates the position of the bodies and draws them to the screen
    for body in bodies:
        body.update_pos()
        body.display()

        # If the mouse hovers over a body, and the mode for the user is 3 (delete), then a box will be drawn over the selected body
        if mode_key == 3:
            body.check_hover()

    # Draws a circle to show the user what body will be placed and shows a line to show which direction and how fast will it go
    if mode_key == 2 and not True in hovering_list:
        if hold == 1:
            pygame.draw.line(screen, line_color, (past_mouse_x,past_mouse_y), (mouse_x, mouse_y), 1)
            pygame.draw.circle(screen, planet_color, (past_mouse_x,past_mouse_y), select_mass)
        else:
            pygame.draw.circle(screen, planet_color, (mouse_x,mouse_y), select_mass)
    
    # Draws the select_mass variable in the corner and blits it, also draws the x and y position of the player
    mass_surface = text_font.render(f"Mass: {select_mass}", True, text_color)

    x_surface = small_text_font.render(f"x: {player_x}", True, text_color)
    y_surface = small_text_font.render(f"y: {player_y}", True, text_color)

    screen.blit(mass_surface, (0,0))

    screen.blit(x_surface, (10,window_size_y-30))
    screen.blit(y_surface, (70+(len(str(player_x))*10),window_size_y-30))

    # Draws the buttons on the screen
    for button in buttons:
        button.draw_button()

    pygame.display.flip()