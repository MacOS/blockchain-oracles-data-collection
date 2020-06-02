/**
    This script implements the on-chain component of the pull in-bound oracle as described in Mühlberger for evalution purposes.

    A pull in-bound oracle is a software artifact that writes data to the blockchain (in-bound) triggered
    by an on-chain event (pull).

    Author: Roman Mühlberger, Stefan Bachhofner

    Mühlberger, R. (2019). Integration of the real world to the blockchain via in-bound and outbound oracles (Unpublished Master thesis).
    Department of Information Systems and Operations, Vienna University of Economics and Business, Vienna, Austria.
 */

pragma solidity ^0.4.21;


contract Customer {

   string firstName;
   string lastName;
   uint taxID;
   string email;
   string product;
   uint quantity;
   string details;

   event VerifyCustomer(
        string firstName,
        string lastName,
        uint taxID,
        string email,
        string product,
        uint quantity,
        string details
    );

    event Error(
        uint orderID,
        uint errorCode
    );

    event Order(
        uint orderID
    );


    function verifyCustomer(string _firstName, string _lastName, uint _taxID, string _email, string _product, uint _quantity, string _details) public payable{
        // Reqeust to verify customer liquidity. This here is, of course, simulated and has to be triggered
	// somehow. We use a push inbound oracle for that purpose.
	emit VerifyCustomer(_firstName, _lastName, _taxID, _email, _product, _quantity, _details);
    }

    function statusCustomerCredibility(bool _isVerified, uint _orderID, uint _errorCode) public payable {
        // Receives the inbound state.
	if(_isVerified) {
            emit Order(_orderID);
        } else {
            emit Error(_orderID, _errorCode);
        }
    }
}
