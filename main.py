"""
демонстрация моделирования теплопроводности
"""

from material import Material
from rod import Rod1D
from visualization import plot_heatmap

MATERIALS = {
    "Алюминий": Material(
        name="Алюминий",
        rho=2700,
        c=900,
        k=237,
    ),
    "Медь": Material(
        name="Медь",
        rho=8960,
        c=385,
        k=401,
    ),
    "Сталь": Material(
        name="Сталь",
        rho=7800,
        c=460,
        k=50,
    ),
    "Стекло": Material(
        name="Стекло",
        rho=2500,
        c=840,
        k=0.8,
    ),
    "Дерево": Material(
        name="Дерево",
        rho=500,
        c=2300,
        k=0.15,
    ),
}


def run_simulation(
    material_key: str = "Алюминий",
    length: float = 0.1,
    nx: int = 100,
    temp_left: float = 373.0,
    temp_right: float = 273.0,
    uniform: bool = True,
    total_time: float = 60.0,
    show_heatmap: bool = True,
    save_heatmap: str | None = None,
) -> None:
    """
    запускает симуляцию теплопроводности для одномерного стержня

    параметры
    ---------
    material_key : str
        ключ материала из словаря MATERIALS
    length : float
        длина стержня, метры
    nx : int
        число точек пространственной сетки
    temp_left : float
        температура на левом конце стержня
    temp_right : float
        температура на правом конце стержня
    uniform : bool
        если True — стержень изначально при temp_right, левый конец temp_left
        если False — стержень изначально при temp_left, правый конец temp_right
    total_time : float
        время моделирования (с)
    show_heatmap : bool
        показать тепловую карту
    save_heatmap : str или None
        путь для сохранения тепловой карты
    """

    if material_key not in MATERIALS:
        print(f"Ошибка: материал '{material_key}' не найден")
        return

    material = MATERIALS[material_key]

    rod = Rod1D(material=material, length=length, nx=nx)

    rod.set_initial_condition(
        temp_left=temp_left,
        temp_right=temp_right,
        uniform=uniform,
    )

    dt = rod._max_time_step()
    nt_est = int(total_time / dt) + 1

    print("=" * 60)
    print(f"Материал:                   {material.name}")
    print(f"Длина стержня:              {length:.3f} м")
    print(f"Точек сетки:                {nx}")
    print(f"α (температуропроводность): {material.alpha:.3e} м²/с")
    print(f"Δt (шаг по времени):        {dt:.4f} с")
    print(f"Оценка числа слоёв:         {nt_est}")
    print(f"Время моделирования:        {total_time:.1f} с")
    print(f"Левая граница:              {temp_left:.1f} К")
    print(f"Правая граница:             {temp_right:.1f} К")
    print(f"Начальное состояние: {'правое значение' if uniform else 'левое значение'}")
    print("=" * 60)

    print("Идёт моделирование...")
    history = rod.solve(total_time)
    print(f"Число слоёв: {history.shape[0]}")
    print(f"Конечная температура в середине: {rod.temp[nx // 2]:.2f} К")
    print()

    if show_heatmap:
        plot_heatmap(
            temp_history=history,
            x=rod.x,
            total_time=total_time,
            title=f"{material.name}: распространение тепла (стержень, {total_time:.0f} с)",
            save_path=save_heatmap,
        )

# ============================================================
def main():
    """
    точка входа. можно менять параметры для разных экспериментов.
    """
    # эксперимент 1: Алюминий
    run_simulation(
        material_key="Алюминий",
        length=0.1,
        nx=100,
        temp_left=373.0,
        temp_right=273.0,
        uniform=True,
        total_time=60.0,
        show_heatmap=True,
        save_heatmap="exp1_aluminium_60s.png",
    )

    # эксперимент 2: Стекло
    run_simulation(
        material_key="Стекло",
        length=0.1,
        nx=100,
        temp_left=373.0,
        temp_right=273.0,
        uniform=True,
        total_time=60.0,
        show_heatmap=True,
        save_heatmap="exp2_glass_60s.png",
    )

    # эксперимент 3: Дерево
    run_simulation(
        material_key="Дерево",
        length=0.1,
        nx=100,
        temp_left=373.0,
        temp_right=273.0,
        uniform=True,
        total_time=60.0,
        show_heatmap=True,
    )

    # эксперимент 4: Алюминий
    run_simulation(
        material_key="Алюминий",
        length=0.5,
        nx=100,
        temp_left=373.0,
        temp_right=273.0,
        uniform=True,
        total_time=60.0,
        show_heatmap=True,
    )

    # эксперимент 5: Алюминий
    run_simulation(
        material_key="Алюминий",
        length=0.1,
        nx=100,
        temp_left=373.0,
        temp_right=273.0,
        uniform=True,
        total_time=120.0,
        show_heatmap=True,
    )

if __name__ == "__main__":
    main()