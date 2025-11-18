import pandas as pd


def format_currency(x: float) -> str:
    if pd.isna(x):
        return "–"
    # millones MXN
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:,.1f}M"
    return f"${x:,.0f}"


def format_percent(x: float) -> str:
    if pd.isna(x):
        return "–"
    # si viene como 0.08 -> 8.0%
    return f"{x*100:,.1f}%" if x < 1.1 else f"{x:,.1f}%"  # por si ya viene en %


def compute_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    # columnas que usaremos
    col_capital = "Capital Dispersado Actual"
    col_crec_saldo = "Crecimiento Saldo Actual"
    col_morosidad = "Morosidad Temprana Actual"
    col_fpd = "% FPD Actual"
    col_ratio_vencida = "Ratio_Cartera_Vencida Actual"
    col_saldo_vencido = "Saldo Insoluto Vencido Actual"

    result = {
        "capital_total": df[col_capital].sum(skipna=True),
        "crec_saldo_prom": df[col_crec_saldo].mean(skipna=True),
        "morosidad_prom": df[col_morosidad].mean(skipna=True),
        "fpd_prom": df[col_fpd].mean(skipna=True),
        "ratio_vencida_prom": df[col_ratio_vencida].mean(skipna=True),
        "saldo_vencido_total": df[col_saldo_vencido].sum(skipna=True),
        "num_sucursales": df["Sucursal"].nunique(),
    }

    return result
