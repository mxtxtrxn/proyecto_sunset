# Proyecto Sunset World — Examen Técnico Data Scientist

**Candidato:** [Tu nombre]
**Fecha:** [Fecha de entrega]
**Contacto:** [tu_email@dominio.com]

Repositorio con la solución completa al examen técnico de Data Science
para Sunset World. Cubre limpieza de datos legados, forecasting de FX,
diseño de un agente de verificación con IA y propuesta de integración
con sistemas legados (Java/Oracle).

---

## Tabla de contenidos

- [Contexto del proyecto](#contexto-del-proyecto)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Requisitos previos](#requisitos-previos)
- [Cómo reproducir](#cómo-reproducir)
- [Resumen por parte](#resumen-por-parte)
- [Decisiones técnicas clave](#decisiones-técnicas-clave)
- [Resultados destacados](#resultados-destacados)
- [Supuestos y limitaciones](#supuestos-y-limitaciones)

---

## Contexto del proyecto

Sunset World es un grupo turístico con múltiples sistemas fragmentados
(Voltux CRM, Share CRM, TMS, Call Center, Finanzas). El examen evalúa
la capacidad de:

1. Trabajar con datos legados, sucios y fragmentados.
2. Construir modelos de forecasting aplicados a tipos de cambio.
3. Diseñar agentes de IA con guardrails y trazabilidad.
4. Proponer integraciones con stack existente (Java 11 / Oracle 11g).

La plataforma objetivo es **Mantis** (multi-modal, RAG, embeddings, agentes).

---

## Estructura del repositorio
proyecto_sunset/
├── data/
│ ├── leads_ventas.csv # Dataset sucio (input Parte 1)
│ ├── leads_ventas_clean.csv # Dataset limpio (output Parte 1)
│ ├── fx_historico.csv # Serie MXN/USD 2014-2024 (input Parte 2)
│ └── fx_forecast.csv # Pronóstico 6 meses (output Parte 2)
├── notebooks/
│ ├── parte1_limpieza.ipynb # Carga, limpieza, enriquecimiento
│ └── parte2_forecasting_fx.ipynb # EDA, ARIMA, XGBoost, pronóstico
├── src/
│ └── generar_datos.py # Script de generación de datos sintéticos
├── reports/
│ ├── informe_parte1.pdf # Informe ejecutivo 1 pág (Parte 1)
│ ├── resumen_parte2.pdf # Resumen ejecutivo 1 pág (Parte 2)
│ ├── parte3_agente_verificacion.pdf # Diseño del agente (Parte 3)
│ ├── parte4_integracion_legados.pdf # Diseño de integración (Parte 4)
│ ├── metricas_fx.csv # MAE/RMSE/MAPE ARIMA vs XGBoost
│ └── pronostico_6m.csv # Pronóstico enero-junio 2025
├── requirements.txt # Dependencias con versiones
├── README.md # Este archivo
└── LICENSE # (Opcional) MIT o similar


---

## Requisitos previos

- **Python 3.11+**
- **Jupyter Notebook** o JupyterLab (o VS Code con extensión Jupyter)
- **Git** (para clonar el repo si es necesario)

**Dependencias principales** (ver `requirements.txt` para versiones exactas):
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
missingno>=0.5
scikit-learn>=1.3
xgboost>=2.0
statsmodels>=0.14
jupyter>=1.0



