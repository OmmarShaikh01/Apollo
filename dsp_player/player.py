import av
import utils
import time, sys
import threading
import pyo
import queue

def tryit(method):
    def try_ex(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            print(f"<{method.__name__}> {e}")        
    return try_ex
        
def input_switcher(dec1, dec2, fader, env = 5):
    def delete():
        del dec1
        
    osc2 = dec2.play()
    s.setCallback(lambda: (dec1.table_update(), dec2.table_update()))
    pyo.CallAfter(lambda: (s.setCallback(lambda: dec2.table_update()),delete()), time = (5 + 0.95))
    fader.setInput(osc2, env)


def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.time() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.time()
            return ret
        return rateLimitedFunction
    return decorate


class QueueReaderThread(threading.Thread):
    """A thread that consumes data from a filehandle and sends the data
    over a Queue.
    """
    
    @utils.timeit
    def __init__(self, path):
        super(QueueReaderThread, self).__init__()
        self.file_h = av.open(path)
        self.duration = self.file_h.duration
        self.daemon = True
        self.queue = queue.Queue(200)
        self.flag = "EXE"
        print(f"<{self.name}> Created")
    
    @RateLimited(2)   
    def fseek(self, time): # sync calls to stop crashes
        lock = threading.RLock()
        with lock:
            try:         
                self.file_h.seek(time*1000000)
                self.file_gen = self.file_h.decode(audio = 0)
                self.flag = "EXE"
                self.EOF = False
                data = next(self.file_gen)
                with self.queue.mutex:
                    self.queue.queue.clear()            
                self.queue.put(data.to_ndarray())
            except Exception as e:
                print(f"<{self.name}><fseek> {e}")

      
    def run(self):
        while self.flag != "END":
            self.EOF = False
            if self.flag == "EXE":
                if not(self.EOF):
                    try:
                        self.file_gen = self.file_h.decode(audio = 0)
                        for data in self.file_gen:
                            self.queue.put(data.to_ndarray())
                        print("Stream > EOF")
                    except av.EOFError:
                        self.EOF = True
                        self.queue.put("EOF")
                    except Exception as e:
                        print(f"<{self.name}><run> {e}")
                        continue
    
    def end(self):
        self.flag = "END"
        
class Decoder:
    """"""
    
    def __init__(self, server, sr = 44100):
        self.pos = 0
        self.sr = sr
        self.pdata = (self.sr * 100)
        self.server = server
        self.channels = 2
        
        
    @tryit    
    def fopen(self, path):
        self.reader = QueueReaderThread(path)
        self.duration = int(self.reader.duration / 1000000)
        self.dtable = pyo.DataTable(size = 4410000, chnls = self.channels)


    @tryit
    def data_to_list(self, data):
        if self.channels == 1:
            data = data[0].tolist()
            return (data,len(data))
        
        if self.channels == 2:
            data = [data[0].tolist(), data[1].tolist()]
            return (data,len(data[0]))
   
   
    @tryit   
    def table_update(self):
        try:
            if self.pdata <= 0:
                self.pos = 0
                self.pdata = (self.sr * 100)
                
            try:
                data = self.reader.queue.get()
                if hasattr(self,"osci"):
                    if (type(data) == type("EOF")):
                        self.osci.stop()
                        return None
                    if (type(data) != type("EOF")):
                        self.osci.out()
                        
            except queue.Empty:
                print(f"<{__name__}> {e}")
                self.server.setCallback(lambda:'')
                return None
            
            if type(data) != None:
                data,lent = self.data_to_list(data)
                table = pyo.DataTable(lent, self.channels, data)
                self.dtable.copyData(table, destpos = self.pos)
                self.pos += lent
                self.pdata -= lent
        except Exception as e:
            self.server.setCallback(lambda:'')
            print(f"<{__name__}> {e}")            
     
        
    @tryit
    def play(self):
        self.reader.start()
        self.table_update()
        self.server.setCallback(self.table_update)
        freq = self.dtable.getRate()
        self.osci = pyo.Osc(table=self.dtable, freq=freq).out()
        return self.osci
      

    

if __name__ == "__main__":
    import sys
    from slider_ui import Ui_MainWindow
    from PyQt5 import QtWidgets
    
    
    path2 = "C:\\Users\\OMMAR\\Music\\SONGS SORTED\\4000\\3750-4000\\14 Lost in Space (feat. A-Wa).mp3"
    path2 = "C:\\Users\\OMMAR\\Music\\SONGS SORTED\\3000\\2250-2500\\01 Younger (feat. Katie Mackie) - FrkMusic.Net.mp3" 
    pathC = "C:\\Users\\OMMAR\\Music\\SONGS SORTED\\4000\\3250-3500\\Troye Sivan - Dear Lord & Father of Mankind.mp3"
    path2 = "C:\\Users\\OMMAR\\Music\\SONGS SORTED\\1000\\750-1000\\Unknown ArtistHoangDon T Say Ft Nevve [zippyaudio11.com].mp3"
    path_2 = "C:\\Users\\OMMAR\\Desktop\\black_theme_apollo\\01 Hit The Pjanoo (Tom Forester Mashup).mp3"
    path_1 = "C:\\Users\\OMMAR\\Desktop\\black_theme_apollo\\250Hz_44100Hz_16bit_30sec.mp3"
    l_path = "C:\\Users\\OMMAR\\Music\\SONGS SORTED\\4000\\3500-3750\\41 Uncaged Vol. 5 Album Mix.mp3"
    

    
    s = pyo.Server(buffersize = 1024).boot()
    s.start()
    
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    dec = Decoder(s)
    dec.fopen(path_2)
    osc = dec.play()
    
    ui.horizontalSlider.setMinimum(0)
    ui.horizontalSlider.setMaximum(dec.duration)
    ui.horizontalSlider.valueChanged.connect(lambda: dec.reader.fseek(ui.horizontalSlider.value()))  
    
    MainWindow.show()
    sys.exit(app.exec_())


    

