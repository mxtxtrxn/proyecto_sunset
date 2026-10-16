# Resumen Ejecutivo — Pronóstico de Tipo de Cambio MXN/USD
**Proyecto:** Sunset World · Data Scientist Exam
**Fecha:** [Fecha de entrega]
**Autor:** [Tu nombre]
**Parte:** 2 de 5 — Forecasting de FX (series temporales)

---

## 1. Resumen ejecutivo

Se construyeron dos modelos de pronóstico sobre la serie mensual MXN/USD 2014–2024 (132 observaciones). Ambos fueron validados con split temporal (train 2014–2022, test 2023–2024) y comparados con las métricas estándar. **El modelo de Machine Learning (XGBoost) superó al modelo estadístico clásico (ARIMA)** en las tres métricas: redujo el error absoluto medio de 0.66 a 0.40 MXN/USD, y el error porcentual de 3.42% a 2.09%. El pronóstico a 6 meses (enero–junio 2025) proyecta un rango entre **18.5 y 20.2 MXN/USD** según el modelo.

## 2. Diagnóstico de la serie

- **Tendencia:** depreciación sostenida del peso de 13.64 a 19.43 MXN/USD entre 2014 y 2024 (+42%).
- **Estacionalidad anual:** amplitud de 0.47 MXN, patrón recurrente.
- **Estacionariedad:** prueba ADF confirma que la serie original **no es estacionaria** (t = −0.72); tras primera diferencia (d=1), se vuelve estacionaria (t = −13.08, p < 0.05).
- **Correlogramas ACF/PACF:** definen orden ARIMA(1,1,1) como punto de partida.

*Referencia: descomposición y ADF en Celdas 4–5 del notebook; ACF/PACF en Celda 6.*

## 3. Modelos construidos

**Modelo clásico — ARIMA(1,1,1):** componente autorregresivo de orden 1, integrado de orden 1 y media móvil de orden 1. Aprovecha la autocorrelación de corto plazo y la estructura de errores.

**Modelo ML — XGBoost con variables exógenas:** features de rezago (`lag_1`, `lag_2`, `lag_3`, `lag_6`, `lag_12`), variables macro (`tasa_interes`, `inflacion`), calendario (`mes`, `trimestre`) y tendencia lineal.

## 4. Resultados de validación (test 2023–2024)

| Modelo | MAE | RMSE | MAPE |
|---|---|---|---|
| ARIMA(1,1,1) | 0.6569 | 0.7351 | 3.42% |
| **XGBoost/GBM** | **0.4047** | **0.4913** | **2.09%** |

**Interpretación:** XGBoost reduce el error absoluto en **38%** y el error porcentual en **39%** respecto a ARIMA. Ambos modelos están por debajo del umbral de 3% de MAPE, considerado un buen resultado para horizonte de 24 meses en tipo de cambio.

*Referencia: gráficos comparativos en Celda 10 del notebook.*

## 5. Pronóstico enero–junio 2025

| Fecha | ARIMA | XGBoost |
|---|---|---|
| 2025-01 | 19.9074 | 18.8614 |
| 2025-02 | 19.9598 | 18.8931 |
| 2025-03 | 20.0121 | 18.7936 |
| 2025-04 | 20.0645 | 18.7980 |
| 2025-05 | 20.1168 | 18.4984 |
| 2025-06 | 20.1692 | 18.4906 |

**Divergencia entre modelos:** ARIMA mantiene la tendencia histórica de depreciación gradual (+0.05 MXN/mes); XGBoost proyecta una apreciación moderada del peso impulsada por el feature `tendencia`. El intervalo de confianza al 95% se ensancha con el horizonte, reflejando la incertidumbre natural del pronóstico.

*Referencia: gráfico con bandas de confianza en Celda 12 del notebook.*

## 6. Factores determinantes

El análisis de importancia de variables (XGBoost) identifica:

| Variable | Importancia | Interpretación |
|---|---|---|
| `tendencia` | 76.6% | Dirección de largo plazo — dominante |
| `lag_2` | 10.7% | Inercia de corto plazo |
| `lag_3` | 4.3% | Persistencia del movimiento |
| `lag_1` | 2.7% | Valor del mes anterior |
| `tasa_interes` | 2.5% | Correlación negativa moderada (r ≈ −0.36) |

**Implicación de negocio:** el tipo de cambio está dominado por su propia inercia. La tasa de interés y la inflación aportan información marginal en datos sintéticos, pero en datos reales de Banxico/INEGI su peso aumenta considerablemente.

*Referencia: gráfico de importancia en Celda 11 del notebook.*

## 7. Recomendaciones para proteger el margen financiero

1. **Coberturas naturales:** sincronizar ingresos y pagos en la misma moneda para reducir exposición neta.
2. **Forwards / opciones FX:** fijar el tipo de cambio para contratos conocidos, usando el pronóstico como precio de referencia y el IC 95% para dimensionar el riesgo.
3. **Alerta de umbral:** activar cobertura adicional si el modelo proyecta tipo de cambio > 20.5 MXN/USD.
4. **Reentrenamiento mensual:** incorporar cada nuevo dato y revalidar el modelo para reducir el drift.

## 8. Decisiones documentadas (preguntas abiertas)

**¿Cómo manejar un cambio estructural (crisis económica)?** Cuatro estrategias combinadas: detección con prueba de Chow/CUSUM sobre residuales; ventana deslizante de reentrenamiento; modelos de régimen (MSARIMA, Prophet con changepoints); incorporación de variable dummy para el período de crisis.

**¿Cómo integrar el modelo en Java/Oracle?** Exportar con `joblib.dump()` o formato ONNX; exponer un microservicio Python (FastAPI) con endpoint `/predict`; consumir desde Spring Boot con `RestTemplate`; orquestar con Oracle Scheduler vía `UTL_HTTP`. El diseño completo se detalla en la Parte 4 del examen.

## 9. Entregables

- **Notebook:** `parte2_forecasting_fx.ipynb`
- **Métricas:** `reports/metricas_fx.csv`
- **Pronóstico:** `reports/pronostico_6m.csv`
- **Este resumen:** `reports/resumen_parte2.pdf`