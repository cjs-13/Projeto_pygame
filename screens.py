import initialize as ini
import assets as asc

def menu_principal(main):
    B_INICIAR_largura = asc.B_INICIAR.get_width()

    largura_geral = ini.LARGURA // 2 - B_INICIAR_largura // 2

    altura_iniciar = ini.ALTURA + 100
    altura_ajuda = ini.ALTURA + 100
    altura_sair = ini.ALTURA + 100

    menu = True

    while menu:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG_INICIO, (0, 0))

        if altura_iniciar > ini.ALTURA // 2.5:
            altura_iniciar -= 14
        else:
            if altura_ajuda > altura_iniciar + (ini.ALTURA // 5):
                altura_ajuda -= 14
            else:
                if altura_sair > altura_ajuda + (ini.ALTURA // 5):
                    altura_sair -= 14

        ini.TELA.blit(asc.B_INICIAR, (largura_geral, altura_iniciar))
        ini.TELA.blit(asc.B_AJUDA, (largura_geral, altura_ajuda))
        ini.TELA.blit(asc.B_SAIR, (largura_geral, altura_sair))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                menu = False
                ini.pg.quit()
                exit()
            if event.type == ini.pg.MOUSEBUTTONDOWN:
                x = ini.pg.mouse.get_pos()[0]
                y = ini.pg.mouse.get_pos()[1]
                if 139 < x < 414 and 256 < y < 289:
                    main()
                if 139 < x < 414 and 352 < y < 395:
                    ajuda(main)
                if 139 < x < 414 and 449 < y < 484:
                    ini.pg.quit()
                    exit()

        ini.pg.display.flip()


def ajuda(main):
    B_VOLTAR_largura = asc.B_VOLTAR.get_width()

    largura = ini.LARGURA // 2 - B_VOLTAR_largura // 2

    altura_voltar = ini.ALTURA

    ajuda = True
    while ajuda:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG_AJUDA, (0, 0))

        if altura_voltar > ini.ALTURA // 1.15:
            altura_voltar -= 4

        ini.TELA.blit(asc.B_VOLTAR, (largura, altura_voltar))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                ini.pg.quit()
                exit()
            if event.type == ini.pg.KEYDOWN:
                if event.key == ini.pg.K_ESCAPE:
                    ajuda = False
            if event.type == ini.pg.MOUSEBUTTONDOWN:
                x = ini.pg.mouse.get_pos()[0]
                y = ini.pg.mouse.get_pos()[1]
                if 123 < x < 414 and 515 < y < 552:
                    menu_principal(main)
        ini.pg.display.flip()


def tela_inicial(main):
    larg_nome = asc.TEXTO.get_width()
    larg_nave_p = asc.NAVE_PRINCIPAL.get_width()
    larg_nave_boss = asc.NAVES_INIMIGAS[4].get_width()

    largura_nome = ini.LARGURA // 2 - larg_nome // 2
    largura_nave = ini.LARGURA // 2 - larg_nave_p // 2
    largura_nave_i1 = ini.LARGURA // 1.5
    largura_nave_i2 = ini.LARGURA // 4 - larg_nave_p // 2
    largura_nave_i3 = ini.LARGURA // 2 - larg_nave_p // 2
    largura_boss = ini.LARGURA // 2 - larg_nave_boss // 2

    altura_nome = ini.ALTURA
    altura_nave_p = ini.ALTURA + 300
    altura_nave_i1 = ini.ALTURA + 350
    altura_nave_i2 = ini.ALTURA + 350
    altura_nave_i3 = ini.ALTURA + 350
    altura_nave_b = ini.ALTURA + 400

    def girar(imagem):
        return ini.pg.transform.rotate(imagem, 180)

    naves_passando = True
    while naves_passando:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG[0], (0, 0))

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
            naves_passando = False
            menu_principal(main)

        ini.TELA.blit(asc.TEXTO, (largura_nome, altura_nome))
        ini.TELA.blit(asc.NAVE_PRINCIPAL, (largura_nave, altura_nave_p))
        ini.TELA.blit(girar(asc.NAVES_INIMIGAS[0]), (int(largura_nave_i1), int(altura_nave_i1)))
        ini.TELA.blit(girar(asc.NAVES_INIMIGAS[1]), (largura_nave_i2, altura_nave_i2))
        ini.TELA.blit(girar(asc.NAVES_INIMIGAS[2]), (largura_nave_i3, altura_nave_i3))
        ini.TELA.blit(girar(asc.NAVES_INIMIGAS[4]), (largura_boss, altura_nave_b))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                naves_passando = False
                ini.pg.quit()
                exit()
            if event.type == ini.pg.KEYDOWN:
                if event.key == ini.pg.K_ESCAPE:
                    menu_principal(main)
        ini.pg.display.flip()


def tela_pause(fase,main):
    larg_nome = asc.TEXTO_PAUSA.get_width()
    B_CONTINUAR_largura = asc.B_INICIAR.get_width()

    largura_nome = ini.LARGURA // 2 - larg_nome // 2
    largura_geral = ini.LARGURA // 2 - B_CONTINUAR_largura // 2

    altura_nome = ini.ALTURA
    altura_continuar = ini.ALTURA + 100
    altura_menu = ini.ALTURA + 100

    pause = True

    while pause:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG[fase.fase], (0, 0))

        if altura_nome > ini.ALTURA // 6:
            altura_nome -= 40
        else:
            if altura_continuar > altura_nome + (ini.ALTURA // 3):
                altura_continuar -= 30
            else:
                if altura_menu > altura_continuar + (ini.ALTURA // 6):
                    altura_menu -= 30

        ini.TELA.blit(asc.TEXTO_PAUSA, (largura_nome, altura_nome))
        ini.TELA.blit(asc.B_CONTINUAR, (largura_geral, altura_continuar))
        ini.TELA.blit(asc.B_BACK_MENU, (largura_geral, altura_menu))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                pause = False
                ini.pg.quit()
                exit()

            if event.type == ini.pg.KEYDOWN:
                if event.key == ini.pg.K_ESCAPE:
                    pause = False
                    menu_principal(main)

            if event.type == ini.pg.MOUSEBUTTONDOWN:
                x = ini.pg.mouse.get_pos()[0]
                y = ini.pg.mouse.get_pos()[1]
                if 137 < x < 409 and 270 < y < 306:
                    pause = False
                if 137 < x < 417 and 354 < y < 395:
                    menu_principal(main)
        ini.pg.display.flip()


def tela_fim_de_jogo(pontos, fase, main):
    label_pontos = ini.FONT_PRINCIPAL.render(f"Sua Pontuação: {pontos}", True, ini.BRANCO)

    larg_nome = asc.TEXTO_GAME_OVER.get_width()
    B_INICIAR_largura = asc.B_INICIAR.get_width()
    larg_pontos = label_pontos.get_width()

    largura_nome = ini.LARGURA // 2 - larg_nome // 2
    largura_geral = ini.LARGURA // 2 - B_INICIAR_largura // 2
    largura_pontos = ini.LARGURA // 2 - larg_pontos // 2

    altura_nome = ini.ALTURA
    altura_try_again = ini.ALTURA + 100
    altura_menu = ini.ALTURA + 100
    altura_pontos = ini.ALTURA + 100

    the_end = True

    while the_end:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG[fase.fase], (0, 0))

        if altura_nome > ini.ALTURA // 6:
            altura_nome -= 20
        else:
            if altura_pontos > altura_nome + (ini.ALTURA // 4):
                altura_pontos -= 20
            else:
                if altura_try_again > altura_pontos + (ini.ALTURA // 6):
                    altura_try_again -= 20
                else:
                    if altura_menu > altura_try_again + (ini.ALTURA // 6):
                        altura_menu -= 20

        ini.TELA.blit(asc.TEXTO_GAME_OVER, (largura_nome, altura_nome))
        ini.TELA.blit(label_pontos, (largura_pontos, altura_pontos))
        ini.TELA.blit(asc.B_TRY_AGAIN, (largura_geral, altura_try_again))
        ini.TELA.blit(asc.B_BACK_MENU, (largura_geral, altura_menu))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                the_end = False
                ini.pg.quit()
                exit()
            if event.type == ini.pg.KEYDOWN:
                if event.key == ini.pg.K_ESCAPE:
                    the_end = False
                    menu_principal(main)
            if event.type == ini.pg.MOUSEBUTTONDOWN:
                x = ini.pg.mouse.get_pos()[0]
                y = ini.pg.mouse.get_pos()[1]
                if 137 < x < 417 and 324 < y < 366:
                    main()
                if 137 < x < 417 and 404 < y < 447:
                    menu_principal(main)
        ini.pg.display.flip()


def tela_vencedor(pontos, fase, main):
    label_pontos = ini.FONT_PRINCIPAL.render(f"Essa foi sua Pontuação: {pontos}", True, ini.BRANCO)

    larg_nome = asc.TEXTO_VENCEDOR.get_width()
    B_INICIAR_largura = asc.B_INICIAR.get_width()
    larg_pontos = label_pontos.get_width()

    largura_nome = ini.LARGURA // 2 - larg_nome // 2
    largura_geral = ini.LARGURA // 2 - B_INICIAR_largura // 2
    largura_pontos = ini.LARGURA // 2 - larg_pontos // 2

    altura_nome = ini.ALTURA
    altura_menu = ini.ALTURA + 100
    altura_pontos = ini.ALTURA + 100

    the_end = True

    while the_end:
        ini.RELOGIO.tick(ini.FPS)
        ini.TELA.blit(asc.BG[fase.fase], (0, 0))

        if altura_nome > ini.ALTURA // 6:
            altura_nome -= 20
        else:
            if altura_pontos > altura_nome + (ini.ALTURA // 4):
                altura_pontos -= 20
            else:
                if altura_menu > altura_pontos + (ini.ALTURA // 6):
                    altura_menu -= 20

        ini.TELA.blit(asc.TEXTO_VENCEDOR, (largura_nome, altura_nome))
        ini.TELA.blit(label_pontos, (largura_pontos, altura_pontos))
        ini.TELA.blit(asc.B_BACK_MENU, (largura_geral, altura_menu))

        for event in ini.pg.event.get():
            if event.type == ini.pg.QUIT:
                the_end = False
                ini.pg.quit()
                exit()
            if event.type == ini.pg.KEYDOWN:
                if event.key == ini.pg.K_ESCAPE:
                    the_end = False
                    menu_principal(main)
            if event.type == ini.pg.MOUSEBUTTONDOWN:
                x = ini.pg.mouse.get_pos()[0]
                y = ini.pg.mouse.get_pos()[1]
                if 137 < x < 417 and 324 < y < 366:
                    menu_principal(main)
        ini.pg.display.flip()
