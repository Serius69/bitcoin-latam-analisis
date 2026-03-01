"""
src/cripto_metrics.py
─────────────────────────────────────────────────────────────────────────────
Módulo de métricas cuantitativas para análisis de criptomonedas.
Reutilizable como librería en otros proyectos.

Uso:
    python src/cripto_metrics.py --tickers BTC-USD ETH-USD --inicio 2022-01-01
"""

import argparse
import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats


# ─── MÉTRICAS ────────────────────────────────────────────────────────────────

def descargar_precios(tickers: list, inicio: str, fin: str = None) -> pd.DataFrame:
    """Descarga precios de cierre ajustados desde Yahoo Finance."""
    raw    = yf.download(tickers, start=inicio, end=fin, auto_adjust=True)
    precios = raw['Close'].dropna()
    print(f"✅ {len(precios)} días | {precios.columns.tolist()}")
    return precios


def retornos_log(precios: pd.DataFrame) -> pd.DataFrame:
    """Retornos logarítmicos diarios."""
    return np.log(precios / precios.shift(1)).dropna()


def calcular_drawdown(serie: pd.Series) -> pd.Series:
    """Drawdown desde máximo histórico acumulado (en %)."""
    maximo = serie.cummax()
    return (serie - maximo) / maximo * 100


def metricas_resumen(precios: pd.DataFrame, tasa_libre_riesgo: float = 0.045) -> pd.DataFrame:
    """
    Calcula tabla resumen de métricas anualizadas para cada activo.
    
    Returns DataFrame con columnas:
        Retorno Anual, Volatilidad, Sharpe, Sortino, Max Drawdown,
        Sesgo, Curtosis, VaR 95%
    """
    retornos  = retornos_log(precios)
    dias      = 252
    resultados = []

    for ticker in precios.columns:
        r  = retornos[ticker].dropna()
        p  = precios[ticker].dropna()
        dd = calcular_drawdown(p)

        ret_anual  = r.mean() * dias
        vol_anual  = r.std()  * np.sqrt(dias)
        sharpe     = (ret_anual - tasa_libre_riesgo) / vol_anual

        # Sortino: penaliza solo la volatilidad negativa
        ret_neg    = r[r < 0]
        sortino    = (ret_anual - tasa_libre_riesgo) / (ret_neg.std() * np.sqrt(dias))

        # VaR paramétrico 95%
        var_95     = stats.norm.ppf(0.05, r.mean(), r.std()) * 100

        resultados.append({
            'Ticker':           ticker,
            'Retorno Anual %':  round(ret_anual * 100, 2),
            'Volatilidad %':    round(vol_anual * 100, 2),
            'Sharpe':           round(sharpe, 3),
            'Sortino':          round(sortino, 3),
            'Max Drawdown %':   round(dd.min(), 2),
            'Sesgo':            round(r.skew(), 3),
            'Curtosis':         round(r.kurtosis(), 3),
            'VaR 95% (diario)': round(var_95, 3),
        })

    return pd.DataFrame(resultados).set_index('Ticker')


def correlacion_rolling(retornos: pd.DataFrame, t1: str, t2: str,
                         window: int = 60) -> pd.Series:
    """Correlación rolling entre dos activos."""
    return retornos[t1].rolling(window).corr(retornos[t2])


def ciclos_mercado(precios_btc: pd.Series, umbral_bull: float = 0.20,
                   umbral_bear: float = -0.20) -> pd.DataFrame:
    """
    Identifica períodos bull/bear/lateral en Bitcoin.
    
    Bull: retorno 60d > umbral_bull
    Bear: retorno 60d < umbral_bear
    Lateral: entre ambos umbrales
    """
    ret_60d = precios_btc.pct_change(60)
    ciclos  = pd.Series('Lateral', index=precios_btc.index)
    ciclos[ret_60d >  umbral_bull] = 'Bull'
    ciclos[ret_60d <  umbral_bear] = 'Bear'

    resumen = ciclos.value_counts()
    pct     = (resumen / len(ciclos) * 100).round(1)
    df_ciclos = pd.DataFrame({'Días': resumen, 'Porcentaje %': pct})
    return ciclos, df_ciclos


# ─── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Métricas cuantitativas para criptomonedas')
    parser.add_argument('--tickers', nargs='+', default=['BTC-USD', 'ETH-USD', 'GLD', 'ILF'],
                        help='Lista de tickers Yahoo Finance')
    parser.add_argument('--inicio', default='2020-01-01', help='Fecha inicio YYYY-MM-DD')
    parser.add_argument('--fin',    default=None, help='Fecha fin YYYY-MM-DD (opcional)')
    parser.add_argument('--rfr',    default=0.045, type=float, help='Tasa libre de riesgo anual')
    args = parser.parse_args()

    print(f'\n{"="*60}')
    print(f'ANÁLISIS CRIPTO — {args.inicio} → {args.fin or "hoy"}')
    print(f'{"="*60}')

    precios  = descargar_precios(args.tickers, args.inicio, args.fin)
    retornos = retornos_log(precios)

    print('\n📊 Métricas anualizadas:')
    resumen = metricas_resumen(precios, tasa_libre_riesgo=args.rfr)
    print(resumen.to_string())

    if 'BTC-USD' in args.tickers:
        print('\n🔄 Ciclos de mercado BTC:')
        _, df_ciclos = ciclos_mercado(precios['BTC-USD'])
        print(df_ciclos.to_string())

    print('\n🔗 Correlaciones con BTC-USD:')
    if 'BTC-USD' in args.tickers:
        for t in args.tickers:
            if t != 'BTC-USD':
                corr = retornos['BTC-USD'].corr(retornos[t])
                print(f'   BTC vs {t:<12}: {corr:+.3f}')

    # Guardar CSV
    resumen.to_csv('datos/metricas_cripto.csv')
    print('\n💾 Métricas guardadas en datos/metricas_cripto.csv')
