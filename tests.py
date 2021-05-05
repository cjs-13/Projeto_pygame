import physics
import classes
import assets

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
