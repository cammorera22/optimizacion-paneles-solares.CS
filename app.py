import streamlit as st
from modelo import optimizar_paneles

st.title("Optimización de Paneles Solares ☀️")

st.markdown("### Parámetros de entrada")

# Entradas dinámicas
consumos = []
areas = []
for i in range(3):
    consumo = st.number_input(f"Consumo mensual Casa {i+1} (kWh)", min_value=50, value=[445,404,125][i])
    area = st.number_input(f"Área disponible Casa {i+1} (m2)", min_value=50, value=[150,188,228][i])
    consumos.append(consumo)
    areas.append(area)

if st.button("Optimizar"):
    solucion, costo = optimizar_paneles(consumos, areas)

    st.subheader("📊 Resultados")
    st.write("Costo total mínimo: $", round(costo,2))

    for casa, paneles in solucion.items():
        st.write(f"**{casa}** → {paneles}")

    st.success("Interpretación: El modelo sugiere la combinación óptima de paneles para cubrir la demanda de cada casa al menor costo posible, respetando las áreas de techo disponibles.")
