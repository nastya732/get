# adc_plot.py
import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    """
    Строит график зависимости напряжения от времени
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(time, voltage, 'b-', linewidth=2, label='Напряжение АЦП')
    plt.title('Зависимость напряжения от времени', fontsize=14)
    plt.xlabel('Время, с', fontsize=12)
    plt.ylabel('Напряжение, В', fontsize=12)
    plt.xlim(0, max(time) if time else 1)
    plt.ylim(0, max_voltage * 1.1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_sampling_period_hist(time):
    """
    Строит распределение количества измерений по их продолжительности
    """
    # Создаем список для хранения промежутков времени между измерениями
    sampling_periods = []
    
    # Заполняем список разницами между соседними моментами времени
    for i in range(1, len(time)):
        period = time[i] - time[i-1]
        sampling_periods.append(period)
    
    # Создаем окно для отображения графика
    plt.figure(figsize=(10, 6))
    
    # Размещаем гистограмму периодов измерений
    plt.hist(sampling_periods, bins=20, alpha=0.7, edgecolor='black')
    
    # Название графика и осей
    plt.title('Распределение периодов измерений', fontsize=14)
    plt.xlabel('Период измерения, с', fontsize=12)
    plt.ylabel('Количество измерений', fontsize=12)
    
    # Границы по оси X
    plt.xlim(0, 0.06)
    
    # Включение сетки
    plt.grid(True, alpha=0.3)
    
    # Отображение гистограммы
    plt.tight_layout()
    plt.show()
    
    # Вывод статистики
    if sampling_periods:
        print(f"Средний период измерений: {sum(sampling_periods)/len(sampling_periods):.4f} с")
        print(f"Минимальный период: {min(sampling_periods):.4f} с")
        print(f"Максимальный период: {max(sampling_periods):.4f} с")