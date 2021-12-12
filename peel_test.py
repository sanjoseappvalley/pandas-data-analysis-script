import glob
import os
import os.path
import sys
from matplotlib import patches
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *


def plotbar(x, y):
    chart_title = entry1.get()
    df = pd.DataFrame({"x": x, "y": y})
    plt.figure(figsize=(12, 6))
    splot = sns.barplot(x="x", y="y", data=df, palette=sns.color_palette('Blues'))
    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.4f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 9), textcoords='offset points')
    plt.title(chart_title)
    plt.xlabel("Pull Samples")
    plt.ylabel("Average Force (N)")
    plt.savefig('bar_chart_of_means.png')
    plt.show()

   
def organizepeeltest():

    location = askdirectory(title = "Select Location of Pull Test Data.")
    if(not location):
        sys.exit(0)

    cleandatalocation = askdirectory(title = "Select Location to Save Cleaned Data.")
    if(not cleandatalocation):
        sys.exit(0)

    os.chdir(location)
    filenames = glob.glob("*.csv")

    sample_names = []
    sample_means = []

    for file in filenames:
        os.chdir(location)
        try:
            # CHECK THIS BEFORE RUN, skip rows depends on which test
            # df = pd.read_csv(file) # to set columns: names = col_list
            # df = pd.read_csv(file, skiprows=4, encoding='utf-8')
            df = pd.read_csv(file)
            #Drop early start and final break
            df.drop(df.head().index, inplace=True) # default = 5
            df.drop(df.tail(50).index, inplace=True)
        except:
            print("couldn't open df")

        df = df.rename(columns = {"Peel Displacement":"Peel Displacement (mm)", "Force":"Force (N)", "Force / Width":"Force/Width (N/mm)"})

         #Calculate the mean of Force column
        df["Force (N)"] = pd.to_numeric(df["Force (N)"])
        sample_mean = df["Force (N)"].mean()

        #Put all sample means in a list
        sample_means.append(sample_mean)
        file_noext = (file.rsplit(".", 1))[0]
        sample_names.append(file_noext)

        #Create new column to indicate sample number
        samplenamelist = []
        for _ in range(len(df)):
            samplenamelist.append(str(file_noext))

        df.insert(0, "Sample", samplenamelist, True)
        os.chdir(cleandatalocation)
        #Export cleaned CSV files individually
        df.to_csv(str(file_noext)+'_Clean.csv')
        
    plotbar(sample_names, sample_means)


# Create the GUI.
peeltestgui = tk.Tk()

peeltestcanvas = tk.Canvas(peeltestgui, width = 400, height = 220)
peeltestcanvas.pack()

entry1 = tk.Entry(peeltestgui)
peeltestcanvas.create_window(200, 70, width=200, window=entry1)

label1 = tk.Label(text="Title of bar chart")
peeltestcanvas.create_window(200, 50, window=label1)

organizepeeltestbutton = tk.Button(text = "Organize Peel Test Data", command = organizepeeltest)
peeltestcanvas.create_window(200, 130, window = organizepeeltestbutton)

peeltestgui.mainloop()