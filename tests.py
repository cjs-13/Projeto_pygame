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


testtimer = [0, 0, 0, 0, 4]
testejogador = css.Jogador(ini.LARGURA//2 - asc.NAVE_PRINCIPAL.get_width()/2, ini.ALTURA - 100)


def test_moviment_left(direction, testejogador):

    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if testejogador.x - testejogador.vel_x > 0:
            testejogador.move_left()

    if testtimer[direction] == 360:
        assert testejogador.x < 10


def test_moviment_right(direction, testejogador):
    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if testejogador.x + testejogador.vel_x + testejogador.largura() < initialize.LARGURA:
            testejogador.move_right()

    if testtimer[direction] == 360:
        assert testejogador.x > initialize.LARGURA - testejogador.largura() - 10


def test_moviment_up(direction, testejogador):
    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if testejogador.y - testejogador.vel_y > 0:
            testejogador.move_up()
    if testtimer[direction] == 360:
        assert testejogador.y < 10


def test_moviment_down(direction, testejogador):
    if testtimer[direction] < 360:
        testtimer[direction] += 1
        if testejogador.y + testejogador.vel_y + testejogador.altura() < initialize.ALTURA:
            testejogador.move_down()
    if testtimer[direction] == 360:
        assert testejogador.y > initialize.ALTURA - testejogador.altura() - 10


def test_timer_position(direction):
    if testtimer[direction] == 360:
        testtimer[4] += 1



def test_moviment_direction(direction, testejogador):
    if direction == 0:
        test_moviment_left(direction, testejogador)

    if direction == 1:
        test_moviment_right(direction, testejogador)

    if direction == 2:
        test_moviment_up(direction, testejogador)

    if direction == 3:
        test_moviment_down(direction, testejogador)


def test_moviment_single(direction, testejogador):
    test_moviment_direction(direction, testejogador)
    test_timer_position(direction)


def test_moviment(testejogador):
    direction = testtimer[4]
    while testtimer[4] < 4:
        print("timer is")
        print(testtimer[direction])
        print(" and position ")
        print(direction)
        if direction < 4:
            test_moviment_single(direction, testejogador)
