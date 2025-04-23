import pygame
import random

class Jugador:
    def __init__(self, x=370, y=480):
        self.imagen = pygame.image.load("jugador.png")
        self.imagen = pygame.transform.scale(self.imagen, (50, 50))
        self.x = x
        self.y = y
        self.velocidad = 0
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()

    def mover(self, direccion):
        self.velocidad = direccion

    def actualizar(self):
        self.x += self.velocidad
        self.x = max(0, min(736, self.x))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

class Enemigo:
    def __init__(self, tipo=1, velocidad_extra=0):
        self.tipo = tipo
        self.image = self.cargar_imagen_por_tipo(tipo)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.velocidad_x = 1 + velocidad_extra
        self.velocidad_y = 5
        self.bala_x = self.x
        self.bala_y = self.y
        self.bala_img = pygame.image.load("bala.png")
        self.bala_img = pygame.transform.scale(self.bala_img, (10, 20))
        self.disparando = False
        self.ancho = self.image.get_width()
        self.alto = self.image.get_height()

    def cargar_imagen_por_tipo(self, tipo):
        rutas = {
            1: "enemigo.png",
            2: "enemigo_2.png",
            3: "enemigo_3.png",
            4: "enemigo_4.png"
        }
        return pygame.image.load(rutas.get(tipo, "enemigo.png"))

    def mover(self):
        self.x += self.velocidad_x
        if self.x <= 0 or self.x >= 736:
            self.velocidad_x *= -1
            self.y += self.velocidad_y

    def dibujar(self, pantalla):
        pantalla.blit(self.image, (self.x, self.y))

    def colision_con(self, bala_x, bala_y):
        enemigo_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        bala_rect = pygame.Rect(bala_x, bala_y, 10, 20)
        return enemigo_rect.colliderect(bala_rect)

    def ha_llegado_al_final(self):
        return self.y > 440

    def iniciar_disparo(self):
        self.disparando = True
        self.bala_x = self.x
        self.bala_y = self.y

    def mover_bala(self, pantalla):
        if self.disparando:
            self.bala_y += 7
            pantalla.blit(self.bala_img, (self.bala_x + 16, self.bala_y))
            if self.bala_y > 600:
                self.disparando = False

