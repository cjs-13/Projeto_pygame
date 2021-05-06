import initialize as ini
import assets as asc
import random
from physics import testa_colisao

# DEFINIÇÃO DAS CLASSES


class Laser():
    def __init__(self, x, y, img, nave, arma):
        self.x = x + nave.arma_x[arma]
        self.y = y + nave.arma_y[arma]
        self.img = img
        self.mascara = ini.pg.mask.from_surface(self.img)
        self.nave = nave
        self.damagetype = nave.layer
        self.vel_x = nave.laservel_x[arma]
        self.vel_y = nave.laservel_y[arma]
        self.hp = nave.laserhp[arma]
        self.arma = arma

    def drawinterno(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))

    def fora_tela(self):
        return (self.y <= 0 or self.y >= ini.ALTURA) or (self.x <= 0 or self.x >= ini.LARGURA)

    def largura(self):
        return self.img.get_width()

    def altura(self):
        return self.img.get_height()

    def moverlaserinterno(self):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.fora_tela():
            self.hp = 0

    def colisaointerno(self, naves, lasers):
        for nave in naves:
            if nave.layer != self.damagetype and testa_colisao(self, nave):
                self.hp -= 1
                if nave.imunity_timer == 0:
                    nave.hp -= 1
                    nave.imunity_timer = 5

    def colisaoLaser(self, lasers):
        for laser in lasers:
            if self.damagetype != laser.damagetype and testa_colisao(self, laser):
                self.hp -= 1

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
        self.hp_regen = 900
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
        return self.y >= ini.ALTURA or self.x <= 0 - self.largura() or self.x >= ini.LARGURA + self.largura()

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

        if self.tipo == "Jogador" and self.hp_regen > 0 and self.hp < self.max_hp:
            self.hp_regen -= 1

    def largura(self):
        return self.nave_img.get_width()

    def altura(self):
        return self.nave_img.get_height()

    def testevida(self, naves):
        if self.tipo == "Jogador" and self.hp_regen == 0:
            self.hp += 1
            self.hp_regen = 900
        if self.hp < 1 and self.lives < 2:
            naves.remove(self)
            if self.tipo == "Inimigo" and self.fora_tela() is not True:
                if naves[0] is not None:
                    jogador = naves[0]
                    if jogador.tipo == "Jogador":
                        jogador.pontos += 10
                        naves[0] = jogador
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
        if self.y > 0:
            self.atirarinterno(0, lasers)
        if self.fora_tela():
            self.hp = 0

    def ai1_inimigo(self, lasers):
        self.y += 1
        if self.aihelper < 0 and (self.x + 104 < ini.LARGURA or self.y > 80):
            self.x -= (self.y // 20) - 4
        elif self.aihelper > 0 and (self.x - 4 > 0 or self.y > 80):
            self.x += (self.y // 20) - 4
        if self.aihelper == 0:
            if self.x >= ini.ALTURA // 2:
                self.aihelper = -1
            elif self.x < ini.ALTURA // 2:
                self.aihelper = 1
        if self.y > 0:
            self.atirarinterno(0, lasers)
        if self.fora_tela():
            self.hp = 0

    def ai2_inimigo(self, lasers):
        if self.y < ini.ALTURA // 2 - ini.SCALE_NAVE[1]:
            self.y += 1
        if self.y > 0:
            self.atirarinterno(1, lasers)
            self.atirarinterno(2, lasers)

    def ai3_inimigo(self, lasers):
        if self.y < - ini.SCALE_NAVE[1]:
            self.aihelper = random.randint(0, 1)
        if self.x + self.largura() + 3 > ini.LARGURA:
            self.aihelper = 1
        elif self.x - 3 < 0:
            self.aihelper = 0
        self.y += 0.5
        if self.aihelper == 0:
            self.x += 2
        elif self.aihelper == 1:
            self.x -= 2
        if self.y > 0:
            self.atirarinterno(0, lasers)
        if self.fora_tela():
            self.hp = 0

    def ai4_boss(self, lasers):
        if self.y + 2 < 10:  # Animacao de entrada
            self.y += 2
        else:
            if self.x + self.largura() + 0.5 > ini.LARGURA:
                self.aihelper = 1
            elif self.x - 0.5 < 0:
                self.aihelper = 0
            if self.aihelper == 0:
                self.x += 0.5
            elif self.aihelper == 1:
                self.x -= 0.5
            self.atirarinterno(1, lasers)
            self.atirarinterno(2, lasers)
            if self.hp <= self.max_hp / 2:
                self.atirarinterno(0, lasers)
                self.atirarinterno(3, lasers)


class Jogador(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vel_x = 5
        self.vel_y = 5
        self.nave_img = asc.NAVE_PRINCIPAL
        self.laser_img = asc.LASER_PRINCIPAL
        self.hp_img = asc.HP
        self.mascara = ini.pg.mask.from_surface(self.nave_img)
        self.tipo = "Jogador"
        self.pontos = 0
        self.layer = 1
        self.damagetype = 1
        self.hp = 10
        self.max_hp = 10
        self.lives = 5
        self.ai = -1
        self.firerate[0] = 15
        self.laserhp[0] = 1
        self.laservel_x[0] = 0
        self.laservel_y[0] = -7
        self.arma_x[0] = 45
        self.arma_y[0] = 0

    def colisao(self, naves):  # Testa a colisao do player com as naves
        for nave in naves:
            if self.layer != nave.layer and testa_colisao(self, nave):
                nave.hp -= 1
                if self.imunity_timer == 0:
                    self.hp -= 1
                    self.imunity_timer = 5

    def draw_hp(self, tela):  # Desenha na tela os status de hp e vida do jogador
        hp_label = ini.FONT_PRINCIPAL.render("HP:", True, ini.BRANCO)
        lives_label = ini.FONT_PRINCIPAL.render(f"Vidas: {self.lives - 1}", True, ini.BRANCO)
        pontos = ini.FONT_PRINCIPAL.render(f"Pontos: {self.pontos}", True, ini.BRANCO)
        tela.blit(self.hp_img[0], (40, ini.ALTURA + 15))
        tela.blit(asc.ch_scale(self.hp_img[1], (28 * self.hp, 5)), (49, ini.ALTURA + 18))
        tela.blit(hp_label, (7, ini.ALTURA + 11))
        tela.blit(lives_label, (ini.SCALE_LABEL_HP[0] + 60, ini.ALTURA + 11))
        tela.blit(pontos, (ini.SCALE_LABEL_HP[0] + 140, ini.ALTURA + 11))


    def move_left(self):
        self.x -= self.vel_x


    def move_right(self):
        self.x += self.vel_x


    def move_up(self):
        self.y -= self.vel_y

    def move_down(self):
        self.y += self.vel_y


class Inimigo(Nave):
    def __init__(self, x, y, ai):
        super().__init__(x, y)
        self.nave_img = asc.NAVES_INIMIGAS[ai]
        self.laser_img = asc.LASER_RED
        self.mascara = ini.pg.mask.from_surface(self.nave_img)
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
        self.nave_img = asc.NAVES_INIMIGAS[ai]
        self.laser_img = asc.LASER_BLUE
        self.mascara = ini.pg.mask.from_surface(self.nave_img)
        self.tipo = "Boss"
        self.layer = 2
        self.damagetype = 2
        self.ai = ai
        self.firerate[0] = 70
        self.firerate[1] = 50
        self.firerate[2] = 50
        self.firerate[3] = 70
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
        self.max_hp = 100
        self.arma_x[0] = self.largura() // 2 - 5 - 62
        self.arma_x[1] = self.largura() // 2 - 5 - 38
        self.arma_x[2] = self.largura() // 2 - 5 + 38
        self.arma_x[3] = self.largura() // 2 - 5 + 62
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
        self.max_dificuty = 3
        self.wave_randomid = [0, 0, 0]
        self.win = False

    def pular_onda(self):
        self.counter = -1
        self.counteracive = True
        self.wave += 1

    def pular_fase(self, nave):
        self.counter = -1
        self.counteracive = True
        self.fase += 1
        self.wave = 0
        if self.dificuty < self.max_dificuty:
            self.dificuty += 1
        if self.fase < 2:
            nave.lives += 1
            nave.hp = nave.max_hp

    def criar_inimigo(self, x, y, ai, naves):  # cria um inimigo
        inimigotempo = Inimigo(x, y - ini.SCALE_NAVE[1], ai)
        naves.append(inimigotempo)

    def direcionar_fase(self, naves):  # testa em qual fase esta e roda ela
        if self.fase == 0:
            self.faseid0(naves)
        if self.fase == 1:
            self.faseid1(naves)
        if self.fase == 2:
            self.faseid2(naves)

    def sem_inimigos(self, naves):  # olha se tem inimigos e reativa o contador
        if len(naves) < 2:
            self.counteracive = True

    def counter_tick(self):
        if self.counteracive:  # anda o contador se ele estiver ativo
            self.counter += 1

    def wave_random(self, type, naves):
        if self.wave_randomid[type] == 0:
            self.wave_id0(naves)
        elif self.wave_randomid[type] == 1:
            self.wave_id1(naves)
        elif self.wave_randomid[type] == 2:
            self.wave_id2(naves)
        elif self.wave_randomid[type] == 3:
            self.wave_id3(naves)
        elif self.wave_randomid[type] == 4:
            self.wave_id4(naves)

    def wave_id0(self, naves):  # onda de id 0, spawna inimigos e uma formação de / \
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0:  # spawna inimigos quando o counter e igual a 0
            self.criar_inimigo(5, 0, 0, naves)
            self.criar_inimigo(450, 0, 0, naves)
        elif self.counter == 240 / self.dificuty:  # spawna inimigos quando o counter e igual a 120 na dificuldade 1
            self.criar_inimigo(65, 0, 0, naves)
            self.criar_inimigo(390, 0, 0, naves)
        elif self.counter == 360 / self.dificuty:  # spawna inimigos quando o counter e igual a 240 na dificuldade 1
            self.criar_inimigo(125, 0, 0, naves)
            self.criar_inimigo(330, 0, 0, naves)
        elif self.counter == 480 / self.dificuty:  # spawna inimigos quando o counter e igual a 360 na dificuldade 1
            self.criar_inimigo(185, 0, 0, naves)
            self.criar_inimigo(270, 0, 0, naves)
        elif self.counter == 600 / self.dificuty:  # termina a onda quando o counter e igual a 480 na dificuldade 1
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
        elif self.counter == 240 / self.dificuty:
            self.counter = -1  # reseta o contador
            self.wave += 1  # anda para a proxima onda
            self.counteracive = False  # desativa o contador

    def wave_id2(self, naves):
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0:  # spawna inimigos quando o counter e igual a 0
            self.criar_inimigo(5, 0, 1, naves)
            self.criar_inimigo(450, 0, 1, naves)
        elif self.counter == 240 / self.dificuty:  # spawna inimigos quando o counter e igual a 120 na dificuldade 1
            self.criar_inimigo(5, 0, 1, naves)
            self.criar_inimigo(450, 0, 1, naves)
        elif self.counter == 360 / self.dificuty:  # spawna inimigos quando o counter e igual a 240 na dificuldade 1
            self.criar_inimigo(5, 0, 1, naves)
            self.criar_inimigo(450, 0, 1, naves)
        elif self.counter == 480 / self.dificuty:  # spawna inimigos quando o counter e igual a 360 na dificuldade 1
            self.criar_inimigo(5, 0, 1, naves)
            self.criar_inimigo(450, 0, 1, naves)
        elif self.counter == 600 / self.dificuty:  # termina a onda quando o counter e igual a 480 na dificuldade 1
            self.counter = -1  # reseta o contador
            self.wave += 1  # anda para a proxima onda
            self.counteracive = False  # desativa o contador

    def wave_id3(self, naves):
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0:
            self.criar_inimigo(5, 0, 2, naves)
            self.criar_inimigo(ini.LARGURA // 2 - ini.SCALE_NAVE[0] // 2, -90, 2, naves)
            self.criar_inimigo(450, 0, 2, naves)
        elif self.counter == 360 / self.dificuty:
            self.counter = -1
            self.wave += 1
            self.counteracive = False

    def wave_id4(self, naves):
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0:
            self.criar_inimigo(5, 0, 3, naves)
            self.criar_inimigo(ini.LARGURA // 2 - ini.SCALE_NAVE[0] // 2, -90, 3, naves)
            self.criar_inimigo(450, 0, 3, naves)
        elif self.counter == 360 / self.dificuty:
            self.counter = -1
            self.wave += 1
            self.counteracive = False

    def wave_boss(self, naves):  # Spawna nave do boss hp multiplicado pela dificudade da fase
        if self.counter % (120 / self.dificuty) != 0:
            self.counteracive = True
        elif self.counter == 0:
            boss = Boss(ini.LARGURA // 2 - ini.SCALE_BOSS[0] // 2, -ini.SCALE_BOSS[1], 4)
            boss.hp *= self.dificuty
            naves.append(boss)
        elif len(naves) < 2:
            self.counter = -1
            self.wave += 1
            self.counteracive = False

    def faseid0(self, naves):  # a primeira fase
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

        elif self.wave == 3 and self.counteracive is False:
            self.counteracive = True

        elif self.wave == 3:
            self.wave_id2(naves)

        elif self.wave == 4 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 2)
            self.counteracive = True

        elif self.wave == 4:
            self.wave_random(0, naves)

        elif self.wave == 5 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 2)
            self.counteracive = True

        elif self.wave == 5:
            self.wave_random(0, naves)

        elif self.wave == 6 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 2)
            self.counteracive = True

        elif self.wave == 6:
            self.wave_random(0, naves)

        elif self.wave == 7 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 2)
            self.counteracive = True

        elif self.wave == 7:
            self.wave_random(0, naves)

        elif self.wave == 8 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 2)
            self.counteracive = True

        elif self.wave == 8:
            self.wave_random(0, naves)

        elif self.wave == 9 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 2)
            self.counteracive = True

        elif self.wave == 9:
            self.wave_random(0, naves)

        elif self.wave == 10 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 10:
            self.wave_boss(naves)

        elif self.wave == 11:
            self.pular_fase(naves[0])

    def faseid1(self, naves):  # segunda fase
        if self.wave == 0:  # onda 1
            self.wave_id3(naves)

        elif self.wave == 1 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 1:
            self.wave_id4(naves)

        elif self.wave == 2 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 2:
            self.wave_id3(naves)

        elif self.wave == 3 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 3:
            self.wave_id0(naves)

        elif self.wave == 4 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 4:
            self.wave_id3(naves)

        elif self.wave == 5 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 5:
            self.wave_random(0, naves)

        elif self.wave == 6 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 6:
            self.wave_random(0, naves)

        elif self.wave == 7 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 7:
            self.wave_random(0, naves)

        elif self.wave == 8 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 8:
            self.wave_random(0, naves)

        elif self.wave == 9 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 9:
            self.wave_random(0, naves)

        elif self.wave == 10 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 10:
            self.wave_id0(naves)

        elif self.wave == 11 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 11:
            self.wave_id1(naves)

        elif self.wave == 12 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 12:
            self.wave_id3(naves)

        elif self.wave == 13 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 13:
            self.wave_boss(naves)

        elif self.wave == 14:
            self.pular_fase(naves[0])

    def faseid2(self, naves):
        if self.wave == 0:
            self.wave_id3(naves)

        elif self.wave == 1 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 1:
            self.wave_random(0, naves)

        elif self.wave == 2 and self.counteracive is False:
            self.wave_randomid[0] = random.randint(0, 4)
            self.counteracive = True

        elif self.wave == 2:
            self.wave_random(0, naves)

        elif self.wave == 3 and self.counteracive is False:
            self.sem_inimigos(naves)

        elif self.wave == 3:
            self.wave_boss(naves)

        elif self.wave == 4:
            self.win = True
