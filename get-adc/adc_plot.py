import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage, 'b-', linewidth=2)
    plt.title('Напряжение от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Напряжение (В)')
    plt.grid(True)
    
    # СОХРАНИТЬ В ФАЙЛ (на всякий случай)
    plt.savefig('voltage_plot.png')
    print("✓ График сохранен как 'voltage_plot.png'")
    
    # ПОКАЗАТЬ НА ЭКРАНЕ
    plt.show()
    print("✓ Окно с графиком должно открыться")