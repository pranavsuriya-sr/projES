import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import schemdraw
import schemdraw.elements as elm
import sympy as sp

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

def main():
    option = st.sidebar.radio('Select',['Power Triangle', 'imped Triangle'])

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
