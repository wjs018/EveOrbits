from Tkinter import *
import tkFileDialog
from ttk import *

import dbQuery as db
import ShipSimulate as sim
import dogma
import numpy as np
import matplotlib
import csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from operator import itemgetter


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

        # Add a label for ship selector

        shipLabel = Label(self, text="Select Ship:").grid(
            row=0, column=0, sticky=W, padx=(5, 5))

        # Add a combobox to list ships

        self.getShipList()

        self.shipVar = StringVar()
        self.shipCombo = Combobox(
            self, textvariable=self.shipVar, state='readonly', width=30, height=20)
        self.shipList = self.ships[1]
        self.shipCombo['values'] = self.shipList
        self.shipCombo.set("Choose One...")
        self.shipCombo.grid(
            row=1, column=0, columnspan=3, sticky=W, padx=(5, 5))

        # Add a label for group selector

        groupLabel = Label(self, text="Select Group:").grid(
            row=3, column=0, sticky=W, padx=(5, 5))

        # Add a combobox to list groups

        # groups = self.getGroupList()

        self.groups = self.getGroupList()

        self.groupVar = StringVar()
        self.groupCombo = Combobox(
            self, textvariable=self.groupVar, state='readonly', width=30, height=15)
        self.groupCombo['values'] = self.groups[1]
        self.groupCombo.set("Choose One...")
        self.groupCombo.grid(
            row=4, column=0, columnspan=3, sticky=W, padx=(5, 5))

        self.groupCombo.bind("<<ComboboxSelected>>", self.getModuleList)

        # Add a label for module selector

        moduleLabel = Label(self, text="Select Module").grid(
            row=6, column=0, sticky=W, padx=(5, 5))

        # Add a combobox for module selector

        self.moduleList = [[], []]

        self.moduleVar = StringVar()
        self.moduleCombo = Combobox(
            self, state='readonly', width=30, height=15)
        self.moduleCombo['values'] = self.moduleList[1]
        self.moduleCombo.set("Choose One...")
        self.moduleCombo.grid(
            row=7, column=0, columnspan=3, sticky=W, padx=(5, 5))

        # Add a button to fit module

        fitButton = Button(self, text="Fit", command=self.addModule).grid(
            row=8, column=2, sticky=NE, padx=(5, 5))

        # Add a label for fitted module listbox

        fittedLabel = Label(self, text="Fitted Modules", padding=(5, 5, 5, 5)).grid(
            row=0, column=3, sticky=W, padx=(5, 5))

        # Add a listbox for the fitted modules

        self.fittedBox = Listbox(self, width=50, height=20)
        self.fittedList = []
        self.fittedIDs = []

        self.fittedBox.grid(
            row=1, column=3, rowspan=10, columnspan=3, sticky=NW, pady=(5, 5), padx=(5, 5))

        # Add a remove selected button

        removeButton = Button(self, text="Remove Selected", command=self.removeModule).grid(
            row=11, column=3, columnspan=3, sticky=SE, pady=(5, 5), padx=(5, 5))

        # Add a label for max speed output

        maxSpeedLabel = Label(
            self, text="Max Speed (m/s):").grid(row=0, column=6, columnspan=3, sticky=SW, padx=(5, 5))

        # Add an output for max speed

        self.maxSpeedVar = StringVar(value="Not Calculated")
        self.maxSpeedResult = Label(self, text=0, textvariable=self.maxSpeedVar, relief="sunken").grid(
            row=1, column=6, columnspan=3, sticky=NW, padx=(5, 5), pady=(5, 0))

        # Add a label for agility output

        agilityLabel = Label(self, text="Agility:").grid(
            row=2, column=6, columnspan=3, sticky=SW, pady=(5, 0), padx=(5, 5))

        # Add an output for agility

        self.agilityVar = StringVar(value="Not Calculated")
        self.agilityResult = Label(self, text=0, textvariable=self.agilityVar, relief="sunken").grid(
            row=3, column=6, columnspan=3, sticky=NW, padx=(5, 5), pady=(5, 0))

        # Add a label for mass output

        massLabel = Label(self, text="Mass (mill kg):").grid(
            row=4, column=6, columnspan=3, sticky=SW, padx=(5, 5), pady=(5, 0))

        # Add an output for mass

        self.massVar = StringVar(value="Not Calculated")
        self.massResult = Label(self, text=0, textvariable=self.massVar, relief="sunken").grid(
            row=5, column=6, columnspan=3, sticky=NW, padx=(5, 5), pady=(5, 0))

        # Add a quit button

        quitButton = Button(self, text="Quit", command=self.quit).grid(
            row=12, column=8, sticky=SE, padx=(5, 5), pady=(10, 5))

        # Add a calculate button

        calcButton = Button(self, text="Calculate!", command=self.calculateAttribs).grid(
            row=12, column=6, columnspan=2, sticky=SE, padx=(5, 5), pady=(10, 5))

        # Add a simulate button

        simButton = Button(self, text="Simulate!", command=self.runSimulation).grid(
            row=12, column=5, sticky=SE, padx=(5, 5), pady=(10, 5))

        # Add a checkbox to output sim results

        self.outputVar = IntVar()
        self.output = Checkbutton(
            self, text="Output sim results to .csv file?", variable=self.outputVar)
        self.output.grid(
            row=12, column=3, columnspan=2, sticky=SW, padx=(5, 5), pady=(10, 5))

        # Add orbit simulation entry fields and labels

        orbitSimLabel = Label(self, text="Parameters for Simulation:").grid(
            row=9, column=0, columnspan=3, sticky=W, padx=(5, 5))
        orbitSimRadLabel = Label(self, text="Start Radius (m):").grid(
            row=10, column=0, columnspan=2, sticky=W, padx=(5, 5))
        orbitSimRadEndLabel = Label(self, text="End Radius (m):").grid(
            row=11, column=0, columnspan=2, sticky=W, padx=(5, 5))
        orbitSimStepLabel = Label(self, text="Number of Radii:").grid(
            row=12, column=0, columnspan=2, sticky=W, padx=(5, 5))

        self.orbitSimRadVar = StringVar()
        self.orbitSimRadEndVar = StringVar()
        self.orbitSimStepVar = StringVar()

        self.orbitSimRadEnt = Entry(self, textvariable=self.orbitSimRadVar).grid(
            row=10, column=2, columnspan=1, sticky=E, padx=(5, 5))
        self.orbitSimRadEndEnt = Entry(self, textvariable=self.orbitSimRadEndVar).grid(
            row=11, column=2, columnspan=1, sticky=E, padx=(5, 5))
        self.orbitSimStepEnt = Entry(self, textvariable=self.orbitSimStepVar).grid(
            row=12, column=2, columnspan=1, sticky=E, padx=(5, 5))

        # Render everything

        self.pack()

    def getShipList(self):
        """
        Returns names and typeIDs of all the ships in the SDE

        Format: [[shipIDs], [shipNames]]
        """

        # First, get groupIDs of the Ships category (6)

        groupIDs = db.getGroupIDs(6)

        # Get shipIDs and shipNames

        shipIDs = []
        shipNames = []

        for i in range(0, len(groupIDs)):

            shipIDsTemp = db.getTypeIDs(groupIDs[i])
            shipIDs.extend(shipIDsTemp)

            for j in range(0, len(shipIDsTemp)):

                shipNames.append(db.getTypeName(shipIDsTemp[j]))

        # Sort by ship name alphabetically, while keeping the correct
        # typeID with the correct name

        shipIDs, shipNames = [
            list(x) for x in zip(*sorted(zip(shipIDs, shipNames), key=itemgetter(1)))]

        self.ships = [shipIDs, shipNames]

        # return ships

    def getGroupList(self):
        """
        Returns names and groupIDs of all the relevant groups in the SDE

        Format: [[groupIDs], [groupNames]]
        """

        # First, define list of all relevant groups (this was done by hand)

        groupIDs = [46, 763, 764, 329, 762, 78, 765, 782,
                    1308, 773, 1232, 300, 747, 957, 954, 955, 958, 956]
        groupNames = []

        for i in range(0, len(groupIDs)):

            selectStr = 'groupName'
            fromStr = 'invGroups'
            whereStr = 'groupID = ' + str(groupIDs[i]) + ' AND published = 1'

            result = db.SDEQuery(selectStr, fromStr, whereStr)

            for j in range(0, len(result)):

                groupNames.append(result[j][0])

        # Sort by group name alphabetically, while keeping the correct
        # groupID with the correct name

        groupIDs, groupNames = [
            list(x) for x in zip(*sorted(zip(groupIDs, groupNames), key=itemgetter(1)))]

        groups = [groupIDs, groupNames]

        return groups

    def getModuleList(self, val):
        """
        Updates the module list based off of the currently selected group.
        """

        idx = self.groupCombo.current()

        if idx != -1:

            groupID = self.groups[0][idx]

            moduleIDs = db.getTypeIDs(groupID)
            moduleNames = db.getTypeNames(groupID)

            self.moduleList = [moduleIDs, moduleNames]

            self.moduleCombo['values'] = self.moduleList[1]
            self.moduleCombo.set("Choose One...")

    def addModule(self):
        """
        This adds the currently selected module from self.moduleCombo
        to the listbox self.fittedBox
        """

        idx = self.moduleCombo.current()

        if idx != -1:

            self.fittedList.append(self.moduleList[1][idx])
            self.fittedIDs.append(self.moduleList[0][idx])

            self.fittedBox.insert(END, self.moduleList[1][idx])

    def removeModule(self):
        """
        This removes the currently selected module in self.fittedBox
        from self.fittedBox
        """

        idxs = self.fittedBox.curselection()

        for i in range(0, len(idxs)):

            self.fittedBox.delete(idxs[i])
            self.fittedIDs.pop(i)

    def calculateAttribs(self):
        """
        This creates a dogma Context object and fits modules that are in
        self.fittedIDs. Active effect modules will automatically be
        online and active. All other modules will just be set to be online. 
        Calculated parameters will be output to the GUI.
        """

        # Define Context object and fit the modules in self.fittedIDs

        self.ctx = dogma.Context()
        self.ctx.set_default_skill_level(5)

        shipIdx = self.shipCombo.current()
        shipID = self.ships[0][shipIdx]
        self.ctx.set_ship(shipID)

        for i in range(0, len(self.fittedIDs)):

            if dogma.type_has_active_effects(self.fittedIDs[i]):

                self.ctx.add_module(
                    self.fittedIDs[i], state=dogma.State.ACTIVE, charge=None)

            else:

                self.ctx.add_module(
                    self.fittedIDs[i], state=dogma.State.ONLINE, charge=None)

        # Now, update calculated attributes in the GUI

        self.maxSpeedVar.set("%.3f" % self.ctx.get_ship_attribute(37))
        self.agilityVar.set("%.5f" % self.ctx.get_ship_attribute(70))
        self.massVar.set("%.2f" % (self.ctx.get_ship_attribute(4) / 1000000))

        self.parent.update_idletasks()

    def runSimulation(self):
        """
        This runs a 2D simulation of the current context object in an orbit
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

            rad, vel, ang = sim.simulateOrbit(self.ctx, self.orbitList[i])

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
