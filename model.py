#It consists of pure application logic, which interacts with the database. 
# It includes all the information to represent data to the end user.
# this is where we would handle any WAV file manipulation

#Create a WAV file class that can be used to manipulate the WAV file and read metadata  
# the controller module will be used to call these methods in model module 

from scipy.signal import welch
import numpy as np
import matplotlib.pyplot as matplt
from matplotlib.figure import Figure
from pydub import AudioSegment
import os
import subprocess
import io
from scipy.fft import fft



class Model:
    def __init__(self):
        '''
        attributes of the WAV file we will be using
        '''
        self._sample_rate = 0
        self._data = 0
        self._num_channels = 0
        self._length = 0
        self._avgRT = 0
        self._spectrum = np.empty((0,0))
        self._freqs = np.array([])
        self._t = np.array([])
        self._graphs = {}
        self._resFreq = 0

    @property
    def graphs(self):
        return self._graphs
    @property
    def length(self):
        return self._length
    @property
    def num_channels(self):
        return self._num_channels
    @property
    def sample_rate(self):
        return self._sample_rate
    @property
    def data(self):
        return self._data
    @property
    def spectrum(self):
        return self._spectrum
    @property
    def freqs(self):
        return self._freqs
    @property
    def t(self):
        return self._t
    @property
    def avgRT(self):
        return self._avgRT
    @property
    def resFreq(self):
        return self._resFreq
    @sample_rate.setter
    def sample_rate(self,value):
        self._sample_rate = value
    @spectrum.setter
    def spectrum(self, value):
        self._spectrum = value
    @freqs.setter
    def freqs(self, value):
        self._freqs = value
    @t.setter
    def t(self, value):
        self._t = value
    @num_channels.setter
    def num_channels(self,value):
        self._num_channels = value
    @length.setter
    def length(self,value):
        self._length = value   
    @graphs.setter
    def graphs(self,name,graph):
        self._graphs[name] = graph 
    @avgRT.setter
    def avgRT(self,value):
        self._avgRT = round(abs(value),2)
    @resFreq.setter
    def resFreq(self,value):
        self._resFreq = round(value,2)
    @data.setter    
    def data(self,value):
        # we can get number of channels by looking at the data
        self._data = value
        self._num_channels = self.data.shape[len(self.data.shape)-1]
        self._length = self.data.shape[0]/self.sample_rate
    
    '''
    input: a filepath to a file
    output: update attributes with WAV file object
    '''
    def openWAVfile(self,filepath):
        #open the WAV file and convert to a WAV file
        # now we load the WAV file but first we gotta handle multiple channels
        try:
            new_path = self.convert_to_wav(filepath)
            audio = AudioSegment.from_wav(new_path)
            self.length = round(audio.duration_seconds,2)
            self.num_channels = audio.channels
            mono_audio = audio.set_channels(1)
            # Convert mono_audio to numpy array
            self._data = np.array(mono_audio.get_array_of_samples())
            self._sample_rate = mono_audio.frame_rate
            self.spectrum, self.freqs, self.t, im = matplt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=matplt.get_cmap("jet"))
            self.avgRT = (self.calculate_reverb(1000) + self.calculate_reverb(250) + self.calculate_reverb(6000))/3
            self.findRes()
        except FileNotFoundError:
            raise FileNotFoundError("File is not a WAV file")
        except ValueError:
            raise ValueError("File is NOT a Audio file")
        
    '''
    just strip the metadata from the file so we can read it correctly
    '''
    def strip_metadata(self,input_file, output_file):
        command = ['ffmpeg', '-i', input_file, '-map_metadata', '-1', '-c:v', 'copy', '-c:a', 'copy', output_file]
        subprocess.run(command, check=True)
        
    '''
    input: a filepath to a file
    output: a WAV file object which will not have metadata 
    '''
    def convert_to_wav(self,filepath):
        # List of known audio file extensions
        
        audioFormats = {
        'wav': None,
        'mp3': AudioSegment.from_mp3,
        'ogg': AudioSegment.from_ogg,
        'flv': AudioSegment.from_flv,
        'aac': lambda fp: AudioSegment.from_file(fp, format='aac'),
        'wma': lambda fp: AudioSegment.from_file(fp, format='wma'),
        'aiff': lambda fp: AudioSegment.from_file(fp, format='aiff'),
        'flac': lambda fp: AudioSegment.from_file(fp, format='flac'),
        'alac': lambda fp: AudioSegment.from_file(fp, format='alac'),
        'm4a': lambda fp: AudioSegment.from_file(fp, format='m4a'),
    }
        # Get the file extension
        file_extension = filepath.split('.')[-1].lower()

        # If the file is not an audio file, raise an exception
        if file_extension not in audioFormats:
            raise ValueError(f"File '{filepath}' is not a recognized audio file.")

        # If the file is not a WAV file, convert it to WAV format
        if file_extension != 'wav':
            # Get the appropriate AudioSegment method
            method = audioFormats[file_extension]
            # Open the file with the appropriate method
            audio = method(filepath)
            # Export the audio in WAV format to a BytesIO object
            wav_file = io.BytesIO()
            audio.export(wav_file, format='wav')
            wav_file.seek(0)  # Go back to the start of the file

            return wav_file

            # Return the path to the new file
            """else:
            return filepath"""
        # If the file is already a WAV file, strip metadata and return the path
        else:
            stripped_wav_filepath = os.path.splitext(filepath)[0] + '_stripped.wav'
            self.strip_metadata(filepath, stripped_wav_filepath)
            return stripped_wav_filepath
    '''
    input: a frequency in hz to be selected
    output: a target frequency around the 1000 hz range
    '''
    def target_freq(self,target):
        for x in self.freqs:
            if (x > target).any():
                break
        return x
    '''
    resonant frequency finder which does FFT to calculate the resonant frequency 
    '''
    def findRes(self):
        freq,power = welch(self.data,self.sample_rate,nperseg=4096)
        topFreq = freq[np.argmax(power)]
        self.resFreq = topFreq

    '''
    input:
    output: a dictionary of all the graphs we will need assigned to the object
    We just create the graphs here and assign them to the object in a dictionary
    '''
    def graph_figures(self):
        #create all figures we will need and assign to dictionary and return

        #create the figure for the spectogram
        Spectogram = Figure(figsize=(6,6),dpi=100)
        self.graphs['Spectogram'] = Spectogram
        #add the plot to the figure
        plot1 = Spectogram.add_subplot(111)
        #add the data to the plot
        _,_,_,im = plot1.specgram(self._data, Fs=self._sample_rate, NFFT=1024, cmap='jet')
        plot1.set_xlabel('Time(s)')
        plot1.set_ylabel('Frequency(Hz)')
        Spectogram.colorbar(im,ax=plot1).set_label('Intensity(dB)')
        #Spectogram.colorbar(im).set_label('Intensity(dB)')

        #Create Low freq figure
        rt60Low = round(abs(self.calculate_reverb(250)),2)
        lowFreq = Figure(figsize=(6,6),dpi=100)
        self.graphs['Low Frequency'] = lowFreq
        lowFreq.suptitle('Low Frequency Figure')
        lowFreq.text(0.95, 0.95, f'rt60: {rt60Low}seconds', horizontalalignment='right', verticalalignment='top', transform=lowFreq.transFigure)
        plot2 = lowFreq.add_subplot(111)
        plot2.plot(self.t,self.frequency_check(250), linewidth=0.5)
        plot2.set_xlabel('Time(s)')
        plot2.set_ylabel('Decibels(dB)')

        #create Mid freq figure
        rt60Mid = round(abs(self.calculate_reverb(1000)),2)
        midFreq = Figure(figsize=(6,6),dpi=100)
        self.graphs['Mid Frequency'] = midFreq
        midFreq.suptitle('High Frequency Figure')
        midFreq.text(0.95, 0.95, f'rt60: {rt60Mid} seconds', horizontalalignment='right', verticalalignment='top', transform=lowFreq.transFigure)
        plot3 = midFreq.add_subplot(111)
        plot3.plot(self.t,self.frequency_check(1000), linewidth=0.5)
        plot3.set_xlabel('Time(s)')
        plot3.set_ylabel('Decibels(dB)')

        # create High freq figure
        rt60High = round(abs(self.calculate_reverb(6000)),2)
        highFreq = Figure(figsize=(6,6),dpi=100)
        self.graphs['High Frequency'] = highFreq
        highFreq.suptitle('High Frequency Figure')
        highFreq.text(0.95, 0.95, f'rt60: {rt60High}seconds', horizontalalignment='right', verticalalignment='top', transform=lowFreq.transFigure)
        plot4 = highFreq.add_subplot(111)
        plot4.plot(self.t,self.frequency_check(4000), linewidth=0.5)
        plot4.set_xlabel('Time(s)')
        plot4.set_ylabel('Decibels(dB)')

        #extra plot 1, RAW amplitude from file
        amplitude = Figure(figsize=(6,6),dpi=100)
        self.graphs['Amplitude'] = amplitude
        amplitude.suptitle('RAW Amplitude Figure')
        plot5 = amplitude.add_subplot(111)
        time = np.arange(len(self.data))/self.sample_rate
        plot5.plot(time,abs(self.data), linewidth=0.5)
        plot5.set_xlabel('Time')
        plot5.set_ylabel('Amplitude')
        plot5.set_ylim(0, 10000)

        # Create a new figure for the combined frequency plot
        combinedFreq = Figure(figsize=(6,6),dpi=100)
        self.graphs['Combined Frequency'] = combinedFreq
        combinedFreq.suptitle('Combined Frequency Figure')
        plot6 = combinedFreq.add_subplot(111)
        # Plot the low, mid, and high frequency data on the same plot
        plot6.plot(self.t, self.frequency_check(250), label='Low Frequency', linewidth=0.5)
        plot6.plot(self.t, self.frequency_check(1000), label='Mid Frequency', linewidth=0.5)
        plot6.plot(self.t, self.frequency_check(4000), label='High Frequency', linewidth=0.5)
        plot6.set_xlabel('Time(s)')
        plot6.set_ylabel('Decibels(dB)')
        plot6.legend()

        # Create a new figure for the magnitude spectrum
        magnitudeSpectrum = Figure(figsize=(6,6),dpi=100)
        self.graphs['Magnitude Spectrum'] = magnitudeSpectrum
        magnitudeSpectrum.suptitle('Magnitude Spectrum Figure')
        plot7 = magnitudeSpectrum.add_subplot(111)
        # Compute and plot the magnitude spectrum
        Pxx, freqs, line = matplt.magnitude_spectrum(self._data, Fs=self._sample_rate, scale='dB', sides='default')
        plot7.plot(freqs, Pxx)
        plot7.set_xlabel('Frequency (Hz)')
        plot7.set_ylabel('Magnitude (dB)')

        #FFT graph
        fftGraph = Figure(figsize=(6,6),dpi=100)
        self.graphs['FFT'] = fftGraph
        fftGraph.suptitle('FFT Figure')
        plot8 = fftGraph.add_subplot(111)
        newData = np.abs(fft(self.data))
        plot8.plot(newData)
        plot8.set_xlabel('Frequency (Hz)')
        plot8.set_ylabel('Magnitude (dB)')

        #Freq vs Power
        freqPower = Figure(figsize=(6,6),dpi=100)
        self.graphs['Freq vs Power'] = freqPower
        freqPower.suptitle('Freq vs Power Figure')
        #here we will be using code given from the annoucement to add an extra graph
        freq,power = welch(self.data,self.sample_rate,nperseg=4096)
        n = len(self.data)
        k = np.arange(n)
        T = n/self.sample_rate
        freq = k/T
        freq = freq[:len(freq)//2]
        Y = np.fft.fft(self.data)/n
        Y = Y[:n//2]
        plot9 = freqPower.add_subplot(111)
        plot9.plot(freq,abs(Y))
        plot9.set_xscale('symlog')
        plot9.set_ylabel('Frequency (Hz)')
        plot9.set_xlabel('Power')


        
    
    '''
    input: a chosen frequency we are checking and turnign into decibles
    output:return the data of the frequency in decible which we 
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
        #add a very small constant to avoid 0
        decible_data = 10 * np.log10(freq_data + 1e-10)
        return decible_data
    '''
    input: a chosen frequency we are checking the reverb time for
    output: the reverb time for the frequency
    '''
    def calculate_reverb(self, chosen_freq):
        decible_data = self.frequency_check(chosen_freq)
        max_index = np.argmax(decible_data)
        value_max = decible_data[max_index]
        #debugger(f'max value {value_max}')
        #debugger(f'max index {max_index}')
        
        #this will get the rest of the array from Max to the end
        spliced_array = decible_data[max_index:]
        #now we can calculate tr20 and explogate it to rt60
        try:
            value_5db = self.nearestValue(spliced_array,value_max-5)
            index_5db = np.where(spliced_array == value_5db)[0][0]
            value_25db = self.nearestValue(spliced_array,value_max-25)
            index_25db = np.where(spliced_array == value_25db)[0][0]
            #now we have our rt20 which we can use to find rt60
            rt20 = self.t[index_5db] - self.t[index_25db]
            rt60 = rt20 * 3
        except IndexError:
            rt60 = 0
            raise IndexError("Frequency is not in the WAV file")
        finally:
            return rt60
    
    '''
    input: an array and a value
    output: the nearest value in the array to the passed value
    '''    
    def nearestValue(self,array,value):
        nparray = np.asarray(array)
        idx = (np.abs(nparray-value)).argmin()
        return nparray[idx]
        
        

    # have methods on what we will do to the WAV file and call in the controller module
def debugger(message):
    print(message)