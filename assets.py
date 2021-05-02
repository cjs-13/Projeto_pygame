import initialize as ini
import os

# FUNÇÕES PARA TORNAR O CÓDIGO MENOS VERBOSO

def load_img(caminho, nome_imagem):
    return ini.pg.image.load(os.path.join(caminho, nome_imagem))


def ch_scale(imagem, escala):
    return ini.pg.transform.scale(imagem, escala)



# CARREGANDO IMAGENS

# Tela inicial e Menu Principal
TEXTO = load_img(ini.DIR, "nome.png").convert_alpha()
BG_INICIO = ch_scale(load_img(ini.DIR, "fundo.png"),(ini.LARGURA, ini.ALTURA + 40))
B_INICIAR = load_img(ini.DIR, "iniciar.png")
B_AJUDA = load_img(ini.DIR, "ajuda.png")
B_SAIR = load_img(ini.DIR, "sair.png")

# Tela de ajuda
BG_AJUDA = ch_scale(load_img(ini.DIR, "BG_ajuda.png").convert(), (ini.LARGURA, ini.ALTURA + 40))
B_VOLTAR = load_img(ini.DIR, "voltar.png")


# Tela de pausa
TEXTO_PAUSA = load_img(ini.DIR,"pause.png").convert_alpha()
B_CONTINUAR = load_img(ini.DIR,"continuar.png")

# Telas de fim de jogo
TEXTO_VENCEDOR = load_img(ini.DIR,"TITLE_vencedor.png").convert_alpha()
TEXTO_GAME_OVER = load_img(ini.DIR,"TITLE_gameover.png").convert_alpha()
B_BACK_MENU = load_img(ini.DIR,"back_to_main_menu.png")
B_TRY_AGAIN = load_img(ini.DIR,"try_again.png")

# Telas das fases do jogo
NAVE_PRINCIPAL = ch_scale(load_img(ini.DIR, "space_ship.png").convert_alpha(), ini.SCALE_NAVE)
LASER_PRINCIPAL = load_img(ini.DIR, "laser_principal.png").convert_alpha()
NAVES_INIMIGAS = list()
for i in range(1, 5):
    NAVES_INIMIGAS.append(ch_scale(load_img(ini.DIR, f"enemy_ship ({i}).png").convert_alpha(), ini.SCALE_NAVE))
for i in range(1, 2):
    NAVES_INIMIGAS.append(ch_scale(load_img(ini.DIR, f"boss_ship ({i}).png").convert_alpha(), ini.SCALE_BOSS))
LASER_RED = load_img(ini.DIR, "laser_red.png").convert_alpha()
LASER_BLUE = load_img(ini.DIR, "laser_blue.png").convert_alpha()
HP = list()
for i in range(1, 3):
    HP.append(ch_scale(load_img(ini.DIR, f"hp ({i}).png"), ini.SCALE_LABEL_HP))
BARRA_INF = ch_scale(load_img(ini.DIR, "barra.png"), (ini.LARGURA, 40))
BG = list()
for i in range(1, 4):
    BG.append(ch_scale(load_img(ini.DIR, f"BG_({i}).png").convert(), (ini.LARGURA, ini.ALTURA + 40)))

# Icone do Jogo
ICONE = load_img(ini.DIR, "windows_icon.png")