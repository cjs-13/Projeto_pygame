import pygame as pg
import random
import os
from sys import exit

LARGURA = 550
ALTURA = 550
FPS = 60
BRANCO = (255, 255, 255)
SCALE_NAVE = (100, 90)
SCALE_BOSS = (350, 280)
SCALE_LABEL_HP = (297, 10)

pg.init()
pg.font.init()
FONT_PRINCIPAL = pg.font.SysFont("Letter Gothic", 35)
TELA = pg.display.set_mode((LARGURA, ALTURA + 40))
RELOGIO = pg.time.Clock()

# FUNÇÕES PARA TORNAR O CÓDIGO MENOS VERBOSO


def load_img(caminho, nome_imagem):
    return pg.image.load(os.path.join(caminho, nome_imagem))


def ch_scale(imagem, escala):
    return pg.transform.scale(imagem, escala)

dir = "assets"

# CARREGANDO IMAGENS

# Tela inicial e Menu Principal


TEXTO = load_img(dir, "nome.png").convert_alpha()
BG_INICIO = load_img(dir, "fundo.png")
B_INICIAR = load_img(dir, "iniciar.png")
B_AJUDA = load_img(dir, "ajuda.png")
B_SAIR = load_img(dir, "sair.png")

# Tela de ajuda
BG_AJUDA = ch_scale(load_img(dir, "BG_ajuda.png").convert(), (LARGURA, ALTURA + 40))
B_VOLTAR = load_img(dir, "voltar.png")

# Telas das fases do jogo
NAVE_PRINCIPAL = ch_scale(load_img(dir, "space_ship.png").convert_alpha(), SCALE_NAVE)
LASER_PRINCIPAL = load_img(dir, "laser_principal.png").convert_alpha()
NAVES_INIMIGAS = list()
for i in range(1, 5):
    NAVES_INIMIGAS.append(ch_scale(load_img(dir, f"enemy_ship ({i}).png").convert_alpha(), SCALE_NAVE))
for i in range(1, 2):
    NAVES_INIMIGAS.append(ch_scale(load_img(dir, f"boss_ship ({i}).png").convert_alpha(), SCALE_BOSS))
LASER_RED = load_img(dir, "laser_red.png").convert_alpha()
LASER_BLUE = load_img(dir, "laser_blue.png").convert_alpha()
HP = list()
HP.append(ch_scale(load_img(dir, "hp (1).png"), SCALE_LABEL_HP))
HP.append(ch_scale(load_img(dir, "hp (2).png"), (280, 5)))
BARRA_INF = ch_scale(load_img(dir, "barra.png"), (LARGURA, 40))
BG = ch_scale(load_img(dir, "BG.png").convert(), (LARGURA, ALTURA + 40))

# Icone do Jogo
ICONE = load_img(dir, "space_ship.png")

# ADIÇÃO DE NOME E ICONE À JANELA DO JOGO

pg.display.set_caption("__Invasores do Espaço__")
pg.display.set_icon(ICONE)

# DEFINIÇÃO DAS CLASSES


class Laser():
    def __init__(self, x, y, img, nave, arma):
        self.x = x + nave.arma_x[arma]
        self.y = y + nave.arma_y[arma]
        self.img = img
        self.mascara = pg.mask.from_surface(self.img)
        self.nave = nave
        self.damagetype = nave.layer
        self.vel_x = nave.laservel_x[arma]
        self.vel_y = nave.laservel_y[arma]
        self.hp = nave.laserhp[arma]
        self.arma = arma

    def drawinterno(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))

    def fora_tela(self):
        return (self.y <= 0 or self.y >= ALTURA) or (self.x <= 0 or self.x >= LARGURA)

    def colisao(self, obj):
        return testa_colisao(self, obj)

    def largura(self):
        return self.img.get_width()

    def altura(self):
        return self.img.get_height()

    def moverlaserinterno(self, lasers):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.fora_tela():
            lasers.remove(self)

    def colisaointerno(self, naves, lasers):
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

    def fora_tela(self):
        return self.y <= 0 or self.y >= ALTURA

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
        elif self.ai == 3:
            self.ai3_inimigo(lasers)
        elif self.ai == 4:
            self.ai4_boss(lasers)

    def ai0_inimigo(self, lasers):
        self.y += 1
        self.atirarinterno(0, lasers)
        if self.fora_tela():
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
        if self.cool_down_counter[0] == 0 and self.cool_down_counter[1] == 0:
            self.atirarinterno(1, lasers)
            self.atirarinterno(2, lasers)

    def ai3_inimigo(self, lasers):
        if self.y == 0:
            self.aihelper = random.randint(0, 1)
        if self.x + self.largura() + 3 > LARGURA:
            self.aihelper = 1
        elif self.x - 3 < 0:
            self.aihelper = 0
        self.y += 1
        if self.aihelper == 0:
            self.x += 2
        elif self.aihelper == 1:
            self.x -= 2
        self.atirarinterno(0, lasers)
        if self.fora_tela():
            self.hp = 0

    def ai4_boss(self, lasers):
        if self.x + self.largura() + 0.5 > LARGURA:
            self.aihelper = 1
        elif self.x - 0.5 < 0:
            self.aihelper = 0
        if self.aihelper == 0:
            self.x += 0.5
        elif self.aihelper == 1:
            self.x -= 0.5
        self.atirarinterno(1, lasers)
        self.atirarinterno(2, lasers)
        if self.hp <= 50:
            self.atirarinterno(0, lasers)
            self.atirarinterno(3, lasers)

class Jogador(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nave_img = NAVE_PRINCIPAL
        self.laser_img = LASER_PRINCIPAL
        self.hp_img = HP
        self.mascara = pg.mask.from_surface(self.nave_img)
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

    def colisao(self, naves): # Testa a colisao do player com as naves
        for nave in naves:
            if self.layer != nave.layer and testa_colisao(self, nave):
                nave.hp -= 1
                if self.imunity_timer == 0:
                    self.hp -= 1
                    self.imunity_timer = 5

    def draw_hp(self, tela): # Desenha na tela os status de hp e vida do jogador
        hp_label = FONT_PRINCIPAL.render("HP:", True, BRANCO)
        lives_label = FONT_PRINCIPAL.render(f"Vidas: {self.lives - 1}", True, BRANCO)
        tela.blit(self.hp_img[0], (50, ALTURA + 15))
        tela.blit(ch_scale(self.hp_img[1], (28 * self.hp, 5)), (59, ALTURA + 18))
        TELA.blit(hp_label, (7, ALTURA + 7))
        tela.blit(lives_label, (SCALE_LABEL_HP[0] + 100, ALTURA + 7))

class Inimigo(Nave):
    def __init__(self, x, y, ai):
        super().__init__(x, y)
        self.nave_img = NAVES_INIMIGAS[ai]
        self.laser_img = LASER_RED
        self.mascara = pg.mask.from_surface(self.nave_img)
        self.tipo = "Inimigo"
        self.layer = 2
        self.damagetype = 2
        self.ai = ai
        self.firerate[0] = 45
        self.firerate[1] = 30
        self.firerate[2] = 30
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

class Boss(Nave):
    def __init__(self, x, y, ai):
        super().__init__(x, y)
        self.nave_img = NAVES_INIMIGAS[ai]
        self.laser_img = LASER_BLUE
        self.mascara = pg.mask.from_surface(self.nave_img)
        self.tipo = "Boss"
        self.layer = 2
        self.damagetype = 2
        self.ai = ai
        self.firerate[0] = 90
        self.firerate[1] = 60
        self.firerate[2] = 60
        self.firerate[3] = 90
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
        self.arma_x[0] = self.largura()//2 - 5 - 62
        self.arma_x[1] = self.largura()//2 - 5 - 38
        self.arma_x[2] = self.largura()//2 - 5 + 38
        self.arma_x[3] = self.largura()//2 - 5 + 62
        self.arma_y[0] = self.altura() - 160
        self.arma_y[1] = self.altura() - 90
        self.arma_y[2] = self.altura() - 90
        self.arma_y[3] = self.altura() - 160


class Fase():
    def __init__(self):
        self.fase = 0
        self.wave = 0
        self.counter = -1
        self.counteracive = True
        self.dificuty = 1

    def pular_onda(self):
        self.counter = -1
        self.counteracive = True
        self.wave += 1

    def pular_fase(self):
        self.counter = -1
        self.counter = True
        self.wave = 0
        self.fase += 1

    def criar_inimigo(self, x, y, ai, naves):  # cria um inimigo
        inimigotempo = Inimigo(x, y, ai)
        naves.append(inimigotempo)

    def direcionar_fase(self,naves):  # testa em qual fase esta e roda ela
        if self.fase == 0:
            self.faseid0(naves)

    def sem_inimigos(self, naves):  # olha se tem inimigos e reativa o contador
        if len(naves) < 2:
            self.counteracive = True

    def counter_tick(self):
        if self.counteracive:  # anda o contador se ele estiver ativo
            self.counter += 1

    def wave_id0(self, naves):  # onda de id 0, spawna inimigos e uma formação de / \
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0: # spawna inimigos quando o counter e igual a 0
            self.criar_inimigo(5, 0, 0, naves)
            self.criar_inimigo(450, 0, 0, naves)
        elif self.counter == 120 / self.dificuty:  # spawna inimigos quando o counter e igual a 120 na dificuldade 1
            self.criar_inimigo(65, 0, 0, naves)
            self.criar_inimigo(390, 0, 0, naves)
        elif self.counter == 240 / self.dificuty:  # spawna inimigos quando o counter e igual a 240 na dificuldade 1
            self.criar_inimigo(125, 0, 0, naves)
            self.criar_inimigo(330, 0, 0, naves)
        elif self.counter == 360 / self.dificuty:  # spawna inimigos quando o counter e igual a 360 na dificuldade 1
            self.criar_inimigo(185, 0, 0, naves)
            self.criar_inimigo(270, 0, 0, naves)
        elif self.counter == 480 / self.dificuty:  # termina a onda quando o counter e igual a 480 na dificuldade 1
            self.counter = -1  # reseta o contador
            self.wave += 1  # anda para a proxima onda
            self.counteracive = False  # desativa o contador

    def wave_id1(self, naves):  # onda de id 1, spawna inimigos em formação de ---
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0:  # spawna a linha de inimigos simples
            self.criar_inimigo(5, 0, 0, naves)
            self.criar_inimigo(105, 0, 0, naves)
            self.criar_inimigo(205, 0, 0, naves)
            self.criar_inimigo(250, 0, 0, naves)
            self.criar_inimigo(350, 0, 0, naves)
            self.criar_inimigo(450, 0, 0, naves)
        elif self.counter == 120 / self.dificuty:
            self.counter = -1  # reseta o contador
            self.wave += 1  # anda para a proxima onda
            self.counteracive = False  # desativa o contador

    def faseid0(self, naves):  # a primeira fasedddda

        if self.wave == 0:  # onda 1
            self.wave_id0(naves)

        elif self.wave == 1 and self.counteracive is False:  # testa se ainda tem inimigos antes de avançar as ondas
            self.sem_inimigos(naves)

        elif self.wave == 1:  # onda 2
            self.wave_id1(naves)

        elif self.wave == 2 and self.counteracive is False:
            self.counteracive = True

        elif self.wave == 2:
            self.wave_id1(naves)

        elif self.wave == 3:
            self.pular_fase()

def testa_colisao(obj1, obj2):
    # obj1 == Laser, obj2 == Nave atingida
    diff_x = obj2.x - obj1.x
    diff_y = obj2.y - obj1.y
    return obj1.mascara.overlap(obj2.mascara, (int(diff_x),int(diff_y))) != None

# JANELAS DO JOGO

def main():
    jogando = True
    jogador_vel = 5
    naves = list()
    jogador = Jogador(LARGURA//2 - NAVE_PRINCIPAL.get_width()/2, ALTURA - 100)
    naves.append(jogador)
    lasers = list()
    fase = Fase()

    while jogando:
        RELOGIO.tick(FPS)
        TELA.blit(BG, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                jogando = False
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    jogando = False
                if event.key == pg.K_u:
                    fase.criar_inimigo(random.randint(5,450),0,3, naves)

                if event.key == pg.K_l:
                    jogador.firerateup()

                if event.key == pg.K_k:
                    fase.pular_fase()

        keys = pg.key.get_pressed()
        if (keys[pg.K_a] or keys[pg.K_LEFT]) and jogador.x - jogador_vel > 0:
            jogador.x -= jogador_vel
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and jogador.x + jogador_vel + jogador.largura() < LARGURA:
            jogador.x += jogador_vel
        if (keys[pg.K_w] or keys[pg.K_UP]) and jogador.y - jogador_vel > 0:
            jogador.y -= jogador_vel
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and jogador.y + jogador_vel + jogador.altura() < ALTURA:
            jogador.y += jogador_vel
        if keys[pg.K_SPACE]:
            jogador.atirarinterno(0, lasers)

        jogador.colisao(naves)
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

        fase.direcionar_fase(naves)
        fase.counter_tick()

        pg.display.flip()

def menu_principal():
    # Pegando a largura as imagens usadas na tela
    B_INICIAR_largura = B_INICIAR.get_width()

    # Definindo a coordenada horizontal de início da imagem
    largura_geral = LARGURA//2 - B_INICIAR_largura//2

    # Definindo a coordenada vertical de início da imagem
    altura_iniciar = ALTURA + 100
    altura_ajuda = ALTURA + 100
    altura_sair = ALTURA + 100
 
    while True:
        RELOGIO.tick(FPS)
        TELA.blit(BG_INICIO, (0, 0))

        # Atualizações na posição vertical de cada imagem
        if altura_iniciar > ALTURA//2.5:
            altura_iniciar -= 14
        else:    
            if altura_ajuda > altura_iniciar + (ALTURA//5):
                altura_ajuda -= 14
            else:
                if altura_sair > altura_ajuda + (ALTURA//5):
                    altura_sair -= 14

        # Colocando imagens na tela
        TELA.blit(B_INICIAR, (largura_geral, altura_iniciar))
        TELA.blit(B_AJUDA, (largura_geral, altura_ajuda))
        TELA.blit(B_SAIR, (largura_geral, altura_sair))
       
        # Controle de Eventos de Mouse e Teclado
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x = pg.mouse.get_pos()[0]
                y = pg.mouse.get_pos()[1]
                if 139 < x < 414 and 256 < y < 289:
                    main()
                if 139 < x < 414 and 352 < y < 395:
                    ajuda()
                if 139 < x < 414 and 449 < y < 484:
                    pg.quit()
                    exit()

        pg.display.flip()

def ajuda():
    # Pegando a largura as imagens usadas na tela
    B_VOLTAR_largura = B_VOLTAR.get_width()

    # Definindo a coordenada horizontal de início da imagem
    largura = LARGURA//2 - B_VOLTAR_largura//2

    # Definindo a coordenada vertical de início da imagem
    altura_voltar = ALTURA
    
    ajuda = True
    while ajuda:
        RELOGIO.tick(FPS)
        TELA.blit(BG_AJUDA, (0, 0))

        # Atualizações na posição vertical de cada imagem
        if altura_voltar > ALTURA//1.15:
            altura_voltar -= 4

        # Colocando imagem na tela
        TELA.blit(B_VOLTAR, (largura, altura_voltar))
        
        # Controle de Eventos de Mouse e Teclado
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    ajuda = False
            if event.type == pg.MOUSEBUTTONDOWN:  # Monitora clique do mouse
                x = pg.mouse.get_pos()[0]
                y = pg.mouse.get_pos()[1]               
                if 123 < x < 414 and 515 < y < 552:
                    menu_principal()
        pg.display.flip()

def tela_inicial():
    # Pegando a largura as imagens usadas na tela
    larg_nome = TEXTO.get_width()
    larg_nave_p = NAVE_PRINCIPAL.get_width()
    larg_nave_boss = NAVES_INIMIGAS[4].get_width()

    # Definindo a coordenada horizontal de início de cada imagem
    largura_nome = LARGURA//2 - larg_nome//2
    largura_nave = LARGURA//2 - larg_nave_p//2
    largura_nave_i1 = LARGURA//1.5
    largura_nave_i2 = LARGURA//4 - larg_nave_p//2
    largura_nave_i3 = LARGURA//2 - larg_nave_p//2
    largura_boss = LARGURA//2 - larg_nave_boss//2

    # Definindo a coordenada vertical de início de cada imagem
    altura_nome = ALTURA
    altura_nave_p = ALTURA + 300
    altura_nave_i1 = ALTURA + 350
    altura_nave_i2 = ALTURA + 350
    altura_nave_i3 = ALTURA + 350
    altura_nave_b = ALTURA  + 400


    def girar(imagem):
        return pg.transform.rotate(imagem,180)

    naves_passando = True
    while naves_passando:
        RELOGIO.tick(FPS)
        TELA.blit(BG, (0, 0))

        # Atualizações na posição vertical de cada imagem
        if altura_nome > -500:
            altura_nome -= 7
        if altura_nave_p > -90:
            altura_nave_p -= 5
        if altura_nave_i1 > -100:
            altura_nave_i1 -= 4
        if altura_nave_i2 > -100:
            altura_nave_i2 -= 4
        if altura_nave_i3 > -100:
            altura_nave_i3 -= 4
        if altura_nave_b > -300:
            altura_nave_b -= 3
        else:
            menu_principal()
        
        # Colocando imagens na tela
        TELA.blit(TEXTO,(largura_nome,altura_nome))
        TELA.blit(NAVE_PRINCIPAL, (largura_nave, altura_nave_p))
        TELA.blit(girar(NAVES_INIMIGAS[0]), (int(largura_nave_i1), int(altura_nave_i1)))
        TELA.blit(girar(NAVES_INIMIGAS[1]), (largura_nave_i2, altura_nave_i2))
        TELA.blit(girar(NAVES_INIMIGAS[2]), (largura_nave_i3, altura_nave_i3))
        TELA.blit(girar(NAVES_INIMIGAS[4]), (largura_boss, altura_nave_b))

        # Controle de Eventos de Mouse e Teclado
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    menu_principal()
        pg.display.flip()

# INICIALIZANDO A APLICAÇÃO
tela_inicial()
