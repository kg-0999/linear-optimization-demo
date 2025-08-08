import streamlit as st
import numpy as np
from scipy.optimize import linprog

st.title("📈 Linear Optimization Tool")
st.subheader('An App by Sai Krishna Gaddam') 
st.write(('This app provides Linear Optimization Solution based on User Input,'  
'Provide Optimization function type, constraints and bounds then click Solve Optimization Problem' 
'If an optimal solution is found, result is shown at the end!'
'Happy Solving!'))
# Step 1: Select Optimization Type
opt_type = st.radio(
    "Select Optimization Type:",
    ("Profit Maximization", "Cost Minimization")
)

# Step 2: Number of variables & constraints
num_vars = st.number_input("Number of variables", min_value=1, max_value=10, value=2)
num_constraints = st.number_input("Number of constraints", min_value=1, max_value=10, value=2)

st.markdown("---")
st.subheader("Objective Function Coefficients")
obj_coeffs = []
for i in range(num_vars):
    coeff = st.number_input(f"Coefficient for x{i+1} in objective function", value=0.0)
    obj_coeffs.append(coeff)

st.markdown("---")
st.subheader("Constraints (A_ub * x ≤ b_ub)")
A = []
b = []
for i in range(num_constraints):
    row = []
    st.markdown(f"**Constraint {i+1}:**")
    for j in range(num_vars):
        val = st.number_input(f"Coefficient for x{j+1} in constraint {i+1}", value=0.0, key=f"A_{i}_{j}")
        row.append(val)
    rhs = st.number_input(f"Right-hand side value for constraint {i+1}", value=0.0, key=f"b_{i}")
    A.append(row)
    b.append(rhs)

st.markdown("---")
st.subheader("Variable Bounds")
bounds = []
for i in range(num_vars):
    lower = st.number_input(f"Lower bound for x{i+1}", value=0.0, key=f"lb_{i}")
    upper = st.number_input(f"Upper bound for x{i+1} (enter None for no limit)", value=10.0, key=f"ub_{i}")
    upper_bound = None if upper == 0 and st.checkbox(f"No upper bound for x{i+1}", key=f"no_ub_{i}") else upper
    bounds.append((lower, upper_bound))

# Step 3: Solve when button clicked
if st.button("Solve Optimization Problem"):
    c = np.array(obj_coeffs)

    # For maximization, linprog minimizes by default, so we multiply by -1
    if opt_type == "Profit Maximization":
        c = -c

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    if res.success:
        st.success("✅ Optimization successful!")
        if opt_type == "Profit Maximization":
            st.write("**Optimal Profit:**", round(-res.fun, 4))
        else:
            st.write("**Minimum Cost:**", round(res.fun, 4))
        st.write("**Optimal Variable Values:**")
        for idx, val in enumerate(res.x):
            st.write(f"x{idx+1} =", round(val, 4))
    else:
        st.error("❌ Optimization failed: " + res.message)
