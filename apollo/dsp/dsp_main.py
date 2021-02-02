import pyo
from PyQt5 import QtWidgets, QtCore, QtGui

import sys, os, time, math


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

class VUMeter:

    def __init__(self, meter):
        self.meter = meter
        self.rect = self.GetRect(meter)
        self.meter.setPixmap(self.GetPixmap())
        self.Qpainter = QtGui.QPainter(self.meter.pixmap())
        self.Gradient = QtGui.QLinearGradient(0, 0, 0, self.rect.height())
        self.Gradient.setColorAt(0, QtGui.QColor(QtGui.qRgba(255, 0, 0, 255)))
        self.Gradient.setColorAt(0.37, QtGui.QColor(QtGui.qRgba(255, 255, 0, 255)))
        self.Gradient.setColorAt(0.4588, QtGui.QColor(QtGui.qRgba(0, 255, 0, 255)))
        self.Gradient.setColorAt(1, QtGui.QColor(QtGui.qRgba(0, 0, 255, 255)))

    def GetPixmap(self):
        pixmap = QtGui.QPixmap(self.rect.width(), self.rect.height())
        pixmap.fill(QtCore.Qt.black)
        return pixmap

    def Painter(self, *args):
        if len(args) == 2:
            self.Dual_channels(Amp = args)
        else:
            pass

    def Amp_toDB(self, amp):
        amp = 20 * math.log10(amp) if amp >= 0.0001 else 20 * math.log10(0.0001)
        amp = amp if not amp <= -70.0 else -70.0
        return amp

    def MaptoMeter(self, amp, height):
        return int(height - ((self.Amp_toDB(amp) / 75 ) + 1) * height)

    def Dual_channels(self, Amp = []):

        self.Qpainter.restore()
        self.Qpainter.fillRect(self.rect, QtCore.Qt.black)
        self.Qpainter.fillRect(QtCore.QRect(0, 0, 15, self.rect.height()), self.Gradient)
        self.Qpainter.fillRect(QtCore.QRect(17, 0, 15, self.rect.height()), self.Gradient)

        self.Qpainter.fillRect(QtCore.QRect(0, 0, 15, self.MaptoMeter(Amp[0], self.rect.height())), QtCore.Qt.black)
        self.Qpainter.fillRect(QtCore.QRect(17, 0, 15, self.MaptoMeter(Amp[1], self.rect.height())), QtCore.Qt.black)
        self.Qpainter.save()
        self.meter.update()


    def GetRect(self, meter):
        H = meter.height()
        W = meter.width()
        return QtCore.QRect(0, 0, W, H)

class MasterProcessor:
    """"""

    def __init__(self, Input):
        self.Input = Input

    def processor(self):
        """"""
        self.Processor = pyo.Sine(0)
        self.Switch = pyo.Selector([self.Input, self.Processor], 0)
        self.Output = pyo.Pan(self.Switch)

        self.PeakAmp = pyo.PeakAmp(self.Output)
        return self.Output

    def Bypass(self, Bool = True):
        if Bool:
            # will Bypass the processor
            self.Switch.setVoice(0)
            self.Processor.stop()
        else:
            # will not Bypass The Processor
            self.Switch.setVoice(1)
            self.Processor.play()

    def SetOutputMul(self, Val):
        self.Switch.setMul((Val / 100) + 0.0001)

    def SetInputMul(self, Val):
        self.Input.setMul((Val / 100) + 0.0001)

    def SetPan(self, Val):
        self.Output.setPan((Val / 100) + 0.0001)

    def BindMixerUI(self, bypass, pan, premix, postmix, meter):
        bypass.setChecked(True)
        pan.setValue(int(self.Output.pan * 100))
        premix.setValue(int(self.Input.mul * 100))
        postmix.setValue(int(self.Switch.mul * 100))

        bypass.toggled.connect(self.Bypass)
        pan.valueChanged.connect(self.SetPan)
        premix.valueChanged.connect(self.SetInputMul)
        postmix.valueChanged.connect(self.SetOutputMul)

        self.VUMeter = VUMeter(meter)
        self.PeakAmp.setFunction(self.VUMeter.Painter)



class ApolloDSP:
    """
    Apollos DSP graph to create Audio Processing Graph used to precess Audio
    """


    def __init__(self, **kwargs):
        self.ComputeGraph = ComputeGraph()
        self.UI = kwargs.get("UI")
        if not kwargs.get("UI"):
            from apollo.app.apollo_TabBindings import ApolloTabBindings
            self.UI = ApolloTabBindings()

        self.StartServer()
        self.MasterProcessorBindings(pyo.PinkNoise())


    def MasterProcessorBindings(self, Input):
        self.MasterProcessor = MasterProcessor(Input)
        self.MasterProcessor.processor().out()
        self.MasterProcessor.BindMixerUI(bypass = self.UI.apollo_PSB_ATOL_masterCH_vol_bypass,
                                         pan = self.UI.apollo_DIAL_ATOL_masterCH_ctrl,
                                         premix = self.UI.apollo_DIAL_ATOL_masterCH_vol_prevmix,
                                         postmix = self.UI.apollo_VSLD_ATOL_masterCH_vol_ctrl,
                                         meter = self.UI.apollo_PIXLB_ATOL_masterCH_VU)

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


        self.Server.setAmp(kwargs.get("amp", 0.1))


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
