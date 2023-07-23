from math import sin, cos, atan2, degrees, radians, ceil, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arrow
from pylab import plot, show, title, xlabel, ylabel, xlim, ylim, grid

# VARIABLES
v_0: float = float(input('Input launch velocity of projectile (positive): ')) # 74
launch_angle: float = radians(float(input('Input launch angle in degrees: '))) # radians(55)
y_o: float = float(input('Input initial height of launch in metres: '))  # 0
g: float = 9.81

# CALCULATIONS
time: float = 2 * v_0 * sin(launch_angle) / g
num_pts_to_plot: int = ceil(30*time) # We want animation frame rate of 30 fps
evenly_spaced_instants = list(np.linspace(0, time, num=num_pts_to_plot, endpoint=True))
y_max: float = (v_0* sin(launch_angle)) ** 2 / (2 * g) + y_o
horiz_displacement: float = 0 if launch_angle == 90 else v_0 * cos(launch_angle) * time 

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

def calc_v_y(instant):
	return -g*instant + v_0*sin(launch_angle)

# PLOTTING DATA
x = [ instant * v_0 * cos(launch_angle) for instant in evenly_spaced_instants ]
y = [ y_pos(instant) for instant in evenly_spaced_instants ]
vi_x = v_0 * cos(launch_angle)
# v_x = [ v_0 * cos(launch_angle) ] * num_pts_to_plot
v_y = [ calc_v_y(instant) for instant in evenly_spaced_instants ]

data_df = pd.DataFrame({'Instant (s)': evenly_spaced_instants, 
					'x': x, 
					'y': y,
	 				# 'v_x': v_x,
		 			'v_y': v_y}, 
					dtype="float64")

h_max_point = pd.DataFrame({"Instant (s)": 0.5 * time, 
					"x": 0.5 * horiz_displacement, 
					"y": y_max,
	 				# 'v_x': v_x[0],
		 			'v_y': 0}, 
					index=[0], dtype="float64")

data_df = pd.concat([data_df, h_max_point], axis=0).sort_values("Instant (s)").reset_index(drop=True)

# data_df['v'] = sqrt(data_df['v_x']**2 + data_df['v_y']**2)

fig, ax = plt.subplots()
points, = ax.plot([], [], "ko") # 'ko' is for black points
y_max_point, = ax.plot([], [], "+", color="black")

# Draw curved trajectory
trajectory, = ax.plot([], [], "b--")

# Function to update plot during animation
def update_plot(frame):
	global ax
	points.set_data(x[frame], y[frame])
	y_max_point.set_data(0.5 * horiz_displacement, y_max)
	trajectory.set_data(x[:frame], y[:frame])

	# Add arrows for horizontal and vertical velocities	
 	# Get the current velocities from the data_df DataFrame
	curr_v_y = data_df['v_y'][frame]

	# Remove previous arrows before adding new ones
	[ arrow.remove() for arrow in ax.patches ]	

	# Calculate the scaling factors for the lengths and widths of the arrows
	x_length_scale = vi_x / (1.1*horiz_displacement)
	y_length_scale = max(v_y) / (1.1*y_max)
	standardized_length_scale = 0.15
	width_scale = 1.1*horiz_displacement/10.89

	# Add vectors and vertical and resultant velocities
	vx_arrow = Arrow(x[frame], 
					 y[frame],
					 (vi_x/x_length_scale)*standardized_length_scale,
					 0,  
					 width=0.1*width_scale, 
					 color='blue'
    )
	vy_arrow = Arrow(x[frame],# + (vi_x/x_length_scale)*standardized_length_scale, 
					 y[frame], 
					 0, 
					 (curr_v_y/y_length_scale)*standardized_length_scale, 
					 width=0.25*width_scale, 
					 color='green'
    )
	v_arrow = Arrow(x[frame], 
					y[frame], 
					(vi_x/x_length_scale)*standardized_length_scale, 
					(curr_v_y/y_length_scale)*standardized_length_scale, 
					width=0.1*width_scale, 
					color='red'
    )
	
	ax.add_patch(vx_arrow)
	ax.add_patch(vy_arrow)
	ax.add_patch(v_arrow)

	return points, y_max_point, trajectory

ax.set_xlim(0, 1.1 * horiz_displacement)
ax.set_ylim(min(y_o, 0), 1.1 * y_max)
ax.set_title("Projectile Motion Graph")

# Remember that we want a frame rate of 30fps
# Blitting is an optimization technique used in animations to only redraw parts of the plot that have changed
# It can improve performance, however in some cases, it can cause issues with the animation
# If you don't care about the vector animations, you can set blit to True, especially when time of flight >= 10 secs
animation = FuncAnimation(fig, update_plot, frames=num_pts_to_plot, interval=num_pts_to_plot/30, blit=False)

plt.show()
