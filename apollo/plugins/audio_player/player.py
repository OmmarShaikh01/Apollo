import time, os, threading, datetime
from pprint import pprint

import pyo, av

from apollo.utils import dedenter, exe_time, tryit
from apollo.plugins.audio_player import AudioTable, MediaFile


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

    def gui(self):
        """
        Info: Starts the GUI for Audio Processor server
        Args: None
        Returns: None
        Errors: None
        """
        self.MainServer.gui(locals())

    def ServerInfo(self):
        """
        Info: Gets server and device info
        Args: None
        Returns: dict
        Errors: None
        """
        info = {}
        info["pa_count_devices"] = pyo.pa_count_devices() # type: ignore
        info["pa_get_default_input"] = pyo.pa_get_default_input() # type: ignore
        info["pa_get_default_output"] = pyo.pa_get_default_output() # type: ignore
        info["pm_get_input_devices"] = pyo.pm_get_input_devices() # type: ignore
        info["pa_count_host_apis"] = pyo.pa_count_host_apis() # type: ignore
        info["pa_get_default_host_api"] = pyo.pa_get_default_host_api() # type: ignore
        info["pm_count_devices"] = pyo.pm_count_devices() # type: ignore
        info["pa_get_input_devices"] = pyo.pa_get_input_devices() # type: ignore
        info["pm_get_default_input"] = pyo.pm_get_default_input() # type: ignore
        info["pm_get_output_devices"] = pyo.pm_get_output_devices() # type: ignore
        info["pm_get_default_output"] = pyo.pm_get_default_output() # type: ignore
        info["pa_get_devices_infos"] = pyo.pa_get_devices_infos() # type: ignore
        info["pa_get_version"] = pyo.pa_get_version() # type: ignore
        info["pa_get_version_text"] = pyo.pa_get_version_text() # type: ignore
        return info


class PlayBack_Controls(AudioInterface): # messed

    def __init__(self):
        super().__init__()
        self.AudioDecoder = None
        self.CurrentFile = None
        self.AudioTable = None

    def play(self, file = None):

        if file != None and os.path.isfile(file):
            self.CurrentFile = file

            self.AudioTable = self.AudioDecoder.GetTable()
            self.reader = pyo.TableRead(self.AudioTable, self.AudioTable.getRate()).out()
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
