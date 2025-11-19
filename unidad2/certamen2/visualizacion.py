import json
import matplotlib.pyplot as plt
from datetime import datetime
import re

ARCHIVO_LOG = "simulacion.log"
SALIDA_IMAGEN = "visualizacion.png"


eventos = []

with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
    for linea in f:
        try:
            entry = json.loads(linea)
            eventos.append(entry)
        except:
            pass


def convertir_lvt(lvt_str):
    try:
        dt = datetime.fromisoformat(lvt_str)
        return dt.timestamp()
    except:
        return 0.0

for ev in eventos:
    ev["lvt_num"] = convertir_lvt(ev["lvt"])



por_hilo = {}

for ev in eventos:
    h = ev["hilo_id"]
    por_hilo.setdefault(h, []).append(ev)

for h in por_hilo:
    por_hilo[h].sort(key=lambda e: e["lvt_num"])

hilos = sorted(list(por_hilo.keys()))
pos_y = {h: i for i, h in enumerate(hilos)}



SIMBOLOS = {
    "EnvioExterno": ("o", "#1f77b4", "Envío externo"),     # azul
    "RecepcionExterno": ("o", "#2ca02c", "Recepción externa"), # verde
    "ProcesoInterno": ("^", "#ff7f0e", "Evento interno"),      # naranja
    "Checkpoint": ("*", "#17becf", "Checkpoint"),            # cyan
    "RollbackInicio": ("X", "#d62728", "Inicio rollback"),   # rojo
    "RollbackFin": ("D", "#8c2d2d", "Fin rollback"),         # bordó
}



plt.figure(figsize=(20, 12))
max_x = max(ev["lvt_num"] for ev in eventos)


for h, y in pos_y.items():
    plt.hlines(y, 0, max_x, colors="#cccccc", linestyles="dashed", linewidth=1)
    plt.text(-10, y, h, fontsize=12, fontweight="bold", va='center')



for h, lista in por_hilo.items():
    for ev in lista:
        x = ev["lvt_num"]
        y = pos_y[h]
        tipo = ev["evento"]

        simbolo, color, _ = SIMBOLOS.get(tipo, ("s", "black", "Otro"))
        plt.scatter(x, y, marker=simbolo, color=color, s=120, edgecolor="black", linewidth=0.7)



rollback_patron = re.compile(r"LVT=([0-9]{1,2}:[0-9]{2}[APMapm]{2})")

def convertir_hora(hora_str):
    try:
        base = "2020-01-01 "
        dt = datetime.strptime(base + hora_str.upper(), "%Y-%m-%d %I:%M%p")
        return dt.timestamp()
    except:
        return None

for h, lista in por_hilo.items():
    for ev in lista:
        if ev["evento"] == "RollbackInicio":
            msg = ev["mensaje"]
            match = rollback_patron.search(msg)
            if match:
                hora_destino = match.group(1)
                dest_x = convertir_hora(hora_destino)
                if dest_x is None:
                    continue

                origen_x = ev["lvt_num"]
                y = pos_y[h]

                plt.annotate(
                    "",
                    xy=(dest_x, y + 0.05),
                    xytext=(origen_x, y + 0.05),
                    arrowprops=dict(
                        arrowstyle="<|-",
                        color="red",
                        lw=3
                    ),
                )

                # Etiqueta opcional
                plt.text(
                    origen_x,
                    y + 0.18,
                    f"Rollback → {hora_destino}",
                    fontsize=8,
                    color="red"
                )


handles = []
labels = []

for tipo in SIMBOLOS:
    simbolo, color, desc = SIMBOLOS[tipo]
    punto = plt.Line2D([0], [0], marker=simbolo, color=color,
                       markersize=10, linestyle="None")
    handles.append(punto)
    labels.append(desc)

plt.legend(handles, labels, fontsize=12, loc="upper center", ncol=6, frameon=True)



plt.title("Diagrama de Espacio–Tiempo: Time Warp / PDES", fontsize=18, fontweight="bold")
plt.xlabel("Tiempo Virtual (LVT)", fontsize=14)
plt.ylabel("Hilos de Ejecución", fontsize=14)
plt.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(SALIDA_IMAGEN, dpi=300)
print("Visualización generada correctamente:", SALIDA_IMAGEN)
