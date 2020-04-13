import datetime

import numpy as np
import web3
import pymongo


class _Oracle(object):
    r"""
        _Oracle is the base class for all oracles.

        Args:
            smart_contract_address (string): An identifier for a smart contract.
            topics (string): An identifier for a topic.
            web_socket (sting): The websocket to be used. It has to start with wss:://some.web.socket 
    """
    def __init__(self, public_address, private_address, smart_contract_address, web_socket):
        self._public_address = public_address
        self._private_address = private_address
        self._smart_contract_address = smart_contract_address
        self._web_socket = web_socket

        self.web_socket = self.connect_to_websocket()
        self._smart_contract = self.get_smart_contract()

    def connect_to_websocket(self):
        web_socket = web3.Web3(
            web3.WebsocketProvider(self._web_socket))

        if web_socket.isConnected():
            print("Succesfully connected to Websocket!")
            return web_socket
        else:
            raise Exception("Not Connected to Websocket!")

    def get_smart_contract(self):
        return self.web_socket.eth.contract(
            address= web3.Web3.toChecksumAddress(self._smart_contract_address),
            abi=self._abi)


class _EventListeningOracle(_Oracle):
    r"""
        _EventListeningOracle is the base class for all oracles that have to listen to events.

        Args:
            filter (string): An identifier for the topic to be listend to.
    """
    def __init__(self, filter, *args, **kwargs):
        super(_EventListeningOracle, self).__init__(args, kwargs)

        self._filter = filter

        self.subscribed_filter = self.subscribe_to_filter(filter)

    def subscribe_to_filter(self, filter):
        return self.web_socket.eth.eth_subscribe({
            "address": web3.Web3.toChecksumAddress(self._smart_contract_address),
            "topics": [self.web_socket.keccak(text=filter).hex()]
        })

    def listen_to_filter(self):
        print(f"Listening to filter {self._filter} from smart contract {self._smart_contract_address}")
        while True:
            for event in self.eth_filter.get_new_entries():
                print(f"(Loop) New Transaction: {event}")
                self.process_new_event(event)

    def process_new_event(self, new_event):
        raise NotImplementedError("process_new_event is not implemented")


class _TransactionSendingOracle(_Oracle):
    r"""
        _TransactionSendingOracle is the base class for all oracles that have to send a transaction.

        Args:
            abi (string): The application binary interface (ABI) of a smart contract.
    """
    def __init__(self, abi, *args, **kwargs):
        super(_TransactionSendingOracle, self).__init__(*args, **kwargs)

        self._abi = abi

        self.ESTIMATED_GAS_MULTIPLIER = 1.2

    def get_nonce(self):
        r"""
            Returns the nonce of the account _public_address.
        """
        return self.web_socket.eth.getTransactionCount(
            web3.Web3.toChecksumAddress(self._public_address))

    def send_raw_transaction(self):
        estimated_gas = self.estimate_gas(self.state)
        transaction = self.assemble_transaction(self.state, estimated_gas)
        signed_transaction = self.sign_transaction(transaction)
        return self.web_socket.eth.sendRawTransaction(
            signed_transaction.rawTransaction)

    def estimate_gas(self, state):
        return int(self.web_socket.eth.estimateGas({
            'from': web3.Web3.toChecksumAddress(self._public_address),
            'to': web3.Web3.toChecksumAddress(self._smart_contract_address),
            'data': self.encoded_abi}) * self.ESTIMATED_GAS_MULTIPLIER)

    def assemble_transaction(self, state, estimated_gas):
        r"""
            Assembles the transaction into a python dictionary. The returned dictionary is then used by
            send_raw_transaction.

            Args:
                state (dic): The state to be inserted into the blockchain.
                estimated_das (int): The estimated gas of the transaction.
        """
        return {
            'nonce': f'{web3.Web3.toHex(self.get_nonce())}',
            'gasPrice': f'{web3.Web3.toHex(self.web_socket.eth.gasPrice)}',
            'gas': f'{web3.Web3.toHex(estimated_gas)}',
            'to': f'{web3.Web3.toChecksumAddress(self._smart_contract_address)}',
            'data': f'{self.encoded_abi}'
        }

    def sign_transaction(self, transaction):
        r"""
            Signs a transaction with the private_key.
        """
        return self.web_socket.eth.account.sign_transaction(
            transaction, self._private_address)


def save_to_mongo(db, collection, document):
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = my_client.db
    my_collection = my_db.collection
    return my_collection.insert_one(document).inserted_id


class RandomArrivalGenerator(object):

    def __init__(self):
        self.order_sample_space = [
            "iPhone 11 Pro",
            "iPhone 11",
            "iPhone XR",
            "iPhone 8",
            "Samsung Galaxy S10",
            "Samsung Galaxy S10e",
            "Samsung Galaxy S10+",
            "Samsung Galaxy Note10",
            "Samsung Galaxy Note10+",
            "Samsung Galaxy A90 5G",
            "Samsung Galaxy A80 5G",
            "Samsung Galaxy A70 5G",
            "Motorola Moto G7 Plus",
            "Motorola Moto G7",
            "Motorola Moto G7 Power"
        ]

        self.location_sample_space = [
            "Vienna",
            "Minsk",
            "Brussels",
            "Sarajevo",
            "Sofia",
            "Zagreb",
            "Nicosia",
            "Prague",
            "Tallinn",
            "Helsinki",
            "Paris",
            "Tbilsi",
            "Berlin",
            "Athens",
            "Budapest",
            "Reykjavik",
            "Dublin",
            "Rome",
            "Pristina",
            "Riga",
            "Vaduz",
            "Vilnius",
            "Luxembourg",
            "Valletta",
            "Amsterdam",
            "Skopje",
            "Oslo",
            "Warsaw",
            "Lisbon",
            "Bucharest",
            "Moscow",
            "Belgrade",
            "Bratislava",
            "Ljubljana",
            "Madrid",
            "Stockholm",
            "Bern",
            "London"
        ]

    def get_random_arrival(self):
        return  {
            "order": np.random.choice(self.order_sample_space, size=1)[0],
            "location": np.random.choice(self.location_sample_space, size=1)[0],
            "timestamp": get_unix_timestamp()
        }


def get_unix_timestamp():
    return datetime.datetime.now().timestamp()


def convert_unix_timesamp_to_datetime(unix_timesamp):
    return datetime.datetime.fromtimestamp(unix_timesamp)