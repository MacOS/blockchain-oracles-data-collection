import QRReader from './vendor/qrscan.js';
import { snackbar } from './snackbar.js';
import styles from '../css/styles.css';
import isURL from 'is-url';
//Web3 added
let Web3 = require ('web3');
var web3 = new Web3(new Web3.providers.WebsocketProvider("ws://127.0.0.1:8545"));
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

  //save result in Blockchain
  function sendToBlockchain(resultText) {
    let contract = '';
    let count;
    var address = "0x580f06fe89c1add98207a0fa9e192cae7fda1b82";
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
    var account = "0x4ddd105c39099f4e962073c4871ef06fab4bfa03"; //"<REDACTED ACCOUNT ADDRESS>";
    //var privateKey = "a11a71bd713bbb32261d40601422ce538f10789680a6e521d0b2a6017a159d61"; //"<REDACTED PRIVATE KEY WITHOUT 0x PREFIX>";
   const privateKey = Buffer.from('fa6e030f514d24b3fecfb9340ee482a578a0c0ccab2911accf7ca93a836172cf', 'hex');
     contract = new web3.eth.Contract(abi, address);

  web3.eth.getTransactionCount(account).then(function(v) {
      console.log(resultText);
      console.log(timestamp);
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
      let rawTransaction = {"from": account, "gasPrice": web3.utils.toHex(gasPrice), "gasLimit": web3.utils.toHex(gasLimit), "to": address, "data": data, "nonce": web3.utils.toHex(count)}
      console.log(rawTransaction);
      let transaction = new EthereumTx(rawTransaction);
      transaction.sign(privateKey);
      let rawTx = '0x'+transaction.serialize().toString('hex');
      console.log(rawTx);
      console.log(txDecoder.decodeTx(rawTx));
      web3.eth.sendSignedTransaction(rawTx, function(err, hash) {

          if(!err) {
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
