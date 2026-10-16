# Informe Ejecutivo — Limpieza y Enriquecimiento de Leads
**Proyecto:** Sunset World · Data Scientist Exam
**Fecha:** [Fecha de entrega]
**Autor:** [Tu nombre]
**Parte:** 1 de 5 — Extracción y limpieza de datos (Oracle simulado)

---

## 1. Resumen ejecutivo

El dataset `leads_ventas.csv` (5,250 registros simulando una tabla Oracle legada) presentaba tres problemas críticos de calidad: **47% de nulos en variables monetarias**, **5% de duplicados exactos** y **fragmentación severa en las columnas categóricas** (`fuente` con 20 variantes del mismo valor, `sala` con 10). Tras aplicar un pipeline de limpieza en cuatro etapas, el dataset quedó reducido a **5,000 registros únicos y normalizados**, listo para alimentar modelos de propensión y análisis de negocio.

## 2. Diagnóstico inicial

**Dimensiones:** 5,250 filas × 8 columnas.

**Calidad de datos:**
- Nulos concentrados en `monto` (47.0%), `vpg` (46.6%), `fecha_venta` (40.3%), `comentarios` (29.6%) y `fuente` (12.6%).
- Los nulos de `fecha_venta`, `monto` y `vpg` corresponden a leads **no convertidos** (información válida, no error).
- **Problema crítico detectado:** ~7% de registros con venta confirmada pero sin valor monetario capturado.
- 250 duplicados exactos (5% del total).

**Fragmentación categórica:**
- `fuente`: 20 valores únicos que en realidad representan 6 categorías reales (ej. `Proveedor A`, `proveedor a`, `PROVEEDOR A`, `ProveedorA`).
- `sala`: 10 valores únicos que representan 4 salas reales (ej. `Cancún`, `cancún`, `CANCÚN`).

*Referencia: exploración detallada en Celdas 3–10 del notebook `parte1_limpieza.ipynb`.*

## 3. Acciones aplicadas

**Normalización de texto:** función `normalizar_texto()` con minúsculas, eliminación de espacios y remoción de acentos, seguida de mapeo a categorías canónicas mediante diccionario.

| Columna | Antes | Después | Reducción |
|---|---|---|---|
| `fuente` | 20 valores | 7 valores | −65% |
| `sala` | 10 valores | 4 valores | −60% |

**Tratamiento de nulos (sin eliminar registros):**
- `comentarios` → relleno con `"Sin comentarios"`.
- `monto` y `vpg` → imputación por **mediana de sala**, aplicada **solo** donde existe `fecha_venta` (evita inventar datos en leads no convertidos).
- `fuente` → relleno con `"Desconocido"`.
- `fecha_venta` → se deja como nula (indica lead no convertido).

**Duplicados:** eliminación con `drop_duplicates()`. Criterio: los 250 duplicados eran **copias exactas en todas las columnas** — no había conflicto de información entre salas.

**Enriquecimiento:** creación de `mes_venta` y `año_venta`, más cálculos de tasa de conversión por fuente y VPG promedio por sala.

## 4. Resultados de negocio

**Tasa de conversión por fuente (post-limpieza):**

| Fuente | Leads | Ventas | Tasa |
|---|---|---|---|
| Hotel | 471 | 295 | **62.6%** |
| Social | 889 | 548 | 61.6% |
| RCI | 404 | 246 | 60.9% |
| Calle | 676 | 409 | 60.5% |
| OTA | 409 | 244 | 59.7% |
| Desconocido | 633 | 374 | 59.1% |
| Portal Web | 652 | 382 | 58.6% |
| Proveedor A | 866 | 498 | **57.5%** |

**VPG promedio por sala:**

| Sala | VPG medio | VPG mediana | N ventas |
|---|---|---|---|
| Cancún | $4,331.34 | $4,389.94 | 854 |
| Los Cabos | $4,224.63 | $4,144.76 | 904 |
| Playa del Carmen | $4,208.97 | $4,232.11 | 624 |
| Puerto Vallarta | $4,161.33 | $4,006.63 | 614 |

*Referencia: gráficos de barras en Celdas 18 y 19 del notebook.*

## 5. Hallazgo clave para el negocio

Antes de normalizar, la fuente "Proveedor A" parecía tener una tasa de conversión mediocre (52–61% según la variante analizada). **Tras consolidar sus 4 variantes, emerge como el canal con mejor desempeño relativo por volumen** (866 leads, 57.5%) junto con Hotel (62.6%) y Social (61.6%). Este tipo de insight solo es visible tras una limpieza correcta de categorías.

## 6. Decisiones documentadas (preguntas abiertas)

**¿Cómo manejar duplicados dependientes de la sala?** Si un mismo `lead_id` apareciera en dos salas distintas, no se trataría como duplicado sino como **evento de negocio** (transferencia legítima). Regla adoptada: eliminar solo duplicados exactos en todas las columnas; conservar registros con sala distinta y marcarlos con bandera `transferido = True`.

**¿Qué hacer sin diccionario de datos?** Proceso de reconstrucción en cuatro pasos: (1) inferencia por nombre + tipo + distribución; (2) entrevistas con usuarios del sistema; (3) trazabilidad hacia el ETL origen; (4) documentación progresiva en un diccionario provisional validado con negocio.

## 7. Entregables

- **Notebook:** `parte1_limpieza.ipynb`
- **Dataset limpio:** `data/leads_ventas_clean.csv` (5,000 × 8)
- **Este informe:** `reports/informe_parte1.pdf`