import audiolazy as lz
import ffmpeg
import audioread
import threading
import os
import sys
import numpy as np
import time
import subprocess as sp
import pyaudio, pyo

class Audio_player():
    """
    Physically, as you probably know, audio is a vibration. Typically, we're
    talking about vibrations of air between approximitely 20Hz and 20,000Hz.
    That means the air is moving back and forth 20 to 20,000 times per second.

    If you measure that vibration and convert it to an electrical signal
    (say, using a microphone), you'll get an electrical signal with the voltage
    varying in the same waveform as the sound. In our pure-tone hypothetical,
    that waveform will match that of the sine function.

    Now, we have an analogue signal, the voltage. Still not digital. But, we
    know this voltage varies between (for example) -1V and +1V. We can, of course,
    attach a volt meter to the wires and read the voltage.

    Arbitrarily, we'll change the scale on our volt meter. We'll multiple the volts
    by 32767. It now calls -1V -32767 and +1V 32767. Oh, and it'll round to the nearest integer.
    Now, we hook our volt meter to a computer, and instruct the computer to read the meter 44,100
    times per second. Add a second volt meter (for the other stereo channel), and we now have the
    data that goes on an audio CD.
    
    This format is called stereo 44,100 Hz, 16-bit linear PCM. And it really is just a bunch of
    voltage measurements"""

    def __init__(self):
        """Constructor"""
        
    def audio_decoder(self, fname):
        """
        reads a file using ffmpeg and decodes and returns
        audio_array(numpy.array),channels(int),rate(int),duration(int)]
        
        para:: fname(str)
        """
        
        
        array, _ = (ffmpeg
                    .input(fname)
                    .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
                    .overwrite_output()
                    .run(capture_stdout=True)
                    )
        audio_array = np.frombuffer(array, dtype = "Int16")
        
        with audioread.audio_open(fname) as file:
            for i in file:
                chunk = int((len(i)))
                break
            channels, rate, duration = file.channels, file.samplerate, file.duration
            file.close()
            
        return  audio_array, chunk, channels, rate, duration
    
    def audio_player_init(self, audio_array, chunk, channels, rate, duration):
        """"""
        

        
        self.audio_array = audio_array
        def callback(*args):
            if bool(args[-1]):
                print("Playback Error")
            indata = self.audio_array
            outdata = indata
            print(len(outdata))
            return (outdata, pyaudio.paContinue)
                
        port_obj = pyaudio.PyAudio()
        stream = port_obj.open(format = pyaudio.paInt16,
                               channels = channels, 
                               rate = rate, 
                               output = True,
                               frames_per_buffer = chunk*10, 
                               stream_callback = callback)    
        
        stream.start_stream()
        while stream.is_active():
            time.sleep
    
        stream.close()
        port_obj.terminate()

audio_object = Audio_player()
fname = "C:\\Users\\OMMAR\\Desktop\\Apollo\\trial_trc\\14235-AAC-20K-FTD.mp3"
audio_array, chunk, channels, sample_rate, duration = audio_object.audio_decoder(fname)
audio_object.audio_player_init(audio_array[:16000*5], chunk, channels, sample_rate, duration)