import numpy as np
from material import Material
from rod import Rod1D

# Материал — алюминий
al = Material(name="Алюминий", rho=2700, c=900, k=207)

# Стержень длиной 1 метр, 50 точек
rod = Rod1D(material=al, length=1.0, nx=50)

# В начальный момент: левый конец 100°C, правый 0°C
rod.set_initial_condition(temp_left=100.0, temp_right=0.0, uniform=True)

# Симулируем 100 секунд
history = rod.solve(total_time=100.0)

print(f"Форма массива history: {history.shape}")
print(f"Температура в середине стержня в конце: {rod.temp[25]:.1f} °C")
print(f"Максимальный шаг по времени: {rod._max_time_step():.4f} с")
print("Массив history:")
print(history)