import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

# Generate the x data (time values)
x = np.append(np.linspace(-3, -3, 15), [np.linspace(-3, 3, 15), np.linspace(3, 3, 15), np.linspace(3, -3, 15)])
y_values =  np.append(np.linspace(-3, 3, 15), [np.linspace(3, 3, 15), np.linspace(3, -3, 15), np.linspace(-3, -3, 15)])
# Initialize an empty line object to update during animation
line, = ax.plot([], [], lw=2)

# Initialize the plot data
def init():
    line.set_data([], [])
    return line,

# Update the plot data
def update(frame):
    # Update the line data with the sine of the current frame
    y = y_values[:frame]
    line.set_data(x[:frame], y)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(x), init_func=init, blit=True, interval=1)

# Show the plot
plt.show()
