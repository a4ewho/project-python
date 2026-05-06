"""
визуализация результатов моделирования теплопроводности
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_heatmap(
        temp_history: np.ndarray,
        x: np.ndarray,
        total_time: float,
        title: str = "Распространение тепла в стержне",
        save_path: str | None = None,
) -> None:
    """
    строит тепловую карту (heatmap) распределения температуры T(x, t).

    параметры
    ---------
    temp_history : np.ndarray
        двумерный массив температуры, shape = (nt, nx)
    x : np.ndarray
        координаты узлов, shape = (nx,)
    total_time : float
        полное время моделирования (для оси y)
    title : str
        заголовок графика
    save_path : str или None
        если указан — сохраняет график в файл
    """
    nt, nx = temp_history.shape

    fig, ax = plt.subplots(figsize=(10, 6))

    # тепловая карта
    im = ax.pcolormesh(
        x,  # координаты x
        np.linspace(0, total_time, nt),  # временные слои
        temp_history,  # значения температуры
        cmap="hot",  # цветовая схема: чёрный → красный → жёлтый → белый
        shading="auto",
    )

    # цветовая шкала
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Температура", fontsize=12)

    ax.set_xlabel("Координата x, м", fontsize=12)
    ax.set_ylabel("Время t, с", fontsize=12)
    ax.set_title(title, fontsize=14)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"График сохранён: {save_path}")

    plt.show()