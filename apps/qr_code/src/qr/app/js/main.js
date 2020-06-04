import QRReader from './vendor/qrscan.js';
import { snackbar } from './snackbar.js';
import styles from '../css/styles.css';
import isURL from 'is-url';
//Web3 added
let Web3 = require ('web3');
 
var web3 = new Web3(new Web3.providers.WebsocketProvider("")); //ADD WEBSOCKET PROVIDER 
var txDecoder = require('ethereum-tx-decoder');
const EthereumTx = require('ethereumjs-tx');
var sha256 = require('js-sha256');

//If service worker is installed, show offline usage notification
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/service-worker.js')
      .then(reg => {
        console.log('SW registered: ', reg);
        if (!localStorage.getItem('offline')) {
          localStorage.setItem('offline', true);
          snackbar.show('App is ready for offline usage.', 5000);
        }
      })
      .catch(regError => {
        console.log('SW registration failed: ', regError);
      });
  });
}

window.addEventListener('DOMContentLoaded', () => {
  //To check the device and add iOS support
  window.iOS = ['iPad', 'iPhone', 'iPod'].indexOf(navigator.platform) >= 0;
  window.isMediaStreamAPISupported = navigator && navigator.mediaDevices && 'enumerateDevices' in navigator.mediaDevices;
  window.noCameraPermission = false;

  var copiedText = null;
  var frame = null;
  var selectPhotoBtn = document.querySelector('.app__select-photos');
  var dialogElement = document.querySelector('.app__dialog');
  var dialogOverlayElement = document.querySelector('.app__dialog-overlay');
  var dialogOpenBtnElement = document.querySelector('.app__dialog-open');
  var dialogCloseBtnElement = document.querySelector('.app__dialog-close');
  var scanningEle = document.querySelector('.custom-scanner');
  var textBoxEle = document.querySelector('#result');
  var helpTextEle = document.querySelector('.app__help-text');
  var infoSvg = document.querySelector('.app__header-icon svg');
  var videoElement = document.querySelector('video');
  window.appOverlay = document.querySelector('.app__overlay');

  //Initializing qr scanner
  window.addEventListener('load', event => {
    QRReader.init(); //To initialize QR Scanner
    // Set camera overlay size
    setTimeout(() => {
      setCameraOverlay();
      if (window.isMediaStreamAPISupported) {
        scan();
      }
    }, 1000);

    // To support other browsers who dont have mediaStreamAPI
    selectFromPhoto();
  });

  function setCameraOverlay() {
    window.appOverlay.style.borderStyle = 'solid';
  }

  function createFrame() {
    frame = document.createElement('img');
    frame.src = '';
    frame.id = 'frame';
  }

  //Dialog close btn event
  dialogCloseBtnElement.addEventListener('click', hideDialog, false);
  dialogOpenBtnElement.addEventListener('click', openInBrowser, false);

  //To open result in browser
  function openInBrowser() {
    console.log('Result: ', copiedText);
    window.open(copiedText, '_blank', 'toolbar=0,location=0,menubar=0');
    copiedText = null;
    hideDialog();
  }

  //Scan
  function scan(forSelectedPhotos = false) {
    if (window.isMediaStreamAPISupported && !window.noCameraPermission) {
      scanningEle.style.display = 'block';
    }

    if (forSelectedPhotos) {
      scanningEle.style.display = 'block';
    }

    QRReader.scan(result => {
      copiedText = result;
      textBoxEle.value = result;
      textBoxEle.select();
      scanningEle.style.display = 'none';
      if (isURL(result)) {
        dialogOpenBtnElement.style.display = 'inline-block';
      }
      dialogElement.classList.remove('app__dialog--hide');
      dialogOverlayElement.classList.remove('app__dialog--hide');
      const frame = document.querySelector('#frame');
      // if (forSelectedPhotos && frame) frame.remove();
      sendToBlockchain(copiedText);
    }, forSelectedPhotos);
  }

  //SEND TO BLOCKCHAIN: PUSH-BASED
  function sendToBlockchain(resultText) {
    let contract = '';
    let count;
    var address = ""; //ADD ADDRESS OF SMART CONTRACT
    //ADD ABI
    var abi = [
  	{
  		"constant": false,
  		"inputs": [
  			{
  				"name": "_order",
  				"type": "string"
  			},
  			{
  				"name": "_location",
  				"type": "string"
  			},
  			{
  				"name": "_timestamp",
  				"type": "uint256"
  			}
  		],
  		"name": "setArrival",
  		"outputs": [],
  		"payable": true,
  		"stateMutability": "payable",
  		"type": "function"
  	},
  	{
  		"anonymous": false,
  		"inputs": [
  			{
  				"indexed": false,
  				"name": "order",
  				"type": "string"
  			},
  			{
  				"indexed": false,
  				"name": "location",
  				"type": "string"
  			},
  			{
  				"indexed": false,
  				"name": "timestamp",
  				"type": "uint256"
  			}
  		],
  		"name": "Arrival",
  		"type": "event"
  	}
  ];
  var timestamp = new Date().getTime();
  var location = 'Port 5, Dubai, UAE';
    var account = ""; //"<REDACTED ACCOUNT ADDRESS>"; // ADD ACCOUNT ADDRESS
    //var privateKey = ""; //"<REDACTED PRIVATE KEY WITHOUT 0x PREFIX>"; //ADD PRIVATE KEY
   const privateKey = Buffer.from('fa6e030f514d24b3fecfb9340ee482a578a0c0ccab2911accf7ca93a836172cf', 'hex'); //ADD PRIVATE KEY
     contract = new web3.eth.Contract(abi, address);

  
  web3.eth.getTransactionCount(account).then(function(v) {
      count = v;
      let data = contract.methods.setArrival(resultText, location, timestamp).encodeABI();
      console.log(data);
      let gasPrice = web3.utils.toHex(21000);
      let gasLimit = web3.utils.toHex(600000);

      let result = web3.eth.estimateGas({
          from: account,
          data: data,
          nonce: count,
          to: address
      });
      //VUILD RAW TRANSACTION
      let rawTransaction = {"from": account, "gasPrice": web3.utils.toHex(gasPrice), "gasLimit": web3.utils.toHex(gasLimit), "to": address, "data": data, "nonce": web3.utils.toHex(count)}
      let transaction = new EthereumTx(rawTransaction);
      //SIGN TRANSACTION
      transaction.sign(privateKey);
      let rawTx = '0x'+transaction.serialize().toString('hex');
      //SEND SIGNED TRANSACTION
      web3.eth.sendSignedTransaction(rawTx, function(err, hash) {

          if(!err) {
            //DISPLAY HASH IF TRANSACTION WAS SUCCESSFUL
              console.log("Tx broadcasted: "+hash);

          }else {
              console.log('Transaction failed');
          }
      });
  });
  }

  //Hide dialog
  function hideDialog() {
    copiedText = null;
    textBoxEle.value = '';

    if (!window.isMediaStreamAPISupported) {
      frame.src = '';
      frame.className = '';
    }

    dialogElement.classList.add('app__dialog--hide');
    dialogOverlayElement.classList.add('app__dialog--hide');
    scan();
  }

  function selectFromPhoto() {
    //Creating the camera element
    var camera = document.createElement('input');
    camera.setAttribute('type', 'file');
    camera.setAttribute('capture', 'camera');
    camera.id = 'camera';
    window.appOverlay.style.borderStyle = '';
    selectPhotoBtn.style.display = 'block';
    createFrame();

    //Add the camera and img element to DOM
    var pageContentElement = document.querySelector('.app__layout-content');
    pageContentElement.appendChild(camera);
    pageContentElement.appendChild(frame);

    //Click of camera fab icon
    selectPhotoBtn.addEventListener('click', () => {
      scanningEle.style.display = 'none';
      document.querySelector('#camera').click();
    });

    //On camera change
    camera.addEventListener('change', event => {
      if (event.target && event.target.files.length > 0) {
        frame.className = 'app__overlay';
        frame.src = URL.createObjectURL(event.target.files[0]);
        if (!window.noCameraPermission) scanningEle.style.display = 'block';
        window.appOverlay.style.borderColor = 'rgb(62, 78, 184)';
        scan(true);
      }
    });
  }
});
