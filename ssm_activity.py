import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D


# Initialize parameters
m = 1.0  # kg
c = 0.4  # kg/s
k = 2.0  # N/m
u = 0.0  # Control input (force in N)
x0 = 0.0 # Initial position
v0 = 0.0 # Initial velocity

# Time setup
t_start = 0
t_end = 5000
dt = 0.05
num_steps = int((t_end - t_start) / dt)

# State space matrices
A = ... # TODO Fill in the dynamics matrix here
B = ... # TODO Fill in the control matrix here

def state_update(state, u, dt):
    # TODO Replace the line below with the state update equation
    raise NotImplementedError("Remove this error and complete the state update function")

# Initial state
x = np.zeros((2, num_steps))
x[:, 0] = [x0, v0]

############### Everything Below is Plotting Code from ChatGPT ###############
# Define the spring drawing function
def draw_spring(ax, start, end, num_coils=10, width=0.5):
    spring_x = np.linspace(start, end, num_coils*4 + 1)
    spring_y = np.array([0, 0.5, -0.5, 0] * num_coils + [0])
    spring_line = Line2D(spring_x, width * spring_y, color='k', lw=2)
    ax.add_line(spring_line)
    return spring_line
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')

# Wall and ground
ax.plot([-2, 2], [-0.5, -0.5], 'k')  # ground
wall = Rectangle((-2, -0.5), 0.2, 1, color='gray')
ax.add_patch(wall)

# Mass as a box
box = Rectangle((x[0, 0]-0.2, -0.5), 0.4, 1.0, color='blue')
ax.add_patch(box)

# Spring
spring_line = draw_spring(ax, -1.8, x[0, 0]-0.2)

status_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, verticalalignment='top')

# Key press event handler
def on_key(event):
    global u
    step_size = 1.0  # Change in force
    if event.key == 'right':
        u = 1.0
    elif event.key == 'left':
        u = -1.0
    elif event.key == 'down':
        u = 0.0

# Connect the key press event to the plot
fig.canvas.mpl_connect('key_press_event', on_key)

# Update function for animation
def update(frame):
    global x
    if frame > 0:
        x[:, frame] = state_update(x[:, frame-1], u, dt)
    
    # Update the position of the box and spring
    box.set_x(x[0, frame] - 0.2)  # Update box position
    spring_line.set_xdata(np.linspace(-1.8, x[0, frame] - 0.2, len(spring_line.get_xdata())))  # Update spring

    status_text.set_text(f'Position: {x[0, frame]:.2f} m\nForce: {u:.2f} N')

    return box, spring_line, status_text

# Initialize function for animation
def init():
    box.set_x(x[0, 0] - 0.2)
    spring_line.set_xdata(np.linspace(-1.8, x[0, 0] - 0.2, len(spring_line.get_xdata())))
    status_text.set_text(f'Position: {x[0, 0]:.2f} m\nForce: {u:.2f} N')

    return box, spring_line, status_text

# Create animation
ani = FuncAnimation(fig, update, frames=num_steps, init_func=init, blit=True, repeat=False, interval=dt*1000)

plt.show()
