import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import PchipInterpolator
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
L1 = int(st.slider("Height of first bar (should be the highest) = ", min_value=1, max_value=100, value=50))
L2 = st.slider("Height of second bar = ", min_value=1, max_value=100, value=40)
L3 = st.slider("Height of third bar = ", min_value=1, max_value=100, value=30)
L4 = st.slider("Height of fourth bar = ", min_value=1, max_value=100, value=20)
L5 = st.slider("Height of fifth bar = ", min_value=1, max_value=100, value=10)

# Ensure that L1 >= L2 >= L3 >= L4 >= L5
if not (L1 >= L2 >= L3 >= L4 >= L5):
    st.error("Error: Heights must be in non-increasing order (L1 >= L2 >= L3 >= L4 >= L5).")
else:
    # Heights in non-increasing order
    heights = [L1, L2, L3, L4, L5]
    labels = ['L1', 'L2', 'L3', 'L4', 'L5']

    # X positions for the heights (spread across the full x-axis)
    x = np.linspace(0, len(labels) - 1, len(labels))  # [0, 1, 2, 3, 4]
    y = np.array(heights)

    # Create a smooth curve using PCHIP interpolation
    pchip = PchipInterpolator(x, y)
    xnew = np.linspace(x.min(), x.max(), 300)  # More points for smooth curve
    ynew = pchip(xnew)
 # Get the positions of the ball
    
    total_time = 3  # total time of the simulation
    ball_positions = simulate_ball_roll(start_pos=0, total_time=total_time, num_steps=100)

       # Simulate the ball's motion
    def simulate_ball_roll(start_pos, total_time, num_steps):
        g = 9.81  # gravity (m/s^2)
        time_steps = np.linspace(0, total_time, num_steps)
        positions = []
        velocity = 0

        for t in time_steps:
            # Simplified physics: v = u + at; here, a is derived from the slope of the curve
            idx = int(np.clip(start_pos + t * 0.1, 0, len(xnew) - 1))
            slope = (ynew[min(idx + 1, len(ynew) - 1)] - ynew[max(idx - 1, 0)]) / (xnew[min(idx + 1, len(xnew) - 1)] - xnew[max(idx - 1, 0)])
            acceleration = -g * slope  # negative because it's moving down
            velocity += acceleration * (total_time / num_steps)
            start_pos += velocity * (total_time / num_steps)
            positions.append(start_pos)

        return positions
   # Add the ball's trajectory
    ball_x = np.linspace(0, len(labels) - 1, len(ball_positions))
    fig.add_trace(go.Scatter(x=ball_x, y=pchip(ball_x), mode='markers', name='Ball Position', marker=dict(color='green', size=12)))

    # Annotate total time taken
    fig.add_annotation(
        x=ball_x[-1],
        y=pchip(ball_x)[-1],
        text=f"Time taken: {total_time:.2f} s",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor="white",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        font=dict(size=12)
    )

    # Update layout
    fig.update_layout(
        title='Smooth Slope with Original Data Points and Ball Simulation',
        xaxis_title='Height Segments',
        yaxis_title='Height (m)',
        xaxis=dict(tickvals=x, ticktext=labels),
        showlegend=True
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig)
