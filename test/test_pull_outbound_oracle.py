import unittest

from oracles.pull_outbound_oracle import PullOutboundOracle

from test import utils as config


class TestPushOutboundOracle(unittest.TestCase):

    def setUp(self):
        self.pull_outbound_oracle = PullOutboundOracle(
            public_address=config.PUBLIC_ADDRESS, private_address=config.PRIVATE_ADDRESS,
            smart_contract_address=config.ARRIVAL_SMART_CONTRACT_ADDRESS,
            web_socket=config.WEB_SOCKET,
            abi=config.ARRIVAL_ABI)

    def test_arrival_retrieval(self):
        retrieved_state = self.pull_outbound_oracle.retrieve_state_from_transaction_hash(
            transaction_hash="0xf15753a9ef3d83e6d9974a936795039605449cdf2530545c8b339deaa6a7641f")

        self.assertEqual(retrieved_state[1], {'_order': 'iPhone 11', '_location': 'Zagreb', '_timestamp': 1586791367})