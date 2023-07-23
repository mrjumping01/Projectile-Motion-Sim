from math import sin, cos, atan2, degrees, radians, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.patches as patches
from pylab import plot, show, title, xlabel, ylabel, xlim, ylim, grid

# VARIABLES
v_0: float = float(input('Input launch velocity of projectile (positive): ')) # 74
launch_angle: float = radians(float(input('Input launch angle in degrees: '))) # radians(55)
num_pts_to_plot: int = int(input('Input number of points to plot (whole number): ')) # 22
y_o: float = float(input('Input initial height of launch in metres: '))  # 0
g: float = 9.81

# CALCULATIONS - ASSUMING NO FRICTION
time: float = 2 * v_0 * sin(launch_angle) / g
evenly_spaced_instants = list(np.linspace(0, time, num=num_pts_to_plot, endpoint=True))
y_max: float = (v_0 * sin(launch_angle)) ** 2 / (2 * g) + y_o
horiz_displacement: float = 0 if round(launch_angle, 2) == 90 else v_0 * cos(launch_angle) * time

# PRINTING CONSTANTS
print(f"\nCalculations do not account for friction. All values are rounded to 2 decimal places.")
print(f"----------\nMax height: {round(y_max, 2)}m")
print(f"Time of flight: {round(time, 2)}s")
print(f"Horizontal displacement: {round(horiz_displacement, 2)}m")
print(f"V_i: {round(v_0, 2)}m/s")
print(f"Vi_x: {round(v_0 * cos(launch_angle), 2)}m/s")
print(f"Vi_y: {round(v_0 * sin(launch_angle), 2)}m/s\n----------")

def y_pos(instant):
	global v_0, launch_angle, g, y_o
	return v_0 * instant * sin(launch_angle) - 0.5 * g * instant ** 2 + y_o

# PLOTTING DATA
x = [ instant * v_0 * cos(launch_angle) for instant in evenly_spaced_instants ]
y = [ y_pos(instant) for instant in evenly_spaced_instants ]

# All points but the point of max height
data_df = pd.DataFrame({'Instant (s)': evenly_spaced_instants,
				   'x': x,
				   'y': y},
				  dtype="float64")

# Point of max height
h_max_point = pd.DataFrame({"Instant (s)": 0.5 * time,
					"x": 0.5 * horiz_displacement,
					"y": y_max},
				   index=[0],
				   dtype="float64")

data_df = pd.concat([data_df, h_max_point], axis=0).sort_values("Instant (s)").reset_index(drop=True)

fig, ax = plt.subplots()
points, = ax.plot(x, y, "ro")
y_max_point, = ax.plot(0.5 * horiz_displacement, y_max, "+", color="black")

ax.set_xlim(0, 1.1 * horiz_displacement)
ax.set_ylim(min(y_o, 0), 1.1 * y_max)
ax.set_title("Projectile Motion Graph")

velocity_vector = None
angle_text = None
dotted_lines = []  # Store the dotted line objects
arc = None  # Store the arc object

def on_click(event):
	global velocity_vector, angle_text, dotted_lines, arc

	if event.inaxes == ax:
		idx = np.searchsorted(x, event.xdata)
		if idx < len(x):
			point_x = x[idx]
			point_y = y[idx]

			# Remove velocity vector, angle text, coordinates, and dotted lines of other points
			if velocity_vector:
				velocity_vector.remove()
				angle_text.remove()
				# coord_text.remove()
				for line in dotted_lines:
					line.remove()
				dotted_lines.clear()
			if arc:
				arc.remove()

			# Defining v_x and v_y at clicked point
			v_x = v_0 * cos(launch_angle)
			v_y = -g*evenly_spaced_instants[idx] + v_0*sin(launch_angle)
   
			# Print info about clicked point
			coord_str = f"({round(point_x, 2)}, {round(point_y, 2)})"
			print(f"----------\nClicked point: {coord_str}")
			print(f"Time: {round(evenly_spaced_instants[idx], 2)}s")
			print(f"Speed: {round(sqrt(v_x**2 + v_y**2), 2)}m/s")
			print(f"V_y: {round(v_y, 2)}m/s")
			
			# Calculate angle of velocity vector knowing tan(theta) = v_y/v_x
			angle = atan2(v_y, v_x)

			# Display velocity vector and angle on plot
			velocity_vector = ax.arrow(point_x, point_y, v_x, v_y, width=0.5, head_width=1, head_length=3, color="blue")
			angle_deg = round(degrees(angle), 2)
			angle_text = ax.text(point_x + 0.5 * v_x, point_y - 0.5 * v_y, f"{angle_deg}°", color="blue",
								 fontsize=8)

			print(f"Velocity vector angle: {angle_deg}°\n----------")
	
			# Draw dotted line
			dotted_line = ax.plot([point_x - v_x, point_x + v_x], [point_y, point_y], "k:", linewidth=0.5)
			dotted_lines.append(dotted_line[0])
   
			# Draw angle arc
			# LOGIC: 
			# If angle upwards, then v_y positive, start at 0 and draw angle in trig direction
			# If angle downwards, v_y negative, start at 360 - abs(angle) (angle negative) and move to 0 in trig direction
			radius = 0.5 * abs(v_x)
			start_angle = 0 if v_y >= 0 else 360 - abs(angle_deg)
			end_angle = start_angle + angle_deg if v_y >= 0 else 0
			# print(start_angle, end_angle)
			arc = patches.Arc((point_x, point_y), radius, radius, 0, start_angle, end_angle, color="green")
			ax.add_patch(arc)
			
			# Update the plot
			plt.draw()


fig.canvas.mpl_connect("button_press_event", on_click)

plt.show()
