"""
Main entry point for apollo as a module

executes apollo inside a production env config
"""
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# pylint: disable=C0413
from apollo.main import main


main()
