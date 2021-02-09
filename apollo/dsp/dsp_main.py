import pyo
from PyQt5 import QtWidgets, QtCore, QtGui

import sys, os, time, math

from apollo.dsp.plugins.SignalProcessors import MasterProcessor
from apollo.dsp.plugins.apollo_mixer import ApolloAudioMixer

class ComputeGraph:
    """"""
    def __init__(self):
        """Constructor"""
        self.Graph = []

    def __repr__(self):
        return str(self.Graph)

    def __str__(self):
        return str(self.Graph)

    def GetGraph(self):
        return self.Graph

    def ReplaceNode(self, obj, Index):
        print(obj, Index)

    def InsertNode(self, obj, Index):
        self.Graph.insert(Index, obj)

class ApolloDSP:
    """
    Apollos DSP graph to create Audio Processing Graph used to precess Audio
    """

    def __init__(self, **kwargs):
        """
        Inits:
        ComputerGraph: defines the Processing Graph for all the filters
        UI: Passed the Parent app Containing UI objects and related functions
        """
        self.ComputeGraph = ComputeGraph()
        self.UI = kwargs.get("UI")
        if not kwargs.get("UI"):
            from apollo.app.apollo_TabBindings import ApolloTabBindings
            self.UI = ApolloTabBindings()

        self.Mixer = ApolloAudioMixer(self.UI.apollo_WDG_ATOL_mixer)
        self.Mixer.create_EmptyMixerChannels(35)
        self.StartServer()

        self.MasterProcessorBindings(pyo.Noise())
        self.ButtonBindings()

    def MasterProcessorBindings(self, Input):
        """
        Inits the Master Filter for Processing the inputs
        """
        self.MasterProcessor = MasterProcessor(Input)
        self.MasterProcessor.processor().out()
        self.Mixer.bind_ProcessortoMixer(self.MasterProcessor, 0)

    def ButtonBindings(self):
        self.UI.apollo_DIAL_ATOL_masterVU_chnl.valueChanged.connect(lambda x: self.Server.setAmp(x /1000))

    def StartServer(self, **kwargs):
        """
        Starts the audio callback server that is used to process all Streams

        :Args:
            sr: Int
                sampling rate of the audio server
            nchnls: Int
                Number of audio channels to send Audio to
            buffersize: Int
                Buffer Size for CPU to process
            duplex: Int
                setDuplex Mode (1 output) (2 Output/Input)
            amp: Int
                 set server amplitude
        """
        self.Server = pyo.Server(kwargs.get("sr", 44100),
                                 kwargs.get("nchnls", 2),
                                 kwargs.get("buffersize", 256),
                                 kwargs.get("duplex", 1)).boot()
        if not self.Server.start():
            raise ConnectionError("Audio Server Failed To start")

        self.Server.setAmp(kwargs.get("amp", 0.000))
        self.Mixer.connect_ServerChannel(self.Server, self.UI.apollo_PIXLB_ATOL_masterVU_VU)
        self.UI.apollo_DIAL_ATOL_masterVU_chnl.setValue(kwargs.get("amp", 0.001))


    def StopServer(self):
        """
        Stops the audio callback server that is used to process all Streams.
        Deletes all the bojects and shuts down Server.
        """
        self.Server.stop()
        self.Server.shutdown()

if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
