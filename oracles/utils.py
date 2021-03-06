r"""this file contains the logic that is either separated out of the oracles (i.e. separation of concerns), 
and helper functions.
"""
import datetime
import time


import numpy as np
import web3
import pymongo



class _Oracle(object):
    r"""
        _Oracle is the base class for all oracles.

        Args:
	    public_address (string): The public key of an account.
	    private_address (string): The private key of an account.
	    abi (string): The application binary interface (abi) for the provided <smart_contract_address>
	    smart_contract_address (string): An identifier for a smart contract.
	    web_socket (sting): The websocket of a blockchain node. It has to start with wss:://some.web.socket 
    """
    def __init__(self, public_address, private_address, abi, smart_contract_address, web_socket):
        self._public_address = public_address
        self._private_address = private_address
        self._smart_contract_address = smart_contract_address
        self._abi = abi
        self._web_socket = web_socket

        self.web_socket = self.connect_to_websocket()
        self._smart_contract = self.get_smart_contract()

    def connect_to_websocket(self):
        r"""Connects to the provided websocket. Raises an exception if a connection failed.
	"""
	web_socket = web3.Web3(
            web3.WebsocketProvider(self._web_socket))

        if web_socket.isConnected():
            print("Succesfully connected to Websocket!")
            return web_socket
        else:
            raise Exception("Not Connected to Websocket!")

    def get_smart_contract(self):
        r"""Resturns the smart contract such that it can be used to interact with.
	"""
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
        super(_EventListeningOracle, self).__init__(*args, **kwargs)

        self._filter = filter

        self.eth_filter = self.subscribe_to_filter(filter)

    def subscribe_to_filter(self, filter):
        r"""Subscribes to the provider filter. This is used to catch recorded blockchain events as 
		soon as they occur.
		"""
	return self.web_socket.eth.filter({
                    "address": web3.Web3.toChecksumAddress(self._smart_contract_address),
		    "topics": [filter]})

    def listen_to_filter(self):
        r"""Listens to <_filter> in an infinite loop. There is currently no way to terminate this loop!
        A new event is processed by the method process_new_event.
        """
        print(f"Listening to filter {self._filter} from smart contract {self._smart_contract_address}")
        while True:
            for event in self.eth_filter.get_new_entries():
                print(f"(Loop) New Transaction: {event}")
                self.process_new_event(event)

    def process_new_event(self, new_event):
        r"""The processing logic for a newly catched event. Child classes have to to implement this method.
        """
        raise NotImplementedError("process_new_event is not implemented")


class _TransactionSendingOracle(_Oracle):
    r"""
        _TransactionSendingOracle is the base class for all oracles that have to send a transaction.

        Args:
            abi (string): The application binary interface (ABI) of a smart contract.
    """
    def __init__(self, *args, **kwargs):
        super(_TransactionSendingOracle, self).__init__(*args, **kwargs)
        
        # This constant is derived from the ethereum developer community and from experience.
        # Generally, this value can be between 1.2 and 1.5. However, 1.2 worked seamlessly.
        self.ESTIMATED_GAS_MULTIPLIER = 1.2

    def get_nonce(self):
        r"""
            Returns the nonce of the account _public_address.
        """
        return self.web_socket.eth.getTransactionCount(
            web3.Web3.toChecksumAddress(self._public_address))

    def send_raw_transaction(self):
        r"""Sends a state to the specified smart contract via a transaction.
        """
        estimated_gas = self.estimate_gas(self.state)
        transaction = self.assemble_transaction(self.state, estimated_gas)
        signed_transaction = self.sign_transaction(transaction)
        return self.web_socket.eth.sendRawTransaction(
            signed_transaction.rawTransaction)

    def estimate_gas(self, state):
        r"""Estimates the amount of gas that is necessary for the transaction to be processed. 
        """ 
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


class RandomArrivalGenerator(object):
    r"""Help class that generates random arrival states.

    It is primarely intendet use is for the push inbound oracle.
    """
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
    r"""A wrapper function to get the current timestamp.
    """
    return datetime.datetime.now().timestamp()


def convert_unix_timestamp_to_datetime(unix_timestamp):
    r"""A wrapper function to transfrom a unix_timestamp into a dattime object.
    """
    return datetime.datetime.fromtimestamp(unix_timestamp)


def save_to_mongo(db, collection, document):
    r"""Helper function to persistently save documents. This is used to save catched events, generated
    states and the like.

    Args:
        db (string): The database where <document> should be stored.
        collection (string): The collection within <database> where the <document> should be stored.
        document (dict): The document as a dict.
    """
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = my_client[db]
    my_collection = my_db[collection]
    return my_collection.insert_one(document).inserted_id
