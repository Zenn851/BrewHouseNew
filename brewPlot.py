import ttkbootstrap as ttk
from random import randint
# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style
import matplotlib as mpl
import matplotlib.dates as dates
from matplotlib.figure import Figure
import time
import threading
import pandas as pd
from datetime import datetime
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np

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
        #self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperature in F")
        self.ax.set_title("Tank Temperate Plotting")
        self.ax.set_facecolor("#354050")

        #self.ax.grid()

    def data_points(self):
        try:
            tempInfo = pd.read_csv('tempInfo.csv')
        except:
            data = {"Tank":["FV1"],"Temperature":[0],"Time":[0]}
            tempInfo = pd.DataFrame.from_dict(data)
            tempInfo.to_csv('tempInfo.csv',index=False)


        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        temp = randint(0, 10)
        tempInfo.loc[len(tempInfo.index)]=["FV1",temp,time]
        #Limits the length of the data frame to 100 readings
        tempInfo=tempInfo.iloc[-100:]
        tempInfo.to_csv('tempInfo.csv', index=False)



    def run(self):
        while True:
            self.data_points()
            self.ax.cla()
            self.plotFormat()
            dpts = pd.read_csv('tempInfo.csv')

            x,y=dpts["Time"][-10:],dpts["Temperature"][-10:]


            self.ax.stackplot(dpts["Time"][-10:],dpts["Temperature"][-10:])
            #self.ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m'))
            self.fig.autofmt_xdate()
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
