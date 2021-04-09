import pygame

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

fondo = 25, 25, 25
screen.fill(fondo)

numero_de_celdas = 100

dimw = width / numero_de_celdas
dimch = height / numero_de_celdas

gamestate = [[0 for i in range(numero_de_celdas)] for j in range(numero_de_celdas)]

# automata palo
'''gamestate[10][2] = 1
gamestate[11][2] = 1
gamestate[12][2] = 1

gamestate[1][1] = 1
gamestate[2][2] = 1
gamestate[2][3] = 1
gamestate[1][3] = 1
gamestate[0][3] = 1'''

gamestate[49][49] = 1
gamestate[50][49] = 1
gamestate[50][50] = 1
gamestate[50][51] = 1
gamestate[51][50] = 1


run = True

while run:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False
    newgamestate = []
    for i in gamestate:
        newgamestate.append(list(i))
    screen.fill(fondo)

    for y in range(0, numero_de_celdas):
        for x in range(0, numero_de_celdas):
            n_neigh = gamestate[(x - 1) % numero_de_celdas][(y - 1) % numero_de_celdas] + \
                      gamestate[x % numero_de_celdas][(y - 1) % numero_de_celdas] + \
                      gamestate[(x + 1) % numero_de_celdas][(y - 1) % numero_de_celdas] + \
                      gamestate[(x - 1) % numero_de_celdas][y % numero_de_celdas] + \
                      gamestate[(x + 1) % numero_de_celdas][y % numero_de_celdas] + \
                      gamestate[(x - 1) % numero_de_celdas][(y + 1) % numero_de_celdas] + \
                      gamestate[x % numero_de_celdas][(y + 1) % numero_de_celdas] + \
                      gamestate[(x + 1) % numero_de_celdas][(y + 1) % numero_de_celdas]

            if gamestate[x][y] == 0 and n_neigh == 3:
                newgamestate[x][y] = 1

            elif gamestate[x][y] == 1 and (n_neigh < 2 or n_neigh > 3):
                newgamestate[x][y] = 0

            poly = [(x * dimch, y * dimch), ((x + 1) * dimch, y * dimch),
                    ((x + 1) * dimch, (y + 1) * dimch), (x * dimch, (y + 1) * dimch)]

            if newgamestate[x][y] == 0:
                pygame.draw.polygon(screen, (0, 0, 0), poly, 1)
            else:
                pygame.draw.polygon(screen, (0, 0, 255), poly, 0)
    gamestate = []
    for i in newgamestate:
        gamestate.append(list(i))
    pygame.display.flip()
