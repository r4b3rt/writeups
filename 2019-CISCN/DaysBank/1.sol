pragma solidity ^0.4.24;

contract DaysBank {
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public gift;
    address owner;

    constructor()public{
        owner = msg.sender;
    }
    
    function func_01DC() {
        require(gift[msg.sender] == 0);
    
        balanceOf[msg.sender] += 1;
        gift[msg.sender] = 1;
    }
    
    function profit() {
        require(balanceOf[msg.sender] == 1);
        require(gift[msg.sender] == 1);
    
        balanceOf[msg.sender] += 1;
        gift[msg.sender] = 2;
    }
    
    event SendFlag(uint256 flagnum, string b64email);
    function payforflag(string b64email) public {
        require(balanceOf[msg.sender] >= 10000);
        emit SendFlag(1, b64email);
    }
    
    function transfer2(address account, uint value) {
        require(value > 2);
        require(balanceOf[msg.sender] > 2);
        require(balanceOf[msg.sender] - value > 0);
    
        balanceOf[msg.sender] -= value;
        balanceOf[account] += value;
    }
    
    function transfer(address account, uint value) {
        require(value > 1);
        require(balanceOf[msg.sender] > 1);
        require(balanceOf[msg.sender] > value);
    
        balanceOf[msg.sender] -= value;
        balanceOf[account] += value;
    }
}
