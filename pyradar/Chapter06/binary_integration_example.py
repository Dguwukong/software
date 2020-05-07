"""
Project: RadarBook
File: binary_integration_example.py
Created by: Lee A. Harrison
On: 10/11/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter06.ui.BinaryIntegration_ui import Ui_MainWindow
from Libs.detection.binary_integration import probability_of_detection
from Libs.detection.single_pulse import pd_rayleigh
from numpy import linspace, log10
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class BinaryIntegration(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.signal_to_noise.returnPressed.connect(self._update_canvas)
        self.probability_of_false_alarm.returnPressed.connect(self._update_canvas)
        self.m.returnPressed.connect(self._update_canvas)
        self.n.returnPressed.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure() 
        self.axes1 = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # Update the canvas for the first display
        self._update_canvas()

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        # Get the parameters from the form
        snr_db = self.signal_to_noise.text().split(',')
        snr = 10.0 ** (linspace(float(snr_db[0]), float(snr_db[1]), 200) / 10.0)
        pfa = float(self.probability_of_false_alarm.text())
        m = int(self.m.text())
        n = int(self.n.text())

        # Calculate the probability of detection
        pd = [probability_of_detection(m, n, pd_rayleigh(isnr, pfa)) for isnr in snr]

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(10.0 * log10(snr), pd, '')

        # Set the plot title and labels
        self.axes1.set_title('Binary Integration (M of N)', size=14)
        self.axes1.set_xlabel('Signal to Noise (dB)', size=12)
        self.axes1.set_ylabel('Probability of Detection', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = BinaryIntegration()  # Set the form
    form.show()                 # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = BinaryIntegration()    # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
