from typing import Callable

import numpy as np

# The optimal step size is the cube root of machine epsilon
step = np.power(np.finfo(float).eps, 1 / 3)


class Differentiator:

    @staticmethod
    def _first_order(f: Callable[[float], float], x: float) -> float:
        return (f(x + step) - f(x - step)) / (2 * step)

    @staticmethod
    def _second_order(f: Callable[[float], float], x: float) -> float:
        return (f(x + step) - 2 * f(x) + f(x - step)) / step ** 2

    @staticmethod
    def numeric_derivative(f: Callable[[float], float], x: float, order: int) -> float:
        if order == 1:
            return Differentiator._first_order(f, x)
        elif order == 2:
            return Differentiator._second_order(f, x)
        else:
            raise NotImplementedError(f'The order {order} has not been implemented.')


if __name__ == '__main__':
    print(step)
