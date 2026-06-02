# Imports
import pygame
import sys
import random
import math

# Initalizing stuff
pygame.init()

window_size_x = 960
window_size_y = 720

window_size = (window_size_x,window_size_y)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("N-body sim")

planet_color = (255,255,255)
line_color = (245,245,245)

def find_distance(other_x, other_y, self_x, self_y):
    return math.sqrt(((other_x-self_x)**2) + ((other_y-self_y)**2))

def find_force_componets(self_x, self_y, self_mass, other_x, other_y, other_mass):
    # Finds the distance between the other body and the current body
    distance = find_distance(other_x, other_y, self_x, self_y)

    # Finds the resulting force exerted on the current body using the Law of Gravitation (setting the gravitational constant to a basic 0.1)
    g = 0.1
    try:
        force = g*((other_mass*self_mass)/(distance**2))
    except ZeroDivisionError:
        force = 0

    # Finds the difference in x and y to be used to find the angle of direction for the current body
    x_side = other_x - self_x
    y_side = other_y - self_y

    angle = math.atan2(y_side, x_side)

    # Uses the force length and the angle to find the componets of the force (fx,fy)
    force_x = math.cos(angle) * force
    force_y = math.sin(angle) * force

    return force_x, force_y

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
        self.speed_x += force_componets[0]
        self.speed_y += force_componets[1]
    
    # Takes the distance between two bodies and checks if they have collided
    def check_collision(self, other_x, other_y, other_mass):
        distance = math.sqrt(((other_x-self.x_pos)**2) + ((other_y-self.y_pos)**2))

        if distance <= other_mass + self.mass:
            return True
        else:
            return False

    # Updates the position of the body based on the body's speed
    def update_pos(self):
        self.x_pos += self.speed_x
        self.y_pos += self.speed_y

    # Displays the body as a circle with its mass being used as the radius
    def display(self):
        pygame.draw.circle(screen, planet_color, (self.x_pos,self.y_pos), self.mass)


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

# Main Game Loop
while True:
    # Gets the mouse x and y to be used for placement code
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]

    # Checks for user input
    for event in pygame.event.get():
        # Quits the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Stores the past position to allow the user to move their mouse to change the speed and direction of the body
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                past_mouse_x = mouse_x
                past_mouse_y = mouse_y
                hold = 1
        # Computates the speed x and y of the body when it is created based on the mouse pos
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # Finds the distance between the past mouse pos and the current mouse pos
                distance = find_distance(mouse_x, mouse_y, past_mouse_x, past_mouse_y)/50

                # Finds the difference in x and y to find the angle
                x_side = past_mouse_x - mouse_x
                y_side = past_mouse_y - mouse_y

                angle = math.atan2(y_side, x_side)

                # Finds the start force x and y and uses it to make the new object
                start_force_x = math.cos(angle) * distance
                start_force_y = math.sin(angle) * distance

                bodies.append(Body(past_mouse_x,past_mouse_y,start_force_x,start_force_y,select_mass))

                hold = 0

        # Changes the select_mass depending on the mousewheel
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                select_mass += 1
            if event.y < 0:
                select_mass -= 1

    # Makes sure the select_mass variable never goes below 0
    if select_mass < 1:
        select_mass = 1
   
    # Clears the screen
    screen.fill((0,0,0))

    # Checks if a body is outside the screen and removes it from the list if it is outside
    for body in bodies:
        if body.x_pos < 0-(body.mass) or body.x_pos > window_size_x+(body.mass) or body.y_pos < 0-(body.mass) or body.y_pos > window_size_y+(body.mass):
            bodies.pop(bodies.index(body))

    # Updates the speed of a given body by looping through every other body and updating its speed
    for body in bodies:
        for other_bodies in bodies:
            if not body == other_bodies:
                # Checks if a collision between bodies has happened and if so, the smaller one gets consumed by the bigger one
                if body.check_collision(other_bodies.x_pos,other_bodies.y_pos,other_bodies.mass) == True:
                    if other_bodies.mass > body.mass:
                        other_bodies.speed_x = ((other_bodies.mass * other_bodies.speed_x) + (body.mass * body.speed_x)) / (body.mass + other_bodies.mass)
                        other_bodies.speed_y = ((other_bodies.mass * other_bodies.speed_y) + (body.mass * body.speed_y)) / (body.mass + other_bodies.mass)

                        other_bodies.mass += body.mass

                        bodies.pop(bodies.index(body))
                    else:
                        body.speed_x = ((body.mass * body.speed_x) + (other_bodies.mass * other_bodies.speed_x)) / (body.mass + other_bodies.mass)
                        body.speed_y = ((body.mass * body.speed_y) + (other_bodies.mass * other_bodies.speed_y)) / (body.mass + other_bodies.mass)

                        body.mass += other_bodies.mass

                        bodies.pop(bodies.index(other_bodies))
                
                body.update_speed(other_bodies.x_pos,other_bodies.y_pos,other_bodies.mass)
    
    # Updates the position of the bodies and draws them to the screen
    for body in bodies:
        body.update_pos()
        body.display()
    
    # Draws a circle to show the user what body will be placed and shows a line to show which direction and how fast will it go
    if hold == 1:
        pygame.draw.circle(screen, planet_color, (past_mouse_x,past_mouse_y), select_mass)
        pygame.draw.line(screen, line_color, (past_mouse_x,past_mouse_y), (mouse_x, mouse_y), 5)
    else:
        pygame.draw.circle(screen, planet_color, (mouse_x,mouse_y), select_mass)

    pygame.display.flip()

    clock.tick(60)