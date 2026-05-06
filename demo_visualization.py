"""
демонстрация визуализации теплопроводности (тест)
"""
import numpy as np
from material import Material
from rod import Rod1D
from visualization import plot_heatmap

def main():
    # создаём стержень из стекла
    glass = Material(
        name="Стекло (оконное)",
        rho=2500,
        c=840,
        k=0.8,
    )

    rod = Rod1D(material=glass, length=0.1, nx=100)  # 10 см, 100 точек

    # левый конец горячий, остальное холодное
    rod.set_initial_condition(
        temp_left=100.0,
        temp_right=0.0,
        uniform=True,
    )

    # моделируем
    total_time = 30.0
    print(f"Моделируется {total_time} секунд...")
    history = rod.solve(total_time)
    print(f"Число временных слоёв: {history.shape[0]}")

    # тепловая карта
    plot_heatmap(
        temp_history=history,
        x=rod.x,
        total_time=total_time,
        title=f"Распространение тепла в стеклянном стержне ({total_time} с)",
    )

if __name__ == "__main__":
    main()