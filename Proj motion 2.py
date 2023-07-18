from math import sin, cos, atan2, degrees, radians, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, xlim, ylim, grid

# VARIABLES
v_0: float = 74
launch_angle: float = radians(55)
num_pts_to_plot: int = 22
g: float = 9.81
initial_height: float = 0  # Set the initial height here

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
	
def y_pos(instant):
	global v_0, launch_angle, g, initial_height
	return v_0 * instant * sin(launch_angle) - 0.5 * g * instant ** 2 + initial_height

# PLOTTING DATA
x = [instant * v_0 for instant in evenly_spaced_instants]
y = [y_pos(instant) for instant in evenly_spaced_instants]

# All points but the point of max height
df = pd.DataFrame({'Instant (s)': evenly_spaced_instants, 
					'x': x, 
					'y': y}, 
					dtype="float64")

# Point of max height
df2 = pd.DataFrame({"Instant (s)": 0.5 * time, 
					"x": 0.5 * horiz_displacement, 
					"y": max_height}, 
					index=[0],
					dtype="float64")

df = pd.concat([df, df2], axis=0).sort_values("Instant (s)").reset_index(drop=True)

fig, ax = plt.subplots()
points, = ax.plot(x, y, "ro")
max_height_point, = ax.plot(0.5 * horiz_displacement, max_height, "+", color="black")

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
			# angle = atan2(point_y - initial_height, point_x)
   			# Formula: v_y(t) = -g*t + vi_y
			angle = atan2(-g*evenly_spaced_instants[idx] + v_0*sin(launch_angle), velocity)

			
			# Display velocity vector
			dx = velocity * cos(angle)
			dy = velocity * sin(angle)
			
			print(velocity, dx, dy, round(degrees(angle), 1))
			velocity_vector = ax.arrow(point_x, point_y, dx, dy, width=0.5, head_width=6, head_length=8, color="blue")
			ax.plot([point_x - dx, point_x + dx], [point_y, point_y], "k:", linewidth=0.5)  # Draw dotted line

			# Display angle
			angle_deg = degrees(angle)
			print(angle, angle_deg)
			angle_text = ax.text(point_x + dx / 2, point_y - dy / 2, f"{round(angle_deg, 2)}°", color="blue",
								 fontsize=8)

			# Update the plot
			plt.draw()


fig.canvas.mpl_connect("button_press_event", on_click)

plt.show()
