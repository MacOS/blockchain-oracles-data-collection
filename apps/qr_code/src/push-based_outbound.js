let Web3 = require ('web3');
var sha256 = require('js-sha256');
const InputDataDecoder = require('ethereum-input-data-decoder');
var txDecoder = require('ethereum-tx-decoder');
const EthereumTx = require('ethereumjs-tx');
const nodemailer = require("nodemailer");


var web3 = new Web3(new Web3.providers.WebsocketProvider("ws://127.0.0.1:8545"));
const decoder = new InputDataDecoder('./abi.json');

var trxData = "";
var inputData = "";
var globalID;

//Subscription to the Event. Please provide the smart Contract address to the field "address" and the topics from the field Topics in the output log from Remix


const subscription = web3.eth.subscribe('logs', {
    address: '0x580f06fe89c1add98207a0fa9e192cae7fda1b82',
    topics: ['0xc1fe86cac1c23daaf64a00413ca2282390682e013e4b996f2de93882a046b83b']
}, function(error, result){
    if(error) console.log(error);
    if (!error) { 
    }
}).on("data", (log) => {
    trxData = log.data;
    console.log(trxData);
    main(trxData);

})
.on("changed", (log) => {
    trxData = log.data;
})
//this function is called upon successful receipt of data and decodes the parameters of string and uint values 

function main (trxData) {
    let hx = '';
    let subscription1 = '';


    if(trxData) {
        console.log(trxData);
    }else {
        console.log("TrxData failed");
    }

    //parameter decoding and save output into r
    const r = web3.eth.abi.decodeParameters([ 'string', 'string', 'uint'], trxData);
    console.log(r);
    var order = r[0];
    var location = r[1];
    var time = r[2];

    //MongoDB client should be running 
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/qrcode";


    //Insert new document into MongoDB
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("qrcode");
        //insert an ID 
        var id = dbo.collection("qrcode").count() + 1;
        var myobj = { ID: id, order: order, location: location, time: time};
        dbo.collection("qrcode").insertOne(myobj, function(err, res) {
            if (err) throw err;
            console.log("1 document inserted");
            db.close();
        });
    }); 
}