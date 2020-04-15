PUBLIC_ADDRESS = "0x53c5ad7262273711255468cacd8c2f64499e9aea"
PRIVATE_ADDRESS = "0xcd29914a528e4cb5164dc13c29e15c6e706962ce8d18ad63b53294f488d0f2bb"

WEB_SOCKET = "wss://ropsten.infura.io/ws/v3/2aa2cc2b93984929b4f859479afc4582"

ARRIVAL_SMART_CONTRACT_ADDRESS = "0x1186aedab8f37c08cc00a887dbb119787cfe6aaf"
ARRIVAL_TOPIC_ADDRESS_ARRIVAL = "0xc1fe86cac1c23daaf64a00413ca2282390682e013e4b996f2de93882a046b83b"
ARRIVAL_ABI = '[\
    {\
        "constant": "false",\
        "inputs": [\
            {"name": "_order", "type": "string"},\
            {"name": "_location", "type": "string"},\
            {"name": "_timestamp", "type": "uint256"}\
        ],\
        "name": "setArrival",\
        "outputs": "[]",\
        "payable": "true",\
        "stateMutability": "payable",\
        "type": "function"\
    },\
    {\
        "anonymous": "false",\
        "inputs": [\
            {"indexed": "false", "name": "order", "type": "string"},\
            {"indexed": "false", "name": "location", "type": "string"},\
            {"indexed": "false", "name": "timestamp", "type": "uint256"}\
        ],\
        "name": "Arrival",\
        "type": "event"\
    }\
]'

CUSTOMER_SMART_CONTRACT_ADDRESS = "0x0a4d9d49bd7e4402a8cfba0b6d6c699756b6655d"
CUSTOMER_TOPIC_ADDRESS_VERIFY_CUSTOMER = "0xa1bbd432cddb2824a78d77c36fc1a89f2638f945e5e906ffe3845f0e89b986d9"
CUSTOMER_TOPIC_ADDRESS_ORDER = "0x7837c29267e8fce8adeced6497a825634c13723231bb84f5f2ce266a696b2ff3"
CUSTOMER_TOPIC_ADDRESS_ERROR = "0x38e3aaf1b2f2c930b2c3ad9e7ba74f151a8852833d7f1f4c6a12793fff19c927"
CUSTOMER_ABI = '[\
	{\
		"constant": "false",\
		"inputs": [\
			{ "name": "_isVerified", "type": "bool" },\
			{ "name": "_orderID", "type": "uint256" },\
			{ "name": "_errorCode", "type": "uint256" }\
		],\
		"name": "statusCustomerCredibility",\
		"outputs": "[]",\
		"payable": "true",\
		"stateMutability": "payable",\
		"type": "function"\
	},\
	{\
		"constant": "false",\
		"inputs": [\
			{ "name": "_firstName", "type": "string" },\
			{ "name": "_lastName", "type": "string" },\
			{ "name": "_taxID", "type": "uint256" },\
			{ "name": "_email", "type": "string" },\
			{ "name": "_product", "type": "string" },\
			{ "name": "_quantity", "type": "uint256" },\
			{ "name": "_details", "type": "string" }\
		],\
		"name": "verifyCustomer",\
		"outputs": "[]",\
		"payable": "true",\
		"stateMutability": "payable",\
		"type": "function"\
	},\
	{\
		"anonymous": "false",\
		"inputs": [\
			{ "indexed": "false", "name": "firstName", "type": "string" },\
			{ "indexed": "false", "name": "lastName", "type": "string" },\
			{ "indexed": "false", "name": "taxID", "type": "uint256" },\
			{ "indexed": "false", "name": "email", "type": "string" },\
			{ "indexed": "false", "name": "product", "type": "string" },\
			{ "indexed": "false", "name": "quantity", "type": "uint256" },\
			{ "indexed": "false", "name": "details", "type": "string" }\
		],\
		"name": "VerifyCustomer",\
		"type": "event"\
	},\
	{\
		"anonymous": "false",\
		"inputs": [\
			{ "indexed": "false", "name": "orderID", "type": "uint256" },\
			{ "indexed": "false", "name": "errorCode", "type": "uint256" }\
		],\
		"name": "Error",\
		"type": "event"\
	},\
	{\
		"anonymous": "false",\
		"inputs": [\
			{ "indexed": "false", "name": "orderID", "type": "uint256" }\
		],\
		"name": "Order",\
		"type": "event"\
	}\
]'