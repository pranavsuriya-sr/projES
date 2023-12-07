import streamlit as st
import numpy as np
from scipy.optimize import minimize

def objective(loads, coefficients):
    return sum(coefficients[i][0] * loads[i]**2 + coefficients[i][1] * loads[i] + coefficients[i][2] for i in range(len(loads)))

def equality_constraint(loads, total_sum):
    return np.sum(loads) - total_sum

def display_equations(coefficients):
    st.subheader("Equations:")
    for i, coeff in enumerate(coefficients):
        a, b, c = coeff
        st.write(f"Equation {i + 1}: {a} * P{i + 1}^2 + {b} * P{i + 1} + {c}")
        st.write(f"Differential Equation {i + 1}:  {2*a} * P{i + 1} + {b} ")

def main():
    st.title("Economic Load Dispatch")

    nod = st.number_input("Enter the number of generators:")
    total_sum = st.number_input("Sum power of generators : ")

    nod = int(nod)

    # Define variables
    loads = [0.0] * nod
    coefficients = []

    for i in range(nod):
        st.subheader(f"Load {i + 1}")
        ai = st.number_input(f"Enter variable coefficient one for Load {i + 1}: ")
        bi = st.number_input(f"Enter variable coefficient two for Load {i + 1}: ")
        ci = st.number_input(f"Enter variable coefficient three for Load {i + 1}: ")
        coefficients.append((ai, bi, ci))

    # Display equations
    display_equations(coefficients)

    # Set up the optimization problem
    cons = ({'type': 'eq', 'fun': lambda loads: equality_constraint(loads, total_sum)})
    bounds = [(0, None) for _ in range(nod)]

    # Solve the optimization problem
    result = minimize(objective, loads, args=(coefficients,), method='SLSQP', constraints=cons, bounds=bounds)

    # Display the solution
    st.subheader("Solution:")
    if result.success:
        for i, load in enumerate(result.x):
            st.write(f"P{i + 1}: {load}")
    else:
        st.write("Solution not found")

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