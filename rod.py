"""
моделирование одномерного случая

∂T/∂t = α · ∂²T/∂x²
"""

import numpy as np
from material import Material


class Rod1D:
    """
    одномерный стержень с моделированием распространения тепла

    параметры
    ---------
    material : Material
        материал стержня (определяет температуропроводность α)
    length : float
        длина стержня, метры
    nx : int
        количество узлов пространственной сетки (по умолчанию 50)

    атрибуты
    --------
    dx : float
        шаг пространственной сетки = length / (nx - 1).
    x : np.ndarray
        массив координат узлов, shape = (nx,).
    temp : np.ndarray
        Текущий профиль температуры, shape = (nx,).
    """

    def __init__(self, material: Material, length: float, nx: int = 50):
        if length <= 0:
            raise ValueError("длина стержня должна быть положительной")
        if nx < 3:
            raise ValueError("число узлов должно быть не менее 3")

        self.material = material
        self.length = length
        self.nx = nx

        self.dx = length / (nx - 1)
        self.x = np.linspace(0, length, nx)
        self.temp = np.zeros(nx)

        # граничные условия (будут заданы в set_initial_condition)
        self._bc_left = 0.0
        self._bc_right = 0.0

    def set_initial_condition(self, temp_left: float, temp_right: float, uniform: bool = True) -> None:
        """
        задаёт начальное распределение температуры: линейный профиль
        между двумя концами, которые поддерживаются при постоянной
        температуре

        параметры
        ---------
        temp_left : float
            Температура на левом конце стержня (x = 0) (К)
        temp_right : float
            Температура на правом конце стержня (x = L) (К)
        uniform : bool
        если True: внутри стержня везде temp_right
        если False: внутри стержня везде temp_left
        """
        self._bc_left = temp_left
        self._bc_right = temp_right

        if uniform:
            self.temp = np.full(self.nx, temp_right)
            self.temp[0] = temp_left
        else:
            self.temp = np.full(self.nx, temp_left)
            self.temp[-1] = temp_right

    def _max_time_step(self) -> float:
        """
        вычисляет максимально допустимый шаг по времени из условия
        устойчивости куранта: dt ≤ dx² / (2α)
        для надёжности берётся 30% от теоретического максимума

        возвращает
        -------
        float
            безопасный шаг по времени (с)
        """
        safety = 0.3
        dt_max = self.dx ** 2 / (2 * self.material.alpha)
        return safety * dt_max

    def solve(self, total_time: float) -> np.ndarray:
        """
        запускает симуляцию и возвращает историю температуры

        параметры
        ---------
        total_time : float
            полное время моделирования (с)

        возвращает
        -------
        np.ndarray
            двумерный массив температуры, shape = (nt, nx),
            где nt — число временных слоёв.
            temp_history[n, i] — температура в точке x[i] на шаге n.

        ошибки
        ------
        ValueError
            если total_time отрицательно
        """
        if total_time <= 0:
            raise ValueError("время моделирования должно быть положительным")

        # шаг по времени
        dt = self._max_time_step()

        # число временных слоёв (округляем вверх) (+1 т.к. добавляем начальные значения)
        nt = int(np.ceil(total_time / dt)) + 1

        # массив для хранения всей истории
        temp_history = np.zeros((nt, self.nx)) # T'[]
        temp_history[0] = self.temp.copy()

        # текущий профиль
        current = self.temp.copy()

        F = self.material.alpha * dt / (self.dx ** 2)

        for N in range(1, nt):
            next_temp = current.copy()
            for i in range(1, self.nx - 1):
                next_temp[i] = current[i] + F * (current[i+1] - 2*current[i] + current[i-1])

            # концы при постоянной температуре
            next_temp[0] = self._bc_left
            next_temp[-1] = self._bc_right

            temp_history[N] = next_temp.copy()

            current = next_temp

        # обновляем текущее состояние стержня
        self.temp = current.copy()

        return temp_history