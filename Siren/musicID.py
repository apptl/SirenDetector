
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
import soundfile as sf
from scipy.signal import spectrogram
import glob


def classifyMusic() :
    
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
    name = input("Test file name")
    x_test, fs_test = sf.read(name)
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
    
    #finding and printing 5 lowest values in norms 
    #basically means shortest distance between song and test song
    for i in sorted(range(len(norms)), key=lambda k: norms[k])[:5]:
        print(norms[i],"  ", files[i])
    
    #spectrogram of test file
    plt.figure(0)
    plt.specgram(x_test, Fs=fs_test)
    plt.title("test file")
    
    
    index=1
    #spectrogram of 2 closest matches
    for i in sorted(range(len(norms)), key=lambda k: norms[k])[:2]:
        x,fs = sf.read(files[i])
        plt.figure(index)
        plt.specgram(x, Fs=fs)
        plt.title(files[i])
        index+=1
    plt.show()


###################  main  ###################
if __name__ == "__main__" :
     classifyMusic()


"""
code to make the audio mono 
from pydub import AudioSegment
sound = AudioSegment.from_wav("alarm-smoke1.wav")
sound = sound.set_channels(1)
sound.export("alarm-smoke1.wav", format="wav")
"""