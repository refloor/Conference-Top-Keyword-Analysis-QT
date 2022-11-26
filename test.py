import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("matplotlib embeded in Python Qt")
        self.initUI()
        self.plotfig()
        
    def initUI(self):
        self.fig = plt.figure()
        self.canvas=FigureCanvas(self.fig)
        self.figtoolbar=NavigationToolbar(self.canvas, self)
        
        self.btn_start=QPushButton("start")
        self.btn_pause=QPushButton("pause")
        hlayout=QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(self.btn_start)
        hlayout.addWidget(self.btn_pause)
        hlayout.addStretch(1)
        
        vlayout=QVBoxLayout()
        vlayout.addWidget(self.figtoolbar)
        vlayout.addWidget(self.canvas)
        vlayout.addLayout(hlayout)
        widget=QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        
        
            
    def plotfig(self):
        ax = self.fig.subplots()
        self.t = np.linspace(0,2*np.pi,50)
        self.lines=ax.plot(np.sin(self.t))
        ax.autoscale_view()

        def aniupdate(i):
            t=self.t+2*np.pi*i/50
            self.lines[0].set_ydata(np.sin(t))
            return self.lines
        self.ani=FuncAnimation(self.fig, aniupdate, interval=100)
        self.btn_start.clicked.connect(self.ani.resume)
        self.btn_pause.clicked.connect(self.ani.pause)
        
app=QApplication(sys.argv)
win = MainWin()
win.show()
sys.exit(app.exec())
