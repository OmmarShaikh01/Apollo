from unittest.mock import Mock, MagicMock
from unittest import TestCase

from apollo.dsp.dsp_main import ComputeGraph
from apollo.test.testUtilities import TestSuit_main

class DSP_MockObjects:
    """"""

    @classmethod
    def Get_MockProcessor(cls, name):
        MockObj = Mock(name = str(name))

        return MockObj


class Test_ComputeGraph(TestCase):
    """"""
    def setUp(self):
        self.INST = ComputeGraph()

    def test_(self):
        self.INST.InsertNode(DSP_MockObjects.Get_MockProcessor(0), 0)
        self.INST.InsertNode(DSP_MockObjects.Get_MockProcessor(1), 1)
        self.INST.InsertNode(DSP_MockObjects.Get_MockProcessor(2), 2)
        print(self.INST)


if __name__ =="__main__":
    Suite = TestSuit_main()
    Suite.AddTest(Test_ComputeGraph)
    Suite.Run()
