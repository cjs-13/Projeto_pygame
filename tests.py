import initialize
import physics
import classes
import assets

# CAIXA BRANCA

obj1 = classes.Jogador(0, 0)
obj2 = classes.Inimigo(0, 0, 0)
obj3 = classes.Laser(100, 60, assets.LASER_PRINCIPAL, obj1, 0)
obj4 = classes.Laser(100, 0, assets.LASER_RED, obj2, 0)


def test_collision_nave():
    assert physics.testa_colisao(obj1, obj2) == True


def test_collision_laser():
    assert physics.testa_colisao(obj3, obj4) == True


def test_no_collision():
    assert physics.testa_colisao(obj1, obj4) == False

# CAIXA PRETA


testtimer = [0, 0, 0, 0, 4]


def test_moviment_left(direction, jogador):

    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if jogador.x - jogador.vel_x > 0:
            jogador.move_left()

    if testtimer[direction] == 360:
        assert jogador.x < 10


def test_moviment_right(direction, jogador):
    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if jogador.x + jogador.vel_x + jogador.largura() < initialize.LARGURA:
            jogador.move_right()

    if testtimer[direction] == 360:
        assert jogador.x > initialize.LARGURA - jogador.largura() - 10


def test_moviment_up(direction, jogador):
    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if jogador.y - jogador.vel_y > 0:
            jogador.move_up()
    if testtimer[direction] == 360:
        assert jogador.y < 10


def test_moviment_down(direction, jogador):
    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if jogador.y + jogador.vel_y + jogador.altura() < initialize.ALTURA:
            jogador.move_down()
    if testtimer[direction] == 360:
        assert jogador.y > initialize.ALTURA - jogador.altura() - 10


def test_timer_position(direction):
    if testtimer[direction] == 360:
        testtimer[4] += 1



def test_moviment_direction(direction, jogador):
    if direction == 0:
        test_moviment_left(direction, jogador)

    if direction == 1:
        test_moviment_right(direction, jogador)

    if direction == 2:
        test_moviment_up(direction, jogador)

    if direction == 3:
        test_moviment_down(direction, jogador)


def test_moviment_single(direction, jogador):
    test_moviment_direction(direction, jogador)
    test_timer_position(direction)


def test_moviment(jogador):
    direction = testtimer[4]
    print("timer is")
    print(testtimer[direction])
    print(" and position ")
    print(direction)
    if direction < 4:
        test_moviment_single(direction, jogador)
