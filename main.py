import pygame
import random
import os
from sys import exit

LARGURA = 750
ALTURA = 500
FPS = 60
BRANCO = (255, 255, 255)
RELOGIO = pygame.time.Clock()


pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA))

# Carregando imagens
NAVE_PRINCIPAL = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_ship.png")).convert_alpha(), (100, 90))
LASER_PRINCIPAL = pygame.image.load(os.path.join("assets", "laser_principal.png")).convert_alpha()
NAVES_INIMIGAS = list()
for i in range(1, 4):
    NAVES_INIMIGAS.append(pygame.image.load(os.path.join("assets", f"enemy_ship ({i}).png")).convert_alpha())
LASER_RED = pygame.image.load(os.path.join("assets", "laser_red.png")).convert_alpha()
LASER_BLUE = pygame.image.load(os.path.join("assets", "laser_blue.png")).convert_alpha()
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG.png")).convert(), (LARGURA, ALTURA))
BG_MENU = list()
for i in range(1, 6):
    BG_MENU.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"BG_menu ({i}).png")).convert(), (LARGURA, ALTURA)))
ICONE = pygame.image.load(os.path.join("assets", "space_ship.png"))
LOGO = pygame.transform.scale(pygame.image.load(os.path.join("assets", "titulo.png")), (400, 400))

pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(ICONE)

# Classes
class Laser():
    def __init__(self, x, y, img, nave):
        self.x = x
        self.y = y
        self.img = img
        self.mascara = pygame.mask.from_surface(self.img)
        self.nave = nave

    def draw(self, tela):
        tela.blit(self.img, (self.x + self.nave.largura()//2 - (self.img.get_width()//2), self.y))

    def mover(self, vel):
        self.y += vel

    def fora_tela(self, altura):
        return self.y <= 0 or self.y >= altura

    def colisao(self, obj, validar):
        return testa_colisao(self, obj, validar)

    def largura(self):
        return self.img.get_width()

    def altura(self):
        return self.img.get_height()

class Nave():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nave_img = None
        self.laser_img = None
        self.tipo = None
        self.lasers = list()
        self.firerate = 15
        self.cool_down_counter = self.firerate
        self.scattershot = False

    def draw(self, tela):
        tela.blit(self.nave_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(tela)

    def atirar(self, nave):
        if self.cool_down_counter == 0:
            self.cool_down_counter = self.firerate
            laser = Laser(self.x, self.y, self.laser_img, nave)
            self.lasers.append(laser)

        self.cool_down_counter -= 1

    def firerateup(self):
        if self.firerate >= 2:
            self.firerate -= 1
    def fireratedown(self):
        self.firerate += 1

    def scattershotttogle(self):
        if self.scattershot == True:
            self.scattershot = False
        else:
            self.scattershot = True

    def largura(self):
        return self.nave_img.get_width()

    def altura(self):
        return self.nave_img.get_height()

class Jogador(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nave_img = NAVE_PRINCIPAL
        self.laser_img = LASER_PRINCIPAL
        self.mascara = pygame.mask.from_surface(self.nave_img)
        self.tipo = "Jogador"

    def mover_laser(self, vel, objs):
        for laser in self.lasers:
            laser.mover(vel)
            if laser.fora_tela(ALTURA):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.colisao(obj, True):
                        #objs.remove(obj)
                        self.lasers.remove(laser)

class Inimigo(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nave_img = NAVES_INIMIGAS[2]
        self.laser_img = LASER_RED
        self.mascara = pygame.mask.from_surface(self.nave_img)
        self.tipo = "Inimigo"
        self.firerate = 45
    def mover_laser(self, vel, obj):
        for laser in self.lasers:
            laser.mover(vel)
            if laser.fora_tela(ALTURA):
                self.lasers.remove(laser)
            elif laser.colisao(obj, False):
                self.lasers.remove(laser)

def testa_colisao(obj1, obj2, validar):
    if validar:
        diff_x = obj2.x - obj1.x - (obj2.largura()//2) + ((obj1.largura() * 3)//2)
        diff_y = obj2.y - obj1.y
    else:
        diff_x = obj2.x - obj1.x - (obj2.largura()//2) - (obj1.largura()//2)
        diff_y = obj2.y - obj1.y
    return obj1.mascara.overlap(obj2.mascara, (diff_x, diff_y)) != None

def main():
    jogando = True
    jogador_vel = 5
    lasers_vel = 7
    jogador = Jogador(300, ALTURA - 100)
    inimigo = Inimigo(random.randint(0,LARGURA),random.randint(0,ALTURA))
    inimigos = list()
    inimigos.append(inimigo)
    while jogando:
        RELOGIO.tick(FPS)
        TELA.blit(BG, (0, 0))
        jogador.draw(TELA)

        for nave in inimigos:
            nave.draw(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jogando = False
                    pygame.quit()
                    exit()
                if event.key == pygame.K_u:
                    inimigo = Inimigo(random.randint(0, LARGURA - inimigo.largura()), random.randint(0, ALTURA - inimigo.altura()))
                    inimigo.firerate = random.randint(1,60)
                    inimigos.append(inimigo)

                if event.key == pygame.K_l:
                    jogador.firerateup()

                if event.key == pygame.K_k:
                    jogador.fireratedown()

                if event.key == pygame.K_i:
                     jogador.scattershotttogle()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and jogador.x - jogador_vel > 0:
            jogador.x -= jogador_vel
        if keys[pygame.K_d] and jogador.x + jogador_vel + jogador.largura() < LARGURA:
            jogador.x += jogador_vel
        if keys[pygame.K_w] and jogador.y - jogador_vel > 0:
            jogador.y -= jogador_vel
        if keys[pygame.K_s] and jogador.y + jogador_vel + jogador.altura() < ALTURA:
            jogador.y += jogador_vel
        if keys[pygame.K_SPACE]:
            jogador.atirar(jogador)

        jogador.mover_laser(-lasers_vel, inimigos)
        for nave in inimigos:
            nave.atirar(nave)
            nave.mover_laser(lasers_vel, jogador)
        pygame.display.flip()

def menu_principal():
    inicio = False
    timer = 0
    indice = 0
    while True:
        RELOGIO.tick(FPS)
        TELA.blit(BG_MENU[indice], (0, 0))
        TELA.blit(LOGO, (180, 100))

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
        pygame.display.flip()

menu_principal()