import initialize as ini
import assets as asc
import classes as css
import screens
from sys import exit

# ADIÇÃO DE NOME E ICONE À JANELA DO JOGO

ini.pg.display.set_caption("Invasores do Espaço")
ini.pg.display.set_icon(asc.ICONE)

# JANELAS DO JOGO

def main():
    jogando = True
    jogador_vel = 5
    naves = list()
    jogador = css.Jogador(ini.LARGURA//2 - asc.NAVE_PRINCIPAL.get_width()/2, ini.ALTURA - 100)
    naves.append(jogador)
    lasers = list()
    fase = css.Fase()
    while jogando:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG[fase.fase], (0, 0))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                jogando = False
                ini.pg.quit()
                exit()
                
            if event.type == ini.pg.MOUSEBUTTONDOWN:
                screens.tela_pause(fase, main)

            if event.type == ini.pg.KEYDOWN:
                if event.key == ini.pg.K_ESCAPE:
                    screens.menu_principal(main)
                if event.key == ini.pg.K_k:
                    if fase.fase < 2:
                        fase.pular_fase(naves[0])

        keys = ini.pg.key.get_pressed()
        if (keys[ini.pg.K_a] or keys[ini.pg.K_LEFT]) and jogador.x - jogador_vel > 0:
            jogador.x -= jogador_vel
        if (keys[ini.pg.K_d] or keys[ini.pg.K_RIGHT]) and jogador.x + jogador_vel + jogador.largura() < ini.LARGURA:
            jogador.x += jogador_vel
        if (keys[ini.pg.K_w] or keys[ini.pg.K_UP]) and jogador.y - jogador_vel > 0:
            jogador.y -= jogador_vel
        if (keys[ini.pg.K_s] or keys[ini.pg.K_DOWN]) and jogador.y + jogador_vel + jogador.altura() < ini.ALTURA:
            jogador.y += jogador_vel
        if keys[ini.pg.K_SPACE]:
            jogador.atirarinterno(0, lasers)

        jogador.colisao(naves)
        for laser in lasers:
            laser.moverlaserinterno(lasers)
            laser.colisaointerno(naves, lasers)
            laser.testevida(lasers)
            laser.drawinterno(ini.TELA)
            laser.ColisaoLaser(lasers)

        if jogador.hp <= 0 and jogador.lives < 2:
            screens.tela_fim_de_jogo(jogador.pontos, fase, main)

        for nave in naves:
            nave.reduzirtimers()
            nave.testevida(naves)
            nave.testeai(lasers)
            nave.draw(ini.TELA)

        if fase.win == True:
            screens.tela_vencedor(jogador.pontos,fase, main)

        ini.TELA.blit(asc.BARRA_INF, (0, ini.ALTURA))
        jogador.draw_hp(ini.TELA)
        fase.direcionar_fase(naves)
        fase.counter_tick()

        ini.pg.display.flip()

# INICIALIZANDO A APLICAÇÃO
screens.tela_inicial(main)

