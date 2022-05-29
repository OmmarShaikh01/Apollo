import os
import sys


try:
    import apollo
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(__file__))

from apollo.main import main
from configs import settings

if __name__ == '__main__':
    settings.setenv("PRODUCTION")
    settings.validators.validate()
    main()
