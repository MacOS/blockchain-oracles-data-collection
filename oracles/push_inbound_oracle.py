'''
    This script implements the push in-bound oracles described in 
    
    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.

	for evalution purposes in the following submitted (not yet peer reviewed!) paper

	Mühlberger, R., Di Ciccio, C., Castello Ferrer, E., Bachhofner, S., and Weber, I. (2020) Foundational
	Oracle Patterns. Business Process Management: Blockchain Forum.

    A push in-bound oracle is a software artifact that writes data to the blockchain (in-bound) triggered
    by an off-chain event (push).

    Author: Stefan Bachhofner, Roman Mühlberger
'''

import web3
from apscheduler.schedulers.blocking import BlockingScheduler

from utils import (
	_TransactionSendingOracle,
	RandomArrivalGenerator,
	save_to_mongo,
	get_unix_timestamp,
	convert_unix_timesamp_to_datetime)

import config


class PushInboundOracle(_TransactionSendingOracle):

    def __init__(self, *args, **kwargs):
        super(PushInboundOracle, self).__init__(*args, **kwargs)


class ArrivalState(PushInboundOracle):

    def __init__(self, arrival, *arg, **kwargs):
        super(ArrivalState, self).__init__(*arg, **kwargs)

        self.state = arrival
        self.encoded_abi = self.encode_abi_arrival()

    def encode_abi_arrival(self):
        return self._smart_contract.encodeABI(
            fn_name="setArrival",
            args=[self.state["order"], self.state["location"], int(self.state["timestamp"])])


def execute_push_inbound_oracle():
    random_arrival_state = RandomArrivalGenerator().get_random_arrival()
    
    push_inbound_oracle = ArrivalState(
        public_address=config.PUBLIC_ADDRESS,
        private_address=config.PRIVATE_ADDRESS,
        smart_contract_address=config.ARRIVAL_SMART_CONTRACT_ADDRESS,
        web_socket=config.WEB_SOCKET,
        abi=config.ARRIVAL_ABI,
        arrival=random_arrival_state)

    start_timestamp = get_unix_timestamp()
    
    transaction_hash = web3.eth.to_hex(
        push_inbound_oracle.send_raw_transaction())
    
    end_timestamp = get_unix_timestamp()

    save_to_mongo(
        db="pushInboundOracle", collection="arrival",
        document={
            "transaction_hash": transaction_hash, 
            "start_timestamp": start_timestamp, "end_timestamp": end_timestamp,
            "document": push_inbound_oracle.state})

    return transaction_hash, push_inbound_oracle.state


def push_inbound_oracle():
    transaction_hash, state = execute_push_inbound_oracle()
    print(f"Timestamp: {convert_unix_timesamp_to_datetime(get_unix_timestamp())} Transaction hash: {transaction_hash} | State: {state}")

 
def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(push_inbound_oracle, "interval", minutes=15)
    scheduler.start()
    return 0


if __name__ == "__main__":
    main()
