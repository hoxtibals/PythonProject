#It acts as an intermediary between view and model.
#It listens to the events triggered by view and queries model for the same.
#This is the file we will run to start the application 
# This will be where we will input the WAV file 
# View -> Controller -> Model

#Where we will call the show error view method
from view import View
from model import Model

class Controller:
    def __init__(self,model,view):
        self.view = view
        self.model = model

        # use methods as different calls to the model and view
# may need to include more stats or calculate them on the fly 
    def passStats(self):
        return {
            'sample_rate': self.model.sample_rate,
            'data': self.model.data,
            'num_channels': self.model.num_channels,
            'length': self.model.length,
            'spectrum': self.model.spectrum,
            'freqs': self.model.freqs,
            't': self.model.t,
        }

    def setFrequency(self,freq):
        # call the method in the model to get the frequency 
        # call the method in the view to display the frequency
        self.model.target_freq(freq)
    def LoadWAVfile(self,filepath):
        # call the method in the model to load the WAV file
        # call the method in the view to display the WAV file
        try:
            self.model.openWAVfile(filepath)
            self.view.show_success("WAV file loaded successfully")
            #now we need to parse the info from opening the WAV file to the view
            #we can access our basic statistics from the model with the 
            #attributes for the model class
            self.view.showStats(self.model.sample_rate, self.model.num_channels, self.model.length)
        except ValueError as error:
            self.view.show_error(error)
        #after this function the basic summar statistics are created, now we just hand them off to the view
        self.view.someMethod()

    '''POSSIBLE FUNCTIONS
    - Create a method to parse the info from the WAV file to TKinter to be shown

    '''

