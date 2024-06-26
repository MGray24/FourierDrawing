import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp

numOfVectors = 41 #will determine accuracy, should be odd
vectorsFromZero = (numOfVectors - 1) // 2
coefs = []
finalPoints = []
# Function to apply the complex exponential
def f(x):
    return shape_points[int(400*x)]
def integrate(k, dx):
    amount = int(1/dx)
    x = 0
    total = 0
    for i in range(amount):
        total += (((np.e)**(-2j * np.pi * k * x)) * f(x)) * dx
        x+=dx
    return total

def seriesAtVal(t):
    total = 0
    for i in range(-vectorsFromZero, vectorsFromZero+1):
        total += coefs[i+vectorsFromZero] * np.e ** (2j * np.pi * t * i)
    return total

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

# Step 1: Define the vertices of the square
vertex1 = -2 + -2j
vertex2 = -2 + 2j
vertex3 = 2 + 2j
vertex4 = 2 + -2j

# Step 2: Generate 100 points per side
side1 = np.linspace(vertex1, vertex2, 100)
side2 = np.linspace(vertex2, vertex3, 100)
side3 = np.linspace(vertex3, vertex4, 100)
side4 = np.linspace(vertex4, vertex1, 100)

# Step 3: Combine all points
shape_points = np.concatenate([side1, side2, side3, side4])

#Apply integrals to find coefficients
for k in range(-vectorsFromZero, vectorsFromZero + 1):
    coef = integrate(k, .01)
    coefs.append(coef)

#use the coefficients to generate points for the drawing
t = 0
for i in range(100):
    finalPoints.append(seriesAtVal(t))
    t += 1/100

real_parts = [c.real for c in finalPoints]
imaginary_parts = [c.imag for c in finalPoints]

# Initialize an empty line object to update during animation
line, = ax.plot([], [], lw=2)

# Initialize the plot data
def init():
    line.set_data([], [])
    return line,

# Update the plot data
def update(frame):
    # Update the line data with the transformed points
    x = real_parts[:frame]
    y = imaginary_parts[:frame]
    line.set_data(x, y)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(real_parts), init_func=init, blit=True, interval=10)

# Show the plot
plt.show()
