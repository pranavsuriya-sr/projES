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
        st.title("Economic Load Dispatch")

        nod = st.number_input("Enter the number of loads:")

        nod = int(nod)

        equations = []
        eqn = []

        pi, ambda = sp.symbols('pi ambda')  # Define symbolic variables

        for i in range(nod):
            st.subheader(f"Load {i + 1}")
            ai = st.number_input(f"Enter variable coefficient one for Load {i + 1}: ")
            bi = st.number_input(f"Enter variable coefficient two for Load {i + 1}: ")
            ci = st.number_input(f"Enter variable coefficient three for Load {i + 1}: ")

            equation = ai * pi**2 + bi * pi + ci  # Define the equation
            eqn = 2 * ai * pi + bi - ambda  # Define the differential equation
            equations.append(equation)

        # Display the equations
        st.subheader("Equations:")
        for equation in equations:
            st.write(equation)

        st.subheader("Differential Equation:")
        st.write(eqn)

        # Solve the differential equation for pi and ambda
        solution = sp.solve(eqn, (pi, ambda))

        st.subheader("Solution:")
        st.write(f"pi = {solution[0][0]}, ambda = {solution[0][1]}")

        # Draw phasor diagram


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