import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Pantalla
screen = pygame.display.set_mode((800, 600))

# Fondo
fondo = pygame.image.load("background.png")

# Título e ícono
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
    enemy_X.append(50 + i * 100) # Espaciado horizontal
    enemy_Y.append(50) # Todos en la misma altura
    enemyX_change.append(2) #Velocidad horizontal
    enemyY_change.append(40) # Bajarán 40px cuando cambian de dirección

# Bala
bala_Img = pygame.image.load("bala.png")
bala_X = 0
bala_Y = 480
balaY_change = 10
estado_bala = "ready" # significa que esta lista para disparar

# Texto GAME OVER
mensaje = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    texto = mensaje.render("GAME OVER", True, (255, 255, 255))
    screen.blit(texto, (200, 250))

def player(x, y):
    screen.blit(jugador, (x, y))

def enemy_draw(x, y, i):
    screen.blit(enemy[i], (x, y))

def disparo(x, y):
    global estado_bala 
    estado_bala = "fuego"
    screen.blit(bala_Img, (x + 16, y + 10)) # +16 y +10 para centrar la bala en la nave

def colicion(enemy_X, enemy_Y, bala_X, bala_Y):
    distance = math.sqrt(math.pow(enemy_X - bala_X, 2) + (math.pow(enemy_Y - bala_Y, 2)))
    if distance < 27:
        return True
    else:
        return False
# Bucle principal
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Detectar teclas presionadas
            if event.key == pygame.K_SPACE and estado_bala == "ready":  # Disparar si la bala está lista
                bala_X = jugador_X  # Posición de la bala en la nave
                bala_Y = jugador_Y
                disparo(bala_X, bala_Y)

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        jugadorX_change = -5
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
            estado_bala = "ready"  # La bala vuelve a estar lista

    # Mostrar jugador y enemigos
    player(jugador_X, jugador_Y)
    for i in range(num_of_enemies):
        # Movimiento horizontal
        enemy_X[i] += enemyX_change[i]
        # Rebote contra los bordes
        if enemy_X[i] <= 0 or enemy_X[i] >= 736:
            enemyX_change[i] *= -1  # Cambiar de dirección
            enemy_Y[i] += enemyY_change[i]  # Bajar al cambiar de dirección

        enemy_draw(enemy_X[i], enemy_Y[i], i)
        # Coliciones
        colicion_ocurrida = colicion(enemy_X[i], enemy_Y[i], bala_X, bala_Y)
        if colicion_ocurrida:
            bala_Y = 480
            estado_bala = "ready"
            enemy_X[i] = 50 + random.randint(0, 7) # Vuelve a colocar la fila
            enemy_Y[i] = 50

    pygame.display.update()

pygame.quit()
