#It consists of pure application logic, which interacts with the database. 
# It includes all the information to represent data to the end user.
# this is where we would handle any WAV file manipulation

#Create a WAV file class that can be used to manipulate the WAV file and read metadata  
# the controller module will be used to call these methods in model module 

class Model:
    def __init__(self,filepath):
        #first we need to verify the WAV file is a WAV file
        #we can do this by checking the file extension

        # give error if not a WAV file will need to be changed (11/30)
        try:
            if filepath[-4:] != ".wav":
                raise ValueError("File is not a WAV file")
        except ValueError:
            print("File is not a WAV file")

    # have methods on what we will do to the WAV file and call in the controller module

