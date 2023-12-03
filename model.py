#It consists of pure application logic, which interacts with the database. 
# It includes all the information to represent data to the end user.
# this is where we would handle any WAV file manipulation

#Create a WAV file class that can be used to manipulate the WAV file and read metadata  
# the controller module will be used to call these methods in model module 

import scipy

class Model:
    def __init__(self):
        #first we need to verify the WAV file is a WAV file
        #we can do this by checking the file extension
        self.sample_rate = 0
        self.data = 0
        self.num_channels = 0
        self.length = 0

    @property
    def sample_rate(self):
        return self.sample_rate
    @property
    def data(self):
        return self.data
    @sample_rate.setter
    def sample_rate(self,value):
        self.sample_rate = value
    @data.setter    
    def data(self,value):
        # we can get number of channels by looking at the data
        self.data = value
        self.num_channels = self.data.shape[len(self.data.shape)-1]
        self.length = self.data.shape[0]/self.sample_rate

    def openWAVfile(self,filepath):
        #open the WAV file and read the metadata
        #return the metadata
        try:
            if filepath[-4:] != ".wav":
                raise ValueError("File is not a WAV file")
            else:
                print("File is a WAV file, name is: " + filepath)
            # now we load the WAV file
            self.sample_rate, self.data = scipy.io.wavfile.read(filepath)
        except ValueError:
            print("File is not a WAV file")

    def packageWAVfile(self):
        #package the WAV file into a WAV file object to be displayed
        pass
        

    # have methods on what we will do to the WAV file and call in the controller module

