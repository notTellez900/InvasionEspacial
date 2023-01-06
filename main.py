import pygame
import random
import math
from pygame import mixer

# Formula de la distancia, siempre será importante
# Lo mejor seria crar la clase enemigo y generar varias instancias de ella
# Inicializar en pygame
pygame.init()

# Creacion de la pantalla
# establecer el modo en que se muestra la pantalla
# Los tamaños se mandan en una tupla
pantalla = pygame.display.set_mode((800, 600))

# Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Titulo e Icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load('ovni.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

# Todos pixeles son relevantes, hay que manejarlos como coordenadas
# hay que tenerlos en cuenta para ubicar las imagenes, etc

# Jugador
img_jugador = pygame.image.load('cohete.png')
# Posicion en X
jugador_x = 368
# Posicion en Y
jugador_y = 500
# Cambio de la posicion en X
jugador_x_cambio = 0
""" 
Debido a que mi jugador mide 64 pixeles, para querer que este en el medio primero es hacer la matematica
de dividir 800/2 y luego restarle la mitad de mi jugador (32) para poder ponerlo
exactamente en la mitad con respecto al eje horizontal

Y para el alto es la altura menos la altura de mi jugador
"""
# Enemigo
img_enemigo = []
# Posicion en X
enemigo_x = []
# Posicion en Y
enemigo_y = []
# Cambio de la posicion en X
enemigo_x_cambio = []
# cambio en Y del enemigo
enemigo_y_cambio = []
# cantidad de enemigos
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Bala
img_bala = pygame.image.load('bala.png')
# Posicion en X
bala_x = 0
# Posicion en Y
bala_y = 500
# cambio en Y de la bala
bala_y_cambio = 1
# Visibilidad de la bala
bala_visible = False

# Variable puntaje
puntaje = 0
fuente = pygame.font.Font('fastest.ttf', 32)
texto_x = 10
text_y = 10

# Texto final juego
fuente_final = pygame.font.Font('fastest.ttf', 40)


# Funcion texto final
def texto_final():
    mi_fuente_final = fuente_final.render('GAME OVER', True, (255,255,255))
    pantalla.blit(mi_fuente_final, (200, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion de la poscion del jugador
def posicion_jugador(posX, posY):
    # Blit significa arrojar, como arrojar a la pantalla
    pantalla.blit(img_jugador, (posX, posY))


# Funcion de la poscion del enemigo
def posicion_enemigo(posX, posY, enemigo):
    # Blit significa arrojar, como arrojar a la pantalla
    pantalla.blit(img_enemigo[enemigo], (posX, posY))


# Funcion disparar bala
def disparar_bala(posX, posY):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (posX + 16, posY + 10))


# Funcion encargada de detectar colisiones
def hay_colision(pos_x_enemigo, pos_y_enemigo, pos_x_bala, pos_y_bala):
    distancia = math.sqrt(math.pow(pos_x_enemigo - pos_x_bala, 2) + math.pow(pos_y_bala - pos_y_enemigo, 2))
    if distancia < 27:
        return True
    else:
        return False


# Eventos, todo lo que ocurra en la pantalla de pygame es un evento
# Loop del juego, es la columna vertebral del juego
se_ejecuta = True
while se_ejecuta:
    # Cargar una imagen de fondo
    pantalla.blit(fondo, (0, 0))
    # Ajustar el color de la pantalla
    # pantalla.fill((205, 144, 228))

    # pygame.event.get() trae todos los eventos de pygame
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # KEYDOWN es tecla presionada
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                # Cada vez que oprima la flecha izquierda se modificará la posicion del jugador en X
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                # Cada vez que oprima la flecha derecha se modificará la posicion del jugador en X
                jugador_x_cambio = +0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                if not bala_visible:
                    sonido_bala.play()
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar flache
        if evento.type == pygame.KEYUP:
            # Cuando el usuario suelte la flecha que ha presionado
            # se establecera un cero para que se quede quieto y no se mueva más
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar posicion
    jugador_x += jugador_x_cambio
    # Mantener dentro de los bordes
    if jugador_x <= -4:
        """
        El jugador no podra salirse del borde por lo que
        siempre se estara reestableciendo su posicion a -4
        cada vez que quiera pasarse del borde izquierdo
        """
        jugador_x = -4
    elif jugador_x >= 740:
        """
        El jugador no podra salirse del borde por lo que
        siempre se estara reestableciendo su posicion a 740
        ya que al tener un ancho de 800 pixeles menos el ancho del jugador (64px)
        esto nos dará el numero al cual se debe reestablecer la posicion del jugador
        siempre que quiera salirse del borde derecho, pero este se puede modificar para que quede mucho mas pegado
        al borde
        """
        jugador_x = 740

    # Modificar posicion el enemigo
    for e in range(cantidad_enemigos):
        # Fin del juego
        if enemigo_y[e] > 470:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener al enemigo dentro de los bordes
        if enemigo_x[e] <= -4:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 740:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        posicion_enemigo(enemigo_x[e], enemigo_y[e], e)

    # Modificar el movimiento de la bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    # Modificar la posicion de la bala
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    posicion_jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, text_y)
    # Update hará que se actualicen los cambios en la pantalla
    pygame.display.update()
