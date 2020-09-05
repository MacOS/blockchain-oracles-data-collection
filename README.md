# Foundational Oracle Patterns: Connecting Blockchain to the Off-chain World
This GitHub repository contains code, which was used for the following paper:
Roman Mühlberger, Stefan Bachhofner, Eduardo Castello Ferrer, Claudio Di Ciccio, Ingo Weber, Maximilian Wöhrer, and Uwe Zdun (2020): 
Foundational Oracle Patterns:Connecting Blockchain to the Off-chain World. International Conference on Business Process Management. 

```
@InProceedings{10.1007/978-3-030-58779-6_3,
author="M{\"u}hlberger, Roman
and Bachhofner, Stefan
and Castell{\'o} Ferrer, Eduardo
and Di Ciccio, Claudio
and Weber, Ingo
and W{\"o}hrer, Maximilian
and Zdun, Uwe",
editor="Asatiani, Aleksandre
and Garc{\'i}a, Jos{\'e} Mar{\'i}a
and Helander, Nina
and Jim{\'e}nez-Ram{\'i}rez, Andr{\'e}s
and Koschmider, Agnes
and Mendling, Jan
and Meroni, Giovanni
and Reijers, Hajo A.",
title="Foundational Oracle Patterns: Connecting Blockchain to the Off-Chain World",
booktitle="Business Process Management: Blockchain and Robotic Process Automation Forum",
year="2020",
publisher="Springer International Publishing",
address="Cham",
pages="35--51",
abstract="Blockchain has evolved into a platform for decentralized applications, with beneficial properties like high integrity, transparency, and resilience against censorship and tampering. However, blockchains are closed-world systems which do not have access to external state. To overcome this limitation, oracles have been introduced in various forms and for different purposes. However so far common oracle best practices have not been dissected, classified, and studied in their fundamental aspects. In this paper, we address this gap by studying foundational blockchain oracle patterns in two foundational dimensions characterising the oracles: (i) the data flow direction, i.e., inbound and outbound data flow, from the viewpoint of the blockchain; and (ii) the initiator of the data flow, i.e., whether it is push or pull-based communication. We provide a structured description of the four patterns in detail, and discuss an implementation of these patterns based on use cases. On this basis we conduct a quantitative analysis, which results in the insight that the four different patterns are characterized by distinct performance and costs profiles.",
isbn="978-3-030-58779-6"
}
```


# Directory Explanations
[apps](https://github.com/MacOS/blockchain-oracles-data-collection/tree/master/apps)

Contains the QR code application as described in the paper.

[evaluation](https://github.com/MacOS/blockchain-oracles-data-collection/tree/master/evaluation)

Contains python and R scripts, which were used to analyse the collected data from the communication between oracles and the blockchain.

[oracles](https://github.com/MacOS/blockchain-oracles-data-collection/tree/master/oracles)

Contains python code for the oracles as described in the paper. However, the code in this direcotry
is one particular (centralized and Ethereum-tailored) implementation of the proposed oracle patterns, and are therefore by no means the only way how they can be implemented.

[solidity](https://github.com/MacOS/blockchain-oracles-data-collection/tree/master/solidity)

Contains the solidity code for the two smart contracts "arrival" and "customer".

[test](https://github.com/MacOS/blockchain-oracles-data-collection/tree/master/test)

Contains some tests for the code in the _oracles_ directory.


# Authors
[Roman Mühlberber, MSc. (WU), Vienna University of Economics and Business](https://scholar.google.at/citations?user=aQVmc18AAAAJ&oi=ao)

[Claudio Di Ciccio, PhD, Sapienza University of Rome](http://diciccio.net/)

[Eduardo Castello Ferrer, PhD, Massachusetts Institute of Technology](https://scholar.google.at/citations?hl=de&user=D1eifv4AAAAJ)

[Stefan Bachhofner, BSc. (WU), Vienna University of Economics and Business](https://scholar.google.at/citations?user=-WZ0YuUAAAAJ)

[Univ. Prof. Dr. Ingo Weber, Chair of Software and Business Engineering, Technische Universitaet Berlin](https://scholar.google.at/citations?user=uZP6cXwAAAAJ)

[Dipl.-Ing. Bakk. (FH) Maximilian Wöhrer, University of Vienna](https://scholar.google.at/citations?user=cLtHNX0AAAAJ)

[Univ. Prof. Dr. Uwe Zdun, University of Vienna](https://scholar.google.at/citations?user=jLm9DCkAAAAJ)

# Links 
[Ethereum price history API?](https://www.reddit.com/r/ethereum/comments/6xbwxp/ethereum_price_history_api/)
