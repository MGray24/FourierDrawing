import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp

plt.switch_backend('TkAgg')

numOfVectors = 40 #will determine accuracy, should be even
vectorsFromZero = (numOfVectors) // 2
coefs = []
finalPoints = []
# Function to apply the complex exponential
def f(x):
    return shape_points[int(1000*x)]
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
        if i != 0: #removes the constant vector
            total += coefs[i+vectorsFromZero] * np.e ** (2j * np.pi * t * i)
    return total

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

# Step 1: Define the vertices of the square
vertex1 = .5 + -2.4899j
vertex2 = .809 + -1.5388j
vertex3 = 0 + -.9511j
vertex4 = 1 + -.9511j
vertex5 = 1.309 + 0j
vertex6 = 1.618 + -.9511j
vertex7 = 2.618 + -.9511j
vertex8 = 1.809 + -1.5388j
vertex9 = 2.118 + -2.4899j
vertex10 = 1.309 + -1.9021j

# Step 2: Generate 100 points per side
side1 = np.linspace(vertex1, vertex2, 100)
side2 = np.linspace(vertex2, vertex3, 100)
side3 = np.linspace(vertex3, vertex4, 100)
side4 = np.linspace(vertex4, vertex5, 100)
side5 = np.linspace(vertex5, vertex6, 100)
side6 = np.linspace(vertex6, vertex7, 100)
side7 = np.linspace(vertex7, vertex8, 100)
side8 = np.linspace(vertex8, vertex9, 100)
side9 = np.linspace(vertex9, vertex10, 100)
side10 = np.linspace(vertex10, vertex1, 100)


# Step 3: Combine all points
shape_points = np.concatenate([side1, side2, side3, side4, side5, side6, side7, side8, side9, side10])

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

# Create line objects for each vector
vectors = [ax.plot([], [], lw=1, color='blue')[0] for _ in range(numOfVectors+1)]

# Initialize the plot data
def init():
    line.set_data([], [])
    ###
    for vector in vectors:
        vector.set_data([], [])
    return [line] + vectors
    ###

# Update the plot data
def update(frame):
    # Update the line data with the transformed points
    x = real_parts[:frame]
    y = imaginary_parts[:frame]
    line.set_data(x, y)

    ### Calculate the current position of each vector
    t = frame / len(real_parts)
    current_pos = 0
    for i, k in enumerate(range(-vectorsFromZero, vectorsFromZero + 1)):
        if k != 0:
            vector_end = current_pos + coefs[i] * np.e ** (2j * np.pi * t * k)
            vectors[i].set_data([current_pos.real, vector_end.real], [current_pos.imag, vector_end.imag])
            current_pos = vector_end


    return [line] + vectors
    ###

# Create the animation
ani = FuncAnimation(fig, update, frames=len(real_parts), init_func=init, blit=True, interval=20)

# Show the plot
plt.show()
