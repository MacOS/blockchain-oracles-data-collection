'''
    This script implements the pull out-bound oracles described in
    
    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
    
    for evalution purposes.

    A pull out-bound oracle is a software artifact that retrieves data from the blockchain (out-bound) triggered
    by an off-chain event (pull).

    Author: Stefan Bachhofner
'''

from apscheduler.schedulers.blocking import BlockingScheduler

from utils import _Oracle, get_unix_timestamp, save_to_mongo
import config


class PullOutboundOracle(_Oracle):

    def __init__(self, *args, **kwargs):
        super(PullOutboundOracle, self).__init__(*args, **kwargs)

    def retrieve_state_from_transaction_hash(self, transaction_hash):
        transaction = self.web_socket.eth.getTransaction(transaction_hash)
        retrieved_state = self._smart_contract.decode_function_input(transaction.input)
        return retrieved_state


def execute_pull_outbound_oracle():
    pull_outbound_oracle = PullOutboundOracle(
        public_address=config.PUBLIC_ADDRESS, private_address=config.PRIVATE_ADDRESS,
        smart_contract_address=config.ARRIVAL_SMART_CONTRACT_ADDRESS,
        web_socket=config.WEB_SOCKET,
        abi=config.ARRIVAL_ABI)

    start_timestamp = get_unix_timestamp()

    retrieved_state = pull_outbound_oracle.retrieve_state_from_transaction_hash(
        transaction_hash="0xf15753a9ef3d83e6d9974a936795039605449cdf2530545c8b339deaa6a7641f")

    end_timestamp = get_unix_timestamp()

    save_to_mongo(
        db="pullOutboundOracle", collection="arrival", 
        document={
            "start_timestamp": start_timestamp, "end_timestamp": end_timestamp,
            "transaction_hash": "0xf15753a9ef3d83e6d9974a936795039605449cdf2530545c8b339deaa6a7641f",
            "state": retrieved_state[1]})

    print(retrieved_state)


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(execute_pull_outbound_oracle, "interval", minutes=15)
    scheduler.start()
    return 0


if __name__ == "__main__":
    main()
