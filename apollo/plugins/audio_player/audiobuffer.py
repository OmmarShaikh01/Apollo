import os
from threading import Thread, Event
import time

from pyo import DataTable, TableRead, TrigFunc
import av

from apollo import exe_time


class BufferInfo():
    """
    Stores the Audio Buffer info
    """
    def __init__(self, frames: int):
        """
        Class Constructor

        Parameters
        ----------
        frames : int
            audio frames info that the buffer holds
        """
        super().__init__()
        self.FrameInfo = dict.fromkeys(range(frames), False)

    def isWritten(self, Frame: "av.audio.frame.AudioFrame"): #type: ignore
        """
        Checks if the frames is written in the buffer and return boolean

        Parameters
        ----------
        Frame : av.audio.frame.AudioFrame
            frame to check for

        Returns
        -------
        boolean
            if the frame is written to buffer
        """
        return self.FrameInfo.get(Frame.index, False)

    @property
    def end_frame(self):
        """
        last frame of the buffer

        Returns
        -------
        int
            last frame of the buffer
        """
        return self.__frames

    @end_frame.setter
    def end_frame(self, value: int):
        """
        sets the end frame of the buffer, ajusts the buffer length according to the end frame

        Parameters
        ----------
        value : int
            total number of frames
        """
        value += 1
        self.__frames = value
        if (len(self.FrameInfo.keys()) - 1) > value:
            for key in range(value, len(self.FrameInfo.keys())):
                self.FrameInfo.__delitem__(key)
        else:
            for key in range(len(self.FrameInfo.keys()), value):
                self.FrameInfo.__setitem__(key, False)



class AudioDecoder(Thread):
    """
    Decodes Samples and add it to the Audio Table
    """
    def __init__(self, InputStream: 'av.container.InputContainer'): # type:ignore
        """
        Class Constructor

        Parameters
        ----------
        InputStream : av.container.InputContainer
            Input stream To get Frames from
        """
        super().__init__()
        self.setup_events()
        self.InputStream = InputStream
        self.start()

    def run(self):
        """
        Main Run method of the thread
        """
        t1 = time.time()
        while self.DecoderStop.is_set():

            # decoder Event loop
            if self.DecoderStream.is_set():
                frame = self.__decode()
                if not (frame == 'EOF'):
                    self.Table.append_frame(frame)

            # default empty state of the thread
            else:
                time.sleep(0.1)

    def setup_events(self):
        """
        Inits all the events
        """
        # create and starts the procesing loop for events to execute
        self.DecoderStop = Event()
        self.DecoderStop.set()

        self.DecoderStream = Event()

    def setTable(self, Table):
        """
        sets the audio table to fill samples

        Parameters
        ----------
        Table : AudioTable
            audio table to fill samples
        """
        self.Table = Table

    def setBuffer(self, BufferInfo):
        """
        Sets the buffer info

        Parameters
        ----------
        BufferInfo : BufferInfo
            buffer info of the table
        """
        self.Buffer = BufferInfo

    def __decode(self):
        """
        Audio Decoder that generated frames to be written

        Returns
        -------
        av.frame.Frame
            frame of audio samples decoded or EOF string at end of file
        """
        # actual decoding and demuxing of file
        for packet in self.InputStream.demux(audio = 0):
            if not(packet.size <= 0):
                for frame in packet.decode():
                    return frame
            else:
                self.halt_decoder()
                return "EOF"

    def decode(self):
        """
        triggers the decode event for the thread
        """
        self.DecoderStop.set()
        self.DecoderStream.set()
        return self

    def halt_decoder(self):
        """
        halts the decode event for the thread
        """
        self.DecoderStream.clear()

    def stop(self):
        """
        stops the threads mainloop
        """
        self.DecoderStop.clear()



class AudioTable(DataTable):
    """
    Holds the acctual smaples
    """
    def __init__(self, path: str, duration: int = None, samplerate: int = 44100, channels: int = 2):
        """
        creates a datatable of decoded samples for a give file path

        Parameters
        ----------
        path : str
            path to a file to decode
        duration : int
            duration of the table, by default None
        samplerate : int, optional
            samplerate of the audio table, by default 44100
        channels : int, optional
            channels of audio, by default 2
        """
        # setting up decoder and input stream
        if path != None and os.path.isfile(path):
            self.file = path
            self.InputStream = av.open(path)
            self.BufferInfo = BufferInfo(300)

            # sets up the decoder
            self.Decoder = AudioDecoder(self.InputStream)
            self.Decoder.setTable(self)
            self.Decoder.setBuffer(self.BufferInfo)
            self.Decoder.decode()
        else:
            raise FileNotFoundError

        # setting up duration for audio table
        if (duration is None) and (path is not None):
            self.duration = int(round(self.InputStream.duration / 1000000))
        elif (duration is not None) and (path is not None):
            self.duration = duration
        else:
            self.duration = 30

        # meta setup for the table class
        self.sample_rate = samplerate
        self.channels = channels
        self.cursor = 0
        self.table_size = int(self.duration * self.sample_rate)

        #calling parent class init
        super().__init__(size = self.table_size, chnls = self.channels)

    def write(self, array, pos):
        """
        Adds given samples to the audio table.

        Parameters
        ----------
        array : np.array
            array that contains audio samples
        pos : int
            pos to add samples to
        """
        def FillSamples(obj, samples, cursor):
            for sample in samples:
                obj.put(sample, cursor)
                # writes so fast that no time to read quick
                if cursor >= self.table_size:
                    cursor = 0
                else:
                    cursor += 1
            return cursor

        array_channels = array.shape[0]

        # noramal one to one cration of channels
        if array_channels == self._chnls:
            for index, obj in enumerate(self._base_objs):
                self.cursor = FillSamples(obj, array[index], pos)

        # for mono audio copies on both channels same audio and converts to dual
        elif (array_channels == 1) and (self._chnls == 2):
            for obj in self._base_objs:
                self.cursor = FillSamples(obj, array[0], pos)

        # 2.1 channel audio support
        # 5.1 channel audio support
        # 7.1 channel audio support

        else:
            raise Exception("Audio Channels Not Compatable")

        self.refreshView()

    def append_frame(self, frame):
        """
        appends an audioframe and extends the audio table with given frame

        Parameters
        ----------
        frame : av.audio.frame.AudioFrame
            A frame of audio
        """
        if not self.BufferInfo.isWritten(frame):
            self.write(frame.to_ndarray(), self.cursor)

    def extend(self, array):
        """
        extends the audio table with given samples.

        Parameters
        ----------
        array : np.array
            array that contains audio samples
        """
        self.write(array, self.cursor)

    def close(self):
        """
        closes all files and threads launched by AudioTable
        """
        self.InputStream.close()
        self.Decoder.stop()

    def decode(self):
        self.Decoder.decode()



class AudioReader(TableRead):
    """
    Reads the Audio buffer
    """
    def __init__(self, table, freq = 1, loop = 0, interp = 2, mul = 1, add = 0):
        """
        Class Constructor

        Parameters
        ----------
        table: PyoTableObject
            Table containing the waveform samples.
        freq: float or PyoObject, optional
            Frequency in cycles per second. Defaults to 1.
        loop: int {0, 1}, optional
            Looping mode, 0 means off, 1 means on. Defaults to 0.
        interp: int, optional
            Choice of the interpolation method. Defaults to 2.
        """
        super().__init__(table, freq = freq, loop = loop, interp = interp, mul = mul, add = add)
        TrigFunc(self["trig"], lambda: print("LOOP\n\n\n\n\n\n\n"))

if __name__ == "__main__":
    from pyo import Server, TableRead

    def close():
        server.closeGui()
        inst.close()

    server = Server().boot()
    inst = AudioTable(r"D:\music\mosesdt.mp3", 0)
    inst.decode()
    inst.view()
    reader = AudioReader(inst, inst.getRate(), loop = 1).out()
    server.gui(locals())
