import pygame
import random
import os
from sys import exit

LARGURA = 550
ALTURA = 550
FPS = 60
BRANCO = (255, 255, 255)
RELOGIO = pygame.time.Clock()
UP_SCALE_TITULO = 3
UP_SCALE_MENU = 2
SCALE_NAVE = (100, 90)
SCALE_BOSS = (350, 280)

pygame.init()
pygame.font.init()
FONT_PRINCIPAL = pygame.font.SysFont("Letter Gothic", 35)
TELA = pygame.display.set_mode((LARGURA, ALTURA + 40))

# Carregando imagens
NAVE_PRINCIPAL = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_ship.png")).convert_alpha(), SCALE_NAVE)
LASER_PRINCIPAL = pygame.image.load(os.path.join("assets", "laser_principal.png")).convert_alpha()
NAVES_INIMIGAS = list()
for i in range(1, 4):
    NAVES_INIMIGAS.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"enemy_ship ({i}).png")).convert_alpha(), SCALE_NAVE))
for i in range(1, 2):
    NAVES_INIMIGAS.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"boss_ship ({i}).png")).convert_alpha(), SCALE_BOSS))
LASER_RED = pygame.image.load(os.path.join("assets", "laser_red.png")).convert_alpha()
LASER_BLUE = pygame.image.load(os.path.join("assets", "laser_blue.png")).convert_alpha()
HP = list()
HP.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "hp (1).png")), (297, 10)))
HP.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "hp (2).png")), (280, 5)))
BARRA_INF = pygame.transform.scale(pygame.image.load(os.path.join("assets", "barra.png")), (LARGURA, 40))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG.png")).convert(), (LARGURA, ALTURA + 40))
ICONE = pygame.image.load(os.path.join("assets", "space_ship.png"))
LOGO = pygame.transform.scale(pygame.image.load(os.path.join("assets", "titulo.png")), (138 * UP_SCALE_TITULO, 46 * UP_SCALE_TITULO))
MENU_OP = list()
for i in range(1, 4):
    MENU_OP.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"menu ({i}).png")), (146 * UP_SCALE_MENU, 23 * UP_SCALE_MENU)))

# Imagens da tela inicial
BG_INICIO = pygame.image.load(os.path.join("assets", "fundo.png"))
B_INICIAR = pygame.image.load(os.path.join("assets", "iniciar.png"))
B_AJUDA = pygame.image.load(os.path.join("assets", "ajuda.png"))
B_SAIR = pygame.image.load(os.path.join("assets", "sair.png"))

# Imagens da tela de ajuda
BG_AJUDA = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG_ajuda.png")).convert(), (LARGURA, ALTURA + 40))
B_VOLTAR = pygame.image.load(os.path.join("assets", "voltar.png"))
# B_AJUDA = pygame.image.load(os.path.join("assets", "ajuda.png"))


pygame.display.set_caption("__Invasores do Espaço__")
pygame.display.set_icon(ICONE)


# Classes
class Laser():
    def __init__(self, x, y, img, nave, arma):
        self.x = x
        self.y = y
        self.img = img
        self.mascara = pygame.mask.from_surface(self.img)
        self.nave = nave
        self.damagetype = nave.layer
        self.vel_x = nave.laservel_x[arma]
        self.vel_y = nave.laservel_y[arma]
        self.hp = nave.laserhp[arma]
        self.arma = arma

    def drawinterno(self, tela):
        tela.blit(self.img, (int(self.x) + self.nave.arma_x[self.arma], int(self.y) + self.nave.arma_y[self.arma]))

    def fora_tela(self,):
        return self.y <= 0 or self.y >= ALTURA

    def colisao(self, obj):
        return testa_colisao(self, obj, self.nave)

    def largura(self):
        return self.img.get_width()

    def altura(self):
        return self.img.get_height()

    def moverlaserinterno(self, lasers):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.fora_tela():
            lasers.remove(self)

    def colisaointerno(self, naves,lasers):
        for nave in naves:
            if nave.layer != self.damagetype and self.colisao(nave):
                self.hp -= 1
                if nave.imunity_timer == 0:
                    nave.hp -= 1
                    nave.imunity_timer = 5

    def testevida(self, lasers):
        if self.hp < 1:
            lasers.remove(self)


class Nave():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nave_img = None
        self.laser_img = None
        self.tipo = None
        self.lasers = list()
        self.firerate = [15, 15, 15, 15, 15]
        self.cool_down_counter = [0, 0, 0, 0, 0]
        self.layer = 2
        self.imunity_timer = 0
        self.hp = 1
        self.max_hp = 1
        self.lives = 1
        self.ai = 0
        self.aihelper = 0
        self.laservel_x = [0, 0, 0, 0, 0]
        self.laservel_y = [0, 0, 0, 0, 0]
        self.laserhp = [0, 0, 0, 0, 0]
        self.arma_x = [0, 0, 0, 0, 0]
        self.arma_y = [0, 0, 0, 0, 0]

    def draw(self, tela):
        tela.blit(self.nave_img, (int(self.x), int(self.y)))

    def atirarinterno(self, arma, lasers):
        if self.cool_down_counter[arma] < 1:
            self.cool_down_counter[arma] = self.firerate[arma]
            laser = Laser(self.x, self.y, self.laser_img, self, arma)
            lasers.append(laser)

    def reduzirtimers(self):
        arma = 0
        while arma < 5:
            if self.cool_down_counter[arma] > 0:
                self.cool_down_counter[arma] -= 1
            arma += 1

        if self.imunity_timer > 0:
            self.imunity_timer -= 1

    def firerateup(self):
        if self.firerate[0] >= 2:
            self.firerate[0] -= 1

    def fireratedown(self):
        self.firerate[0] += 1

    def largura(self):
        return self.nave_img.get_width()

    def altura(self):
        return self.nave_img.get_height()

    def testevida(self, naves):
        if self.hp < 1 and self.lives < 2:
            naves.remove(self)
        elif self.hp < 1 and self.lives > 1:
            self.lives -= 1
            self.hp = self.max_hp
            self.imunity_timer = 180

    def testeai(self, lasers):
        if self.ai == 0:
            self.ai0_inimigo(lasers)
        elif self.ai == 1:
            self.ai1_inimigo(lasers)
        elif self.ai == 2:
            self.ai2_inimigo(lasers)

    def ai0_inimigo(self, lasers):
        self.y += 1
        self.atirarinterno(0, lasers)
        if self.fora_tela(ALTURA):
            self.hp = 0

    def ai1_inimigo(self, lasers):
        if self.y < 80:
            self.y += 2
        if self.aihelper == 0:
            self.x += 3
        elif self.aihelper == 1:
            self.x -= 3
        self.atirarinterno(0, lasers)
        if self.x < 5:
            self.aihelper = 0
        elif self.x > ALTURA - 100:
            self.aihelper = 1

    def ai2_inimigo(self, lasers):
        if self.y < 20:
            self.y += 2
        if self.cool_down_counter[1] == 0 and self.cool_down_counter[1] == 0:
            self.atirarinterno(1, lasers)
            self.atirarinterno(2, lasers)
        if self.fora_tela(ALTURA):
            self.hp = 0


class Jogador(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nave_img = NAVE_PRINCIPAL
        self.laser_img = LASER_PRINCIPAL
        self.hp_img = HP
        self.mascara = pygame.mask.from_surface(self.nave_img)
        self.tipo = "Jogador"
        self.pontos = 0
        self.layer = 1
        self.damagetype = 1
        self.hp = 10
        self.max_hp = 10
        self.lives = 3
        self.ai = -1
        self.firerate[0] = 15
        self.laserhp[0] = 1
        self.laservel_x[0] = 0
        self.laservel_y[0] = -7
        self.arma_x[0] = 45
        self.arma_y[0] = 0

    def draw_hp(self, tela):
        tela.blit(self.hp_img[0], (50, ALTURA + 15))
        tela.blit(pygame.transform.scale(self.hp_img[1], (28 * self.hp, 5)), (59, ALTURA + 18))

class Inimigo(Nave):
    def __init__(self, x, y, ai):
        super().__init__(x, y)
        self.nave_img = NAVES_INIMIGAS[ai]
        self.laser_img = LASER_RED
        self.mascara = pygame.mask.from_surface(self.nave_img)
        self.tipo = "Inimigo"
        self.layer = 2
        self.damagetype = 2
        self.ai = ai
        self.firerate[0] = 45
        self.firerate[1] = 30
        self.firerate[2] = 30
        self.cool_down_counter[2] = 60
        self.laserhp[0] = 1
        self.laserhp[1] = 1
        self.laserhp[2] = 1
        self.laservel_x[0] = 0
        self.laservel_x[1] = 0
        self.laservel_x[2] = 0
        self.laservel_y[0] = 7
        self.laservel_y[1] = 7
        self.laservel_y[2] = 7
        self.arma_x[0] = 45
        self.arma_x[1] = 30
        self.arma_x[2] = 60
        self.arma_y[0] = self.altura() - 30
        self.arma_y[1] = self.altura() - 30
        self.arma_y[2] = self.altura() - 30

    def fora_tela(self, altura):
        return self.y >= altura


class Boss(Nave):
    def __init__(self, x, y, ai):
        super().__init__(x, y)
        self.nave_img = NAVES_INIMIGAS[3]
        self.laser_img = LASER_BLUE
        self.mascara = pygame.mask.from_surface(self.nave_img)
        self.tipo = "Boss"
        self.firerate = 60
        self.layer = 2
        self.damagetype = 2
        self.ai = ai
        self.laserhp[0] = 1
        self.laserhp[1] = 1
        self.laserhp[2] = 1
        self.laserhp[3] = 1
        self.laservel_x[0] = 0
        self.laservel_x[1] = 0
        self.laservel_x[2] = 0
        self.laservel_x[3] = 0
        self.laservel_y[0] = 7
        self.laservel_y[1] = 7
        self.laservel_y[2] = 7
        self.laservel_y[3] = 7
        self.hp = 100
        self.arma_x[0] = self.x + 40
        self.arma_x[1] = self.x + 40
        self.arma_x[2] = self.x + 40
        self.arma_x[3] = self.x + 40
        self.arma_y[0] = self.y - 80
        self.arma_y[1] = self.y - 80
        self.arma_y[2] = self.y - 80
        self.arma_y[3] = self.y - 80


# obj1 == Laser, obj2 == Nave atingida, obj3 == Nave que disparou
def testa_colisao(obj1, obj2, obj3):
    diff_x = 0
    diff_y = 0
    if obj3.tipo == "Jogador" or obj3.tipo == "Inimigo":
        diff_x = int(obj2.x - obj1.x - int(obj3.largura()/2) + (obj1.largura()/2))
        diff_y = int(obj2.y - obj1.y)
        if obj3.tipo == "Inimigo":
            diff_y = int(diff_y - obj2.altura() + obj1.altura())
    elif obj3.tipo == "Boss":
        diff_x = int(obj2.x - obj1.x - obj2.largura() + obj1.largura())
        diff_y = int(obj2.y - obj1.y + obj1.altura())
    return obj1.mascara.overlap(obj2.mascara, (diff_x, diff_y)) != None


def main():
    jogando = True
    jogador_vel = 5
    inimigos_vel = 1
    naves = list()
    jogador = Jogador(LARGURA//2 - NAVE_PRINCIPAL.get_width()/2, ALTURA - 100)
    naves.append(jogador)
    lasers = list()
    hp_label = FONT_PRINCIPAL.render("HP:", True, BRANCO)

    while jogando:
        RELOGIO.tick(FPS)
        TELA.blit(BG, (0, 0))

        #Spawn aleatório de inimigos
        if len(naves) < 5:
            inimigotempo = Inimigo(random.randint(0, 450), 0, random.randint(0, 2))
            naves.append(inimigotempo)

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
                    inimigotempo = Inimigo(random.randint(100, 450), 0, random.randint(0, 2))
                    naves.append(inimigotempo)

                if event.key == pygame.K_l:
                    jogador.firerateup()

                if event.key == pygame.K_k:
                    jogador.fireratedown()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and jogador.x - jogador_vel > 0:
            jogador.x -= jogador_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and jogador.x + jogador_vel + jogador.largura() < LARGURA:
            jogador.x += jogador_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and jogador.y - jogador_vel > 0:
            jogador.y -= jogador_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and jogador.y + jogador_vel + jogador.altura() < ALTURA:
            jogador.y += jogador_vel
        if keys[pygame.K_SPACE]:
            jogador.atirarinterno(0, lasers)

        for laser in lasers:
            laser.moverlaserinterno(lasers)
            laser.colisaointerno(naves, lasers)
            laser.testevida(lasers)
            laser.drawinterno(TELA)
        for nave in naves:
            nave.reduzirtimers()
            nave.testevida(naves)
            nave.testeai(lasers)
            nave.draw(TELA)

        TELA.blit(BARRA_INF, (0, ALTURA))
        jogador.draw_hp(TELA)
        TELA.blit(hp_label, (7, ALTURA + 7))

        pygame.display.flip()


def menu_principal():
    B_INICIAR_largura = B_INICIAR.get_width()
    # B_INICIAR_altura = B_INICIAR.get_height()
    largura_geral = LARGURA//2 - B_INICIAR_largura//2

    altura_iniciar = ALTURA
    altura_ajuda = ALTURA
    altura_sair = ALTURA
 
    while True:
        RELOGIO.tick(FPS)
        TELA.blit(BG_INICIO, (0, 0))

        # Animação na TELA inicial
        if altura_iniciar > ALTURA//3:
            altura_iniciar -= 4
        if altura_ajuda > ALTURA//2:
            altura_ajuda -= 3
        if altura_sair > ALTURA//1.5:
            altura_sair -= 2

        TELA.blit(B_INICIAR, (largura_geral, altura_iniciar))
        TELA.blit(B_AJUDA, (largura_geral, altura_ajuda))
        TELA.blit(B_SAIR, (largura_geral, altura_sair))
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Monitora clique do mouse
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if 123 < x < 414 and 220 < y < 255:
                    # print("Botão iniciar apertado")
                    main()
                if 123 < x < 414 and 313 < y < 349:
                    # print("Botão ajuda apertado")
                    ajuda()
                if 123 < x < 414 and 405 < y < 436:
                    # print("Botão sair apertado")
                    pygame.quit()
                    exit()

        pygame.display.flip()


def ajuda():
    B_VOLTAR_largura = B_VOLTAR.get_width()
    # B_VOLTAR_altura = B_VOLTAR.get_height()
    largura = LARGURA//2 - B_VOLTAR_largura//2
    altura_voltar = ALTURA
    
    while True:
        RELOGIO.tick(FPS)
        TELA.blit(BG_AJUDA, (0, 0))

        if altura_voltar > ALTURA//1.15:
            altura_voltar -= 4

        TELA.blit(B_VOLTAR, (largura, altura_voltar))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Monitora clique do mouse
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                if 123 < x < 414 and 515 < y < 552:
                    menu_principal()

        pygame.display.flip()


menu_principal()
