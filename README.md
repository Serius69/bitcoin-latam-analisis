# ₿ Bitcoin y Criptomonedas — Análisis para Mercado LATAM

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2-purple?style=flat)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)
![Bitcoin](https://img.shields.io/badge/Bitcoin-F7931A?style=flat&logo=bitcoin&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Activo-brightgreen)

Análisis cuantitativo del comportamiento de Bitcoin y criptomonedas principales desde la perspectiva de un inversor latinoamericano. Incluye análisis de volatilidad, drawdown, correlación dinámica con activos LATAM y comparación como cobertura frente a la inflación boliviana.

---

## 🎯 Contexto Bolivia

Con el dólar paralelo boliviano en alza desde 2022 y restricciones cambiarias formales, Bitcoin ha ganado relevancia como alternativa de ahorro e inversión. Este análisis cuantifica tres preguntas clave:

1. ¿Cuánto más volátil es BTC vs activos tradicionales?
2. ¿Está correlacionado con los mercados LATAM o diversifica?
3. ¿Protege contra la inflación boliviana mejor que mantener bolivianos?

---

## 📐 Técnicas Aplicadas

| Técnica | Descripción |
|---|---|
| **Retornos logarítmicos** | Base para todas las métricas estadísticas |
| **Volatilidad rolling 30d** | Volatilidad cambiante en el tiempo (precursor de GARCH) |
| **Drawdown analysis** | Caída máxima desde pico: el peor escenario realista |
| **Correlación rolling 60d** | ¿La correlación con LATAM cambia en crisis? |
| **Sharpe & Sortino Ratio** | Retorno ajustado por riesgo total y riesgo a la baja |
| **Ciclos bull/bear** | Identificación de fases de mercado por retorno 60d |
| **Cobertura vs inflación BO** | Comparación poder adquisitivo BTC vs BOB |

---

## 📊 Activos Analizados

| Ticker | Instrumento | Por qué incluirlo |
|---|---|---|
| `BTC-USD` | Bitcoin | Activo principal del análisis |
| `ETH-USD` | Ethereum | Segunda cripto por capitalización |
| `BNB-USD` | Binance Coin | Referencia exchange LATAM más usado |
| `ILF` | iShares Latin America 40 | Benchmark mercado LATAM |
| `GLD` | SPDR Gold ETF | Activo refugio clásico — benchmark de cobertura |

---

## 📁 Estructura

```
bitcoin-latam-analisis/
├── bitcoin_latam.ipynb       # Análisis completo — exploración y visualizaciones
├── src/
│   └── cripto_metrics.py     # Módulo de métricas reutilizable (CLI)
├── datos/                    # CSVs generados por el script
├── img/                      # Gráficas exportadas
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

```bash
git clone https://github.com/Serius69/bitcoin-latam-analisis
cd bitcoin-latam-analisis

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mkdir -p datos img

# Notebook interactivo
jupyter lab bitcoin_latam.ipynb
```

**Usar el módulo desde CLI:**
```bash
# Análisis con tickers por defecto (BTC, ETH, GLD, ILF)
python src/cripto_metrics.py

# Análisis personalizado
python src/cripto_metrics.py --tickers BTC-USD ETH-USD SOL-USD --inicio 2022-01-01

# Con otra tasa libre de riesgo
python src/cripto_metrics.py --rfr 0.06
```

**Usar como módulo Python:**
```python
from src.cripto_metrics import descargar_precios, metricas_resumen, calcular_drawdown

precios  = descargar_precios(['BTC-USD', 'GLD'], inicio='2023-01-01')
resumen  = metricas_resumen(precios)
print(resumen)
```

---

## 📈 Output del Script

```
Ticker     Retorno Anual %  Volatilidad %  Sharpe  Sortino  Max Drawdown %
BTC-USD          +156.3          73.2       2.10    3.05         -77.2
ETH-USD          +143.8          78.5       1.81    2.67         -81.4
GLD                +8.2          12.1       0.31    0.48         -18.3
ILF               -12.1          22.4      -0.74   -1.02         -44.1
```

---

## ⚠️ Advertencia

Este análisis es educativo. Bitcoin es uno de los activos más volátiles del mercado. Drawdowns del -70 al -80% son frecuentes. No constituye asesoramiento financiero.

---

## 🔗 Proyectos Relacionados

- [💱 Dólar Paralelo Bolivia — ARIMA](https://github.com/Serius69/dolar-paralelo-bolivia-arima)
- [📈 Portafolio de Activos BO](https://github.com/Serius69/portafolio-acciones-bolivia)
- [🇧🇴 Inflación Bolivia — SARIMA](https://github.com/Serius69/inflacion-bolivia-series-tiempo)

---

## 👤 Autor

**Sergio** — Data Scientist en Finanzas | [github.com/Serius69](https://github.com/Serius69)
