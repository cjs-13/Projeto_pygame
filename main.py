import pygame
import os
from sys import exit

LARGURA = 750
ALTURA = 750
FPS = 60
BRANCO = (255, 255, 255)
RELOGIO = pygame.time.Clock()

pygame.init()

# Carregando imagens
ICONE = pygame.image.load(os.path.join("assets", "space_ship.png"))
NAVE_PRINCIPAL = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_ship.png")), (100, 90))
LASERS_PRINCIPAL = pygame.image.load(os.path.join("assets", "laser_principal.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG (4).png")), (LARGURA, ALTURA))
BG_menu = list()
for i in range(1, 6):
    BG_menu.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"BG_menu ({i}).png")), (LARGURA, ALTURA)))

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(ICONE)

# Classes
class Laser:
    def __init__(self, x, y, img, nave):
        self.x = x
        self.y = y
        self.img = img
        self.mascara = pygame.mask.from_surface(self.img)
        self.nave = nave

    def draw(self, tela):
        tela.blit(self.img, (self.x + self.nave.largura()/2 - 5, self.y))

    def mover(self, vel):
        self.y += vel

    def fora_tela(self, altura):
        return self.y <= 0 or self.y >= altura

    def colisao(self, obj):
        return testa_colisao(self, obj)

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
        for laser in self.lasers:
            laser.draw(tela)

    def atirar(self, nave):
        laser = Laser(self.x, self.y, self.laser_img, nave)
        self.lasers.append(laser)

    def mover_laser(self, vel, obj):
        for laser in self.lasers:
            laser.move(vel)
            if laser.fora_tela(ALTURA):
                self.lasers.remove(laser)
            elif laser.colisao(obj):
                self.lasers.remove(laser)

    def largura(self):
        return self.nave_img.get_width()

    def altura(self):
        return self.nave_img.get_height()


class Jogador(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nave_img = NAVE_PRINCIPAL
        self.laser_img = LASERS_PRINCIPAL
        self.mascara = pygame.mask.from_surface(self.nave_img)

    def mover_laser(self, vel, objs):
        for laser in self.lasers:
            laser.mover(vel)
            if laser.fora_tela(ALTURA):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.colisao(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

def testa_colisao(obj1, obj2):
    diff_x = obj2.x - obj1.x
    diff_y = obj2.y - obj1.y
    return obj1.mascara.overlap(obj2.mascara, (diff_x, diff_y)) != None

def main():
    jogando = True
    jogador_vel = 5
    lasers_vel = 5
    jogador = Jogador(300, 650)
    inimigos = list()
    while jogando:
        RELOGIO.tick(FPS)
        tela.blit(BG, (0, 0))
        jogador.draw(tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jogador.atirar(jogador)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and jogador.x - jogador_vel > 0:
            jogador.x -= jogador_vel
        if keys[pygame.K_d] and jogador.x + jogador_vel + jogador.largura() < LARGURA:
            jogador.x += jogador_vel
        if keys[pygame.K_w] and jogador.y - jogador_vel > 0:
            jogador.y -= jogador_vel
        if keys[pygame.K_s] and jogador.y + jogador_vel + jogador.altura() < ALTURA:
            jogador.y += jogador_vel

        jogador.mover_laser(-lasers_vel, inimigos)

        pygame.display.flip()

def menu_principal():
    inicio = False
    timer = 0
    indice = 0
    while True:
        RELOGIO.tick(FPS)
        tela.blit(BG_menu[indice], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                inicio = True

        if inicio:
            if timer < 10:
                timer += 1
            else:
                indice += 1
                timer = 0
            if indice > 4:
                main()
                inicio = False

        pygame.display.flip()

menu_principal()
