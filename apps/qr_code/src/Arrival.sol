pragma solidity ^0.4.21;


contract Arrival {
   //Contract for QR code scans

   string order;
   string location;
   uint timestamp;


   //event with details scanned by the QR Code web application
   event Arrival(
      string order,
      string location,
      uint timestamp
    );


   //function to emit the information from the QR code
   function setArrival(string _order, string _location, uint _timestamp) public payable{
      order = _order;
      location = _location;
      timestamp = _timestamp;

      emit Arrival(_order, _location, _timestamp);
   }
}