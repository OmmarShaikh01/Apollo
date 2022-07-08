import os
import sys

sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    from configs import settings

    settings.setenv("PRODUCTION")
    settings.validators.validate(only_current_env=True)

    from apollo.main import main

    main()
