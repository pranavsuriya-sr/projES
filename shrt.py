import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import schemdraw
import schemdraw.elements as elm
import sympy as sp

def draw_phasor_diagram(Vr, angle, resistance, reactance, current):
    # Convert angle to radians
    angle_rad = np.radians(angle)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Calculate the coordinates for Vs, Ir, and Ix
    Vs_x = 0
    Vs_y = 0

    Vr_x = Vr * np.cos(angle_rad)
    Vr_y = Vr * np.sin(angle_rad)

    Ir_x = Vr_x + current
    Ir_y = Vr_y

    Ix_x = Ir_x
    Ix_y = Ir_y + current

    # Plot the phasor diagram
    plt.figure(figsize=(8, 8))

    # Plotting Vs vector with arrow
    plt.arrow(0, 0, Ix_x, Ix_y, head_width=0.5, head_length=0.5, fc='blue', ec='blue', label='Vs')

    # Plotting Vr vector with arrow
    plt.arrow(0, 0, Vr_x, Vr_y, head_width=0.5, head_length=0.5, fc='green', ec='green', label='Vr')

    plt.arrow(Vr_x, Vr_y, Ir_x - Vr_x, Ir_y - Vr_y, head_width=0.5, head_length=0.5, fc='red', ec='red', label='Ir')

    plt.arrow(Ir_x, Ir_y, Ix_x - Ir_x, Ix_y - Ir_y, head_width=0.5, head_length=0.5, fc='purple', ec='purple', label='Ix')

    # Add labels and legend
    plt.text(Vr_x / 2, Vr_y / 2, 'Vr', color='green', fontsize=12, ha='right', va='bottom')
    plt.text((Ir_x + Vr_x) / 2, (Ir_y + Vr_y) / 2, 'Ir', color='red', fontsize=12, ha='right', va='bottom')
    plt.text((Ix_x + Ir_x) / 2, (Ix_y + Ir_y) / 2, 'Ix', color='purple', fontsize=12, ha='right', va='bottom')
    plt.text(Ix_x / 2, Ix_y / 2, 'Vs', color='blue', fontsize=12, ha='right', va='bottom')

    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Phasor Diagram')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    st.pyplot()

def main():
        st.title("Phasor Diagram of a Short Transmission Line")
        Vr = st.slider("Enter Vr:", min_value=0, max_value=100, value=30, step=1)
        angle = st.slider("Enter angle (degrees):", min_value=0, max_value=360, value=30, step=1)
        current = st.slider("Enter current:", min_value=0, max_value=50, value=10, step=1)

        resistance = 30
        reactance = 20
        draw_phasor_diagram(Vr, angle, resistance, reactance, current)


if __name__ == '__main__':
    main()

# Copyright text at the bottom
st.markdown(
    '<div style="text-align:center; margin-top: 42px">'
    '<a href = "https://pranavsuriya-sr.github.io/personalPortfolio/" style = "text-decoration: none;" ><p style="font-size: 10px;">PranavSuriya Devs © 2023 Project Hack Community.</a></p>'
    '<p style="font-size: 10px;">Open Source rights reserved.</p>'
    '</div>',
    unsafe_allow_html=True
)