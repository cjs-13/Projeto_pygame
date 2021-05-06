def testa_colisao(obj1, obj2):
    # obj1 == Laser, obj2 == Nave atingida
    diff_x = obj2.x - obj1.x
    diff_y = obj2.y - obj1.y
    return obj1.mascara.overlap(obj2.mascara, (int(diff_x),int(diff_y))) != None
