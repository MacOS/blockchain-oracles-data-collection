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