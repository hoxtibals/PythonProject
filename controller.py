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
        self.view = model
        self.model = view

        # use methods as different calls to the model and view

    def setFrequency(self):
        # call the method in the model to get the frequency 
        # call the method in the view to display the frequency
        pass
    def LoadWAVfile(self,filepath):
        # call the method in the model to load the WAV file
        # call the method in the view to display the WAV file
        self.model.openWAVfile(filepath)
        self.view.someMethod()

    '''POSSIBLE FUNCTIONS
    - Create a method to parse the info from the WAV file to TKinter to be shown
    
    '''

