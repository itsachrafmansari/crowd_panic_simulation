import math

import pygame
import pymunk
import sys

from pymunk import Vec2d

pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 0)


class Person:
    def __init__(self, space, screen, x, y, radius, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.body = pymunk.Body(1, 1, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0
        self.shape.friction = 1
        space.add(self.body, self.shape)

    def update_coordinates(self):
        self.x = self.body.position.x
        self.y = self.body.position.y

    def pull_to_point(self, point_x, point_y):
        direction_vector = Vec2d(point_x - self.x, point_y - self.y)
        distance_to_point = math.sqrt(direction_vector.x**2 + direction_vector.y**2)

        if distance_to_point:
            self.body.apply_impulse_at_world_point(0.001 * distance_to_point * direction_vector, (self.x, self.y))

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.shape.body.position, self.radius)


class Obstacle:
    def __init__(self, space, screen, x, y, ):
        pass

    def create_obstacle(self, main_space):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (450, 450)
        shape = pymunk.Circle(body, 60)
        shape.elasticity = 1
        main_space.add(body, shape)
        return shape


    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            pygame.draw.circle(screen, (0, 255, 0), (int(obstacle.body.position.x), int(obstacle.body.position.y)), 60)


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
        self.shape.elasticity = 0
        space.add(self.shape)


    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.left, self.top, self.width, self.height))


persons = [
    Person(space, screen, 100, 100, 20, (100, 40, 0)),
    Person(space, screen, 230, 200, 20, (100, 40, 0)),
    Person(space, screen, 230, 100, 20, (100, 40, 0)),
    Person(space, screen, 230, 100, 20, (100, 40, 0)),
]

walls = [
    Wall(space, screen, 450, 560, 830, 10, (0, 40, 0)),
    Wall(space, screen, 450, 40, 830, 10, (0, 40, 0)),
    Wall(space, screen, 40, 300, 10, 510, (0, 40, 0)),
    Wall(space, screen, 860, 300, 10, 510, (0, 40, 0)),
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    for wall in walls:
        wall.draw()

    for person in persons:
        person.update_coordinates()
        person.pull_to_point(450, 300)
        person.draw()


    space.step(1/60)
    pygame.display.update()
    clock.tick(60)
