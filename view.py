
#It represents the model’s data to user
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as matplt


class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        '''
        TAKEN FROM CLASS 11-29 PARTTICIPATION
        we can use the this class to call the methods in the final module
        '''
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
        
        

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
    
    ''' 
    Input: an emptry string which we set to the path of the file we select in the dialog
    Output: the chosen path directory in string format
    '''
    def pickFile(self, path_file):
        path_file.set(tk.filedialog.askopenfilename())
        return path_file
    
    def loadWAVfileButton(self):
        '''
        handle button click
        :return:
        '''
        if self.controller:
            path_file = filedialog.askopenfilename()
            self.controller.loadWAVfile(path_file)
        
            
            
    def StartWindow():
        mainWindow = tk.Tk()
        mainWindow.title("WAV file reader")
        
        
        mainWindow.mainloop()
    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Show a message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)
        
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
        self.numChannelsLabel = tk.Label(self.statisticsFrame, text=f'Number of Channels: {stats["num_channels"]}')
        self.numChannelsLabel.pack()
        self.lengthLabel = tk.Label(self.statisticsFrame, text=f'Length: {stats["length"]}')
        self.lengthLabel.pack()
            
    def showStatsButton(self):
        self.controller.StatsButtonClicked()
    def loadGraph(self):
        #loads the graph into the frame 
        pass
    
    def hide_message(self):
        self.message_label['text'] = ''
    



def pickFile(path_file):
    path_file.set(tk.filedialog.askopenfilename())
    return path_file