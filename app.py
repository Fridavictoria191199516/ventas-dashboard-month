
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("📊 Dashboard de Conciliación de Ventas")

# Subida de archivo
archivo = st.file_uploader("Sube el archivo de ventas (.xlsx)", type=["xlsx"])
if archivo:
    df = pd.read_excel(archivo)

    # Normalización de nombres de canal
    mapeo_canales = {
        "CCK": "Circle K Stores, Inc.",
        "LINN": "LINN",
        "la red + bait": "la red + bait",
        "MERCURIO": "M3rcurio",
        "FINABIEN": "FINABIEN",
        "FDA": "Farmacias del Ahorro",
        "BIMBONET": "Bimbo Net",
        "OMM Web": "Web OMM",
        "WALLET PP": "PagaCel Wallet",
        "CRM OMM": "CRM OMM",
        "RECARGASELL": "RECARGASELL",
        "Distae": "Distae",
        "Charrocel": "Charrocel",
        "Gugacom": "Gugacom",
        "Taveron CRM": "Taveron CRM"
    }
    df["Nombre cliente"] = df["Nombre cliente"].replace(mapeo_canales)

    st.sidebar.header("Filtros")
    canales_excluir = st.sidebar.multiselect("Excluir canales (opcional)", options=df["Nombre cliente"].unique())

    # Aplicar exclusión
    df_filtrado = df[~df["Nombre cliente"].isin(canales_excluir)]

    st.subheader("Conciliación MVNOs")
    mvno_summary = df_filtrado.groupby("MVNO").agg(
        Transacciones=("Cantidad", "sum"),
        Comision_MVNO=("Comisión MVNO", "sum")
    ).reset_index()
    st.dataframe(mvno_summary, use_container_width=True)

    total_mvno = mvno_summary["Comision_MVNO"].sum()
    st.metric("💸 Total a pagar a MVNOs", f"${total_mvno:,.2f}")

    st.subheader("Conciliación por Canal de Venta")
    canal_summary = df_filtrado.groupby("Nombre cliente").agg(
        Ventas=("Cantidad", "sum"),
        Comision_Canal=("Comisión Canal", "sum")
    ).reset_index()
    st.dataframe(canal_summary, use_container_width=True)

    total_canal = canal_summary["Comision_Canal"].sum()
    st.metric("💰 Total a cobrar por Canal", f"${total_canal:,.2f}")

    st.subheader("📈 Margen de Utilidad")
    utilidad = total_canal - total_mvno
    st.metric("📌 Margen de utilidad total", f"${utilidad:,.2f}")

    st.download_button(
        label="📥 Descargar resumen MVNOs (Excel)",
        data=mvno_summary.to_excel(index=False, engine="openpyxl"),
        file_name="resumen_mvnos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.download_button(
        label="📥 Descargar resumen Canales (Excel)",
        data=canal_summary.to_excel(index=False, engine="openpyxl"),
        file_name="resumen_canales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Sube un archivo para comenzar.")
