"""
Main entry point for apollo as a module

executes apollo inside a production env config

TODO:
Add vendor packages in build
"""
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from apollo.main import main


main()
