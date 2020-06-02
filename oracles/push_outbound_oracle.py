'''
    This file implements the push out-bound oracles described in

    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.

    for evalution purposes in the following submitted (not yet peer reviewed!) paper

    Mühlberger, R., Di Ciccio, C., Castello Ferrer, E., Bachhofner, S., and Weber, I. (2020) Foundational
    Oracle Patterns. Business Process Management: Blockchain Forum.

    A push out-bound oracle is a software artifact that retrieves data from the blockchain (out-bound) triggered
    by an on-chain event (push).

    Author: Stefan Bachhofner, Roman Mühlberger
'''
from utils import _EventListeningOracle, save_to_mongo, get_unix_timestamp
import config



class PushOutboundOracle(_EventListeningOracle):
    r"""Implements the logic for the PushOutboundOracle.
    """
    def __init__(self, *args, **kwargs):
        super(PushOutboundOracle, self).__init__(*args, **kwargs)

    def process_new_event(self, new_event):
        received_timestamp = get_unix_timestamp()
        save_to_mongo(
            db="pushOutboundOracle", collection="arrival",
            document={"received_timestamp": received_timestamp, "event": new_event})


def push_outbound_oracle():
    r"""Warpps the PushOutboundOracle such that it enters its infinite loop.
    """
    push_outbound_oracle = PushOutboundOracle(
        public_address=config.PUBLIC_ADDRESS,
        private_address=config.PRIVATE_ADDRESS,
        web_socket=config.WEB_SOCKET,
        smart_contract_address=config.ARRIVAL_SMART_CONTRACT_ADDRESS,
        abi=config.ARRIVAL_ABI,
        filter=config.ARRIVAL_TOPIC_ADDRESS_ARRIVAL)

    push_outbound_oracle.listen_to_filter()


def main():
    push_outbound_oracle()


if __name__ == "__main__":
    main()
