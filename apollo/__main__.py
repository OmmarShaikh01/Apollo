import os
import sys

sys.path.append(os.path.dirname(__file__))


if __name__ == '__main__':
    from configs import settings
    settings.setenv("PRODUCTION")
    settings.validators.validate()
    print(settings.current_env)

    from apollo.main import main

    main()
