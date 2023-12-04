#It consists of pure application logic, which interacts with the database. 
# It includes all the information to represent data to the end user.
# this is where we would handle any WAV file manipulation

#Create a WAV file class that can be used to manipulate the WAV file and read metadata  
# the controller module will be used to call these methods in model module 

import scipy
import numpy as np
import matplotlib.pyplot as matplt


class Model:
    def __init__(self):
        '''
        attributes of the WAV file we will be using to manipulate the WAV file
        '''
        self.sample_rate = 0
        self.data = 0
        self.num_channels = 0
        self.length = 0
        self.spectrum = np.empty((0,0))
        self.freqs = np.array([])
        self.t = np.array([])

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

    @property
    def spectrum(self):
        return self._spectrum
    @spectrum.setter
    def spectrum(self, value):
        self._spectrum = value
    @property
    def freqs(self):
        return self._freqs
    @freqs.setter
    def freqs(self, value):
        self._freqs = value
    @property
    def t(self):
        return self._t
    @t.setter
    def t(self, value):
        self._t = value
    @property
    def im(self):
        return self._im
    @im.setter
    def im(self, value):
        self._im = value

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
            self.spectrum, self.freqs, self.t, im = matplt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=matplt.get_cmap("jet"))
        except ValueError:
            print("File is not a WAV file")

        '''
        returns a mid range frequency
        '''

    def target_freq(self):
        for x in self.freqs:
            if x > 1000:
                break
        return x
    
    '''
    return the data of the frequency in decible which we 
    can pass directly to the plot directory
    '''
    def frequency_check(self):
       #debugger(f'frequencies {self.freqs[:10]}')
        target_freq = self.target_freq()
        #debugger(f'target frequency {target_freq}')
        index_freq = np.where(self.freqs == target_freq)[0][0]
        #debugger(f'index of target frequency {index_freq}')

        freq_data = self.spectrum[index_freq]
        #debugger(f'spectrum data {freq_data}')

        decible_data = 10 * np.log10(freq_data)
        return decible_data

    def packageWAVfile(self):
        #package the WAV file into a WAV file object to be displayed
        pass
        

    # have methods on what we will do to the WAV file and call in the controller module
def debugger(message):
    print(message)
