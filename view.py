#View represents the HTML files, which interact with the end user. 
#It represents the model’s data to user
import tkinter as tk
import matplotlib.pyplot as matplt

def StartWindow():
    mainWindow = tk.Tk()
    mainWindow.title("WAV file reader")
    
    #we need to use a figrure to display the graph inside Tkinter 
    graph = matplt.figure(figsize = (5,5), dpi = 100)
    plot = graph.add_subplot(1,1,1)
    plot.plot([1,2,3,4,5,6,7,8,9,10], [2,4,6,8,10,12,14,16,18,20])
    
    mainWindow.mainloop()
    
StartWindow()