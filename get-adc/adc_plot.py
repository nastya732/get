# adc_plot.py
import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    """
    Строит график зависимости напряжения от времени
    """
    plt.figure(figsize=(10, 6))
    
    # График зависимости напряжений от времени
    plt.plot(time, voltage, 'b-', linewidth=2, label='Напряжение АЦП')
    
    # Названия и подписи
    plt.title('Зависимость напряжения от времени', fontsize=14)
    plt.xlabel('Время, с', fontsize=12)
    plt.ylabel('Напряжение, В', fontsize=12)
    
    # Границы осей
    plt.xlim(0, max(time) if time else 1)
    plt.ylim(0, max_voltage * 1.1)  # +10% для лучшего отображения
    
    # Сетка
    plt.grid(True, alpha=0.3)
    
    # Легенда
    plt.legend()
    
    # Отображение графика
    plt.tight_layout()
    plt.show()