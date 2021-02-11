import pyo
from PyQt5 import QtWidgets, QtCore, QtGui

import sys, os, time, math


class VUMeter:
    """
    VU meter class paints the amplitude bars of the given aplitude by an callback function
    """

    def __init__(self, Parent: QtWidgets.QWidget = None, Meter: QtWidgets.QLabel = None):
        """
        :Args:
            Parent: QWidget
                Parent WIdget to place the widget into
            Meter: QLabel
                QLabel to draw the VU meter to

        :Inits:
            meter: QLabel to daw the bars
            rect: frame rectangale
            Gradient: colour gradient to use
            pixmap: Pixmap to use and draw the VU bars to
            Qpainter: Painter object to use
            scale: scaling factor for the amplitude
        """

        # creates the UI and sets the VUmeter ui to the passed in parent widget
        if Parent != None:
            self.setupUi(Parent)
            self.meter = self.apollo_PIXLB_ATOL_masterCH_VU
            Parent.layout().addWidget(self.GetWidget(), 0, Parent.layout().count(), 1, 1, QtCore.Qt.AlignLeft)

        # assigns the meter for which the VU meter will be drawn
        if Meter != None:
            self.meter = Meter

        self.rect = self.GetRect(self.meter)
        self.Gradient = self.GetGradient(self.rect.height())
        self.pixmap = self.GetPixmap(self.rect.width(), self.rect.height())
        self.meter.setPixmap(self.pixmap)
        self.Qpainter = QtGui.QPainter(self.meter.pixmap())
        self.scale = 1

    def MonitorResize(self):
        """
        Monitors the resize functions of the frames and label rects ad reintis the variables
        """
        if (self.meter.height() - 2) > self.rect.height():
            self.Qpainter.end()
            self.rect = self.GetRect(self.meter)
            self.Gradient = self.GetGradient(self.rect.height())
            self.pixmap = self.GetPixmap(self.rect.width(), self.rect.height())
            self.meter.setPixmap(self.pixmap)
            self.Qpainter = QtGui.QPainter(self.meter.pixmap())

    def Painter(self, *args: list):
        """
        Main callback function in which amplitudes are passed in as an argument
        """
        # checks for the avilable channels of audio
        if len(args) == 2:
            self.Dual_channels(Amp = args)
        else:
            pass

    def Amp_toDB(self, amp: int) -> float:
        """
        converts the aqmplitude to decibles
        clips the values below 0.000001 to -120Db

        :Args:
            amp: Float
                amplitude value
        """
        amp = 20 * math.log10(amp) if amp >= 0.000001 else 20 * math.log10(0.000001)
        amp = amp if not amp <= -120 else -120
        return amp

    def MaptoMeter(self, amp: int, height: int) -> int:
        """
        Maps the amplitude value to the height of black top rect that hides the underlying gradient

        :Args:
            amp: Float
                amplitude value
            height: int
                height of the pixmap

        :Return:
            height of the top bar that will shade the rect
        """
        return int(height - ((amp * self.scale) * height))

    def Dual_channels(self, Amp = []):
        """
        Draws the Dual channel Amplitude bar

        :Args:
            amp: Float
                amplitude value
        """
        # Monitors the resize changes
        self.MonitorResize()

        self.Qpainter.restore()
        # adds a Black BackGround
        self.Qpainter.fillRect(self.rect, QtCore.Qt.black)

        # adds the gradient bars
        self.Qpainter.fillRect(QtCore.QRect(0, 0, 15, self.rect.height()), self.Gradient)
        self.Qpainter.fillRect(QtCore.QRect(17, 0, 15, self.rect.height()), self.Gradient)

        # adds the overlay
        self.Qpainter.fillRect(QtCore.QRect(0, 0, 15, self.MaptoMeter(Amp[0], self.rect.height())), QtCore.Qt.black)
        self.Qpainter.fillRect(QtCore.QRect(17, 0, 15, self.MaptoMeter(Amp[1], self.rect.height())), QtCore.Qt.black)

        # Debug line
        # print(self.MaptoMeter(Amp[0], self.rect.height()), self.MaptoMeter(Amp[1], self.rect.height()))

        # saves and updates
        self.Qpainter.save()
        self.meter.update()

    def GetGradient(self, Height: int) -> QtGui.QLinearGradient:
        """
        Gets the Height and generates the linear gradient according to it.

        :Args:
            height: int
                Height of the pixmap

        :Return:
            A Gradient Object
        """
        Gradient = QtGui.QLinearGradient(0, 0, 0, Height)
        Gradient.setColorAt(0, QtGui.QColor(QtGui.qRgba(255, 0, 0, 255)))
        Gradient.setColorAt(0.37, QtGui.QColor(QtGui.qRgba(255, 255, 0, 255)))
        Gradient.setColorAt(0.4588, QtGui.QColor(QtGui.qRgba(0, 255, 0, 255)))
        Gradient.setColorAt(1, QtGui.QColor(QtGui.qRgba(0, 0, 255, 255)))
        return Gradient

    def GetPixmap(self, W: int, H: int) -> QtGui.QPixmap:
        """
        Gets the Widgets Dimension and genrates a pixmap related to it

        :Args:
            height: int
                Height of the Widget
            width: int
                Width of the Widget

        :Return:
            A pixmap Object
        """
        pixmap = QtGui.QPixmap(W, H)
        pixmap.fill(QtCore.Qt.black)
        return pixmap

    def GetRect(self, meter: QtWidgets.QLabel) -> QtCore.QRect:
        """
        Gets the Widgets Dimension and genrates a rect frame related to it

        :Args:
            meter: Qlabel
                Qlabel to generate a rect for

        :Return:
            A rect Object
        """
        H = meter.height()
        W = meter.width()
        return QtCore.QRect(0, 0, W, H)

    def GetWidget(self) -> QtWidgets.QFrame:
        """
        returns the Top level frame for the Mixer Ui for placeing in a mainwindow frame
        """
        return self.apollo_FR_ATOL_masterCH

    def setupUi(self, Parent: QtWidgets.QWidget):
        """
        Desigener generated code for the Mixer meter UI
        """

        self.apollo_FR_ATOL_masterCH = QtWidgets.QFrame(Parent)
        self.apollo_FR_ATOL_masterCH.setGeometry(QtCore.QRect(304, 152, 38, 324))
        self.apollo_FR_ATOL_masterCH.setMinimumSize(QtCore.QSize(38, 0))
        self.apollo_FR_ATOL_masterCH.setMaximumSize(QtCore.QSize(38, 16777215))
        self.apollo_FR_ATOL_masterCH.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apollo_FR_ATOL_masterCH.setObjectName("apollo_FR_ATOL_masterCH")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.apollo_FR_ATOL_masterCH)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.apollo_FR_ATOL_masterCH_VU = QtWidgets.QFrame(self.apollo_FR_ATOL_masterCH)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_FR_ATOL_masterCH_VU.sizePolicy().hasHeightForWidth())
        self.apollo_FR_ATOL_masterCH_VU.setSizePolicy(sizePolicy)
        self.apollo_FR_ATOL_masterCH_VU.setMinimumSize(QtCore.QSize(32, 0))
        self.apollo_FR_ATOL_masterCH_VU.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_ATOL_masterCH_VU.setObjectName("apollo_FR_ATOL_masterCH_VU")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.apollo_FR_ATOL_masterCH_VU)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.apollo_HDLBD_ATOL_masterCH_Header = QtWidgets.QLabel(self.apollo_FR_ATOL_masterCH_VU)
        self.apollo_HDLBD_ATOL_masterCH_Header.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_HDLBD_ATOL_masterCH_Header.setMaximumSize(QtCore.QSize(32, 32))
        self.apollo_HDLBD_ATOL_masterCH_Header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apollo_HDLBD_ATOL_masterCH_Header.setAlignment(QtCore.Qt.AlignCenter)
        self.apollo_HDLBD_ATOL_masterCH_Header.setObjectName("apollo_HDLBD_ATOL_masterCH_Header")
        self.verticalLayout_2.addWidget(self.apollo_HDLBD_ATOL_masterCH_Header)
        self.apollo_PIXLB_ATOL_masterCH_VU = QtWidgets.QLabel(self.apollo_FR_ATOL_masterCH_VU)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.apollo_PIXLB_ATOL_masterCH_VU.sizePolicy().hasHeightForWidth())
        self.apollo_PIXLB_ATOL_masterCH_VU.setSizePolicy(sizePolicy)
        self.apollo_PIXLB_ATOL_masterCH_VU.setMinimumSize(QtCore.QSize(32, 96))
        self.apollo_PIXLB_ATOL_masterCH_VU.setMaximumSize(QtCore.QSize(32, 96))
        self.apollo_PIXLB_ATOL_masterCH_VU.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apollo_PIXLB_ATOL_masterCH_VU.setAlignment(QtCore.Qt.AlignCenter)
        self.apollo_PIXLB_ATOL_masterCH_VU.setObjectName("apollo_PIXLB_ATOL_masterCH_VU")
        self.verticalLayout_2.addWidget(self.apollo_PIXLB_ATOL_masterCH_VU)
        self.apollo_DIAL_ATOL_masterCH_ctrl = QtWidgets.QDial(self.apollo_FR_ATOL_masterCH_VU)
        self.apollo_DIAL_ATOL_masterCH_ctrl.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_ctrl.setMaximumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_ctrl.setMaximum(100)
        self.apollo_DIAL_ATOL_masterCH_ctrl.setSliderPosition(50)
        self.apollo_DIAL_ATOL_masterCH_ctrl.setObjectName("apollo_DIAL_ATOL_masterCH_ctrl")
        self.verticalLayout_2.addWidget(self.apollo_DIAL_ATOL_masterCH_ctrl)
        self.verticalLayout_4.addWidget(self.apollo_FR_ATOL_masterCH_VU)
        self.apollo_FR_ATOL_masterCH_vol = QtWidgets.QFrame(self.apollo_FR_ATOL_masterCH)
        self.apollo_FR_ATOL_masterCH_vol.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_ATOL_masterCH_vol.setObjectName("apollo_FR_ATOL_masterCH_vol")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.apollo_FR_ATOL_masterCH_vol)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl = QtWidgets.QSlider(self.apollo_FR_ATOL_masterCH_vol)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.apollo_VSLD_ATOL_masterCH_vol_ctrl.sizePolicy().hasHeightForWidth())
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setSizePolicy(sizePolicy)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setMinimumSize(QtCore.QSize(32, 0))
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setMaximumSize(QtCore.QSize(32, 16777215))
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setMaximum(200)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setOrientation(QtCore.Qt.Vertical)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setObjectName("apollo_VSLD_ATOL_masterCH_vol_ctrl")
        self.verticalLayout_3.addWidget(self.apollo_VSLD_ATOL_masterCH_vol_ctrl)
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix = QtWidgets.QDial(self.apollo_FR_ATOL_masterCH_vol)
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setMaximumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setMaximum(100)
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setObjectName("apollo_DIAL_ATOL_masterCH_vol_prevmix")
        self.verticalLayout_3.addWidget(self.apollo_DIAL_ATOL_masterCH_vol_prevmix)
        self.apollo_PSB_ATOL_masterCH_vol_bypass = QtWidgets.QPushButton(self.apollo_FR_ATOL_masterCH_vol)
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setMaximumSize(QtCore.QSize(32, 16777215))
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setCheckable(True)
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setObjectName("apollo_PSB_ATOL_masterCH_vol_bypass")
        self.verticalLayout_3.addWidget(self.apollo_PSB_ATOL_masterCH_vol_bypass)
        self.verticalLayout_4.addWidget(self.apollo_FR_ATOL_masterCH_vol)

        # Setting up palceholder text
        self.apollo_HDLBD_ATOL_masterCH_Header.setText("M")
        self.apollo_PIXLB_ATOL_masterCH_VU.setText("M")
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setText("OO")

class MixerChannelsWidget(VUMeter):
    """
    Class for controling mixer channels
    """

    def __init__(self, Parent):
        """Constructor"""
        super().__init__(Parent)
        self.Input = pyo.Sine(100)
        self.processor()
        self.BindMixerUI(bypass = self.apollo_PSB_ATOL_masterCH_vol_bypass,
                         pan = self.apollo_DIAL_ATOL_masterCH_ctrl,
                         premix = self.apollo_DIAL_ATOL_masterCH_vol_prevmix,
                         postmix = self.apollo_VSLD_ATOL_masterCH_vol_ctrl)
        self.SetMeterCallback(self.Painter)

    def SetMeterCallback(self, Call: callable):
        """
        Assigns a callback for the VUmeter to draw the Amp peaks
        """
        self.PeakAmp.setFunction(Call)

    def processor(self):
        """
        Processing block of the Master filter and returns the output stream
        """
        # Inits the Previous Processing block
        self.Processor = pyo.Sine(0)

        # Inits the switch to use for bypassing between original and processed signal
        self.Switch = pyo.Selector([self.Input, self.Processor], 0)

        # inits the Paning Filter for the Audio
        self.Output = pyo.Pan(self.Switch, mul = 1.15)

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
        self.Input.setMul((Val / 100) + 0.0001)

    def SetPan(self, Val: int):
        """
        sets the pan for the filter
        """
        self.Output.setPan((Val / 100) + 0.0001)

    def ReplaceInput(self, Input):
        self.Switch.setInputs([Input, self.Processor])

    def BindMixerUI(self, bypass, pan, premix, postmix):
        """
        Binds the Internal Function to UI Objects
        """
        bypass.setChecked(True)
        pan.setValue(int(self.Output.pan * 100))
        premix.setValue(int(self.Input.mul * 100))
        postmix.setValue(int(self.Switch.mul * 100))

        bypass.toggled.connect(self.Bypass)
        pan.valueChanged.connect(self.SetPan)
        premix.valueChanged.connect(self.SetInputMul)
        postmix.valueChanged.connect(self.SetOutputMul)


class ApolloAudioMixer:
    """
    Manages all the Mixer channels and it corresponding widgets
    """

    def __init__(self, Parent: QtWidgets.QWidget, Input: "pyo.Input"):
        """Constructor"""
        self.Parent = Parent
        self.Mixer_alloc = {}

        self.MasterInput = Input
        self.MasterOutput = None

    def set_MasterInput(self, Input: "pyo.Input"):
        self.MasterInput = Input

    def get_MasterOutput(self):
        return self.MasterOutput

    def connect_ServerChannel(self, server: pyo.Server, meter: QtWidgets.QLabel):
        # sets tehe VU meter for the server Amp
        self.MasterVU_Meter = VUMeter(Meter = meter)
        # adds an scaling factor for displaying the amplitude
        self.MasterVU_Meter.scale = 100
        # binds the server callback to the meter painter
        server.setMeterCallable(self.MasterVU_Meter.Painter)

    def create_EmptyMixerChannels(self, Channels: int = 32):
        self.N_channels = Channels
        self.MixerDict = {}
        for channel in range(Channels):
            MixerChannel = MixerChannelsWidget(Parent = self.Parent)
            self.MixerDict[channel] = MixerChannel
            self.Mixer_alloc[channel] = []
        self.cascading_connectChannels(self.MixerDict)

    def cascading_connectChannels(self, Channels: dict):
        for Channel, Widget in Channels.items():

            if (Channel == 0):
                self.MasterOutput = Widget.Output
                self.MasterOutput.out(2)

            if not(Channel == 0 or Channel == self.N_channels - 1):
                NextChannel = Channels[Channel-1]
                NextChannel.ReplaceInput(Widget.Output)

            if (Channel == self.N_channels - 1):
                NextChannel = Channels[Channel-1]
                NextChannel.ReplaceInput(Widget.Output)
                Widget.ReplaceInput(self.MasterInput)

if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
