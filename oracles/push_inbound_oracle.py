'''
    This script implements the push in-bound oracles described in 
    
    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
    
    for evalution purposes.

    A push in-bound oracle is a software artifact that writes data to the blockchain (in-bound) triggered
    by an off-chain event (push).

    Author: Stefan Bachhofner
'''

from .utils import _TransactionSendingOracle


class PushInboundOracle(_TransactionSendingOracle):

    def __init__(self, *args, **kwargs):
        super(self, PushInboundOracle).__init__(args, kwargs)


class ArrivalState(PushInboundOracle):

    def __init__(self, arrival):
        self.arrival = arrival
        self.encoded_abi = self.encode_abi_arrival()

    def encode_abi_arrival(self)
        return self.smart_contract.encodeABI(
            fn_name="setArrival",
            args=[self.arrival["order"], self.arrival["location"], int(self.arrival["timestamp"])])



 
def main():
    return 0


if __name__ == "__main__":
    main()