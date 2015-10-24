# EveOrbits

EveOrbits is a simulation designed to systematically determine the radius a ship will orbit a point in space.

EveOrbits features a GUI to allow the user to specify a fit for a given ship as well as visualize simulation results.

## Dependencies

* Python 2.x (Python 3 untested)
* External fitting tool in order to get navigation paramters for a ship/fit.

## Using the GUI

Running BasicGUI.py brings up the graphical interface for EveOrbits. Down the left side of the window are three inputs for the maximum speed in m/s, the mass of the ship in millions of kg, and the agility multiplier for the ship. These can be found either through the in-game fitting window, or through a third party fitting tool such as EFT, pyfa, or o.smium.org.

The right side of the window is where parameters for the simulation are entered. The top entry box is the first radius at which an orbit is prescribed to the ship in meters. The second entry box is the final radius at which an orbit is prescribed to the ship in meters. The final box is the total number of radii at which to run the simulation. Together, the three values are arguments in a `numpy.linspace` command. The checkbox allows for the simulation results to be output to a .csv file. The save location will be given by the user via a dialog window. Once all of these parameters are set to your liking, hitting the `Simulate!` button will run the simulations of the orbits via calls to ShipSimulate.py. Depending on the what was entered, and the ship/fitting, this can take up to a few minutes, especially for large, slow ships as their dynamics evolve on a longer timescale.

Once a simulation is complete, a graph will open up showing the results. It plots the difference between the prescribed and actual orbital radius as a function of the prescribed radius. Multiple graph windows can be open at once just by running another simulation via the main window. The values that are plotted can be changed in the `MainWindow.runSimulation` function. If selected, the .csv file that is output will contain more information than the plot shows by default. In addition to the radii, the .csv file will show the stable velocity achieved by the orbiting ship as well as the angular velocity of the orbit.

## Using the `simulateOrbit` function

The GUI can be a bit limiting if a systematic simulation of multiple ships/fits is desired. In this case, you can use the `ShipSimulate.simulateOrbit` function. The function is passed a `dogma.Context` object from the libdogma engine as well as a prescribed orbit radius in meters. It will output the actual orbit radius as well as the orbital velocity and angular velocity. A simple example is included in the ShipSimulate.py file.

## Contact

* Walter Schwenger, wjs018@gmail.com
