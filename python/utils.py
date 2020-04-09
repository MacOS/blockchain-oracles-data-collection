import web3


class Oracle(object):

    def __init__(self, smart_contract_address, topics, web_socket):
        self._smart_contract_address = smart_contract_address
        self._topics = topics
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


class EventListeningOracle(Oracle):

    def __init__(self, filter, *args, **kwargs):
        super(self, EventListeningOracle).__init__(args, kwargs)

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


class TransactionSendingOracle(Oracle):

    def __init__(self, *args, **kwargs):
        super(self, TransactionSendingOracle).__init__(args, kwargs)

    def send_raw_transaction(self, state):
        raise NotImplementedError("send raw transaction not implemented")

    def estimate_gas(self, state):
        raise NotImplementedError("estimate gas not implemented")

    def assemble_transaction(self, state, estimated_gas):
        raise NotImplementedError("assemble transaction not implemented")

    def sign_transaction(self, transaction):
        raise NotImplementedError("sign transaction not implemented")