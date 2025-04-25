import pygame
from jugador_enemigo_final import Jugador, Enemigo
from puntajes_python import actualizar_ranking, cargar_ranking
import random
import sys

# Inicialización de Pygame y configuración básica de ventana
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Carga de sonidos del juego
sonido_laser = pygame.mixer.Sound("laser.wav")
sonido_explosion = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("background.wav")
pygame.mixer.set_num_channels(32)
canal_laser = pygame.mixer.Channel(2)
sonido_laser.set_volume(0.5)        # Volumen del sonido del láser
canal_laser.set_volume(0.5)

# Recursos gráficos
fondo = pygame.image.load("background.png")
bala_img = pygame.image.load("bala.png")
bala_img = pygame.transform.scale(bala_img, (15, 15))
corazon_img = pygame.image.load("corazon.png")
corazon_img = pygame.transform.scale(corazon_img, (20, 20))

# Fuentes de texto
fuente_titulo = pygame.font.Font('freesansbold.ttf', 64)
fuente_grande = pygame.font.Font('freesansbold.ttf', 40)
fuente_mediana = pygame.font.Font('freesansbold.ttf', 28)

# Variables globales del juego
bala_x = 0
bala_y = 480
bala_cambio_y = 10
estado_bala = "ready"
nivel = 1
enemigos = []
jugador = Jugador()
vidas = 3
score = 0  # Puntaje del jugador

# Reinicia el estado completo del juego
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

# Dispara la bala desde el jugador
def disparar_bala(x, y):
    global estado_bala
    estado_bala = "fuego"
    #canal_laser.play(sonido_laser)
    screen.blit(bala_img, (x + 16, y + 10))

# Muestra la pantalla de Game Over y espera tecla ESC
def mostrar_game_over(nombre_jugador):
    global score
    screen.fill((0, 0, 0))
    actualizar_ranking(nombre_jugador, score)

    texto_game_over = fuente_titulo.render("GAME OVER", True, (255, 0, 0))
    texto_rect = texto_game_over.get_rect(center=(400, 220))
    screen.blit(texto_game_over, texto_rect)

    texto_score = fuente_grande.render(f"Puntaje: {score}", True, (255, 255, 0))
    score_rect = texto_score.get_rect(center=(400, 300))
    screen.blit(texto_score, score_rect)

    texto_continuar = fuente_mediana.render("Presiona ESC para volver al menú", True, (200, 200, 200))
    continuar_rect = texto_continuar.get_rect(center=(400, 370))
    screen.blit(texto_continuar, continuar_rect)
    pygame.display.update()

    # Espera que el jugador presione ESC para volver al menú
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                esperando = False

# Muestra el tutorial con controles y reglas
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

def mostrar_ranking():
    screen.fill((0, 0, 0))
    screen.blit(fondo, (0, 0))

    ranking = cargar_ranking()  # Cargar los puntajes más altos
    titulo = fuente_titulo.render("RANKING", True, (255, 255, 0))
    titulo_rect = titulo.get_rect(center=(400, 80))
    screen.blit(titulo, titulo_rect)

    if not ranking:
        mensaje = fuente_mediana.render("No hay puntajes registrados aún.", True, (255, 255, 255))
        mensaje_rect = mensaje.get_rect(center=(400, 200))
        screen.blit(mensaje, mensaje_rect)
    else:
        for i, entrada in enumerate(ranking):
            texto_ranking = fuente_mediana.render(
                f"{i + 1}. {entrada['nombre']} - {entrada['puntaje']}", True, (255, 255, 255)
            )
            texto_rect = texto_ranking.get_rect(center=(400, 160 + i * 40))
            screen.blit(texto_ranking, texto_rect)

    texto_volver = fuente_mediana.render("Presiona ESC para volver", True, (180, 180, 180))
    volver_rect = texto_volver.get_rect(center=(400, 500))
    screen.blit(texto_volver, volver_rect)

    pygame.display.update()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                esperando = False


def pedir_nombre():
    nombre = ""
    escribiendo = True
    while escribiendo:
        screen.fill((0, 0, 0))
        texto = fuente_grande.render("Ingresa tu nombre:", True, (255, 255, 255))
        screen.blit(texto, (200, 200))
        texto_nombre = fuente_grande.render(nombre + "|", True, (0, 255, 0))
        screen.blit(texto_nombre, (200, 260))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre.strip():
                    escribiendo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12 and event.unicode.isprintable():
                        nombre += event.unicode
    return nombre

# Menú principal del juego con navegación y selección
def mostrar_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("background.wav")
    pygame.mixer.music.play(-1)

    en_menu = True
    opciones = ["Iniciar Juego", "Tutorial", "Multijugador", "Ranking", "Salir"]
    indice_opcion = 0
    while en_menu:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))

        # Título centrado
        titulo = fuente_titulo.render("SPACE INVADERS", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(400, 120))
        screen.blit(titulo, titulo_rect)

        # Espaciado vertical entre opciones y elevarlas un poco
        base_y = 220  # Antes estaba más abajo, ahora más arriba
        spacing = 60

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == indice_opcion else (150, 150, 150)
            fuente_actual = fuente_grande if i != indice_opcion else pygame.font.Font('freesansbold.ttf', 48)
            texto = fuente_actual.render(opcion, True, color)
            texto_rect = texto.get_rect(center=(400, base_y + i * spacing))  # Centramos horizontalmente
            screen.blit(texto, texto_rect)

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
                        nombre_jugador = pedir_nombre()
                        iniciar_juego(False, nombre_jugador)
                    elif seleccion == "Tutorial":
                        mostrar_tutorial()
                    elif seleccion == "Multijugador":
                        nombre_jugador = pedir_nombre()
                        iniciar_juego(True, nombre_jugador)
                    elif seleccion == "Ranking":
                        mostrar_ranking()
                    elif seleccion == "Salir":
                        pygame.quit()
                        exit()


# Muestra mensaje temporal cuando se sube de nivel
def mostrar_mensaje_nivel(texto_nivel):
    screen.fill((0, 0, 0))  # Fondo negro
    texto = fuente_titulo.render(texto_nivel, True, (255, 255, 0))
    texto_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(texto, texto_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Pausa visual



# Genera enemigos en una grilla de 8 columnas x 3 filas
def crear_enemigos(nivel):
    filas = 3
    columnas = 8
    enemigos_grupo = []
    for fila in range(filas):
        for col in range(columnas):
            x = 80 + col * 80
            y = 50 + fila * 60
            enemigo = Enemigo(x=x, y=y)
            enemigos_grupo.append(enemigo)
    return enemigos_grupo

# Detecta si una bala colisiona con un jugador
def colision_jugador(jugador, bala_x, bala_y):
    jugador_rect = pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto)
    bala_rect = pygame.Rect(bala_x, bala_y, 10, 20)
    return jugador_rect.colliderect(bala_rect)

# Dibuja el nivel, score y vidas restantes en pantalla
def mostrar_nv(nivel, vidas, score):
    texto_nivel = fuente_mediana.render(f"Nivel: {nivel}", True, (255, 255, 255))
    texto_score = fuente_mediana.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(texto_nivel, (10, 10))
    screen.blit(texto_score, (10, 40))
    for i in range(vidas):
        screen.blit(corazon_img, (760 - i * 25, 570))

# Lógica que mueve a los enemigos, cambia dirección al chocar bordes
def mover_enemigos(enemigos):
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

# Permite que los enemigos disparen con probabilidad baja
def disparar_enemigos(enemigos):
    for enemigo in enemigos:
        if random.randint(0, 1000) == 1:
            enemigo.iniciar_disparo()

def dibujar_vidas(jugador, x, y):
    for i in range(jugador.vidas):
        screen.blit(corazon_img, (x + i * 25, y))


# Bucle principal de juego (modo 1 o 2 jugadores)
def dibujar_vidas(jugador, x, y):
    for i in range(jugador.vidas):
        screen.blit(corazon_img, (x + i * 25, y))


def iniciar_juego(multijugador=False, nombre_jugador="Jugador"):
    global nivel, enemigos, jugador, vidas, estado_bala, bala_x, bala_y, score
    pygame.mixer.music.stop()
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
                elif event.key == pygame.K_SPACE and estado_bala == "ready" and jugador.vivo:
                    bala_x = jugador.x
                    bala_y = jugador.y
                    estado_bala = "fuego"
                    sonido_laser.play()
                if multijugador and jugador2.vivo:
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

        if jugador.vivo:
            jugador.actualizar()
            jugador.dibujar(screen)
        if multijugador and jugador2.vivo:
            jugador2.actualizar()
            jugador2.dibujar(screen)

        mover_enemigos(enemigos)
        disparar_enemigos(enemigos)

        if estado_bala == "fuego":
            disparar_bala(bala_x, bala_y)
            bala_y -= bala_cambio_y
            if bala_y <= 0:
                bala_y = 480
                estado_bala = "ready"

        if multijugador and estado_bala2 == "fuego":
            screen.blit(bala_img, (bala2_x + 16, bala2_y + 10))
            bala2_y -= bala_cambio_y
            if bala2_y <= 0:
                bala2_y = 480
                estado_bala2 = "ready"

        for enemigo in enemigos[:]:
            if enemigo.ha_llegado_al_final():
                mostrar_game_over(nombre_jugador)
                return
            enemigo.dibujar(screen)
            if enemigo.disparando:
                enemigo.mover_bala(screen)
                if jugador.vivo and colision_jugador(jugador, enemigo.bala_x, enemigo.bala_y):
                    enemigo.disparando = False
                    jugador.perder_vida()

                elif multijugador and jugador2.vivo and colision_jugador(jugador2, enemigo.bala_x, enemigo.bala_y):
                    enemigo.disparando = False
                    jugador2.perder_vida()

            if enemigo.colision_con(bala_x, bala_y) and jugador.vivo:
                canal_explosion = pygame.mixer.Channel(1)
                canal_explosion.play(sonido_explosion)
                bala_y = 480
                estado_bala = "ready"
                enemigos.remove(enemigo)
                score += 10

            elif multijugador and enemigo.colision_con(bala2_x, bala2_y) and jugador2.vivo:
                canal_explosion = pygame.mixer.Channel(1)
                canal_explosion.play(sonido_explosion)
                bala2_y = 480
                estado_bala2 = "ready"
                enemigos.remove(enemigo)
                score += 10

        if not enemigos and jugador.vivo and (not multijugador or jugador2.vivo):
            pygame.display.update()
            pygame.time.delay(300)
            nivel += 1
            mostrar_mensaje_nivel(f"NIVEL {nivel}")
            enemigos = crear_enemigos(nivel)
        if not jugador.vivo and (not multijugador or not jugador2.vivo):
            mostrar_game_over(nombre_jugador)
            return

        # HUD de nivel, score y vidas de cada jugador
        nivel_text = fuente_mediana.render(f"Nivel: {nivel}", True, (255, 255, 255))
        screen.blit(nivel_text, (10, 10))
        score_text = fuente_mediana.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 40))

        if jugador.vivo:
            dibujar_vidas(jugador, 650, 560)
        if multijugador and jugador2.vivo:
            dibujar_vidas(jugador2, 10, 560)

        pygame.display.update()

        if not jugador.vivo and (not jugador2.vivo if multijugador else True):
            mostrar_game_over(nombre_jugador)
            return


# Lanza el menú principal en bucle infinito
while True:
    mostrar_menu()