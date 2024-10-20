'''Поворот объемного тела относительно осей координат на заданный
угол'''
from CubeFactory import CubeFactory
from cube import Cube


def main():
    cube = Cube([[0, 0, 0],
                 [10, 0, 0],
                 [10, 10, 0],
                 [0, 10, 0],
                 [0, 0, 10],
                 [10, 0, 10],
                 [10, 10, 10],
                 [0, 10, 10]], "cyan")
    factory = CubeFactory(cube)
    while True:
        try:
            factory.draw(cube)
        except Exception as e:
            break


if __name__ == "__main__":
    main()
