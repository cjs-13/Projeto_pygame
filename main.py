import pygame
from sys import exit

# Constantes
LARGURA = 750
ALTURA = 750
FPS = 60
BRANCO = (255, 255, 255)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))

def main():
    relogio = pygame.time.Clock()
    while True:
        tela.fill(BRANCO)
        relogio.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()

main()