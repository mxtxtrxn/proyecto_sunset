# ============================================================
# generar_datos.py
# Genera datos sintéticos para el examen de Sunset World
# Salida: data/leads_ventas.csv y data/fx_historico.csv
# ============================================================

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# Semillas para reproducibilidad
random.seed(42)
np.random.seed(42)

# Ruta de salida (un nivel arriba de src/, dentro de data/)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. leads_ventas.csv (simula tabla Oracle con datos sucios)
# ============================================================
n = 5000

fuentes_raw = [
    "Proveedor A", "proveedor a", "PROVEEDOR A", "ProveedorA",
    "Portal Web", "portal web", "PORTAL WEB",
    "Social", "social", "Facebook", "FB",
    "Calle", "calle", "Calle TMS",
    "RCI", "rci", "OTA", "ota",
    "Hotel", "hotel", None, "", "N/A"
]

salas = [
    "Cancún", "cancún", "CANCÚN", "Playa del Carmen", "PDC",
    "Puerto Vallarta", "PV", "Los Cabos", "Cabo", "cabo"
]

comentarios_ok = [
    "Cliente interesado, pidió información por email.",
    "No contesta llamadas, dejar seguimiento.",
    "Solicitó cotización para 2 adultos y 2 niños.",
    "Muy interesado, agendar presentación.",
    "Pidió hablar con supervisor.",
    "Ya había hecho tour antes.",
    "Prefiere destino de playa.",
    "Objeción de precio, volver a llamar.",
    "Cliente molesto por llamadas repetidas.",
    "Solicitó cancelar su registro."
]

data = []
for i in range(n):
    lead_id = 100000 + i
    fuente = random.choice(fuentes_raw)
    fecha_creacion = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))

    # 60% de leads con venta
    if random.random() < 0.60:
        fecha_venta = fecha_creacion + timedelta(days=random.randint(1, 90))
        monto = round(random.uniform(15000, 250000), 2)
        vpg = round(random.uniform(500, 8000), 2)
    else:
        fecha_venta = None
        monto = None
        vpg = None

    sala = random.choice(salas)
    comentario = random.choice(comentarios_ok) if random.random() < 0.7 else None

    data.append([lead_id, fuente, fecha_creacion, fecha_venta,
                 monto, vpg, sala, comentario])

# Duplicados intencionales (5% de los registros)
duplicados = random.sample(data, int(n * 0.05))
data.extend(duplicados)

# Nulos adicionales en monto/vpg (10%)
for row in data:
    if random.random() < 0.10 and row[4] is not None:
        row[4] = None
    if random.random() < 0.10 and row[5] is not None:
        row[5] = None

df_leads = pd.DataFrame(data, columns=[
    "lead_id", "fuente", "fecha_creacion", "fecha_venta",
    "monto", "vpg", "sala", "comentarios"
])

ruta_leads = os.path.join(OUTPUT_DIR, "leads_ventas.csv")
df_leads.to_csv(ruta_leads, index=False)
print(f"⚠️ leads_ventas.csv generado: {len(df_leads)} registros en {ruta_leads}")


# ============================================================
# 2. fx_historico.csv (serie mensual MXN/USD 2014–2024)
# ============================================================
fechas = pd.date_range(start="2014-01-01", end="2024-12-01", freq="MS")
n_fx = len(fechas)

# Serie simulada con tendencia, estacionalidad y ruido
np.random.seed(7)
tendencia = np.linspace(13.0, 20.0, n_fx)
estacionalidad = 0.5 * np.sin(np.linspace(0, 8 * np.pi, n_fx))
ruido = np.random.normal(0, 0.4, n_fx)
tipo_cambio = tendencia + estacionalidad + ruido

tasa_interes = (
    4.0
    + 2.0 * np.sin(np.linspace(0, 4 * np.pi, n_fx))
    + np.random.normal(0, 0.3, n_fx)
)

inflacion = (
    3.5
    + 1.5 * np.sin(np.linspace(0, 6 * np.pi, n_fx))
    + np.random.normal(0, 0.2, n_fx)
)

df_fx = pd.DataFrame({
    "fecha": fechas.strftime("%Y-%m-%d"),
    "tipo_cambio": np.round(tipo_cambio, 4),
    "tasa_interes": np.round(tasa_interes, 4),
    "inflacion": np.round(inflacion, 4),
})

# Insertar algunos nulos intencionales (2%)
idx_nulos = np.random.choice(df_fx.index, size=int(n_fx * 0.02), replace=False)
df_fx.loc[idx_nulos, "tipo_cambio"] = None

ruta_fx = os.path.join(OUTPUT_DIR, "fx_historico.csv")
df_fx.to_csv(ruta_fx, index=False)
print(f"📈 fx_historico.csv generado: {len(df_fx)} registros en {ruta_fx}")