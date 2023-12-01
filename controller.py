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

        



