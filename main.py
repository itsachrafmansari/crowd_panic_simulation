import math
import pygame
import pymunk
import sys

from pymunk import Vec2d
from random import randint
from matplotlib import pyplot as plt

fps = 60
pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 0)

f_x, f_y = -300, 300
total_time = 0
time_list = []
number_of_people = 100
number_of_people_per_time = []
number_of_people_left_per_time = []


class Person:
    def __init__(self, space, screen, x, y, radius, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

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
        force_end = Vec2d(point_x-self.x, point_y-self.y)
        force_end = force * (force_end * force_end.length)/1081
        self.body.apply_force_at_world_point(force_end, force_origin)

    def draw_person(self):
        pygame.draw.circle(self.screen, self.color, self.shape.body.position, self.radius)

    def draw_force(self, force_end_x, force_end_y):
        force_origin = Vec2d(self.x, self.y)
        force_end = Vec2d(force_end_x-self.x, force_end_y-self.y)
        force_end = force_origin + (force_end * force_end.length)/1081

        pygame.draw.line(screen, (255, 255, 255), force_origin, force_end)


class Obstacle:
    def __init__(self, space, screen, x, y, width, height, rotation, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = y - height / 2
        self.right = x + width / 2
        self.left = x - width / 2
        self.bottom = y + height / 2
        self.color = color
        self.body = pymunk.Body(1, 1, body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.body.angle = rotation * (math.pi / 180)

        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.elasticity = 1
        self.shape.friction = 1
        space.add(self.body, self.shape)


    def draw(self):
        vertices = []
        for vertex in self.shape.get_vertices():
            x, y = vertex.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x, y))
        pygame.draw.polygon(self.screen, self.color, vertices, True)


class Wall:
    def __init__(self, space, screen, x, y, width, height, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = y - height / 2
        self.right = x + width / 2
        self.left = x - width / 2
        self.bottom = y + height / 2
        self.color = color

        self.shape = pymunk.Poly(
            space.static_body,
            [(self.left, self.top), (self.right, self.top), (self.right, self.bottom), (self.left, self.bottom)]
        )
        self.shape.elasticity = 1
        self.shape.friction = 1
        space.add(self.shape)


    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.left, self.top, self.width, self.height))


walls = [
    Wall(space, screen, 450, 560, 830, 10, (0, 40, 0)),
    Wall(space, screen, 450, 40, 830, 10, (0, 40, 0)),
    Wall(space, screen, 40, 150, 10, 210, (0, 40, 0)),
    Wall(space, screen, 40, 450, 10, 210, (0, 40, 0)),
    Wall(space, screen, 860, 300, 10, 510, (0, 40, 0))
]
obstacles = [
    Obstacle(space, screen, x=100, y=150, width=10, height=240, rotation=30, color=(255, 0, 0)),
    Obstacle(space, screen, x=100, y=450, width=10, height=240, rotation=-30, color=(255, 0, 0)),
    Obstacle(space, screen, x=450, y=180, width=15, height=200, rotation=45, color=(255, 0, 0)),
    Obstacle(space, screen, x=450, y=420, width=15, height=200, rotation=-45, color=(255, 0, 0)),
]
persons = [Person(space, screen, randint(500, 800), randint(100, 500), 10, (100, 40, 0)) for k in range(number_of_people)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if len(persons) == 0:
        break

    screen.fill((0, 0, 0))

    for wall in walls:
        wall.draw()

    for obstacle in obstacles:
        obstacle.draw()

    for person in persons:
        if person.x < 20:
            persons.remove(person)
            continue
        person.update_coordinates()
        person.pull_to_point(f_x, f_y, 60)
        person.draw_person()
        # person.draw_force(f_x, f_y)

    number_of_people_per_time.append(len(persons))
    number_of_people_left_per_time.append(number_of_people - len(persons))
    time_list.append(round(total_time/60, 2))
    total_time += 1

    space.step(1/fps)
    pygame.display.update()
    clock.tick(fps)

plt.title(f"Total time was {round(total_time / 60, 2)} seconds")
plt.xlabel("Time in seconds")
plt.ylabel("Number of people")
plt.plot(time_list, number_of_people_per_time, color=(1, 0, 0), label="People inside")
plt.plot(time_list, number_of_people_left_per_time, color=(0, 1, 0), label="People removed")
plt.legend()
plt.show()
