import pygame
import random
import math

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
fondo = pygame.image.load("background.png")
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Jugador
jugador = pygame.image.load("jugador.png")
jugador_X = 370
jugador_Y = 480
jugadorX_change = 0

# Enemigos
enemy = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy.append(pygame.image.load('enemigo.png'))
    enemy_X.append(50 + i * 100)
    enemy_Y.append(50)
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bala
bala_Img = pygame.image.load("bala.png")
bala_X = 0
bala_Y = 480
balaY_change = 10
estado_bala = "ready"

# Fuentes
fuente_titulo = pygame.font.Font('freesansbold.ttf', 64)
fuente_grande = pygame.font.Font('freesansbold.ttf', 40)
fuente_mediana = pygame.font.Font('freesansbold.ttf', 28)

# Controles (configuración predeterminada)
controles = {
    'izquierda': pygame.K_LEFT,
    'derecha': pygame.K_RIGHT,
    'disparo': pygame.K_SPACE
}

# Funciones del juego
def game_over():
    texto = fuente_titulo.render("GAME OVER", True, (255, 255, 255))
    screen.blit(texto, (200, 250))

def player(x, y):
    screen.blit(jugador, (x, y))

def enemy_draw(x, y, i):
    screen.blit(enemy[i], (x, y))

def disparo(x, y):
    global estado_bala
    estado_bala = "fuego"
    screen.blit(bala_Img, (x + 16, y + 10))

def colicion(enemy_X, enemy_Y, bala_X, bala_Y):
    distance = math.sqrt(math.pow(enemy_X - bala_X, 2) + (math.pow(enemy_Y - bala_Y, 2)))
    return distance < 27

def configurar_controles():
    global controles
    en_config = True
    opciones = list(controles.keys())
    indice_opcion = 0

    esperando_nueva_tecla = False

    while en_config:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))

        titulo = fuente_titulo.render("CONFIGURAR CONTROLES", True, (255, 255, 255))
        screen.blit(titulo, (60, 60))

        for i, accion in enumerate(opciones):
            if esperando_nueva_tecla and i == indice_opcion:
                texto_linea = f"{accion.upper()}: Presiona una tecla..."
            else:
                tecla_actual = pygame.key.name(controles[accion]).upper()
                texto_linea = f"{accion.upper()}: {tecla_actual}"

            color = (255, 255, 255) if i == indice_opcion else (180, 180, 180)
            fuente_actual = pygame.font.Font('freesansbold.ttf', 36) if i == indice_opcion else fuente_grande
            texto = fuente_actual.render(texto_linea, True, color)
            screen.blit(texto, (100, 160 + i * 60))

        instruccion = fuente_mediana.render("ESC para volver", True, (200, 200, 200))
        screen.blit(instruccion, (280, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if esperando_nueva_tecla:
                if event.type == pygame.KEYDOWN:
                    controles[opciones[indice_opcion]] = event.key
                    esperando_nueva_tecla = False

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        indice_opcion = (indice_opcion + 1) % len(opciones)
                    elif event.key == pygame.K_UP:
                        indice_opcion = (indice_opcion - 1) % len(opciones)
                    elif event.key == pygame.K_RETURN:
                        esperando_nueva_tecla = True
                    elif event.key == pygame.K_ESCAPE:
                        en_config = False

# 🧾 MENÚ DE PAUSA
def menu_pausa():
    en_pausa = True
    opciones = ["Reanudar", "Reiniciar", "Volver al Inicio", "Settings", "Salir"]
    indice_opcion = 0

    while en_pausa:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))

        titulo = fuente_titulo.render("PAUSA", True, (255, 255, 255))
        screen.blit(titulo, (300, 100))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == indice_opcion else (150, 150, 150)
            fuente_activa = fuente_grande if i != indice_opcion else pygame.font.Font('freesansbold.ttf', 48)  # Más grande
            texto = fuente_activa.render(opcion, True, color)
            screen.blit(texto, (250, 200 + i * 70))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    indice_opcion = (indice_opcion + 1) % len(opciones)
                elif event.key == pygame.K_UP:
                    indice_opcion = (indice_opcion - 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    if opciones[indice_opcion] == "Reanudar":
                        return "reanudar"
                    elif opciones[indice_opcion] == "Reiniciar":
                        return "reiniciar"
                    elif opciones[indice_opcion] == "Volver al Inicio":
                        return "inicio"
                    elif opciones[indice_opcion] == "Settings":
                        mostrar_settings()
                    elif opciones[indice_opcion] == "Salir":
                        pygame.quit()
                        exit()

# 🧾 SETTINGS
def mostrar_settings():
    en_settings = True
    opciones = list(controles.keys())
    indice_opcion = 0
    esperando_nueva_tecla = False

    while en_settings:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))

        titulo = fuente_grande.render("SETTINGS", True, (255, 255, 255))
        screen.blit(titulo, (310, 50))

        for i, accion in enumerate(opciones):
            if esperando_nueva_tecla and i == indice_opcion:
                texto_linea = f"{accion.upper()}: Presiona una tecla..."
            else:
                tecla_actual = pygame.key.name(controles[accion]).upper()
                texto_linea = f"{accion.upper()}: {tecla_actual}"

            color = (255, 255, 255) if i == indice_opcion else (180, 180, 180)
            fuente_actual = pygame.font.Font('freesansbold.ttf', 36) if i == indice_opcion else fuente_grande
            texto = fuente_actual.render(texto_linea, True, color)
            screen.blit(texto, (100, 160 + i * 60))

        instruccion = fuente_mediana.render("ESC para volver", True, (200, 200, 200))
        screen.blit(instruccion, (280, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if esperando_nueva_tecla:
                if event.type == pygame.KEYDOWN:
                    controles[opciones[indice_opcion]] = event.key
                    esperando_nueva_tecla = False

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        indice_opcion = (indice_opcion + 1) % len(opciones)
                    elif event.key == pygame.K_UP:
                        indice_opcion = (indice_opcion - 1) % len(opciones)
                    elif event.key == pygame.K_RETURN:
                        esperando_nueva_tecla = True
                    elif event.key == pygame.K_ESCAPE:
                        en_settings = False

# 🧾 MENÚ PRINCIPAL
def mostrar_menu():
    en_menu = True
    opciones = ["Iniciar Juego", "Settings", "Salir"]
    indice_opcion = 0

    while en_menu:
        screen.fill((0, 0, 0))
        screen.blit(fondo, (0, 0))

        titulo = fuente_titulo.render("SPACE INVADER", True, (255, 255, 255))
        screen.blit(titulo, (160, 100))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == indice_opcion else (150, 150, 150)
            fuente_activa = fuente_grande if i != indice_opcion else pygame.font.Font('freesansbold.ttf', 48)
            texto = fuente_activa.render(opcion, True, color)
            x = 240
            y = 250 + i * 70
            screen.blit(texto, (x, y))

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
                    if opciones[indice_opcion] == "Iniciar Juego":
                        en_menu = False
                    elif opciones[indice_opcion] == "Settings":
                        mostrar_settings()
                    elif opciones[indice_opcion] == "Salir":
                        pygame.quit()
                        exit()

# Llamar al menú antes de iniciar el juego
mostrar_menu()

# Bucle principal del juego
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and estado_bala == "ready":
                bala_X = jugador_X
                bala_Y = jugador_Y
                disparo(bala_X, bala_Y)

            if event.key == pygame.K_ESCAPE:
                resultado_pausa = menu_pausa()
                if resultado_pausa == "reanudar":
                    pass  # Reanudar el juego sin hacer nada
                elif resultado_pausa == "reiniciar":
                    jugador_X = 370
                    jugador_Y = 480
                    enemy_X = [50 + i * 100 for i in range(num_of_enemies)]
                    enemy_Y = [50 for _ in range(num_of_enemies)]
                elif resultado_pausa == "inicio":
                    mostrar_menu()
                    running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[controles['izquierda']]:
        jugadorX_change = -5
    elif keys[controles['derecha']]:
        jugadorX_change = 5
    else:
        jugadorX_change = 0

    jugador_X += jugadorX_change
    jugador_X = max(0, min(736, jugador_X))

    # Movimiento de la bala
    if estado_bala == "fuego":
        disparo(bala_X, bala_Y)
        bala_Y -= balaY_change
        if bala_Y <= 0:
            bala_Y = 480
            estado_bala = "ready"

    # Mostrar jugador y enemigos
    player(jugador_X, jugador_Y)
    for i in range(num_of_enemies):
        enemy_X[i] += enemyX_change[i]
        if enemy_X[i] <= 0 or enemy_X[i] >= 736:
            enemyX_change[i] *= -1
            enemy_Y[i] += enemyY_change[i]

        if enemy_Y[i] > 440:
            for j in range(num_of_enemies):
                enemy_Y[j] = 2000
            game_over()
            break

        enemy_draw(enemy_X[i], enemy_Y[i], i)

        if colicion(enemy_X[i], enemy_Y[i], bala_X, bala_Y):
            bala_Y = 480
            estado_bala = "ready"
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(30, 150)

    pygame.display.update()

pygame.quit()
