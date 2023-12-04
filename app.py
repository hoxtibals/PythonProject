#main file where we will create the App class

import tkinter as tk
from model import Model
from view import View
from controller import Controller
# test code

# testing model openwavfile method
    # model = Model()
    # model.openWAVfile("test.wav")
    
    
def start_program():
    mainW = tk.Tk()
    mainW.title("WAV File Analyzer")
    mainW.mainloop()
    WAVframe = tk.frame()
    Wav_view = View(WAVframe)
    Wav_model = Model()
    #create the controller and assign it to view and model
    Wav_controller = Controller(Wav_model,Wav_view)
    Wav_view.set_controller(Wav_controller)

if __name__ == '__main__':
    start_program()
    
    

    