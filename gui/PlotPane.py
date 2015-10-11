from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc
rc('font', **{'family':'verdana'})
import sys


class PlotPane(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.create_plot()

    def create_plot(self):
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.xaxis.grid()
        self.axes.yaxis.grid()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def refresh_plot(self, x_list, y_list):
        self.axes.clear()
        self.axes.xaxis.grid()
        self.axes.yaxis.grid()
        self.axes.plot(x_list, y_list)
        self.figure.canvas.draw()

def draw_2d_plot(x_list=None, y_list=None):
    app = QApplication(sys.argv)
    plot = PlotPane()
    plot.refresh_plot(x_list, y_list)
    plot.show()
    sys.exit(app.exec_())


# def draw(x_list, y_list):
#     figure = plt.figure()
#     axes = figure.add_subplot(1, 1, 1)
#     axes.xaxis.grid()
#     axes.yaxis.grid()
#     axes.plot(x_list, y_list)
#     plt.show()