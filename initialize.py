import pygame as pg

LARGURA = 550
ALTURA = 550
FPS = 60
BRANCO = (255, 255, 255)
SCALE_NAVE = (100, 90)
SCALE_BOSS = (350, 280)
SCALE_LABEL_HP = (297, 10)

pg.init()
pg.font.init()
FONT_PRINCIPAL = pg.font.SysFont("Letter Gothic", 25)
TELA = pg.display.set_mode((LARGURA, ALTURA + 40))
RELOGIO = pg.time.Clock()
DIR = "assets"
