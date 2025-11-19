import subprocess
import time
import matplotlib.pyplot as plt
import statistics

# Configuración
EVENTOS = 5000  # Número de eventos
WORKERS = [1, 2, 4, 8]  # Diferentes números de workers
REPETICIONES = 30   # Número de ejecuciones por cada caso
CMD_BASE = ["go", "run", ".", "-num_eventos_ext", str(EVENTOS)]  # Comando base

def ejecutar(workers):
    """Función para ejecutar la simulación con el número de workers especificado."""
    cmd = CMD_BASE + ["-num_workers", str(workers), "-destino", f"sim_{workers}w.log"]
    inicio = time.time()
    salida = subprocess.run(cmd, capture_output=True, text=True)
    fin = time.time()
    duracion = fin - inicio
    print(salida.stdout)
    return duracion

def main():
    tiempos_promedio = {}

    print("\n=== EJECUCIÓN AUTOMÁTICA DE ESCALABILIDAD ===\n")

    # Ejecutar simulación para cada cantidad de workers
    for w in WORKERS:
        print(f"\n>> Ejecutando {REPETICIONES} veces con {w} workers...")
        resultados = []
        for i in range(REPETICIONES):
            print(f"   Corrida {i+1}/{REPETICIONES}...")
            t = ejecutar(w)
            resultados.append(t)

        tiempos_promedio[w] = statistics.mean(resultados)
        print(f"Tiempo promedio con {w} workers: {tiempos_promedio[w]:.6f}s")

    # Cálculo de speedup
    T1 = tiempos_promedio[1]  # Tiempo con 1 worker
    speedup = {w: T1 / tiempos_promedio[w] for w in WORKERS}

    # Mostrar los resultados
    print("\n=== SPEEDUP PROMEDIO ===")
    for w, s in speedup.items():
        print(f"S({w}) = {s:.4f}")

    # ===============================
    # GRÁFICO: Tiempos Promedio vs Workers
    # ===============================
    plt.figure(figsize=(12, 6))
    plt.plot(WORKERS, [tiempos_promedio[w] for w in WORKERS], marker='s', linewidth=3, color='purple', label="Tiempo Promedio")
    plt.title("Tiempos Promedio vs Workers", fontsize=16)
    plt.xlabel("Número de Workers", fontsize=14)
    plt.ylabel("Tiempo (s)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.xticks(WORKERS)
    plt.legend()
    plt.savefig("tiempos_promedio.png", dpi=300)
    print("Gráfico guardado como 'tiempos_promedio.png'")

    # ===============================
    # GRÁFICO: Speedup Real vs Ideal
    # ===============================
    plt.figure(figsize=(12, 6))
    plt.plot(WORKERS, [speedup[w] for w in WORKERS], marker='o', linewidth=3, label="Speedup Real")
    plt.plot(WORKERS, WORKERS, linestyle='--', color='gray', linewidth=2, label="Speedup Ideal")
    plt.title("Escalabilidad – Speedup Promedio vs Workers", fontsize=16)
    plt.xlabel("Número de Workers", fontsize=14)
    plt.ylabel("Speedup", fontsize=14)
    plt.xticks(WORKERS)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    plt.savefig("speedup.png", dpi=300)
    print("Gráfico guardado como 'speedup.png'")

    # ===============================
    # GRÁFICO: Speedup en Porcentaje
    # ===============================
    # Calcular speedup en términos porcentuales
    speedup_porcentaje = {w: (speedup[w] - 1) * 100 for w in WORKERS}

    plt.figure(figsize=(12, 6))
    plt.plot(WORKERS, [speedup_porcentaje[w] for w in WORKERS], marker='o', linewidth=3, color='orange', label="Speedup (%)")
    plt.title("Speedup Expresado en Porcentaje", fontsize=16)
    plt.xlabel("Número de Workers", fontsize=14)
    plt.ylabel("Mejora (%) respecto a 1 Worker", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.xticks(WORKERS)
    plt.legend()
    plt.savefig("speedup_porcentaje.png", dpi=300)
    print("Gráfico guardado como 'speedup_porcentaje.png'")

    print("\n=== ANÁLISIS COMPLETO ===")
    print("Se midieron los tiempos, se calculó el speedup y se generaron los gráficos obligatorios.")

if __name__ == "__main__":
    main()
