import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os.path
from tkinter import messagebox
from rent import Rent


class DialogWindow(tk.Toplevel):
    '''
    this class creates the radiobuttons for the user to select their choice
    '''

    def __init__(self, master, rent):
        self.rent = rent
        tk.Toplevel.__init__(self, master)

        canvas = tk.Canvas(self, height=700, width=1000, background='#2C5881')
        canvas.pack()

        self.grab_set()
        self.focus_set()
        self.transient(master)

        self.frame = tk.Frame(self, background='#81F0F7', border=5)
        self.frame.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)

        self.selection = tk.IntVar(master)
        self.selection.set(0)
        self.cityList = rent

        x = 0.05
        #print("start button", self.cityList)
        for i in range(len(self.cityList)):
            self.radioButton = tk.Radiobutton(self.frame, text=self.cityList[i], variable=self.selection, value=i,
                                              background='#81F0F7',
                                              font=("Palatino Linotype", 15, 'bold'), indicatoron=False)
            self.radioButton.place(relx=0.2, rely=x, relwidth=0.6, relheight=.08)
            x += 0.09

        self.radioButton10 = tk.Radiobutton(self.frame, text='All', variable=self.selection, value=-1,
                                            background='#81F0F7',
                                            font=("Palatino Linotype", 15, 'bold'), indicatoron=False)
        self.radioButton10.place(relx=0.2, rely=x, relwidth=0.6, relheight=.06)

        self.plotButton = tk.Button(self.frame, text='Okay',
                                    command=self.setNum,
                                    font=("Palatino Linotype", 15, 'bold'))
        self.plotButton.pack(side='bottom', fill='both')

    def setNum(self):
        self.num = self.selection.get()
        self.destroy()

    def getNum(self):
        return self.num


class PlotWindow(tk.Toplevel):
    '''
    this class plots the price trend or bar chart depending on the user choice
    '''

    def __init__(self, master, fct, *args):
        self.master = master
        super().__init__(master)
        #self.rent = rent
        fig = plt.figure(figsize=(8, 7))
        fct(*args)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
        '''
    def plotGUI(self, rent, num):
        
        fig = plt.figure(figsize=(13, 12))
        rent.priceTrend(num)
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().grid()
        canvas.draw()

        # def plotBar(self, rent):
        '''
        '''
        this function plots the bar chart using the currentBarChart function in rent.py
        :param master: the root class which is Tk
        '''


class MainWindow(tk.Tk):
    '''
    this class create main window from tk class and catches errors with the opening of the files
    '''

    def __init__(self, *infilenames):
        self.rent = Rent()
        super().__init__()
        # self.rentFiles = infilenames
        self.canvas = tk.Canvas(self, height=700, width=1200)
        self.canvas.pack()

        frame = tk.Frame(self.canvas, background='#2C5881', border=5)
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        button = tk.Button(frame, text='Rental Price Trend', background='#CBD7D5', border=5, command=self.displayDialog)
        button.place(relx=0.05, rely=0.6, relwidth=0.4, relheight=0.2)
        button.config(font=("Palatino Linotype", 20, 'bold'))

        button2 = tk.Button(frame, text='Current Rental Prices', background='#CBD7D5', border=5,
                            command=self.displayBar)
        button2.place(relx=0.55, rely=0.6, relwidth=0.4, relheight=0.2)
        button2.config(font=("Palatino Linotype", 20, 'bold'))

        label = tk.Label(frame, text='Rent Data for Santa Clara County', background='#2C5881')
        label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)
        label.config(font=("Palatino Linotype", 40, 'bold'))

        label2 = tk.Label(frame,
                          text='The purpose of this app is to allow a user to find rental trends and current prices',
                          background='#2C5881')
        label2.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.2)
        label2.config(font=("Palatino Linotype", 15, 'italic'))

        for file in infilenames:
            if os.path.exists(file) == False or os.path.isfile(file) == False:
                tk.messagebox.showwarning("Error", "Cannot open this file\n(%s)" % file)


    def displayDialog(self):
        '''
        opens a DialogWindow for the price trend and plots the trend depending on user choice
        '''
        #print("before dialog window", self.rent.cityList)
        dWin = DialogWindow(self, self.rent.cityList) #create get method for citylist
        self.wait_window(dWin)
        choice = dWin.getNum()
        PlotWindow(self, self.rent.priceTrend, choice)


    def displayBar(self):
        '''
        creates a plotWindow graphing the bar chart
        '''
        bWin = PlotWindow(self, self.rent.currentRentBarChart)


infileNames = ["rent.csv", "zipCity.csv"]

mainWin = MainWindow(*infileNames)
mainWin.mainloop()
