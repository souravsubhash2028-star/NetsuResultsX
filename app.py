import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Netsu ResultsX",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Netsu ResultsX")
st.subheader("Aerospace Thermal Analysis Tool")

materials = pd.read_csv("materials.csv")

material = st.selectbox(
    "Select Material",
    materials["Material"]
)

row = materials[materials["Material"] == material].iloc[0]

k = row["k"]

thickness = st.number_input(
    "Thickness (m)",
    min_value=0.0001,
    value=0.01
)

area = st.number_input(
    "Area (m²)",
    min_value=0.01,
    value=1.0
)

deltaT = st.number_input(
    "Temperature Difference ΔT (K)",
    value=100.0
)

h = st.number_input(
    "Convective Heat Transfer Coefficient h (W/m²K)",
    value=25.0
)

emissivity = st.number_input(
    "Emissivity ε",
    min_value=0.0,
    max_value=1.0,
    value=float(row["Emissivity"])
)

mli_layers = st.slider(
    "MLI Layers",
    0,
    40,
    10
)

if st.button("Calculate"):

    sigma = 5.67e-8

    T_hot = 400
    T_cold = T_hot - deltaT

    q_cond = (k * area * deltaT) / thickness

    q_conv = h * area * deltaT

    q_rad = (
        emissivity
        * sigma
        * area
        * (T_hot**4 - T_cold**4)
    )

    thermal_resistance = thickness / (k * area)

    U = 1 / thermal_resistance

    mli_factor = 1 - (0.015 * mli_layers)

    if mli_factor < 0.3:
        mli_factor = 0.3

    adjusted_heat = q_cond * mli_factor

    st.success("Analysis Completed")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Heat Conduction Rate",
            f"{q_cond:.2f} W"
        )

        st.metric(
            "Convective Heat Transfer",
            f"{q_conv:.2f} W"
        )

        st.metric(
            "Radiative Heat Transfer",
            f"{q_rad:.2f} W"
        )

    with col2:
        st.metric(
            "Thermal Resistance",
            f"{thermal_resistance:.6f} K/W"
        )

        st.metric(
            "Overall Heat Transfer Coefficient",
            f"{U:.2f} W/m²K"
        )

        st.metric(
            "MLI Adjusted Heat Loss",
            f"{adjusted_heat:.2f} W"
        )

    if adjusted_heat < 500:
        st.success("🟢 Excellent Thermal Protection")

    elif adjusted_heat < 2000:
        st.warning("🟡 Moderate Thermal Performance")

    else:
        st.error("🔴 Poor Thermal Protection")

    st.info(
        f"Material Used: {material}"
    )
