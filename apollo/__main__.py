"""
Main entry point for apollo as a module

executes apollo inside a production env config

TODO:
Add vendor packages in build
"""
import ctypes
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    from configs import settings

    settings.setenv("PRODUCTION")
    settings.validators.validate_all(only_current_env = True)

    from apollo.__version__ import __version__
    from apollo.main import main

    # Enables App Icon in Taskbar
    myappid = f"apollo.apollo.player.{'_'.join(map(str, __version__))}"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    main()
