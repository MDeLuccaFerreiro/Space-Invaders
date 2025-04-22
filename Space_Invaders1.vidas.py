import pygame
from jugador_enemigo import Jugador, Enemigo
import random
import sys

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Recursos
fondo = pygame.image.load("background.png")
bala_img = pygame.image.load("bala.png")
corazon_img = pygame.image.load("corazon.png")
corazon_img = pygame.transform.scale(corazon_img, (20, 20))

# Sonidos
sonido_laser = pygame.mixer.Sound("laser.wav")
sonido_explosion = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("background.wav")

# Fuentes
fuente_titulo = pygame.font.Font('freesansbold.ttf', 64)
fuente_grande = pygame.font.Font('freesansbold.ttf', 40)
fuente_mediana = pygame.font.Font('freesansbold.ttf', 28)

# Variables globales
bala_x = 0
bala_y = 480
bala_cambio_y = 10
estado_bala = "ready"

nivel = 1
enemigos = []
jugador = Jugador()
vidas = 3
score = 0  # Variable para el puntaje

# Funciones auxiliares
def reiniciar_juego():
    global vidas, jugador, nivel, enemigos, bala_x, bala_y, estado_bala, score
    vidas = 3
    jugador = Jugador()
    nivel = 1
    enemigos = crear_enemigos(nivel)
    bala_x = 0
    bala_y = 480
    estado_bala = "ready"
    score = 0  # Reiniciar puntaje

def disparar_bala(x, y):
    global estado_bala
    estado_bala = "fuego"
    sonido_laser.play()
    screen.blit(bala_img, (x + 16, y + 10))

def mostrar_game_over():
    global score
    texto = fuente_titulo.render("GAME OVER", True, (255, 255, 255))
    score_text = fuente_grande.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(texto, (200, 250))
    screen.blit(score_text, (250, 320))
    pygame.display.update()
    pygame.time.delay(2000)

def mostrar_tutorial():
    en_tutorial = True
    while en_tutorial:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))
        titulo = fuente_grande.render("TUTORIAL", True, (255, 255, 255))
        instrucciones = [
            "Jugador 1: Flechas + Espacio",
            "Jugador 2: A / D + W (en multijugador)",
            "Presiona ESC para pausar el juego",
            "Evita que los enemigos lleguen abajo",
            "Elimina enemigos para avanzar de nivel",
            "Presiona ESC para volver al menú"
        ]
        screen.blit(titulo, (250, 30))
        for i, texto in enumerate(instrucciones):
            linea = fuente_mediana.render(texto, True, (200, 200, 200))
            screen.blit(linea, (60, 120 + i * 35))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                en_tutorial = False

def mostrar_menu():
    pygame.mixer.music.play(-1)
    en_menu = True
    opciones = ["Iniciar Juego", "Tutorial", "Multijugador", "Salir"]
    indice_opcion = 0
    while en_menu:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))
        titulo = fuente_titulo.render("SPACE INVADERS", True, (255, 255, 255))
        screen.blit(titulo, (160, 100))
        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == indice_opcion else (150, 150, 150)
            fuente_actual = fuente_grande if i != indice_opcion else pygame.font.Font('freesansbold.ttf', 48)
            texto = fuente_actual.render(opcion, True, color)
            screen.blit(texto, (200, 250 + i * 70))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    indice_opcion = (indice_opcion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    indice_opcion = (indice_opcion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    seleccion = opciones[indice_opcion]
                    if seleccion == "Iniciar Juego":
                        pygame.mixer.music.stop()
                        iniciar_juego(False)
                    elif seleccion == "Tutorial":
                        mostrar_tutorial()
                    elif seleccion == "Multijugador":
                        pygame.mixer.music.stop()
                        iniciar_juego(True)
                    elif seleccion == "Salir":
                        pygame.quit()
                        exit()

def mostrar_mensaje_nivel(texto_nivel):
    texto = fuente_titulo.render(texto_nivel, True, (255, 255, 0))
    screen.blit(texto, (250, 250))
    pygame.display.update()
    pygame.time.delay(2000)

def crear_enemigos(nivel):
    velocidad_extra = (nivel - 1) * 0.4
    cantidad = min(10, 5 + nivel)
    return [Enemigo(velocidad_extra=velocidad_extra) for _ in range(cantidad)]

def colision_jugador(jugador, bala_x, bala_y):
    jugador_rect = pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto)
    bala_rect = pygame.Rect(bala_x, bala_y, 10, 20)
    return jugador_rect.colliderect(bala_rect)

def mostrar_nv(nivel, vidas, score):
    texto_nivel = fuente_mediana.render(f"Nivel: {nivel}", True, (255, 255, 255))
    texto_score = fuente_mediana.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(texto_nivel, (10, 10))
    screen.blit(texto_score, (10, 40))
    for i in range(vidas):
        screen.blit(corazon_img, (760 - i * 25, 570))

# Juego principal
def iniciar_juego(multijugador=False):
    global nivel, enemigos, jugador, vidas, estado_bala, bala_x, bala_y, score
    reiniciar_juego()
    jugador2 = Jugador(x=200) if multijugador else None
    estado_bala2 = "ready"
    bala2_x, bala2_y = 0, 480
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jugador.mover(-5)
                elif event.key == pygame.K_RIGHT:
                    jugador.mover(5)
                elif event.key == pygame.K_SPACE and estado_bala == "ready":
                    bala_x = jugador.x
                    bala_y = jugador.y
                    disparar_bala(bala_x, bala_y)
                if multijugador:
                    if event.key == pygame.K_a:
                        jugador2.mover(-5)
                    elif event.key == pygame.K_d:
                        jugador2.mover(5)
                    elif event.key == pygame.K_w and estado_bala2 == "ready":
                        bala2_x = jugador2.x
                        bala2_y = jugador2.y
                        estado_bala2 = "fuego"
                        sonido_laser.play()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    jugador.mover(0)
                if multijugador and event.key in (pygame.K_a, pygame.K_d):
                    jugador2.mover(0)
                if event.key == pygame.K_ESCAPE:
                    return

        jugador.actualizar()
        jugador.dibujar(screen)
        if multijugador:
            jugador2.actualizar()
            jugador2.dibujar(screen)

        # Disparo jugador 1
        if estado_bala == "fuego":
            disparar_bala(bala_x, bala_y)
            bala_y -= bala_cambio_y
            if bala_y <= 0:
                bala_y = 480
                estado_bala = "ready"

        # Disparo jugador 2
        if multijugador and estado_bala2 == "fuego":
            screen.blit(bala_img, (bala2_x + 16, bala2_y + 10))
            bala2_y -= bala_cambio_y
            if bala2_y <= 0:
                bala2_y = 480
                estado_bala2 = "ready"

        for enemigo in enemigos[:]:
            enemigo.mover()
            enemigo.dibujar(screen)

            if enemigo.disparando:
                enemigo.mover_bala(screen)
                if colision_jugador(jugador, enemigo.bala_x, enemigo.bala_y) or (
                        multijugador and colision_jugador(jugador2, enemigo.bala_x, enemigo.bala_y)):
                    enemigo.disparando = False
                    vidas -= 1
                    if vidas <= 0:
                        mostrar_game_over()
                        return

            if not enemigo.disparando and random.randint(0, 250) == 1:
                enemigo.iniciar_disparo()

            if enemigo.ha_llegado_al_final():
                for e in enemigos:
                    e.y = 2000
                mostrar_game_over()
                return

            if enemigo.colision_con(bala_x, bala_y):
                sonido_explosion.stop()
                sonido_explosion.play()
                bala_y = 480
                estado_bala = "ready"
                enemigos.remove(enemigo)
                score += 10  # Aumentar puntaje al eliminar un enemigo

            elif multijugador and enemigo.colision_con(bala2_x, bala2_y):
                sonido_explosion.stop()
                sonido_explosion.play()
                bala2_y = 480
                estado_bala2 = "ready"
                enemigos.remove(enemigo)
                score += 10  # Aumentar puntaje al eliminar un enemigo

        if not enemigos:
            nivel += 1
            mostrar_mensaje_nivel(f"NIVEL {nivel}")
            enemigos = crear_enemigos(nivel)

        mostrar_nv(nivel, vidas, score)
        pygame.display.update()

# Ejecutar
while True:
    mostrar_menu()
