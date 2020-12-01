import sys, os
sys.path.append(os.path.split(os.path.abspath(__file__))[0].rsplit("\\", 2)[0])

from apollo.test.testUtilities import TestSuit_main
from apollo.test.test_utils import Test_ConfigManager, Test_PlayingQueue
from apollo.test.test_library_manager import Test_LibraryManager
from apollo.test.test_TabFunctions import Test_ApolloTabFunctions_Queueing, Test_ApolloTabFunctions_selection

Suite = TestSuit_main()
Suite.AddTest(Test_ConfigManager)
Suite.AddTest(Test_PlayingQueue)
Suite.AddTest(Test_LibraryManager)
Suite.AddTest(Test_ApolloTabFunctions_Queueing)
Suite.AddTest(Test_ApolloTabFunctions_selection)
Suite.Run(QT = True)
