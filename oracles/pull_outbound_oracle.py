'''
    This script implements the pull out-bound oracles described in
    
    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
    
    for evalution purposes.

    A pull out-bound oracle is a software artifact that retrieves data from the blockchain (out-bound) triggered
    by an off-chain event (pull).

    Author: Stefan Bachhofner
'''

from .utils import _Oracle


class PullOutboundOracle(_Oracle):

    def __init__(self):
        super(PullOutboundOracle self).__init__()


def main():
    return 0


if __name__ == "__main__":
    main()