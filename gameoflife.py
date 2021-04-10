# importo la libreria pygame
import pygame

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
        textos('presiona "C" para modo automatico', Blanco, -60, tamanho="pequenha")
        pygame.display.update()
        # agrego una condicion si se cumple salgo del bucle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            teclado = pygame.key.get_pressed()
            if teclado[pygame.K_c]:
                juego_de_la_vida()


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
    juego[49][49] = 1
    juego[50][49] = 1
    juego[50][50] = 1
    juego[50][51] = 1
    juego[51][50] = 1

    # creo un bucle
    run = True
    while run:
        # agrego una condicion si se cumple salgo del bucle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
        # creo una nueva matriz a partir de la matriz juego
        actualizo_juego = []
        for i in juego:
            actualizo_juego.append(list(i))
        pantalla.fill(Gris)
        # hago un ciclo que recorra la matriz y compruebe cuantas celulas vivas hay alrededor de cada celula
        for y in range(numero_de_celdas):
            for x in range(numero_de_celdas):
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
