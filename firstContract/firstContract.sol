contract MyShop {
    mapping(address => uint) balances;

    event Deposit(address indexed _from, uint _amount);


    function deposit() external payable  {
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function getBalance() external view returns(uint){
        return balances[msg.sender];
    }

    function withdraw(uint _amount) external payable {
        require(_amount <= balances[msg.sender] || _amount > 0, "Not enough maoney to withdraw(");
        payable(msg.sender).transfer(_amount);
        balances[msg.sender] -= _amount;
    }
}