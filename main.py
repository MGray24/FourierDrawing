import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp

plt.switch_backend('TkAgg')

numOfVectors = 400 #will determine accuracy, should be even
vectorsFromZero = (numOfVectors) // 2
coefs = []
finalPoints = []
# Function to apply the complex exponential
def f(x):
    return points[int(len(points)*x)]
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


# Step 1: Define the vertices of the square
# Load the image
image_path = 'img.png'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection
edges = cv2.Canny(gray, threshold1=50, threshold2=150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extract the points from the contours
points = []
for contour in contours:
    for point in contour:
        points.append(tuple(point[0]))  # point is a list containing the [x, y] coordinates


# Convert to numpy array for easier manipulation if needed
points = np.array(points)
points = [complex(x, -y) for x, y in points]

real_parts = [z.real for z in points]
imaginary_parts = [z.imag for z in points]
min_x, max_x = min(real_parts), max(real_parts)
min_y, max_y = min(imaginary_parts), max(imaginary_parts)

x_range = (max_x+min_x)/2
y_range = (max_y+min_y)/2
points = [point - x_range - y_range for point in points]
min_x -= x_range
min_y -= y_range
max_x -= x_range
max_y -= y_range

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

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
ani = FuncAnimation(fig, update, frames=len(real_parts), init_func=init, blit=True, interval=60)

# Show the plot
plt.show()
