import pyo
from PyQt5 import QtWidgets, QtCore, QtGui

import sys, os, time, math


class BaseProcessor:
    """
    Base class for audio processing plugins
    """
    def __init__(self):
        """Constructor"""
        self.MasterInput = None
        self.ProcessorName = None

    def SetMeterCallback(self, Call: callable):
        """
        Assigns a callback for the VUmeter to draw the Amp peaks
        """
        self.PeakAmp.setFunction(Call)

    def processor(self):
        """
        Processing block of the Master filter and returns the output stream
        """
        if self.MasterInput == None:
            raise TypeError("Variable Of type Pyo.Input Expected but got None")

        # Inits the Previous Processing block
        self.Processor = pyo.Sine(0)

        # Inits the switch to use for bypassing between original and processed signal
        self.Switch = pyo.Selector([self.MasterInput, self.Processor], 0)

        # inits the Paning Filter for the Audio
        self.Output = pyo.Pan(self.Switch)

        # inits the peakamp that will be used to monitor the audio amplitude
        self.PeakAmp = pyo.PeakAmp(self.Output)

        return self.Output

    def Bypass(self, Bool = True):
        """
        Inits the switch to use for bypassing between original and processed signal
        """
        if Bool:
            # will Bypass the processor
            self.Switch.setVoice(0)
            self.Processor.stop()
        else:
            # will not Bypass The Processor
            self.Switch.setVoice(1)
            self.Processor.play()

    def SetOutputMul(self, Val: int):
        """
        sets the amplitude for the processor swith
        """
        self.Switch.setMul((Val / 100) + 0.0001)

    def SetInputMul(self, Val: int):
        """
        sets the amplitude for the input
        """
        self.MasterInput.setMul((Val / 100) + 0.0001)

    def SetPan(self, Val: int):
        """
        sets the pan for the filter
        """
        self.Output.setPan((Val / 100) + 0.0001)

    def ReplaceInput(self, Input):
        pass

    def BindMixerUI(self, bypass, pan, premix, postmix):
        """
        Binds the Internal Function to UI Objects
        """
        bypass.setChecked(True)
        pan.setValue(int(self.Output.pan * 100))
        premix.setValue(int(self.MasterInput.mul * 100))
        postmix.setValue(int(self.Switch.mul * 100))

        bypass.toggled.connect(self.Bypass)
        pan.valueChanged.connect(self.SetPan)
        premix.valueChanged.connect(self.SetInputMul)
        postmix.valueChanged.connect(self.SetOutputMul)

class MasterProcessor(BaseProcessor):
    """
    Master Processor that will accept the Input when all the processing is done
    """
    def __init__(self, Input):
        """
        Inits the Input Stream
        """
        super().__init__()
        self.MasterInput = Input
        self.ProcessorName = "Master"


if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
