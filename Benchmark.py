from tkinter import Tk, Label, Button, StringVar
import platform
import os
import psutil
from cpuinfo import get_cpu_info
from GPUtil import getGPUs
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def obter_informacoes_placa_mae():
    if os.path.isfile('/sys/devices/virtual/dmi/id/board_name'):
        with open('/sys/devices/virtual/dmi/id/board_name', 'r') as file:
            return file.read().strip()
    else:
        return "Informação não disponível"

def obter_uso_cpu():
    usage = psutil.cpu_percent(interval=1)
    return f"Uso de CPU: {usage}%"

def obter_temperatura_cpu():
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
            temperature = int(file.read()) / 1000
            return f"Temperatura: {temperature}°C"
    else:
        return "Informação não disponível"

def obter_uso_disco():
    usage = psutil.disk_usage('/').percent
    return f"Uso de Disco: {usage}%"

def obter_informacoes_placa_video():
    try:
        gpus = getGPUs()
        gpu = gpus[0]  # Assume que há apenas uma GPU instalada
        gpu_name = gpu.name
        gpu_usage = gpu.load * 100
        gpu_temp = gpu.temperature
        return gpu_name, gpu_usage, gpu_temp
    except:
        return "Informação não disponível"

def exibir_informacoes_sistema():
    root = Tk()
    root.title("Benchmark")

    Label(root, text="Informações do Sistema", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    ram_info = StringVar()
    processador_info = StringVar()
    cores_info = StringVar()
    velocidade_info = StringVar()
    placa_mae_info = StringVar()
    disco_info = StringVar()
    placa_video_info = StringVar()
    uso_gpu_info = StringVar()
    temperatura_info = StringVar()
    sistema_operacional_info = StringVar()
    versao_info = StringVar()
    arquitetura_info = StringVar()

    ram_info.set("")
    processador_info.set("")
    cores_info.set("")
    velocidade_info.set("")
    placa_mae_info.set("")
    disco_info.set("")
    placa_video_info.set("")
    uso_gpu_info.set("")
    temperatura_info.set("")
    sistema_operacional_info.set("")
    versao_info.set("")
    arquitetura_info.set("")

    Label(root, text="Memória RAM:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    Label(root, textvariable=ram_info).grid(row=1, column=1, padx=10, pady=5, sticky="w")

    Label(root, text="Processador:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    Label(root, textvariable=processador_info).grid(row=2, column=1, padx=10, pady=5, sticky="w")
    Label(root, textvariable=cores_info).grid(row=3, column=1, padx=10, pady=5, sticky="w")
    Label(root, textvariable=velocidade_info).grid(row=4, column=1, padx=10, pady=5, sticky="w")

    Label(root, text="Placa-mãe:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    Label(root, textvariable=placa_mae_info).grid(row=5, column=1, padx=10, pady=5, sticky="w")

    Label(root, text="Armazenamento:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    Label(root, textvariable=disco_info).grid(row=6, column=1, padx=10, pady=5, sticky="w")

    Label(root, text="Placa de Vídeo:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
    Label(root, textvariable=placa_video_info).grid(row=7, column=1, padx=10, pady=2, sticky="w")
    Label(root, textvariable=uso_gpu_info).grid(row=8, column=1, padx=10, pady=2, sticky="w")
    Label(root, textvariable=temperatura_info).grid(row=9, column=1, padx=10, pady=2, sticky="w")

    Label(root, text="Sistema Operacional:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
    Label(root, textvariable=sistema_operacional_info).grid(row=10, column=1, padx=10, pady=2, sticky="w")
    Label(root, textvariable=versao_info).grid(row=11, column=1, padx=10, pady=2, sticky="w")
    Label(root, textvariable=arquitetura_info).grid(row=12, column=1, padx=10, pady=2, sticky="w")

    info_label = Label(root, text="Buscando Informações")
    info_label.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

    def atualizar_informacoes():
        info_label.config(text="Buscando informações...")

        ram_info.set(f"Quantidade: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
        cpu_info = get_cpu_info()
        processador_info.set(f"Marca: {cpu_info['brand_raw']}")
        cores_info.set(f"Núcleos: {psutil.cpu_count(logical=True)}")
        velocidade_info.set(f"Velocidade: {psutil.cpu_freq().max:.2f} GHz")
        placa_mae_info.set(obter_informacoes_placa_mae())
        disco_info.set(f"Total: {round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB")
        placa_video = obter_informacoes_placa_video()
        placa_video_info.set(f"Nome: {placa_video[0]}")
        uso_gpu_info.set(f"Uso de GPU: {placa_video[1]:.2f}%")
        temperatura_info.set(f"Temperatura: {placa_video[2]}°C")
        sistema_operacional_info.set(f"Sistema: {platform.uname().system}")
        versao_info.set(f"Versão: {platform.uname().version}")
        arquitetura_info.set(f"Arquitetura: {platform.uname().machine}")

        info_label.config(text="Informações atualizadas")

    def gerar_grafico():
        fig, ax = plt.subplots()
        x = []
        y = []

        def update(i):
            nonlocal x, y
            x.append(i)
            y.append(i ** 2)
            ax.clear()
            ax.plot(x, y)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Teste Gráfico')

        animation = FuncAnimation(fig, update, interval=1000)
        plt.show()

    def finalizar_teste():
        plt.close()  # Fecha a janela do gráfico

    Button(root, text="Iniciar Benchmark", command=atualizar_informacoes).grid(row=14, column=0, padx=10, pady=10)
    Button(root, text="Teste Gráfico", command=gerar_grafico).grid(row=14, column=1, padx=10, pady=10)
    Button(root, text="Finalizar Teste Gráfico", command=finalizar_teste).grid(row=15, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

exibir_informacoes_sistema()