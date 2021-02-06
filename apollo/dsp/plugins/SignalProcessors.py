import pyo
from PyQt5 import QtWidgets, QtCore, QtGui

import sys, os, time, math

class VUMeter:
    """
    VU meter class paints the amplitude bars of the given aplitude by an callback function
    """
    def __init__(self, Parent):
        """
        Inits
        meter: QLabel to daw the bars
        rect: frame rectangale
        Gradient: colour gradient to use
        pixmap: Pixmap to use and draw the VU bars to
        Qpainter: Painter object to use
        scale: scaling factor for the amplitude
        """
        self.setupUi(Parent)
        self.meter = self.apollo_PIXLB_ATOL_masterCH_VU

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

    def Painter(self, *args):
        """
        Main callback function in which amplitudes are passed in as an argument
        """
        # checks for the avilable channels of audio
        if len(args) == 2:
            self.Dual_channels(Amp = args)
        else:
            pass

    def Amp_toDB(self, amp):
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

    def MaptoMeter(self, amp, height):
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

    def GetGradient(self, Height):
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

    def GetPixmap(self, W, H):
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

    def GetRect(self, meter):
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

    def GetWidget(self):
        return self.apollo_FR_ATOL_masterCH

    def setupUi(self, Parent):
        self.apollo_FR_ATOL_masterCH = QtWidgets.QFrame(Parent)
        self.apollo_FR_ATOL_masterCH.setGeometry(QtCore.QRect(304, 152, 38, 324))
        self.apollo_FR_ATOL_masterCH.setMinimumSize(QtCore.QSize(38, 0))
        self.apollo_FR_ATOL_masterCH.setMaximumSize(QtCore.QSize(38, 16777215))
        self.apollo_FR_ATOL_masterCH.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apollo_FR_ATOL_masterCH.setObjectName("apollo_FR_ATOL_masterCH__12")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.apollo_FR_ATOL_masterCH)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName("verticalLayout_4__12")

        self.apollo_FR_ATOL_masterCH_VU = QtWidgets.QFrame(self.apollo_FR_ATOL_masterCH)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_FR_ATOL_masterCH_VU.sizePolicy().hasHeightForWidth())
        self.apollo_FR_ATOL_masterCH_VU.setSizePolicy(sizePolicy)
        self.apollo_FR_ATOL_masterCH_VU.setMinimumSize(QtCore.QSize(32, 0))
        self.apollo_FR_ATOL_masterCH_VU.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_ATOL_masterCH_VU.setObjectName("apollo_FR_ATOL_masterCH_VU__12")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.apollo_FR_ATOL_masterCH_VU)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2__12")

        self.apollo_HDLBD_ATOL_masterCH_Header = QtWidgets.QLabel(self.apollo_FR_ATOL_masterCH_VU)
        self.apollo_HDLBD_ATOL_masterCH_Header.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_HDLBD_ATOL_masterCH_Header.setMaximumSize(QtCore.QSize(32, 32))
        self.apollo_HDLBD_ATOL_masterCH_Header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.apollo_HDLBD_ATOL_masterCH_Header.setAlignment(QtCore.Qt.AlignCenter)
        self.apollo_HDLBD_ATOL_masterCH_Header.setObjectName("apollo_HDLBD_ATOL_masterCH_Header__12")
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
        self.apollo_PIXLB_ATOL_masterCH_VU.setObjectName("apollo_PIXLB_ATOL_masterCH_VU__12")
        self.verticalLayout_2.addWidget(self.apollo_PIXLB_ATOL_masterCH_VU)

        self.apollo_DIAL_ATOL_masterCH_ctrl = QtWidgets.QDial(self.apollo_FR_ATOL_masterCH_VU)
        self.apollo_DIAL_ATOL_masterCH_ctrl.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_ctrl.setMaximumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_ctrl.setMaximum(100)
        self.apollo_DIAL_ATOL_masterCH_ctrl.setSliderPosition(50)
        self.apollo_DIAL_ATOL_masterCH_ctrl.setObjectName("apollo_DIAL_ATOL_masterCH_ctrl__12")
        self.verticalLayout_2.addWidget(self.apollo_DIAL_ATOL_masterCH_ctrl)

        self.verticalLayout_4.addWidget(self.apollo_FR_ATOL_masterCH_VU)

        self.apollo_FR_ATOL_masterCH_vol = QtWidgets.QFrame(self.apollo_FR_ATOL_masterCH)
        self.apollo_FR_ATOL_masterCH_vol.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_ATOL_masterCH_vol.setObjectName("apollo_FR_ATOL_masterCH_vol__12")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.apollo_FR_ATOL_masterCH_vol)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3__12")

        self.apollo_VSLD_ATOL_masterCH_vol_ctrl = QtWidgets.QSlider(self.apollo_FR_ATOL_masterCH_vol)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.apollo_VSLD_ATOL_masterCH_vol_ctrl.sizePolicy().hasHeightForWidth())
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setSizePolicy(sizePolicy)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setMinimumSize(QtCore.QSize(32, 0))
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setMaximumSize(QtCore.QSize(32, 16777215))
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setMaximum(100)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setOrientation(QtCore.Qt.Vertical)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.apollo_VSLD_ATOL_masterCH_vol_ctrl.setObjectName("apollo_VSLD_ATOL_masterCH_vol_ctrl__12")
        self.verticalLayout_3.addWidget(self.apollo_VSLD_ATOL_masterCH_vol_ctrl)

        self.apollo_DIAL_ATOL_masterCH_vol_prevmix = QtWidgets.QDial(self.apollo_FR_ATOL_masterCH_vol)
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setMaximumSize(QtCore.QSize(32, 32))
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setMaximum(100)
        self.apollo_DIAL_ATOL_masterCH_vol_prevmix.setObjectName("apollo_DIAL_ATOL_masterCH_vol_prevmix__12")
        self.verticalLayout_3.addWidget(self.apollo_DIAL_ATOL_masterCH_vol_prevmix)

        self.apollo_PSB_ATOL_masterCH_vol_bypass = QtWidgets.QPushButton(self.apollo_FR_ATOL_masterCH_vol)
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setMaximumSize(QtCore.QSize(32, 16777215))
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setCheckable(True)
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setObjectName("apollo_PSB_ATOL_masterCH_vol_bypass__12")

        self.verticalLayout_3.addWidget(self.apollo_PSB_ATOL_masterCH_vol_bypass)
        self.verticalLayout_4.addWidget(self.apollo_FR_ATOL_masterCH_vol)

        # SettingUP text
        self.apollo_HDLBD_ATOL_masterCH_Header.setText("M")
        self.apollo_PIXLB_ATOL_masterCH_VU.setText("M")
        self.apollo_PSB_ATOL_masterCH_vol_bypass.setText("OO")


class BaseProcessor:
    """"""

    def __init__(self):
        """Constructor"""
        self.MasterInput = None

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

    def SetOutputMul(self, Val):
        """
        sets the amplitude for the processor swith
        """
        self.Switch.setMul((Val / 100) + 0.0001)

    def SetInputMul(self, Val):
        """
        sets the amplitude for the input
        """
        self.MasterInput.setMul((Val / 100) + 0.0001)

    def SetPan(self, Val):
        """
        sets the pan for the filter
        """
        self.Output.setPan((Val / 100) + 0.0001)

    def ReplaceInput(self, Input):
        pass

    def BindMixerUI(self, bypass, pan, premix, postmix, meter):
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

        self.VUMeter = VUMeter(meter)
        self.PeakAmp.setFunction(self.VUMeter.Painter)

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


if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
