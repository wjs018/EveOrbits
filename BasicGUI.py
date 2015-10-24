#=========================================================================
#
# Basic GUI interface for simulating the orbits of ships in Eve Online.
#
# contact: wjs018@gmail.com
#
#=========================================================================

from Tkinter import *
import tkFileDialog
from ttk import *

import dbQuery as db
import ShipSimulate as sim
import numpy as np
from operator import itemgetter
import csv

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class MainWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.plotNum = 0

        self.initUI()

    def initUI(self):

        # Set window title

        self.parent.title("EVE Orbits")

        # Set style for widgets

        Style().configure("TButton", padding=5)

        inputLabel = Label(self, text="Navigation Parameters:").grid(
            row=0, column=0, columnspan=3, sticky=W, padx=(5, 5), pady=(5,5))
        
        # Add a label for max speed output

        maxSpeedLabel = Label(
            self, text="Max Speed (m/s):").grid(row=1, column=0, columnspan=3, sticky=SW, padx=(5, 5))

        # Add an Entry for max speed

        self.maxSpeedVar = StringVar()
        self.maxSpeedResult = Entry(self, textvariable=self.maxSpeedVar).grid(
            row=2, column=0, columnspan=3, sticky=NW, padx=(5, 5), pady=(0, 5))

        # Add a label for mass output

        massLabel = Label(self, text="Mass (mill kg):").grid(
            row=3, column=0, columnspan=3, sticky=SW, padx=(5, 5), pady=(5, 0))

        # Add an Entry for mass

        self.massVar = StringVar()
        self.massResult = Entry(self, textvariable=self.massVar).grid(
            row=4, column=0, columnspan=3, sticky=NW, padx=(5, 5), pady=(0, 5))

        # Add a label for agility output

        agilityLabel = Label(self, text="Agility:").grid(
            row=5, column=0, columnspan=3, sticky=SW, padx=(5, 5), pady=(5, 0))

        # Add an output for agility

        self.agilityVar = StringVar()
        self.agilityResult = Entry(self, textvariable=self.agilityVar).grid(
            row=6, column=0, columnspan=3, sticky=NW, padx=(5, 5), pady=(0, 5))

        # Add a quit button

        quitButton = Button(self, text="Quit", command=self.quit).grid(
            row=8, column=5, sticky=SW, padx=(5, 5), pady=(5, 5))
        
        # Add a simulate button

        simButton = Button(self, text="Simulate!", command=self.runSimulation).grid(
            row=8, column=3, columnspan=2, sticky=SE, padx=(5, 5), pady=(5, 5))

        # Add a checkbox to output sim results

        self.outputVar = IntVar()
        self.output = Checkbutton(
            self, text="Output sim results to .csv file?", variable=self.outputVar)
        self.output.grid(
            row=7, column=3, columnspan=3, sticky=SW, padx=(5, 5), pady=(5, 10))

        # Add orbit simulation entry fields and labels

        orbitSimLabel = Label(self, text="Parameters for Simulation:").grid(
            row=0, column=3, columnspan=3, sticky=W, padx=(5, 5), pady=(5,5))
        orbitSimRadLabel = Label(self, text="Start Radius (m):").grid(
            row=1, column=3, columnspan=3, sticky=W, padx=(5, 5), pady=(5,0))
        orbitSimRadEndLabel = Label(self, text="End Radius (m):").grid(
            row=3, column=3, columnspan=3, sticky=W, padx=(5, 5), pady=(5,0))
        orbitSimStepLabel = Label(self, text="Number of Radii:").grid(
            row=5, column=3, columnspan=3, sticky=W, padx=(5, 5), pady=(5,0))

        self.orbitSimRadVar = StringVar()
        self.orbitSimRadEndVar = StringVar()
        self.orbitSimStepVar = StringVar()

        self.orbitSimRadEnt = Entry(self, textvariable=self.orbitSimRadVar).grid(
            row=2, column=3, columnspan=3, sticky=NW, padx=(5, 5), pady=(0,5))
        self.orbitSimRadEndEnt = Entry(self, textvariable=self.orbitSimRadEndVar).grid(
            row=4, column=3, columnspan=3, sticky=NW, padx=(5, 5), pady=(0,5))
        self.orbitSimStepEnt = Entry(self, textvariable=self.orbitSimStepVar).grid(
            row=6, column=3, columnspan=3, sticky=NW, padx=(5, 5), pady=(0,5))

        # Render everything

        self.pack()

    def runSimulation(self):
        """
        This runs a 2D simulation of a ship with the given paramters in an orbit
        specified by the user in the GUI. The results of this simulation are
        then output to the GUI.
        """

        # Define some variables

        self.orbitList = np.linspace(float(self.orbitSimRadVar.get()), float(
            self.orbitSimRadEndVar.get()), num=self.orbitSimStepVar.get())
        self.radiusList = []
        self.radDiffList = []
        self.velList = []
        self.angList = []

        for i in range(0, len(self.orbitList)):

            # Run the simulation

            rad, vel, ang = sim.simulateOrbit(float(self.maxSpeedVar.get()), float(
                self.massVar.get()), float(self.agilityVar.get()), self.orbitList[i])

            # Store the results

            self.radiusList.append(rad)
            self.radDiffList.append(rad - self.orbitList[i])
            self.velList.append(vel)
            self.angList.append(ang)

        # Save a csv file with results if box is checked

        if self.outputVar.get() == 1:

            outputfile = tkFileDialog.asksaveasfilename(
                defaultextension=".csv")

            if outputfile:

                writeFile = open(outputfile, 'wb')

            writer = csv.writer(writeFile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(('Prescribed Orbit Radius (m)',
                             'Actual Orbit Radius (m)',
                             'Difference in Orbit Radii (m)',
                             'Orbital Speed (m/s)',
                             'Angular Velocity (rad/s)'))

            for i in range(0, len(self.radiusList)):

                writer.writerow((self.orbitList[i],
                                 self.radiusList[i],
                                 self.radDiffList[i],
                                 self.velList[i],
                                 self.angList[i]))

            writeFile.close()

        # Plot some results

        self.plotNum += 1

        # First, make a new window

        graph = Toplevel()
        graph.title("Graph " + str(self.plotNum))

        # Create our plot and axes

        figure = Figure()
        ax = figure.add_subplot(111)
        plot = ax.plot(self.orbitList, self.radDiffList, 'ob')
        ax.set_xlabel('Prescribed Orbit Radius (m)')
        ax.set_ylabel('Actual - Prescribed Difference (m)')

        # Configure our graph to expand when the window is resized

        Grid.rowconfigure(graph, 0, weight=1)
        Grid.columnconfigure(graph, 0, weight=1)

        # Draw the figure in our window

        canvas = FigureCanvasTkAgg(figure, master=graph)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, sticky=NSEW)

        # Create the toolbar at the bottom of the graph and a Frame
        # to hold it in

        toolbarFrame = Frame(graph)
        toolbarFrame.grid(row=1, sticky=W)
        toolbar = NavigationToolbar2TkAgg(canvas, toolbarFrame)
        toolbar.update()


def main():

    matplotlib.use('TkAgg')
    root = Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
