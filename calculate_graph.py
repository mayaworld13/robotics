#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import cgi
import cgitb
from io import BytesIO
import base64

cgitb.enable()


def calculate_motion(theta_i, theta_f, T):
    if theta_i == theta_f:
        
        t = np.array([0])
        theta = np.array([theta_i])
        theta_dot = np.array([0])
        theta_double_dot = np.array([0])
        V_max = 0
        A_max = 0
    else:
        # Calculate coefficients
        a = theta_i
        b = 0
        c = 3 * (theta_f - theta_i) / T**2
        d = -2 * (theta_f - theta_i) / T**3

        # Time points
        t = np.linspace(0, T, 1000)

        # Position polynomial
        theta = a + b * t + c * t*2 + d * t*3

        # Velocity polynomial
        theta_dot = b + 2 * c * t + 3 * d * t**2

        # Acceleration polynomial
        theta_double_dot = 2 * c + 6 * d * t

        # Find maximum velocity and acceleration
        t_max_velocity = -b / (2 * c)
        V_max = b + 2 * c * t_max_velocity + 3 * d * t_max_velocity**2
        A_max = 2 * c

    return t, theta, theta_dot, theta_double_dot, V_max, A_max

# Parse form data
form = cgi.FieldStorage()
theta_i = float(form["initial_position"].value)
theta_f = float(form["final_position"].value)
T = float(form["time_duration"].value)

# Calculate motion parameters
t, theta, theta_dot, theta_double_dot, V_max, A_max = calculate_motion(theta_i, theta_f, T)

# Generate the HTML response
print("Content-type: text/html\n")
print("<html><head><title>Cubic spline trajectory</title>")

# Add CSS styles within a <style> tag
print("<style>")
print("  body { background-color: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; }")
print("  .container { max-width: 800px; margin: 0 auto; padding: 20px; background-color: #000; box-shadow: 0 0 15px #0f0; border-radius: 8px; border: 1px solid #0f0; }")
print("  h1 { font-size: 24px; color: #0f0; text-transform: uppercase; letter-spacing: 2px; }")
print("  img { display: block; margin: 0 auto; max-width: 100%; }")
print("  .graph-container { display: flex; justify-content: center; }")
print("  p { font-size: 18px; color: #0f0; margin-top: 20px; }")
print("</style>")

print("</head><body>")
print("<div class='container'>")
print("<h1>Cubic Spline Trajectory</h1>")

# Plotting code
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t, theta)
plt.title('Joint Position vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Position (degrees)')
plt.subplot(3, 1, 2)
plt.plot(t, theta_dot)
plt.title('Joint Velocity vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (degrees/s)')
plt.subplot(3, 1, 3)
plt.plot(t, theta_double_dot)
plt.title('Joint Acceleration vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (degrees/s^2)')
plt.tight_layout()

# Save the graph as a binary image
buffer = BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Display the binary image in the HTML response
image_data = base64.b64encode(buffer.read()).decode()
print("<div class='graph-container'>")
print(f"<img src='data:image/png;base64,{image_data}'>")
print("</div>")

# Display maximum velocity and acceleration
print(f"<p>Maximum Velocity (V_max): {V_max} degrees/s</p>")
print(f"<p>Maximum Acceleration (A_max): {A_max} degrees/s^2</p>")

print("</div></body></html>")
