import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import PchipInterpolator
import math
from scipy.integrate import quad
from numpy import trapz
st.title("Simulating a brachistochrone")
g = 9.81

L1 = 100
L2 = st.slider("Height of first bar (should be the highest) = ", min_value=1, max_value=100)
L3 = st.slider("Height of second bar = ", min_value=1, max_value=100)
L4 = st.slider("Height of third bar = ", min_value=1, max_value=100)
L10 = 1

# Ensure that L1 >= L2 >= L3 >= L4 >= L5
if not (L1 >= L2 >= L3 >= L4 >= L10):
    st.error("Error: Heights must be in non-increasing order (L1 >= L2 >= L3 >= L4 >= L5).")
else:
    # Heights in non-increasing order
    heights = [L1, L2, L3, L4,L10]
    labels = ['L1', 'L2', 'L3', 'L4','L10']

    # X positions for the heights (spread across the full x-axis)
    x = np.linspace(0, len(labels) - 1, len(labels))  # [0, 1, 2, 3, 4]
    y = np.array(heights)

    # Create a smooth curve using PCHIP interpolation
    pchip = PchipInterpolator(x, y)
    xnew = np.linspace(x.min(), x.max(), 3000)  # More points for smooth curve
    ynew = pchip(xnew)

    dx = xnew[1] - xnew[0]

    derivative_func = pchip.derivative()
    dy_dx = derivative_func(xnew)
    y1 = L1
    x1 = 100
    x2 = 0
    x_values = xnew
    # Calculations
    a = dy_dx**2
    b = 1 + a
    c = np.sqrt(b)
    d = 2*g*(y1-ynew)

    e = np.sqrt(d)
    # Check for negative or zero values to avoid division by zero
    f = np.where(e > 0, c / e, 0)  # Use 0 if e is not positive
    h = f * dx
# Calculate total time
    total_time = trapz(h)

    # Display total time
    st.metric("Total Time to Descend:", f"{total_time:.2f} seconds")

# Create Plotly figure
fig = go.Figure()

# Add the smooth curve
fig.add_trace(go.Scatter(x=xnew, y=ynew, mode='lines', name='Smooth Slope', line=dict(color='blue')))

# Add original data points
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Original Data Points', marker=dict(color='red', size=10)))



# Update layout
fig.update_layout(
    title='Smooth Slope with Original Data Points',
    xaxis_title='Height Segments',
    yaxis_title='Height (m)',
    xaxis=dict(tickvals=x, ticktext=labels),
    showlegend=True
)

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)

