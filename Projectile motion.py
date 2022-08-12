from math import sin, radians
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pylab import plot, show, title, xlabel, ylabel, xlim, ylim, grid

# IMPORTING MODULES FOR MATHEMATICS AND PLOTTING

# ---------------------------------------------------------------------

# VARIABLES

# v_0 = float( input("What is the initial speed? ") )
# launch_angle = radians( float(input("What is the launch angle? ")) )
# num_pts_to_plot = int( input("Points to plot: ") )

v_0:float = 74
launch_angle:float = radians(55)
num_pts_to_plot:int = 22
g:float = 9.81

# elevation = input("What is the elevation of the projectile?")

# ----------------------------------------------------------------------

# CALCULATIONS

time:float = 2 * v_0 * sin(launch_angle) / g
evenly_spaced_instants = list(np.linspace(0, time, num=num_pts_to_plot, endpoint=True))

# We need half as many pts for height as descent is mirror of ascent
max_height:float = (v_0**2 * sin(launch_angle)**2) / (2*g)

horiz_displacement:float = v_0 * time

# ----------------------------------------------------------------------

# PRINTING RESULTS

print(f"""\nAll values are rounded to 2 decimal places.\nMax height: {round(max_height, 2)}m
Time of flight: {round(time, 2)}s
Horizontal displacement: {round(horiz_displacement, 2)}m\n""")

# print(f"Time of flight: {round(time, 2)}s")

if launch_angle == 90: horiz_displacement = 0

# print(f"Horizontal displacement: {round(horiz_displacement, 2)}m\n")

# ----------------------------------------------------------------------

# PLOTTING DATA

x = [ instant * v_0 for instant in evenly_spaced_instants ]
y = [ (v_0 * (instant) * sin(launch_angle)) - 0.5 * g * (instant)**2 
		for instant in evenly_spaced_instants ]

df = pd.DataFrame({'Instant (s)': evenly_spaced_instants,
					'x': x, 
					'y': y}, 
				  dtype="float64")
# Max height entry
df2 = pd.DataFrame({"Instant (s)": time / 2, 
		  				"x": horiz_displacement / 2, 
		  				"y": max_height}, 
					index=[0], 
					dtype="float64")

df = pd.concat([df, df2], axis=0).sort_values("Instant (s)").reset_index(drop=True)

# df = df.sort_values("Instant (s)")
print(df)

# plt.plot(x, y, "ro", linewidth=1)
# plt.show()

fig, ax = plt.subplots()
ax.plot(x, y, "ro")
ax.plot(horiz_displacement / 2, max_height, "+", color="black")

# Plot a vertical line for max height, and add text for it
ax.axvline(x=horiz_displacement/2, 
			ymin=min(y), 
			ymax=max_height, 
			color="black", 
			linestyle=":", 
			linewidth=2)

ax.text(horiz_displacement/2, 
		 max_height * 1.02, 
		 f"Max h: {round(max_height, 2)}", 
		 horizontalalignment="center")

ax.set_xlim(0, 1.1*horiz_displacement)
ax.set_ylim(0, 1.1*max_height)
ax.set_title("Projectile Motion Graph")
plt.show()

"""
for i in range(0, num_pts_to_plot + 1):
	t_for_c = i * time_interval       
	
	x = t_for_c * v_0 * cos(launch_angle)
	y = (v_0 * t_for_c * sin(launch_angle)) - 0.5 * g * t_for_c**2
	
	print(
		round(x, 2),
		round(y, 2),
		round(t_for_c, 2)
	)
	
	plot(x, y, 'ro')
#   plot([t_20 * math.cos(launch_angle) * v_0], [i * t_20 * math.sin(launch_angle) * initial_speed], 'ro')
	plot(x, y, linewidth = 2)

grid()

title("Projectile Motion Graph ")

xlim(0, horiz_displacement * 1.1)
ylim(0, max_height * 1.1)
 
xlabel("Distance travelled (m) ")
ylabel("Height (m) ")

show()
"""
