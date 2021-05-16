import time, os, sys, argparse, queue, threading
from pprint import pprint

import pyo, av

from apollo.utils import dedenter, tryit
from apollo.plugins.audio_player.audiotables import AudioTable

"""
Plugin Support:
# Bitrate:
    -> 44100
# Formats:
    -> .mp3
# Channels:
    -> 2
"""

class AudioDecoder(threading.Thread):
    """
    Info: Main Interface to access all audio deccoders.
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self, path):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()
        self.start()
        self.file = path
        self.AudioTable = AudioTable()
        self.ThreadState = "ACTIVE"

    def run(self):
        """
        Info: threade runner
        Args: None
        Returns: None
        Errors: None
        """
        while self.ThreadState != "EXIT":
            if self.ThreadState == "DECODE":
                self.__Decode(self.file)
            else:
                time.sleep(0.01)

    def stop(self):
        """
        Info: thread exit
        Args: None
        Returns: None
        Errors: None
        """
        self.ThreadState = "EXIT"

    def GetTable(self):
        self.AudioTable

    def decode(self):
        self.ThreadState = "DECODE"

    def __Decode(self, path = None):
        """
        Info: Audio Decoder
        Args: None
        Returns: None
        Errors: None`
        """
        if path is not None:
            self.file = path

        print(f"Playing: {self.file}")

        # variable Declaration
        self.ThreadState = "DECODING"

        # actual decoding and demuxing of file
        with av.open(self.file) as InputStream:
            for packet in InputStream.demux(audio = 0):
                if packet.size <= 0:
                    break
                for frame in packet.decode():
                    self.AudioTable.put(frame)

        self.ThreadState = "DECODED"
        print(self.AudioTable.GetTableData())
        print(self.ThreadState)


class AudioInterface:
    """
    Info: Main Interface to access all audio related functions.
    Args: None
    Returns: None
    Errors:
    1. VSCode debugger Mode errors out the PortAudio. FIX: Launch server in GUI Mode
    """
    def __init__(self):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """

    def ServerBootUp(self):
        """
        Info: Starts the Audio Processor server
        Args: None
        Returns: None
        Errors: None
        """
        self.MainServer = pyo.Server().boot()
        return self

    def ServerInfo(self):
        """
        Info: Gets server and device info
        Args: None
        Returns: dict
        Errors: None
        """
        info = {}
        info["pa_count_devices"] = pyo.pa_count_devices()
        info["pa_get_default_input"] = pyo.pa_get_default_input()
        info["pa_get_default_output"] = pyo.pa_get_default_output()
        info["pm_get_input_devices"] = pyo.pm_get_input_devices()
        info["pa_count_host_apis"] = pyo.pa_count_host_apis()
        info["pa_get_default_host_api"] = pyo.pa_get_default_host_api()
        info["pm_count_devices"] = pyo.pm_count_devices()
        info["pa_get_input_devices"] = pyo.pa_get_input_devices()
        info["pm_get_default_input"] = pyo.pm_get_default_input()
        info["pm_get_output_devices"] = pyo.pm_get_output_devices()
        info["pm_get_default_output"] = pyo.pm_get_default_output()
        info["pa_get_devices_infos"] = pyo.pa_get_devices_infos()
        info["pa_get_version"] = pyo.pa_get_version()
        info["pa_get_version_text"] = pyo.pa_get_version_text()
        return info


class PlayBack_Controls(AudioInterface):

    def __init__(self):
        super().__init__()
        self.AudioDecoder = None
        self.CurrentFile = None
        self.AudioTable = None

    def play(self, file = None):

        if file != None and os.path.isfile(file):
            self.CurrentFile = file

            if self.AudioDecoder != None:
                self.AudioDecoder.stop()

            self.AudioDecoder = AudioDecoder(file)
            self.AudioTable = self.AudioDecoder.GetTable()
            self.AudioDecoder.decode()
            return True

        elif file == None:
            return True

        else:
            return False

    def pause(self): ...

    def stop(self):
        self.AudioDecoder.stop()

    def seek_f(self): ...
    def seek_b(self): ...
    def skip_f(self): ...
    def skip_b(self): ...


################################################################################
# CLI for Apollos DSP
################################################################################
class PlayerCLI:
    """
    Info: Player CLI
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        self.Exit = False
        self.PlayBack_Controls = PlayBack_Controls().ServerBootUp()

    def RunLoop(self):
        """
        Info: Runs MainLoop
        Args: None
        Returns: None
        Errors: None
        """
        self.Exit = True

        Fname = None

        while self.Exit:
            Arg = (input(">>> ").strip()).split(" ")

            if "help" in Arg:
                HelpStr = f"""
                {'Arguments:': <12} | Description
                {'-'*40}
                {'exit': <12} | to exit the player
                {'help': <12} | to display this page
                {'play': <12} | Plays the given file
                {'pause': <12} | Pauses Playback
                {'stop': <12} | ends playback
                {'seek_f': <12} | seeks forward
                {'seek_b': <12} | seeks backward
                {'skip_f': <12} | skips forward
                {'skip_b': <12} | skips backward
                {'server_info': <12} | prints serverinfo
                {'-'*40}
                """
                print(dedenter(HelpStr, 16))

            if "server_info" in Arg:
                pprint(self.PlayBack_Controls.ServerInfo())

            if "play" in Arg:
                if len(Arg) > (Arg.index("play") + 1):
                    Fname = (Arg[Arg.index("play") + 1])
                    if not self.PlayBack_Controls.play(Fname):
                        print(f">>> ERROR: FileName <{Fname}> Invalid or Empty")
                        continue
                else:
                    if not self.PlayBack_Controls.play():
                        print(f">>> ERROR: FileName <{Fname}> Invalid or Empty 1")
                        continue

            if 'pause' in Arg:
                print('pause')

            if 'stop' in Arg:
                print('stop')

            if 'seek_f' in Arg:
                print('seek_f')

            if 'seek_b' in Arg:
                print('seek_b')

            if 'skip_f' in Arg:
                print('skip_f')

            if 'skip_b' in Arg:
                print('skip_b')

            if "exit" in Arg:
                self.PlayBack_Controls.stop()
                self.Exit = False


if __name__ == "__main__":
    # Inst = PlayerCLI()
    # Inst.RunLoop()
    Player = PlayBack_Controls().ServerBootUp()
    Player.play("D:\\music\\cantstopohn.mp3")
