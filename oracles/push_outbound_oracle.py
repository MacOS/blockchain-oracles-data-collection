 '''
    This file implements the push out-bound oracles described in

    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
    
    for evalution purposes.

    A push out-bound oracle is a software artifact that retrieves data from the blockchain (out-bound) triggered
    by an on-chain event (push).

    Author: Stefan Bachhofner
'''

from .utils import _EventListeningOracle


class PushOutboundOracle(_EventListeningOracle):

    def __init__(self):
        super(self, PushOutboundOracle).__init__()

 
def main():
    return 0


if __name__ == "__main__":
    main()