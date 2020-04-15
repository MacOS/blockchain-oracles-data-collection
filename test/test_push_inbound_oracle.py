import unittest

from oracles import PushInboundOracle, ArrivalState
from oracles.utils import _TransactionSendingOracle

from test import utils


class TestPushInboundOracle(unittest.TestCase):

    def setUp(self):
        self.push_inbound_oracle = ArrivalState(
            public_address=utils.PUBLIC_ADDRESS,
            private_address=utils.PRIVATE_ADDRESS,
            smart_contract_address=utils.ARRIVAL_SMART_CONTRACT_ADDRESS,
            web_socket=utils.WEB_SOCKET,
            abi=utils.ARRIVAL_ABI,
            arrival={"order": "iPhone Phantasy Test", "location": "Neverlend", "timestamp": 1586632028.655743})

    def test_push_inbound_oracle(self):
        self.assertEqual(issubclass(PushInboundOracle, _TransactionSendingOracle), True)

    def test_arrival_state(self):
        self.assertEqual(issubclass(ArrivalState, PushInboundOracle), True)

    def test_arrival_state_transaction_sending(self):
        transaction_hash = self.push_inbound_oracle.send_raw_transaction()
        print(transaction_hash)


if __name__ == "__main__":
    unittest.main()