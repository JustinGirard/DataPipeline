import sys
sys.path.append('../')
from processingNetwork.ProcessingNetwork import ProcessingNetwork
from processingNetwork.ProcessingNode import ProcessingNode

class Test(ProcessingNode):
    def do_input(self,feature,context):
        return {'hey':'this is a test'}