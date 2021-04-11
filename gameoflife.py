# importo la libreria pygame
import pygame
import time
from math import floor
import random

# inicia pygame
pygame.init()

# variables para los colores
Negro = 0, 0, 0
Azul = 0, 0, 255
Gris = 25, 25, 25
Blanco = 255, 255, 255
fontgrande = pygame.font.SysFont("comicsansms", 80)
fontpequenha = pygame.font.SysFont("comicsansms", 25)

# creo una ventana y le asigno un nombre al juego
t_ventana = 1000
pantalla = pygame.display.set_mode((t_ventana, t_ventana))
pygame.display.set_caption("Juego De La Vida")


def tex_objetos(texto, color, tamanho):
    if tamanho == "pequenha":
        textSuperficie = fontpequenha.render(texto, True, color)
    elif tamanho == "grande":
        textSuperficie = fontgrande.render(texto, True, color)
    return textSuperficie, textSuperficie.get_rect()


def textos(msg, color, y_pos=0, tamanho="pequenha"):
    text_superficie, textRect = tex_objetos(msg, color, tamanho)
    textRect.center = (t_ventana / 2), (t_ventana / 2) + y_pos
    pantalla.blit(text_superficie, textRect)


def Intro():
    run = True
    while run:
        # pinto la pantalla
        pantalla.fill(Gris)
        textos("El juego de la vida", Azul, -150, tamanho="grande")
        textos('presiona "C" para modo patrones preconfigurados', Blanco, -60, tamanho="pequenha")
        textos('presiona "A" para modo patrones manuales', Blanco, 0, tamanho="pequenha")
        textos('presiona "R" para modo patrones aleatorios', Blanco, -30, tamanho="pequenha")
        pygame.display.update()
        # agrego una condicion si se cumple salgo del bucle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            else:
                teclado = pygame.key.get_pressed()
                if teclado[pygame.K_c]:
                    juego_de_la_vida()
                    run = False
                elif teclado[pygame.K_a]:
                    juego_con_jugador()
                    run = False
                elif teclado[pygame.K_r]:
                    juego_random()
                    run = False

def juego_random():
    # pinto la pantalla
    pantalla.fill(Gris)

    # especifico el numero n*n celdas que quiero en mi programa
    numero_de_celdas = 100

    # asigno el tamaño de cada celda
    d_celdas = t_ventana / numero_de_celdas

    # creo una matriz de ceros por comprension de tamaño nxn
    juego = [[0 for i in range(numero_de_celdas)] for j in range(numero_de_celdas)]

    for i in range(1000):
        juego[random.randint(0, 99)][random.randint(1, 99)] = 1


    # creo un bucle
    run = True
    pausar = False
    vel = .5
    while run:
        time.sleep(vel)
        # creo una nueva matriz a partir de la matriz juego
        actualizo_juego = []
        for i in juego:
            actualizo_juego.append(list(i))
        pantalla.fill(Gris)
        # agrego una condicion si se cumple salgo del bucle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausar = not pausar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    Intro()
                    run = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    vel += .1
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if vel > 0.1:
                        vel -= .1
        # hago un ciclo que recorra la matriz y compruebe cuantas celulas vivas hay alrededor de cada celula
        for y in range(numero_de_celdas):
            for x in range(numero_de_celdas):
                if pausar:
                    celulas_vecinas = juego[(x - 1) % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[x % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[(x - 1) % numero_de_celdas][y % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][y % numero_de_celdas] \
                                      + juego[(x - 1) % numero_de_celdas][(y + 1) % numero_de_celdas] \
                                      + juego[x % numero_de_celdas][(y + 1) % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][(y + 1) % numero_de_celdas]
                    # reglas del juego
                    # Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación")
                    if juego[x][y] == 1 and (celulas_vecinas < 2 or celulas_vecinas > 3):
                        actualizo_juego[x][y] = 0
                    # 1 si una celula esta muerta y tiene 3 vecinas vivas la celula nace
                    elif juego[x][y] == 0 and celulas_vecinas == 3:
                        actualizo_juego[x][y] = 1

                # creo una lista especificando sus coordenadas x & y de las celulas para posteriormente ser pintadas
                celda = [(x * d_celdas, y * d_celdas), ((x + 1) * d_celdas, y * d_celdas),
                         ((x + 1) * d_celdas, (y + 1) * d_celdas), (x * d_celdas, (y + 1) * d_celdas)]

                # pinto la celdas
                if actualizo_juego[x][y] == 0:
                    pygame.draw.polygon(pantalla, Negro, celda, 1)
                else:
                    pygame.draw.polygon(pantalla, Azul, celda, 0)

        # actualizo el estado del juego
        juego = []
        for i in actualizo_juego:
            juego.append(list(i))
        pygame.display.flip()


def juego_de_la_vida():
    # pinto la pantalla
    pantalla.fill(Gris)

    # especifico el numero n*n celdas que quiero en mi programa
    numero_de_celdas = 100

    # asigno el tamaño de cada celda
    d_celdas = t_ventana / numero_de_celdas

    # creo una matriz de ceros por comprension de tamaño nxn
    juego = [[0 for i in range(numero_de_celdas)] for j in range(numero_de_celdas)]

    # agrego un patron preconfigurado
    # figura 1
    juego[3][90] = 1
    juego[4][90] = 1
    juego[4][89] = 1
    juego[4][88] = 1
    juego[5][87] = 1
    juego[6][87] = 1
    juego[6][88] = 1

    juego[3][80] = 1
    juego[4][80] = 1
    juego[4][81] = 1
    juego[4][82] = 1
    juego[5][83] = 1
    juego[6][82] = 1
    juego[6][83] = 1

    juego[8][85] = 1
    juego[9][85] = 1
    juego[10][85] = 1
    juego[11][85] = 1
    juego[12][85] = 1
    juego[13][85] = 1

    juego[18][90] = 1
    juego[17][90] = 1
    juego[17][89] = 1
    juego[17][88] = 1
    juego[16][87] = 1
    juego[15][87] = 1
    juego[15][88] = 1

    juego[18][80] = 1
    juego[17][80] = 1
    juego[17][81] = 1
    juego[17][82] = 1
    juego[16][83] = 1
    juego[15][82] = 1
    juego[15][83] = 1

    # forma 2
    juego[41][87] = 1
    juego[41][88] = 1
    juego[41][89] = 1
    juego[43][86] = 1
    juego[44][86] = 1
    juego[45][86] = 1
    juego[43][91] = 1
    juego[44][91] = 1
    juego[45][91] = 1
    juego[46][87] = 1
    juego[46][88] = 1
    juego[46][89] = 1

    juego[41][81] = 1
    juego[41][82] = 1
    juego[41][83] = 1
    juego[43][79] = 1
    juego[44][79] = 1
    juego[45][79] = 1
    juego[43][84] = 1
    juego[44][84] = 1
    juego[45][84] = 1
    juego[46][81] = 1
    juego[46][82] = 1
    juego[46][83] = 1

    juego[53][87] = 1
    juego[53][88] = 1
    juego[53][89] = 1
    juego[49][86] = 1
    juego[50][86] = 1
    juego[51][86] = 1
    juego[49][91] = 1
    juego[50][91] = 1
    juego[51][91] = 1
    juego[48][87] = 1
    juego[48][88] = 1
    juego[48][89] = 1

    juego[48][81] = 1
    juego[48][82] = 1
    juego[48][83] = 1
    juego[49][79] = 1
    juego[50][79] = 1
    juego[51][79] = 1
    juego[49][84] = 1
    juego[50][84] = 1
    juego[51][84] = 1
    juego[53][81] = 1
    juego[53][82] = 1
    juego[53][83] = 1

    # forma3
    juego[32][76] = 1
    juego[33][74] = 1
    juego[33][75] = 1
    juego[34][76] = 1
    juego[34][77] = 1
    juego[35][75] = 1

    # forma4
    juego[17][64] = 1
    juego[17][65] = 1
    juego[17][66] = 1
    juego[17][67] = 1
    juego[17][68] = 1
    juego[17][69] = 1
    juego[18][64] = 1
    juego[18][65] = 1
    juego[18][66] = 1
    juego[18][67] = 1
    juego[18][68] = 1
    juego[18][69] = 1

    juego[17][62] = 1
    juego[18][62] = 1
    juego[19][62] = 1
    juego[20][62] = 1
    juego[21][62] = 1
    juego[22][62] = 1
    juego[17][61] = 1
    juego[18][61] = 1
    juego[19][61] = 1
    juego[20][61] = 1
    juego[21][61] = 1
    juego[22][61] = 1

    juego[24][61] = 1
    juego[24][62] = 1
    juego[24][63] = 1
    juego[24][64] = 1
    juego[24][65] = 1
    juego[24][66] = 1
    juego[25][61] = 1
    juego[25][62] = 1
    juego[25][63] = 1
    juego[25][64] = 1
    juego[25][65] = 1
    juego[25][66] = 1

    juego[25][68] = 1
    juego[24][68] = 1
    juego[23][68] = 1
    juego[22][68] = 1
    juego[21][68] = 1
    juego[20][68] = 1
    juego[25][69] = 1
    juego[24][69] = 1
    juego[23][69] = 1
    juego[22][69] = 1
    juego[21][69] = 1
    juego[20][69] = 1

    # forma
    juego[45][72] = 1
    juego[44][72] = 1
    juego[43][71] = 1
    juego[43][70] = 1
    juego[43][69] = 1
    juego[44][68] = 1
    juego[45][68] = 1
    juego[46][71] = 1
    juego[46][70] = 1
    juego[46][69] = 1

    juego[53][72] = 1
    juego[52][72] = 1
    juego[51][71] = 1
    juego[51][70] = 1
    juego[51][69] = 1
    juego[53][68] = 1
    juego[52][68] = 1
    juego[54][71] = 1
    juego[54][70] = 1
    juego[54][69] = 1

    # forma
    juego[67][72] = 1
    juego[67][71] = 1
    juego[68][72] = 1
    juego[68][71] = 1
    juego[62][75] = 1
    juego[62][76] = 1
    juego[61][75] = 1
    juego[61][76] = 1

    juego[66][81] = 1
    juego[66][82] = 1
    juego[65][81] = 1
    juego[65][82] = 1
    juego[71][77] = 1
    juego[71][78] = 1
    juego[72][77] = 1
    juego[72][78] = 1

    juego[64][75] = 1
    juego[64][76] = 1
    juego[64][77] = 1
    juego[64][78] = 1
    juego[65][79] = 1
    juego[66][79] = 1
    juego[67][79] = 1
    juego[68][79] = 1
    juego[66][78] = 1
    juego[67][77] = 1
    juego[65][76] = 1

    juego[69][75] = 1
    juego[69][76] = 1
    juego[69][77] = 1
    juego[69][78] = 1
    juego[65][74] = 1
    juego[66][74] = 1
    juego[67][74] = 1
    juego[68][74] = 1

    # forma
    juego[81][86] = 1
    juego[81][87] = 1
    juego[82][86] = 1
    juego[82][85] = 1
    juego[83][87] = 1
    juego[83][88] = 1
    juego[83][89] = 1
    juego[82][89] = 1
    juego[82][90] = 1

    juego[87][86] = 1
    juego[87][87] = 1
    juego[86][86] = 1
    juego[86][85] = 1
    juego[85][87] = 1
    juego[85][88] = 1
    juego[85][89] = 1
    juego[86][89] = 1
    juego[86][90] = 1

    # forma
    juego[86][66] = 1
    juego[87][65] = 1
    juego[88][64] = 1
    juego[87][63] = 1
    juego[86][62] = 1
    juego[85][61] = 1
    juego[84][60] = 1
    juego[83][59] = 1
    juego[82][60] = 1
    juego[81][61] = 1
    juego[82][62] = 1
    juego[83][63] = 1
    juego[84][64] = 1
    juego[85][65] = 1

    # creo un bucle
    run = True
    pausar = False
    vel = .3
    while run:
        time.sleep(vel)
        # creo una nueva matriz a partir de la matriz juego
        actualizo_juego = []
        for i in juego:
            actualizo_juego.append(list(i))
        pantalla.fill(Gris)
        # agrego una condicion si se cumple salgo del bucle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausar = not pausar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    Intro()
                    run = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    vel += .1
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if vel > 0.1:
                        vel -= .1
        # hago un ciclo que recorra la matriz y compruebe cuantas celulas vivas hay alrededor de cada celula
        for y in range(numero_de_celdas):
            for x in range(numero_de_celdas):
                if pausar:
                    celulas_vecinas = juego[(x - 1) % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[x % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[(x - 1) % numero_de_celdas][y % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][y % numero_de_celdas] \
                                      + juego[(x - 1) % numero_de_celdas][(y + 1) % numero_de_celdas] \
                                      + juego[x % numero_de_celdas][(y + 1) % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][(y + 1) % numero_de_celdas]
                    # reglas del juego
                    # Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación")
                    if juego[x][y] == 1 and (celulas_vecinas < 2 or celulas_vecinas > 3):
                        actualizo_juego[x][y] = 0
                    # 1 si una celula esta muerta y tiene 3 vecinas vivas la celula nace
                    elif juego[x][y] == 0 and celulas_vecinas == 3:
                        actualizo_juego[x][y] = 1

                # creo una lista especificando sus coordenadas x & y de las celulas para posteriormente ser pintadas
                celda = [(x * d_celdas, y * d_celdas), ((x + 1) * d_celdas, y * d_celdas),
                         ((x + 1) * d_celdas, (y + 1) * d_celdas), (x * d_celdas, (y + 1) * d_celdas)]

                # pinto la celdas
                if actualizo_juego[x][y] == 0:
                    pygame.draw.polygon(pantalla, Negro, celda, 1)
                else:
                    pygame.draw.polygon(pantalla, Azul, celda, 0)

        # actualizo el estado del juego
        juego = []
        for i in actualizo_juego:
            juego.append(list(i))
        pygame.display.flip()


def juego_con_jugador():
    # pinto la pantalla
    pantalla.fill(Gris)

    # especifico el numero n*n celdas que quiero en mi programa
    numero_de_celdas = 40

    # asigno el tamaño de cada celda
    d_celdas = t_ventana / numero_de_celdas

    # creo una matriz de ceros por comprension de tamaño nxn
    juego = [[0 for i in range(numero_de_celdas)] for j in range(numero_de_celdas)]

    # creo un bucle
    run = True
    pausar = False
    vel = .5
    while run:
        time.sleep(vel)
        # creo una nueva matriz a partir de la matriz juego
        actualizo_juego = []
        for i in juego:
            actualizo_juego.append(list(i))
        pantalla.fill(Gris)
        # agrego una condicion si se cumple salgo del bucle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausar = not pausar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    Intro()
                    run = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    vel += .1
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if vel > 0.1:
                        vel -= .1
            mouse = pygame.mouse.get_pressed()
            if mouse[0] or mouse[1] or mouse[2] == 1:
                posx, posy = pygame.mouse.get_pos()
                celposx, celposy = int(floor(posx / d_celdas)), int(floor(posy / d_celdas))
                juego[celposx][celposy] = 1
        # creo una nueva matriz a partir de la matriz juego
        actualizo_juego = []
        for i in juego:
            actualizo_juego.append(list(i))
        pantalla.fill(Gris)
        # hago un ciclo que recorra la matriz y compruebe cuantas celulas vivas hay alrededor de cada celula
        for y in range(numero_de_celdas):
            for x in range(numero_de_celdas):
                if pausar:
                    celulas_vecinas = juego[(x - 1) % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[x % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][(y - 1) % numero_de_celdas] \
                                      + juego[(x - 1) % numero_de_celdas][y % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][y % numero_de_celdas] \
                                      + juego[(x - 1) % numero_de_celdas][(y + 1) % numero_de_celdas] \
                                      + juego[x % numero_de_celdas][(y + 1) % numero_de_celdas] \
                                      + juego[(x + 1) % numero_de_celdas][(y + 1) % numero_de_celdas]
                    # reglas del juego
                    # Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación")
                    if juego[x][y] == 1 and (celulas_vecinas < 2 or celulas_vecinas > 3):
                        actualizo_juego[x][y] = 0
                    # 1 si una celula esta muerta y tiene 3 vecinas vivas la celula nace
                    elif juego[x][y] == 0 and celulas_vecinas == 3:
                        actualizo_juego[x][y] = 1

                # creo una lista especificando sus coordenadas x & y de las celulas para posteriormente ser pintadas
                celda = [(x * d_celdas, y * d_celdas), ((x + 1) * d_celdas, y * d_celdas),
                         ((x + 1) * d_celdas, (y + 1) * d_celdas), (x * d_celdas, (y + 1) * d_celdas)]

                # pinto la celdas
                if actualizo_juego[x][y] == 0:
                    pygame.draw.polygon(pantalla, Negro, celda, 1)
                else:
                    pygame.draw.polygon(pantalla, Azul, celda, 0)

        # actualizo el estado del juego
        juego = []
        for i in actualizo_juego:
            juego.append(list(i))
        pygame.display.flip()

Intro()
