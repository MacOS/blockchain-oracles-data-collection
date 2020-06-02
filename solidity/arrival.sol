/**
    This script implements the on-chain component of the push in-bound oracle as described in Mühlberger for evalution purposes.

    A push inbound oracle is a software artifact that writes data to the blockchain (in-bound) triggered
    by an off-chain event (pull).

    It is used to evalute the push inbound oracle, push outbound oracle, and the pull outbound oracle.

    Author: Roman Mühlberger, Stefan Bachhofner

    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.

    Mühlberger, R., Di Ciccio, C., Castello Ferrer, E., Bachhofner, S., and Weber, I. (2020) Foundational
    Oracle Patterns. Business Process Management: Blockchain Forum.
**/



pragma solidity ^0.4.21;


contract Arrival {

   string order;
   string location;
   uint timestamp;

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
