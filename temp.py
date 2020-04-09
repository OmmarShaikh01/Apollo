import pyo
import ffmpeg, audioread
import numpy as np

import sys, re, json
import subprocess as sp
 
def audio_setup():
    audio_setup = {}
    
    audio_setup["PA-ver"] =pyo.pa_get_version()
    audio_setup["PA-ver_info"] =pyo.pa_get_version_text()

    list_host_apis = {}
    for line in (((sp.getoutput([sys.executable, "-c", "import pyo ;pyo.pa_list_host_apis()"]).split('Host APIS:'))[1]).split('\n')):
        temp = []
        line = (line.split(':'))
        if line != ['']:
            for item in line[1:]:
                temp.append(item.split(',')[0])    
            list_host_apis[temp[0]] = {'id': temp[1], 'name': temp[2], 'num_devices': temp[3], 'default_in': temp[4], 'default_out': temp[5]}
            
    audio_setup["host_api"] = list_host_apis
    audio_setup["def_host_api"] =pyo.pa_get_default_host_api()
    in_dev, out_dev =  pyo.pa_get_devices_infos()[0], pyo.pa_get_devices_infos()[1]
    audio_setup["indev"] = in_dev
    audio_setup['outdev'] = out_dev
    audio_setup['def_in'] =out_dev[pyo.pa_get_default_output()]
    audio_setup['def-out'] =in_dev[pyo.pa_get_default_input()]
    return audio_setup

def audio_data_reader(fname):
    file_info = pyo.sndinfo(fname, print=False)
    file_info1 = {
    'number of frames': file_info[0], 
    'duration': file_info[1], 
    'sr': file_info[2], 
    'channels': file_info[3], 
    'format': file_info[4], 
    'sample_type': file_info[5]}
    return (file_info1)

def audio_decoder(fname):
    """
    reads a file using ffmpeg and decodes and returns
    audio_array(numpy.array),channels(int),rate(int),duration(int)]
    
    para:: fname(str)
    """
    
    
    array, _ = (ffmpeg
                .input(fname)
                .output('-', format = 's16le', acodec = "pcm_s16le", ac = 2, ar = 44000)
                .overwrite_output()
                .run(capture_stdout=True)
                )
    audio_array = np.frombuffer(array, dtype="int16")
    print(audio_array.max(), audio_array.min())
    return  audio_array[:1000000]

def spectro (x): 
    import matplotlib.pyplot as plt
    t = 240
    NFFT = 1024
    Fs = 16000
    ax2 = plt.subplot()
    Pxx, freqs, bins, im = ax2.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900)
    plt.show()
