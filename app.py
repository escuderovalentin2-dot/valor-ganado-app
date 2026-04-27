import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
import io

# Configuración de la página para móviles y PC
st.set_page_config(page_title="Consultoría EVM - Valentín Escudero", layout="wide")

st.title("📊 Sistema de Análisis de Valor Ganado (EVM)")
st.write("Herramienta profesional para la optimización de procesos en ingeniería civil.")

# 1. ENTRADA DE DATOS EN LA BARRA LATERAL
with st.sidebar:
    st.header("Configuración del Proyecto")
    bac = st.number_input("Presupuesto Total (BAC)", min_value=0.0, value=10000.0, step=100.0)
    meses_totales = st.slider("Tiempo total (meses)", 1, 60, 12)
    mes_estudio = st.slider("Mes de corte actual", 1, meses_totales, 1)

# 2. INGRESO DE DATOS DINÁMICO
st.subheader("📝 Datos Acumulados")
datos = []

# Creamos columnas para que la entrada de datos sea limpia
col1, col2, col3 = st.columns(3)

for i in range(1, meses_totales + 1):
    with st.expander(f"Periodo {i}", expanded=(i == mes_estudio)):
        c1, c2, c3 = st.columns(3)
        pv_acum = c1.number_input(f"PV Acumulado Mes {i}", key=f"pv_{i}", value=float(i*(bac/meses_totales)))
        
        if i <= mes_estudio:
            ac_acum = c2.number_input(f"AC Acumulado Mes {i}", key=f"ac_{i}", value=float(i*(bac/meses_totales)*1.05))
            avance_real = c3.number_input(f"% Avance Real (0-1.0) Mes {i}", key=f"av_{i}", value=0.10*i, max_value=1.0)
        else:
            ac_acum = None
            avance_real = None
            
        datos.append({'Periodo': i, 'PV': pv_acum, 'AC': ac_acum, 'Avance_Real': avance_real})

# 3. PROCESAMIENTO (Lógica del Master Valentín Escudero)
df = pd.DataFrame(datos)
df['EV'] = bac * df['Avance_Real']
df['CPI'] = df['EV'] / df['AC']
df['SPI'] = df['EV'] / df['PV']
# ... (aquí siguen el resto de tus fórmulas)

# 4. VISUALIZACIÓN EN LA APP
st.subheader("📈 Curva S y Desempeño")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['Periodo'], df['PV'], label='PV', marker='o')
ax.plot(df['Periodo'][:mes_estudio], df['AC'][:mes_estudio], label='AC', marker='^')
ax.plot(df['Periodo'][:mes_estudio], df['EV'][:mes_estudio], label='EV', marker='s')
ax.legend()
st.pyplot(fig)

# Muestra de métricas clave (Kpis)
if mes_estudio > 0:
    ultimo_cpi = df.loc[mes_estudio-1, 'CPI']
    ultimo_spi = df.loc[mes_estudio-1, 'SPI']
    
    k1, k2, k3 = st.columns(3)
    k1.metric("CPI (Eficiencia Costo)", f"{ultimo_cpi:.2f}", delta="Bien" if ultimo_cpi >= 1 else "Sobre Presupuesto")
    k2.metric("SPI (Eficiencia Tiempo)", f"{ultimo_spi:.2f}", delta="A tiempo" if ultimo_spi >= 1 else "Retrasado")
    k3.metric("EAC (Proyección Final)", f"{bac/ultimo_cpi:,.2f}")