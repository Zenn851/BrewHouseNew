import ttkbootstrap as ttk
from random import randint
# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style
import matplotlib as mpl
from matplotlib.figure import Figure
import time
import threading
import pandas as pd
from datetime import datetime

mpl.style.use('dark_background')

class BrewPlotting(threading.Thread):

    def __init__ (self,name,root):
        threading.Thread.__init__(self)
        self.name = name

        lab = ttk.Label(root).pack()

        self.fig = Figure(facecolor="#354050")
        self.ax = self.fig.add_subplot(111)
        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.get_tk_widget().pack(side="top",fill='both',expand=True)

    def plotFormat(self):
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.set_title("show a titellllll")
        self.ax.set_facecolor("#354050")

        #self.ax.grid()

    def data_points(self):
        try:
            tempInfo = pd.read_csv('tempInfo.csv')
        except:
            tempInfo = pd.DataFrame(columns = ["Tank","Temperature","Time"])
            tempInfo.to_csv('tempInfo.csv')

        x = []
        y = []

        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        temp = randint(0, 10)



        tempInfo.to_csv('tempInfo.csv')



    def run(self):
        while True:
            self.data_points()
            self.ax.cla()
            self.plotFormat()
            dpts = pd.read_csv('tempInfo.csv')
            self.ax.plot(dpts["Time"],dpts["Temperature"], marker='o', color='orange')
            self.graph.draw()
            time.sleep(1)

if __name__ == '__main__':
    def app():
        # initialise a window.
        root = ttk.Window("Brew", "superhero",resizable=(False, False))
        root.geometry('800x600') #1280x1024


        i = BrewPlotting(name="Plot",root=root)
        i.setDaemon(True)
        i.start()

        root.mainloop()


    app()


# x_data.append(new_x)
# y_data.append(new_y)
# x_data = x_data[1:]
# Y_data = y_data[1:]
