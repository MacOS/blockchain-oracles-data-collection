'''
    This script implements the push in-bound oracles described in 
    
    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
    
    for evalution purposes.

    A push in-bound oracle is a software artifact that writes data to the blockchain (in-bound) triggered
    by an on-chain event (push).

    Author: Stefan Bachhofner
'''

from utils import Oracle


class PushInboundOracle(Oracle):

    def __init__(self):
        super(self, PushInboundOracle).__init__()
 
 
def main():
    return 0


if __name__ == "__main__":
    main()