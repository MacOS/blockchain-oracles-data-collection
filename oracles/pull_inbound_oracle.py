'''
    This script implements the pull in-bound oracles described in
    
    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
    
    for evalution purposes.

    A pull in-bound oracle is a software artifact that writes data to the blockchain (in-bound) triggered
    by an on-chain event (pull).

    Author: Stefan Bachhofner
'''
from multiprocessing import Process
import time

import numpy as np
import web3
from apscheduler.schedulers.background import BackgroundScheduler

from push_inbound_oracle import PushInboundOracle
from utils import _EventListeningOracle, _TransactionSendingOracle, get_unix_timestamp, convert_unix_timesamp_to_datetime, save_to_mongo
import config


class PullInboundOracle(_EventListeningOracle, _TransactionSendingOracle):

    def __init__(self, *args, **kwargs):
        super(PullInboundOracle, self).__init__(*args, **kwargs)


class VerifyCustomerState(PushInboundOracle):

    def __init__(self, verify_customer, *args, **kwargs):
        super(VerifyCustomerState, self).__init__(*args, **kwargs)

        self.state = verify_customer
        self.encoded_abi = self.encoded_abi_verify_customer()

    def encoded_abi_verify_customer(self):
        return self._smart_contract.encodeABI(
            fn_name="verifyCustomer", 
            args=[
                self.state["first_name"], self.state["last_name"], int(self.state["tax_ID"]), self.state["e_mail"],
                self.state["product"], int(self.state["quantity"]), self.state["details"]])


class OrderState(PullInboundOracle):

    def __init__(self, *args, **kwargs):
        super(OrderState, self).__init__(*args, **kwargs)

        # This here is our state from an off-chain component
        self.count = 0

    def encoded_abi_order(self, order):
        return self._smart_contract.encodeABI(
            fn_name="statusCustomerCredibility", 
            args=[order["is_verified"], int(order["order_ID"]), order["error_code"]])

    def process_new_event(self, new_event):
        verify_customer_received_timestamp = get_unix_timestamp()

        # Respond to event via transaction
        self.count += 1
        self.state = {
            "is_verified": True, "order_ID": self.count, "error_code": 0}
        self.encoded_abi = self.encoded_abi_order(self.state)
        start_timestamp = get_unix_timestamp()
        transaction_hash = web3.eth.to_hex(
            self.send_raw_transaction())
        end_timestamp = get_unix_timestamp()

        save_to_mongo(
            db="pullInboundOracle", collection="order",
            document={
                "transaction_hash": transaction_hash,
                "order": self.state, "order_start_timestamp": start_timestamp, "order_end_timestamp": end_timestamp,
                "verify_customer": new_event, "verify_customer_received_timestamp": verify_customer_received_timestamp})

        print(f'(Order) Timestamp: {convert_unix_timesamp_to_datetime(get_unix_timestamp())} | Transaction hash: {transaction_hash} |')


class RandomVerifyCustomerGenerator(object):

    def __init__(self):
        self.first_name_sample_space = ["Tony", "Steve", "Natascha", "Carol"]
        self.last_name_sample_space = ["Stark", "Rogers", "Romanof", "Danvors"]
        self.tax_ID_sample_space = ["123456789", "987654321", "123454321", "987656789"]
        self.e_mail_sample_space = ["@avengers.com", "@disney.com", "@marvel.studios.com", "@marvel.cinematic.universe.com"]
        self.product_sample_space = ["Thors Hammer", "Iron Man Suite", "iPhone XX", "Apple Watch"]
        self.quantity_sample_space = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.details_sample_space = ["Birthday Gift", "Wedding", "Easter"]

    def get_random_verify_customer(self):
        return {
            "first_name": np.random.choice(self.first_name_sample_space, size=1)[0],
            "last_name": np.random.choice(self.last_name_sample_space, size=1)[0],
            "tax_ID": int(np.random.choice(self.tax_ID_sample_space, size=1)[0]),
            "e_mail": np.random.choice(self.e_mail_sample_space, size=1)[0],
            "product": np.random.choice(self.product_sample_space, size=1)[0],
            "quantity": int(np.random.choice(self.quantity_sample_space, size=1)[0]),
            "details": np.random.choice(self.details_sample_space, size=1)[0]
        }


def execute_push_inbound_oracle():
    r""" Sends a transaction to the smart contract which triggers an event, which then
    triggers the pull inbound oracle.
    """
    random_verify_customer_state = RandomVerifyCustomerGenerator().get_random_verify_customer()

    push_inbound_oracle = VerifyCustomerState(
        verify_customer=random_verify_customer_state,
        public_address=config.PUBLIC_ADDRESS, private_address=config.PRIVATE_ADDRESS,
        smart_contract_address=config.CUSTOMER_SMART_CONTRACT_ADDRESS, abi=config.CUSTOMER_ABI,
        web_socket=config.WEB_SOCKET)

    start_timestamp = get_unix_timestamp()

    transaction_hash = web3.eth.to_hex(
        push_inbound_oracle.send_raw_transaction())

    end_timestamp = get_unix_timestamp()

    save_to_mongo(
        db="pullInboundOracle", collection="verifyCustomer", 
        document={
            "transaction_hash": transaction_hash,
            "start_timestamp": start_timestamp, "end_timestamp": end_timestamp,
            "document": random_verify_customer_state})

    print(f'(Verify Customer) Timestamp: {convert_unix_timesamp_to_datetime(get_unix_timestamp())} | Transaction hash: {transaction_hash} |'\
          f'Verify Customer: {random_verify_customer_state}')


def execute_pull_inbound_oracle():
    pull_inbound_oracle = OrderState(
        filter=config.CUSTOMER_TOPIC_ADDRESS_VERIFY_CUSTOMER,
        public_address=config.PUBLIC_ADDRESS, private_address=config.PRIVATE_ADDRESS,
        smart_contract_address=config.CUSTOMER_SMART_CONTRACT_ADDRESS, abi=config.CUSTOMER_ABI,
        web_socket=config.WEB_SOCKET)

    pull_inbound_oracle.listen_to_filter()


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(execute_push_inbound_oracle, "interval", minutes=15)
    scheduler.start()

    execute_push_inbound_oracle()

    return 0


if __name__ == "__main__":
    main()