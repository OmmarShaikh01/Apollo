import pip, sys, os

def main():
    compatible = True
    if sys.version_info < (3, 8): compatible = False
    elif (hasattr(sys, 'base_prefix') or hasattr(sys, 'base_prefix')) and (sys.prefix != sys.base_prefix):
        pip.main(["install", "numpy" , "pyo", "pyaudio", "PyQt5", "beets", "tinytag"])
    else: compatible = False
    if not compatible:
        raise ValueError('This script is only for use with Python 3.8 or later')
