# Figures out the resulting speed and mass of the bigger body (winner) and adds the "losing" body to a list to be deleted
import math

def winner_loser_momentum_and_mass(winner, loser):
    # Changes the x and y position of the winning body to a point that lines between the two bodies with a ratio of loser.mass/winner.mass
    winner.x_pos = ((winner.mass*winner.x_pos) + (loser.mass*loser.x_pos)) / (winner.mass + loser.mass)
    winner.y_pos = ((winner.mass*winner.y_pos) + (loser.mass*loser.y_pos)) / (winner.mass + loser.mass)

    winner.speed_x = ((winner.mass * winner.speed_x) + (loser.mass * loser.speed_x)) / (winner.mass + loser.mass)
    winner.speed_y = ((winner.mass * winner.speed_y) + (loser.mass * loser.speed_y)) / (winner.mass + loser.mass)

    winner.mass += loser.mass

    return loser

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
def find_distance_componets(past_x, past_y, current_x, current_y, s_mass):
    # Finds the distance between the past mouse pos and the current mouse pos
    distance = find_distance(past_x, past_y, current_x, current_y)

    if distance >= s_mass:
        distance -= s_mass
    else:
        return 0,0

    # Finds the difference in x and y to find the angle
    x_side = past_x - current_x
    y_side = past_y - current_y

    angle = math.atan2(y_side, x_side)

    # Finds the start force x and y and uses it to make the new object
    start_force_x, start_force_y = final_x_y_componets(distance, angle)

    return start_force_x, start_force_y