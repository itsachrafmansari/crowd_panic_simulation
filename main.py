from random import randint
from sys import exit
import pygame


# Initialisation de la simulation
pygame.init()
clock = pygame.time.Clock()
longeur_de_plan = 1000
hauteur_de_plan = 700
couleur_de_arriere_plan = (255, 255, 250)
screen = pygame.display.set_mode((longeur_de_plan, hauteur_de_plan))
fps = 60
nombre_des_individus = 100
individu_vitesse = 3
individu_height = 30
individu_width = 30
collision_tolerance = 10


class Individu(pygame.Rect):

    def __init__(self, left, top, width, height, x_speed, y_speed, color):
        super().__init__(left, top, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color = color


    def deplacer(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.left <= 0 and self.x_speed < 0:
            self.x_speed *= -1
        if self.right >= longeur_de_plan and self.x_speed > 0:
            self.x_speed *= -1
        if self.top <= 0 and self.y_speed < 0:
            self.y_speed *= -1
        if self.bottom >= hauteur_de_plan and self.y_speed > 0:
            self.y_speed *= -1
        
        pygame.draw.circle(screen, self.color, self.center, self.width / 2)


    def check_collision(self, collision_objects_list):
        collision_objects = collision_objects_list[:]
        collision_objects.pop(collision_objects_list.index(self))
        collision_objects.append(wall1)
        collision_objects.append(wall2)

        for other_object in collision_objects:
            if self.colliderect(other_object):
                if abs(other_object.bottom - self.top) < collision_tolerance and self.y_speed < 0:
                    self.y_speed *= -1
                if abs(other_object.top - self.bottom) < collision_tolerance and self.y_speed > 0:
                    self.y_speed *= -1
                if abs(other_object.left - self.right) < collision_tolerance and self.x_speed > 0:
                    self.x_speed *= -1
                if abs(other_object.right - self.left) < collision_tolerance and self.x_speed < 0:
                    self.x_speed *= -1


    def check_exit(self, collision_objects_list):
        if (475 + (individu_width/2) < self.centerx < 525 - (individu_width/2)) and (250 + (individu_height/2) < self.centery < 450 - (individu_height/2)):
            collision_objects_list.remove(self)
            return True
        else:
            return False


def create_people():
    x_radndom = randint(individu_width*2, longeur_de_plan - individu_width*2)
    y_radndom = randint(individu_height*2, hauteur_de_plan - individu_height*2)

    person = Individu(x_radndom, y_radndom, individu_width, individu_height, individu_vitesse, individu_vitesse, (randint(0,255), randint(0,255), randint(0,255)))

    return person


objects = [create_people() for i in range(nombre_des_individus+1)]

wall1 = pygame.Rect(475, 0, 50, 250)
wall2 = pygame.Rect(475, 450, 50, 250)


# Démarrage de la simulation
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(couleur_de_arriere_plan)
    pygame.draw.rect(screen, (0, 0, 0), wall1)
    pygame.draw.rect(screen, (0, 0, 0), wall2)
    for obj in objects:
        if not obj.check_exit(objects):
            obj.deplacer()
            obj.check_collision(objects)
    pygame.display.flip()
    clock.tick(fps)
