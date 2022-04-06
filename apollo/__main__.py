import os
import sys

try:
    from apollo.main import main
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(__file__))
    from apollo.main import main

main()
