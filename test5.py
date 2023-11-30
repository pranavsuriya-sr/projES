import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import schemdraw
import schemdraw.elements as elm

def calculate_power_triangle(voltage, current, phase_angle):
    p = voltage * current * np.cos(np.radians(phase_angle))
    q = voltage * current * np.sin(np.radians(phase_angle))
    s = voltage * current
    return p, q, s

def calculate_imped_triangle(voltage, current, phase_angle):
    res = (voltage / current) * np.cos(np.radians(phase_angle))
    reac = (voltage / current) * np.sin(np.radians(phase_angle))
    imped = np.sqrt(res**2 + reac**2)
    return res, reac, imped

def plot_power_triangle(p, q, s, angle):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, s + 5)
    ax.set_ylim(0, s + 5)

    vertices = [(0, 0), (p, 0), (p, q)]
    triangle = Polygon(vertices, closed=True, edgecolor='black', linewidth=2, fill=None)
    ax.add_patch(triangle)

    ax.text(p / 2, -1, f'Real Power: {p:.2f}', ha='center')
    ax.text(p + 1, q / 2, f'Reactive Power: {q:.2f}', va='center', rotation=90)
    ax.text(p / 2, q / 2, f'Apparent Power: {s:.2f}', ha='center', va='center', rotation=angle)

    ax.set_xlabel('Real Power')
    ax.set_ylabel('Reactive Power')

    st.pyplot(fig)

def plot_imped_triangle(res, reac, imped, angle):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, imped + 5)
    ax.set_ylim(0, imped + 5)

    vertices = [(0, 0), (res, 0), (res, reac)]
    triangle = Polygon(vertices, closed=True, edgecolor='black', linewidth=2, fill=None)
    ax.add_patch(triangle)

    ax.text(res / 2, -1, f'res: {res:.2f}', ha='center')
    ax.text(res + 1, reac / 2, f'reac: {reac:.2f}', va='center', rotation=90)
    ax.text(res / 2, reac / 2, f'imped: {imped:.2f}', ha='center', va='center', rotation=angle)

    ax.set_xlabel('res')
    ax.set_ylabel('reac')

    st.pyplot(fig)

def draw_circuit(components, voltage):
    d = schemdraw.Drawing()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    comMap = {
        'Resistor': (elm.Resistor, 'Ω'),
        'Inductor': (elm.Inductor, 'H'),
        'Capacitor': (elm.Capacitor, 'F')
    }

    totImp = 0
    for i, component in enumerate(components):
        compType, compVal = component['type'], component['value']
        compClass, compUnit = comMap[compType]
        
        if i > 0:
            d.add(elm.Dot())

        compInst = compClass(label=f'{compVal}{compUnit}')
        d.add(compInst)

        imped = calculate_imped(compType, compVal)
        totImp += imped

    d.add(elm.SourceV(label=f'{voltage}V'))
    d.draw()

    return totImp

def calculate_imped(compType, compVal):
    omega = 2 * 3.14159265358979323846 

    if compType == 'Resistor':
        imped = compVal
    elif compType == 'Inductor':
        imped = complex(0, omega * compVal)
    elif compType == 'Capacitor':
        imped = complex(0, -1 / (omega * compVal))
    else:
        imped = 0

    return imped

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

    # Plotting Ir vector with arrow
    plt.arrow(Vr_x, Vr_y, Ir_x - Vr_x, Ir_y - Vr_y, head_width=0.5, head_length=0.5, fc='red', ec='red', label='Ir')

    # Plotting Ix vector with arrow
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
    st.sidebar.markdown("Types of triangle or Circuit Generator : ")
    option = st.sidebar.radio('Select',['Power Triangle', 'imped Triangle', 'Circuit Generator and Solver', 'Phasor Diagram'])

    if option == 'Power Triangle':
        st.subheader('Select the type of triangle in the sidebar: imped / Power')
        st.title('Power Triangle Calculator')
        voltage = st.slider('Voltage', min_value=0, max_value=100, value=50)
        current = st.slider('Current', min_value=0, max_value=100, value=25)
        phase_angle = st.slider('Phase Angle', min_value=0, max_value=90, value=30)
        p, q, s = calculate_power_triangle(voltage, current, phase_angle)
        st.subheader('Power Triangle')
        plot_power_triangle(p, q, s, phase_angle)

    elif option == 'imped Triangle':
        st.subheader('Select the type of triangle in the sidebar: imped / Power')
        st.title('imped Triangle Calculator')
        voltage = st.slider('Voltage', min_value=0, max_value=100, value=10)
        current = st.slider('Current', min_value=0, max_value=100, value=5)
        phase_angle = st.slider('Phase Angle', min_value=0, max_value=90, value=0)
        res, reac, imped = calculate_imped_triangle(voltage, current, phase_angle)
        st.subheader('imped Triangle')
        plot_imped_triangle(res, reac, imped, phase_angle)

    elif option == 'Circuit Generator and Solver':
        st.title('Circuit Diagram Generator and Solver')
        st.sidebar.header('Number of Components')
        num_components = st.sidebar.number_input('Number of Components', min_value=1, step=1, value=1)
        components = []
        for i in range(num_components):
            st.sidebar.subheader(f'Component {i + 1}')
            compType = st.sidebar.selectbox(f'Select Component Type {i + 1}', ['Resistor', 'Inductor', 'Capacitor'])
            compVal = st.sidebar.number_input(f'{compType} Value {i + 1} ({compType})', min_value=0.001, step=0.001, value=0.01)
            components.append({'type': compType, 'value': compVal})
        voltage = st.number_input('Enter Voltage Across the Circuit (V)', min_value=0, step=1, value=10)
        totImp = draw_circuit(components, voltage)
        current = voltage / totImp
        st.write(f'Total imped: {totImp:.2f} Ω')
        st.write(f'Current: {current:.2f} A')
        st.pyplot()

    elif option == 'Phasor Diagram':
        st.title("Phasor Diagram of a Short Transmission Line")

    # Get user input using sliders
        Vr = st.slider("Enter Vr:", min_value=0, max_value=100, value=30, step=1)
        angle = st.slider("Enter angle (degrees):", min_value=0, max_value=360, value=30, step=1)
        current = st.slider("Enter current:", min_value=0, max_value=50, value=10, step=1)

    # Hardcoded parameters for resistance and reactance (you can modify as needed)
        resistance = 30
        reactance = 20

    # Draw phasor diagram
        draw_phasor_diagram(Vr, angle, resistance, reactance, current)

if __name__ == '__main__':
    main()

# Copyright text at the bottom
st.sidebar.markdown(
    '<div style="text-align:center; margin-top: 370px">'
    '<a href = "https://pranavsuriya-sr.github.io/personalPortfolio/" style = "text-decoration: none;" ><p style="font-size: 10px;">PranavSuriya Devs © 2023 Project Hack Community.</a></p>'
    '<p style="font-size: 10px;">Open Source rights reserved.</p>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div style="text-align:center; margin-top: 42px">'
    '<a href = "https://pranavsuriya-sr.github.io/personalPortfolio/" style = "text-decoration: none;" ><p style="font-size: 10px;">PranavSuriya Devs © 2023 Project Hack Community.</a></p>'
    '<p style="font-size: 10px;">Open Source rights reserved.</p>'
    '</div>',
    unsafe_allow_html=True
)
