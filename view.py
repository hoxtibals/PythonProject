
#It represents the model’s data to user
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as matplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        '''
        TAKEN FROM CLASS 11-29 PARTTICIPATION
        we can use the this class to call the methods in the final module
        '''
        self.figures = {}
        # create widgets
        self.message_label = tk.Label(self, text='', foreground='black')
        self.message_label.pack()
        
        # save button
        self.WAVbutton = tk.Button(self, text='Open WAV file', command=self.loadWAVfileButton)
        self.WAVbutton.pack()
        
        #statistics window
        self.stats_label = tk.Label(self, text='Summary Stats: ', foreground='black')
        self.stats_button = tk.Button(self, text='Show Stats', command=self.showStatsButton)
        self.stats_label.pack()
        
        self.loadGraphButton = tk.Button(self, text='Show Graph', command=self.showGraphButton)
        
        

        # set the controller
        self.controller = None

    def add_figure(self, name, figure):
        """
        Add a figure to the dictionary of figures
        :param name: name of the figure
        :param figure: the figure
        :return:
        """
        self.figures[name] = figure

    def set_controller(self, controller):
        """
        Set the controller
        :param controller: the controller for the view to reference
        :return:
        """
        self.controller = controller
    
    '''
    handles the button clicked event for the loadWav file
    '''
    def loadWAVfileButton(self):
        '''
        handle button click
        :return:
        '''
        if self.controller:
            path_file = filedialog.askopenfilename()
            self.controller.loadWAVfile(path_file)
            self.WAVbutton = tk.Button(self, text='Load Spectogram', command= self.showGraphButton)
            self.WAVbutton.pack()
        
        
            
        
    def set_freq_button(self, freq):
        '''
        Set the frequency
        :param freq:
        :return:
        '''
        #This will be called when button is pushed, will call controller to use command
        self.controller.setFrequency(freq)
    def create_stats(self):
        #we use controller methods to get the statistics from the model
        self.statisticsFrame = tk.Frame(self)
        self.statisticsFrame.pack()

        stats = self.controller.passStats()
        self.sampleRateLabel = tk.Label(self.statisticsFrame, text=f'Sample Rate: {stats["sample_rate"]}')
        self.sampleRateLabel.pack()
        self.numChannelsLabel = tk.Label(self.statisticsFrame, text=f'Number of Channels (before change): {stats["num_channels"]}')
        self.numChannelsLabel.pack()
        self.lengthLabel = tk.Label(self.statisticsFrame, text=f'Length: {stats["length"]}')
        self.lengthLabel.pack()
            
    def showGraphButton(self):
        graphFrame = tk.Frame(self)
        graphFrame.pack()
        
        self.graphDefault = tk.StringVar()
        self.graphDefault.set('Spectogram')
        self.controller.graphButtonClicked(graphFrame)
        menuOptions = self.figures.keys() if self.figures else ["No figures"]
        self.optionDropdown = tk.OptionMenu(graphFrame, self.graphDefault,*menuOptions, 
            command = lambda selected: self.displayGraph(self.figures[selected], graphFrame) if self.figures else None)
        self.optionDropdown.pack()

        
        
        
    def showStatsButton(self):
        self.controller.StatsButtonClicked()
    
    def hide_message(self):
        self.message_label['text'] = ''
        
    def displayGraph(self, figure,frame):
        """
        Display the graph
        :param figure: the figure that will be displayed (this will be called in the controller)
        :param frame: the frame we wish to assign the graph to
        :return:
        """
        # how we get rid of the old graph when a new one is selected
        if hasattr(self, 'graph'):
            self.graph.get_tk_widget().pack_forget()
        self.graph = FigureCanvasTkAgg(figure, master=frame)
        self.graph.get_tk_widget().pack()
        self.graph.draw()
        pass
    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        #self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Show a message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        #self.message_label.after(3000, self.hide_message)
    
