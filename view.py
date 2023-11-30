#View represents the HTML files, which interact with the end user. 
#It represents the model’s data to user
import tkinter as tk
import matplotlib.pyplot as matplt

class View(tk.Frame):
    def __init__(self, parent):
        '''
        TAKEN FROM CLASS 11-29 PARTTICIPATION
        we can use the this class to call the methods in the final module
        '''
        # create widgets
        # label
        self.label = ttk.Label(self, text='Email:')
        self.label.grid(row=1, column=0)

        # save button
        self.save_button = ttk.Button(self, text='Save', command=self.save_button_clicked)
        self.save_button.grid(row=1, column=3, padx=10)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=2, column=1, sticky=tk.W)

        # set the controller
        self.controller = None
    def pickFile(path_file):
        path_file.set(tk.filedialog.askopenfilename())
        return path_file
    
    def StartWindow():
        mainWindow = tk.Tk()
        mainWindow.title("WAV file reader")
        
        #we need to use a figrure to display the graph inside Tkinter 
        graph = matplt.figure(figsize = (5,5), dpi = 100)
        plot = graph.add_subplot(1,1,1)
        
        #button to load WAV file we will need to import the command from another module
        #we will use a string to keep track of file path, we will need to use
        #LAMDA function to ensure the command is not called when the window is created
        path_file = tk.StringVar()
        load = tk.Button(mainWindow, text = "Load WAV file", command = lambda:pickFile(path_file))
        load.pack()
        #example input used to test plot
        plot.plot([1,2,3,4,5,6,7,8,9,10], [2,4,6,8,10,12,14,16,18,20])
        
        mainWindow.mainloop()
