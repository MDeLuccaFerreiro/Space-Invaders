import pygame
import random

class Jugador:
    def __init__(self, x=370, y=480):
        # Carga y escala imagen del jugador
        self.imagen = pygame.image.load("jugador.png")
        self.imagen = pygame.transform.scale(self.imagen, (50, 50))
        self.x = x
        self.y = y
        self.velocidad = 0  # Dirección y velocidad horizontal
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()

    def mover(self, direccion):
        # Cambia la velocidad para moverse en la dirección dada
        self.velocidad = direccion

    def actualizar(self):
        # Actualiza la posición del jugador y limita su movimiento dentro de pantalla
        self.x += self.velocidad
        self.x = max(0, min(736, self.x))

    def dibujar(self, pantalla):
        # Dibuja al jugador en pantalla
        pantalla.blit(self.imagen, (self.x, self.y))


class Enemigo:
    def __init__(self, x, y, tipo=1, velocidad_extra=0):
        self.tipo = tipo
        self.image = self.cargar_imagen_por_tipo(tipo)
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Requiere coordenadas x e y al crear un enemigo
        if x is None or y is None:
            raise ValueError("Las coordenadas x e y deben ser proporcionadas para cada enemigo")

        self.x = x
        self.y = y

        self.velocidad_x = 1 + velocidad_extra  # Velocidad horizontal puede aumentar con el nivel
        self.velocidad_y = 2
        self.bala_x = self.x
        self.bala_y = self.y
        self.bala_img = pygame.image.load("bala.png")
        self.bala_img = pygame.transform.scale(self.bala_img, (10, 20))
        self.disparando = False
        self.ancho = self.image.get_width()
        self.alto = self.image.get_height()
        self.contador_disparo = 0  # Controla la frecuencia de disparo del enemigo

    def cargar_imagen_por_tipo(self, tipo):
        # Devuelve la imagen según el tipo de enemigo (1 a 4)
        rutas = {
            1: "enemigo.png",
            2: "enemigo_2.png",
            3: "enemigo_3.png",
            4: "enemigo_4.png"
        }
        return pygame.image.load(rutas.get(tipo, "enemigo.png"))

    def dibujar(self, pantalla):
        # Dibuja al enemigo en la pantalla
        pantalla.blit(self.image, (self.x, self.y))

    def colision_con(self, bala_x, bala_y):
        # Comprueba si la bala colisiona con este enemigo
        enemigo_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto).inflate(-10, -10)
        bala_rect = pygame.Rect(bala_x, bala_y, 10, 20)
        return enemigo_rect.colliderect(bala_rect)

    def ha_llegado_al_final(self):
        # Devuelve True si el enemigo bajó demasiado
        return self.y > 440

    def iniciar_disparo(self):
        # Activa disparo desde la posición del enemigo
        self.disparando = True
        self.bala_x = self.x
        self.bala_y = self.y

    def mover_bala(self, pantalla):
        # Mueve la bala del enemigo hacia abajo y la dibuja
        if self.disparando:
            self.bala_y += 2
            pantalla.blit(self.bala_img, (self.bala_x + 16, self.bala_y))
            if self.bala_y > 600:
                self.disparando = False

    def crear_enemigos(nivel):
        # Crea una grilla de enemigos, con velocidad ajustada al nivel
        enemigos = []
        velocidad_extra = (nivel - 1) * 0.4
        for fila in range(3):
            for columna in range(8):
                x = 50 + columna * 80
                y = 50 + fila * 50
                enemigo = Enemigo(tipo=random.choice([1, 2, 3, 4]), x=x, y=y, velocidad_extra=velocidad_extra)
                enemigos.append(enemigo)
        return enemigos

    def mover_enemigos(enemigos):
        # Mueve los enemigos horizontalmente y baja al chocar con los bordes
        if not enemigos:
            return

        x_min = min(e.x for e in enemigos)
        x_max = max(e.x for e in enemigos)

        choca_izq = x_min <= 0
        choca_der = x_max >= 736

        if choca_izq or choca_der:
            for enemigo in enemigos:
                enemigo.y += 10
                enemigo.velocidad_x *= -1

        for enemigo in enemigos:
            enemigo.x += enemigo.velocidad_x

    def actualizar_disparo(self):
        # Controla el tiempo entre disparos (cada X ciclos)
        self.contador_disparo += 1
        if self.contador_disparo > 100:
            self.contador_disparo = 0
            self.iniciar_disparo()

    def disparar_enemigos(enemigos):
        # Administra los disparos de todos los enemigos (con probabilidad)
        for enemigo in enemigos:
            enemigo.actualizar_disparo()
            if random.randint(0, 1000) == 1 and enemigo.contador_disparo == 0:
                enemigo.iniciar_disparo()