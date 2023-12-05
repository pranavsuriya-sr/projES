import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import schemdraw
import schemdraw.elements as elm
import sympy as sp

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

def main():
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