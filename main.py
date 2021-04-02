import pygame
import os
from sys import exit

LARGURA = 750
ALTURA = 750
FPS = 60
BRANCO = (255, 255, 255)

pygame.init()

# Carregando imagens
ICONE = pygame.image.load(os.path.join("assets", "space_ship.png"))
NAVE_PRINCIPAL = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_ship.png")), (100, 90))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG (4).png")), (LARGURA, ALTURA))

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(ICONE)

# Classes
class Nave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nave_img = None
        self.laser_img = None
        self.lasers = list()
        self.cool_down_counter = 0

    def draw(self, tela):
        tela.blit(self.nave_img, (self.x, self.y))

    def largura(self):
        return self.nave_img.get_width()

    def altura(self):
        return self.nave_img.get_height()

class Jogador(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nave_img = NAVE_PRINCIPAL
        self.laser_img = None
        self.mascara = pygame.mask.from_surface(self.nave_img)


def main():
    jogando = True
    relogio = pygame.time.Clock()
    jogador_vel = 5
    jogador = Jogador(300, 650)
    while jogando:
        relogio.tick(FPS)
        tela.blit(BG, (0, 0))
        jogador.draw(tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and jogador.x - jogador_vel > 0:
            jogador.x -= jogador_vel
        if keys[pygame.K_d] and jogador.x + jogador_vel + jogador.largura() < LARGURA:
            jogador.x += jogador_vel
        if keys[pygame.K_w] and jogador.y - jogador_vel > 0:
            jogador.y -= jogador_vel
        if keys[pygame.K_s] and jogador.y + jogador_vel + jogador.altura() < ALTURA:
            jogador.y += jogador_vel

        pygame.display.flip()

main()