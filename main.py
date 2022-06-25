import math
import pygame
import pygame.gfxdraw
import pymunk
import sys

from pymunk import Vec2d
from random import randint, sample
from matplotlib import pyplot as plt

fps = 60
pygame.init()
screen = pygame.display.set_mode((1300, 700))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 0)

f_x, f_y = -100, 350
total_time = 0
time_list = []
radius_of_person = 10
number_of_people = 900
number_of_people_per_time = []
number_of_people_per_time_infected = []
number_of_people_per_time_non_infected = []
number_of_people_per_time_removed = []
infection_radius = radius_of_person * 3
infected_people_at_start = 1


def calculate_distance(ax, ay, bx, by):
    return math.sqrt((bx - ax)**2 + (by - ay)**2)


class Obstacle:
    def __init__(self, space, screen, x, y, width, height, rotation, color, is_circle=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_circle = is_circle
        self.top = y - height / 2
        self.right = x + width / 2
        self.left = x - width / 2
        self.bottom = y + height / 2
        self.color = color
        self.body = pymunk.Body(1, 1, body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.body.angle = rotation * (math.pi / 180)

        if self.is_circle:
            self.shape = pymunk.Circle(self.body, self.width)
        else:
            self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.elasticity = 1
        self.shape.friction = 1
        space.add(self.body, self.shape)


    def draw(self):
        if self.is_circle:
            pygame.draw.circle(self.screen, self.color, self.shape.body.position, self.width)
        else:
            vertices = []
            for vertex in self.shape.get_vertices():
                x, y = vertex.rotated(self.shape.body.angle) + self.shape.body.position
                vertices.append((x, y))
            pygame.gfxdraw.filled_polygon(self.screen, vertices, self.color)


class Person:
    def __init__(self, space, screen, x, y, radius, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.is_infected = False

        self.body = pymunk.Body(50, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0
        self.shape.friction = 1
        space.add(self.body, self.shape)

    def update_coordinates(self):
        self.x = self.body.position.x
        self.y = self.body.position.y

    def pull_to_point(self, point_x, point_y, force):
        force_origin = Vec2d(self.x, self.y)
        force_end = force * Vec2d(point_x - self.x, point_y - self.y) / 100
        # force_end = force * (force_end * force_end.length)/100000
        self.body.apply_force_at_world_point(force_end, force_origin)

    def draw_person(self):
        pygame.draw.circle(self.screen, self.color, self.shape.body.position, self.radius)

    def draw_infection_radius(self):
        pygame.draw.circle(self.screen, self.color, self.shape.body.position, infection_radius, 1)

    def draw_force(self, force_end_x, force_end_y):
        force_origin = Vec2d(self.x, self.y)
        force_end = Vec2d(force_end_x-self.x, force_end_y-self.y)
        force_end = force_origin + (force_end * force_end.length)/1081

        pygame.draw.line(screen, (0, 255, 255), force_origin, force_end)

    def check_for_infection(self, list_of_other_people):
        if self.is_infected:
            for person in list_of_other_people:
                distance_to_person = calculate_distance(self.x, self.y, person.x, person.y)
                if distance_to_person <= infection_radius and not person.is_infected:
                    person.is_infected = True


obstacles = [
    Obstacle(space, screen, x=770, y=40, width=980, height=10, rotation=0, color=(0, 0, 0)),
    Obstacle(space, screen, x=770, y=660, width=980, height=10, rotation=0, color=(0, 0, 0)),
    Obstacle(space, screen, x=172, y=150, width=10, height=315, rotation=45, color=(0, 0, 0)),
    Obstacle(space, screen, x=172, y=550, width=10, height=315, rotation=-45, color=(0, 0, 0)),
    Obstacle(space, screen, x=1265, y=350, width=10, height=630, rotation=0, color=(0, 0, 0)),
    Obstacle(space, screen, x=190, y=225, width=10, height=270, rotation=75, color=(255, 0, 0)),
    Obstacle(space, screen, x=190, y=475, width=10, height=270, rotation=-75, color=(255, 0, 0)),
    Obstacle(space, screen, x=430, y=112, width=10, height=270, rotation=55, color=(255, 0, 0)),
    Obstacle(space, screen, x=430, y=588, width=10, height=270, rotation=-55, color=(255, 0, 0)),
    Obstacle(space, screen, x=400, y=350, width=70, height=0, rotation=0, color=(255, 0, 0), is_circle=True),
]

people = [Person(space, screen, randint(500, 1250), randint(150, 550), radius_of_person, (0, 0, 200)) for k in range(number_of_people)]


for j in sample(range(number_of_people), infected_people_at_start):
    people[j].is_infected = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if len(people) == 0:
        break

    number_of_people_infected = 0
    number_of_people_non_infected = 0

    screen.fill((255, 255, 255))

    for obstacle in obstacles:
        obstacle.draw()

    for person in people:
        if person.x < 35:
            people.remove(person)
            continue

        person.check_for_infection(people)

        if person.is_infected:
            number_of_people_infected += 1
            person.color = (255, 0, 0)
            person.pull_to_point(f_x, f_y, 900)
        else:
            number_of_people_non_infected += 1
            person.pull_to_point(f_x, f_y, 300)
        person.update_coordinates()
        person.draw_person()
        # person.draw_force(f_x, f_y)

    number_of_people_removed = number_of_people - len(people)

    number_of_people_per_time.append(len(people))
    number_of_people_per_time_infected.append(number_of_people_infected)
    number_of_people_per_time_non_infected.append(number_of_people_non_infected)
    number_of_people_per_time_removed.append(number_of_people_removed)

    time_list.append(round(total_time/60, 2))
    total_time += 1

    space.step(1/fps)
    pygame.display.update()
    clock.tick(fps)

plt.title(f"Temps total est {round(total_time / 60, 2)} seconde(s)")
plt.xlabel("Temps en secondes")
plt.ylabel("Nombre d'individus")
plt.plot(time_list, number_of_people_per_time, color=(0, 0, 0), label="Person a l'interieur")
plt.plot(time_list, number_of_people_per_time_infected, color=(1, 0, 0), label="I : Infectee")
plt.plot(time_list, number_of_people_per_time_non_infected, color=(0, 1, 0), label="S : Susceptible")
plt.plot(time_list, number_of_people_per_time_removed, color=(0, 0, 1), label="R : Removed (Supprime)")
plt.legend()
plt.show()
