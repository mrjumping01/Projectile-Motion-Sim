"""from math import sin, cos, radians
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pylab import plot, show, title, xlabel, ylabel, xlim, ylim, grid

# VARIABLES
# Speed in m/s, angles in degrees
v_0: float = 74
launch_angle: float = radians(55)
num_pts_to_plot: int = 22
g: float = 9.81

# CALCULATIONS
time: float = 2 * v_0 * sin(launch_angle) / g
evenly_spaced_instants = list(np.linspace(0, time, num=num_pts_to_plot, endpoint=True))
max_height: float = (v_0**2 * sin(launch_angle)**2) / (2 * g)
horiz_displacement: float = v_0 * time

# PRINTING RESULTS
print(f"\nAll values are rounded to 2 decimal places.\nMax height: {round(max_height, 2)}m\nTime of flight: {round(time, 2)}s\nHorizontal displacement: {round(horiz_displacement, 2)}m\n")

if launch_angle == 90:
    horiz_displacement = 0

# PLOTTING DATA
x = [instant * v_0 for instant in evenly_spaced_instants]
y = [v_0 * instant * sin(launch_angle) - 0.5 * g * instant**2 for instant in evenly_spaced_instants]

df = pd.DataFrame({'Instant (s)': evenly_spaced_instants, 'x': x, 'y': y}, dtype="float64")
df2 = pd.DataFrame({"Instant (s)": time / 2, "x": horiz_displacement / 2, "y": max_height}, index=[0], dtype="float64")
df = pd.concat([df, df2], axis=0).sort_values("Instant (s)").reset_index(drop=True)

fig, ax = plt.subplots()
ax.plot(x, y, "ro")
ax.plot(horiz_displacement / 2, max_height, "+", color="black")

# Draw instantaneous velocity vectors
for i in range(len(x)):
    angle = launch_angle
    dx = v_0 * cos(launch_angle) * cos(angle)
    dy = v_0 * cos(launch_angle) * sin(angle)
    ax.arrow(x[i], y[i], dx, dy, width=0.5, color="blue")

# Draw double-headed arrow for max height
ax.annotate("", xy=(horiz_displacement / 2, max_height), xytext=(horiz_displacement / 2, 0),
            arrowprops=dict(arrowstyle="<->", linewidth=1.5))
ax.text(horiz_displacement / 2, max_height / 2, "Max Height", horizontalalignment="center")

ax.set_xlim(0, 1.1 * horiz_displacement)
ax.set_ylim(0, 1.1 * max_height)
ax.set_title("Projectile Motion Graph")
plt.show()
"""

from math import sin, cos, atan2, degrees, radians
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, xlim, ylim, grid

# VARIABLES
v_0: float = 74
launch_angle: float = radians(55)
num_pts_to_plot: int = 22
g: float = 9.81
initial_height: float = 10  # Set the initial height here

# CALCULATIONS
time: float = 2 * v_0 * sin(launch_angle) / g
evenly_spaced_instants = list(np.linspace(0, time, num=num_pts_to_plot, endpoint=True))
max_height: float = (v_0 ** 2 * sin(launch_angle) ** 2) / (2 * g) + initial_height
horiz_displacement: float = v_0 * time

# PRINTING RESULTS
print(
    f"\nAll values are rounded to 2 decimal places.\nMax height: {round(max_height, 2)}m\nTime of flight: {round(time, 2)}s\nHorizontal displacement: {round(horiz_displacement, 2)}m\n")

if launch_angle == 90:
    horiz_displacement = 0

# PLOTTING DATA
x = [instant * v_0 for instant in evenly_spaced_instants]
y = [v_0 * instant * sin(launch_angle) - 0.5 * g * instant ** 2 + initial_height for instant in evenly_spaced_instants]

df = pd.DataFrame({'Instant (s)': evenly_spaced_instants, 'x': x, 'y': y}, dtype="float64")
df2 = pd.DataFrame({"Instant (s)": time / 2, "x": horiz_displacement / 2, "y": max_height}, index=[0],
                   dtype="float64")
df = pd.concat([df, df2], axis=0).sort_values("Instant (s)").reset_index(drop=True)

fig, ax = plt.subplots()
points, = ax.plot(x, y, "ro")
max_height_point, = ax.plot(horiz_displacement / 2, max_height, "+", color="black")

ax.set_xlim(0, 1.1 * horiz_displacement)
ax.set_ylim(min(initial_height, 0), 1.1 * max_height)
ax.set_title("Projectile Motion Graph")

velocity_vector = None
angle_text = None
coord_text = None


def on_click(event):
    global velocity_vector, angle_text, coord_text

    if event.inaxes == ax:
        idx = np.searchsorted(x, event.xdata)
        if idx < len(x):
            point_x = x[idx]
            point_y = y[idx]

            # Remove velocity vector, angle text, and coordinates of other points
            if velocity_vector:
                velocity_vector.remove()
                angle_text.remove()
                coord_text.remove()

            # Display coordinates
            coord_str = f"({round(point_x, 2)}, {round(point_y, 2)})"
            print(f"Clicked point: {coord_str}")
            coord_text = ax.annotate(coord_str, xy=(point_x, point_y), xytext=(point_x + 10, point_y),
                                     textcoords="data",
                                     arrowprops=dict(arrowstyle="->"))

            # Calculate velocity vector and angle
            velocity = v_0 * cos(launch_angle)
            angle = atan2(point_y - initial_height, point_x - 0)

            # Display velocity vector
            dx = velocity * np.cos(angle)
            dy = velocity * np.sin(angle)
            velocity_vector = ax.arrow(point_x, point_y, dx, dy, width=0.5, head_width=2, head_length=2, color="blue")
            ax.plot([point_x, point_x + dx], [point_y, point_y + dy], "k:", linewidth=0.5)  # Draw dotted line

            # Display angle
            angle_deg = degrees(angle)
            angle_text = ax.text(point_x + dx / 2, point_y + dy / 2, f"{round(angle_deg, 2)}°", color="blue",
                                 fontsize=8)

            # Update the plot
            plt.draw()


fig.canvas.mpl_connect("button_press_event", on_click)

plt.show()
