# Projectile Motion Simulation

This Python code simulates the motion of a projectile launched at a given velocity and angle. It calculates the trajectory of the projectile, plots the motion graph, and provides interactive features.

## Dependencies

The following Python libraries are required to run the code:
- `math`: Provides mathematical functions such as sine, cosine, and square root.
- `numpy`: Handles numerical operations and array manipulations.
- `pandas`: Manages successive position data in tabular form.
- `matplotlib.pyplot`: Generates plots and visualizations.
- `matplotlib.patches`: Provides classes for drawing shapes and patches.

Make sure you have these libraries installed before running the code.

## Usage

1. Launch the program and provide the following input parameters:
   - `launch velocity of projectile (positive)`: The initial velocity of the projectile in meters per second (m/s).
   - `launch angle in degrees`: The launch angle of the projectile in degrees.
   - `number of points to plot (whole number)`: The number of data points to plot in the motion graph.
   - `initial height of launch in meters`: The initial height of the projectile at launch in meters (m).
   
2. The program will calculate the trajectory of the projectile assuming no friction. It will display various calculations, such as the maximum height, time of flight, horizontal displacement, and initial velocities.

3. A plot will be generated showing the motion of the projectile. The red dots represent the trajectory, and the black plus sign indicates the point of maximum height.

4. Interact with the plot by clicking on any point along the trajectory. The program will display information about the clicked point, including the coordinates, time, speed, and vertical velocity.

5. The program will draw a velocity vector and display its angle with respect to the horizontal axis. It will also draw a dotted line from the point to the x-axis, representing the horizontal component of the velocity.

6. The plot will update dynamically to reflect the changes made by clicking on different points.

7. Close the plot window to exit the program.

## Limitations

- The simulation assumes no friction or air resistance, which may not be realistic in practical scenarios.
- The simulation does not consider external factors such as wind or other forces acting on the projectile.
- The calculation and plotting of the trajectory are based on simplified mathematical models and may not perfectly match real-world observations.

## Acknowledgements

This code was developed to provide a basic simulation of projectile motion using Python. It was inspired by the concepts of physics and numerical calculations. Feel free to modify and expand the code according to your specific needs.

