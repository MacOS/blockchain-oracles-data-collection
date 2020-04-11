import web3


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
        self._public_address = private_address
        self._smart_contract_address = smart_contract_address
        self._web_socket = web_socket

        self.web_socket = self.connect_to_websocket()

    def connect_to_websocket(self):
        web_socket = web3.Web3(
            web3.WebsocketProvider(self._web_socket))

        if web_socket.isConnected():
            print("Succesfully connected to Websocket!")
            return web_socket
        else:
            raise Exception("Not Connected to Websocket!")


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

    def subscribe_to_filters(self, filter):
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

        self._smart_contract = self.get_smart_contract()

    def get_smart_contract(self):
        return self.web_socket.eth.contract(
            address= web3.Web3.toChecksumAddress(self._smart_contract_address),
            abi=self._abi
        )

    def get_nonce(self):
        r"""
            Returns the nonce of the account _public_address.
        """
        return self._web_socket.eth.getTransactionCount(
            web3.Web3.toChecksumAddress(self._public_address))

    def send_raw_transaction(self, state):
        raise NotImplementedError("send raw transaction not implemented")

    def estimate_gas(self, state):
        return self._web_socket.eth.estimateGas({
            'from': web3.Web3.toChecksumAddress(self.public_key),
            'to': web3.Web3.toChecksumAddress(self.smart_contract_address),
            'data': self.encoded_abi
        })

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
            'gasPrice': f'{web3.Web3.toHex(self._web_socket.eth.gasPrice)}',
            'gas': f'{web.Web3.toHex(estimated_gas)}',
            'to': f'{web3.Web3.toChecksumAddress(self._smart_contract_address)}',
            'data': f'{self.encoded_abi}'
        }

    def sign_transaction(self, transaction):
        r"""
            Signs a transaction with the private_key.
        """
        return self._web_socket.eth.account.sign_transaction(
            transaction, self._private_key)