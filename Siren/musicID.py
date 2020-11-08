#Arpan patel
import numpy as np
from numpy.linalg import norm
import soundfile as sf
from scipy.signal import spectrogram
import glob
import pyaudio
import wave
from pydub import AudioSegment
import time

def record():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels']))

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channelss = 2
    fs = 22050  # Record at 44100 samples per second
    seconds = 10
    filename = "output.wav"


    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    device_index = 0 #int(input("Enter index of the device: "))

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=2,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input_device_index = device_index,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channelss)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def convert_mono():
    sound = AudioSegment.from_wav("output.wav")
    sound = sound.set_channels(1)
    sound.export("output.wav", format="wav")

def classifyMusic() :
    convert_mono()
    allsig = []
    index=0
    norms = []
    names = []
    
    #reading all the files that meets the pattern "song-songname.wav"
    files = [f for f in glob.glob( "*.wav", recursive=True)]
    for f in files:
        x, fs = sf.read(f)
        #spectrogram values for each songs
        freq, t, Sxx = spectrogram(x, fs=fs, nperseg=fs//2)
        signature = []
       
        #max freqency presented in time segment
        wow = np.max(Sxx[:,0])
        for i in range(0,len(Sxx[0])): 
            wow = np.max(Sxx[:,i])
            for k in range(0,len(Sxx)):           
                if(Sxx[k][i] == wow):
                    #append all the max from all segments to create a song signature
                    #for each song
                    signature.append(freq[k])
        #now append each song signature to the list
        #basically like creating datbase of files signatures
        allsig.append(signature)   
        names.append(f)
        index+=1
        
    #spectrogram values of the test song 
    #name = input("Test file name")
    x_test, fs_test = sf.read("output.wav")
    f_test, t_test, Sxx_test = spectrogram(x_test, fs=fs_test, nperseg=fs_test//2)
    #print(x_test)
    
    signature_test = []
    wow_test = np.max(Sxx_test[:,0])
   
    for i in range(0,len(Sxx_test[0])): 
        wow_test = np.max(Sxx_test[:,i])
        for k in range(0,len(Sxx_test)):           
            if(Sxx_test[k][i] == wow_test):
                signature_test.append(f_test[k])
    
    
    # finding taxicab distance of each songs with test song
    for k in range(0,len(allsig)):
        
        a = np.asarray(allsig[k])
        b = np.asarray(signature_test)
        if(len(b) > len(a)):
            b = b[0:len(a)]
        elif(len(a) > len(b)):
            a = a[0:len(b)]
     
        temp = int(norm((a-b),ord=1))
        norms.append(temp)
    
    siren_or_alarm = []
    
    #finding and printing 5 lowest values in norms 
    #basically means shortest distance between song and test song
    for i in sorted(range(len(norms)), key=lambda k: norms[k])[:3]:
        #print(norms[i],"  ", files[i])
        siren_or_alarm.append(files[i])
    if("siren" in siren_or_alarm[1] and norms[i] < 10000):
        detected = "Siren"
    elif("alarm" in siren_or_alarm[1] and norms[i] < 10000):
        detected =  "Alarm"
    else:
        detected = "It's Nothing"
        
    return detected


###################  main  ###################
if __name__ == "__main__" :

        record()
        time.sleep(1)
        classifier = classifyMusic()
        print(" ")
        print(classifier)
  