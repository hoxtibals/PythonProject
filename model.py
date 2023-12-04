#It consists of pure application logic, which interacts with the database. 
# It includes all the information to represent data to the end user.
# this is where we would handle any WAV file manipulation

#Create a WAV file class that can be used to manipulate the WAV file and read metadata  
# the controller module will be used to call these methods in model module 

import scipy
import numpy as np
import matplotlib.pyplot as matplt
import pydub


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
    #This is without the use of Pydub, if this isnt working we can change it
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
    
    '''
    input: a frequency in hz to be selected
    output: a target frequency around the 1000 hz range
    '''
    def target_freq(self,target):
        for x in self.freqs:
            if x > target:
                break
        return x
    
    '''
    return the data of the frequency in decible which we 
    can pass directly to the plot directory
    '''
    def frequency_check(self,chosen_freq):
       #debugger(f'frequencies {self.freqs[:10]}')
       #1000 hz is the target frequency for mid range
        target_freq = self.target_freq(chosen_freq)
        #debugger(f'target frequency {target_freq}')
        index_freq = np.where(self.freqs == target_freq)[0][0]
        #debugger(f'index of target frequency {index_freq}')

        freq_data = self.spectrum[index_freq]
        #debugger(f'spectrum data {freq_data}')

        decible_data = 10 * np.log10(freq_data)
        return decible_data
    
    def calculat_reverb(self, chosen_freq):
        decible_data = self.frequency_check(chosen_freq)
        max_index = np.argmax(decible_data)
        value_max = decible_data[max_index]
        #debugger(f'max value {value_max}')
        #debugger(f'max index {max_index}')
        
        #this will get the rest of the array from Max to the end
        spliced_array = decible_data[max_index:]
        #now we can calculate tr20 and explogate it to rt60
        value_5db = self.nearestValue(spliced_array,value_max-5)
        index_5db = np.where(spliced_array == value_5db)
        value_25db = self.nearestValue(spliced_array,value_max-25)
        index_25db = np.where(spliced_array == value_25db)
        #now we have our rt20 which we can use to find rt60
        rt20 = self.t[index_5db] - self.t[index_25db]
        rt60 = rt20 * 3
        return rt60
        
    def nearestValue(array,value):
        nparray = np.asarray(array)
        idx = (np.abs(nparray-value)).argmin()
        return nparray[idx]
        

    def packageWAVfile(self):
        #package the WAV file into a WAV file object to be displayed
        pass
        

    # have methods on what we will do to the WAV file and call in the controller module
def debugger(message):
    print(message)
