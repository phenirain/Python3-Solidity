// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.4.16 <0.9.0;

contract MyEstate {
    enum typeOfEstate {
        house,
        flat,
        loft
    }

    enum AdvStatus {
        Opened,
        Closed
    }

    struct Estate {
        uint size;
        string estateAddress;
        address owner;
        typeOfEstate estateType;
        bool isActive;
        uint id;
    }

    struct Advertisement {
        address seller;
        address buyer;
        uint sum;
        uint estateId;
        uint date;
        AdvStatus isOpen; 
        uint id;
    }

    uint estateCounter = 0;
    uint advCounter = 0;
    mapping(uint => Estate) estates;
    mapping(uint => Advertisement) advs;
    mapping(uint => uint) advIds;
    mapping(address => uint) balances;
    mapping(address => uint[]) estatesOwners; 

    // estates[i].owner == address(0) - check null address

    event estateCreated(address owner, uint id, uint date, typeOfEstate estateType);
    event advCreated(address owner, uint estateId, uint id, uint date, uint sum);
    event estateStatusChanged(address owner, uint estateId, uint advId, uint date, bool isOpen);
    event advStatusChanged(address owner, uint estateId, uint date, bool isActive);
    event fundsBack(address to, uint sum, uint date);
    event estatePurchased(address owner, address buyer, uint advId, uint estateId, AdvStatus isOpen, uint date, uint sum);
    event Deposit(address indexed _from, uint _amount);


    modifier enoughMoney(uint value, uint price) {
        require(value >= price, "You don`t have enougn money");
        _;
    }

    modifier estateExist(uint estateId) {
        require(estates[estateId].owner != address(0), "No one estates has this id");
        _;
    }

    modifier advExist(uint advId) {
        require(advIds[advId] != 0, "No one advertisements has this id");
        _;
    }

    modifier onlyEstateOwner(uint idEstate) {
        require(estates[idEstate].owner == msg.sender, "You are not estate`s owner");
        _;
    }
    modifier onlyAdvOwner(uint idEstate) {
        require(advs[idEstate].seller == msg.sender, "You are not advertisement`s owner");
        _;
    }
    modifier isActiveEstate(uint idEstate) {
        require(estates[idEstate].isActive, "This estate unavailable");
        _;
    }
    modifier isOpenAdv(uint idEstate) {
        require(advs[idEstate].isOpen == AdvStatus.Opened, "This advertisement closed");
        _;
    }

    function createEstate(uint size, string memory estateAddress, uint estateType) public {
        require(size >= 1, "Size must be larger than 0");
        estateCounter++;
        estates[estateCounter] = Estate(size, estateAddress, msg.sender, typeOfEstate(estateType), true, estateCounter);
        emit estateCreated(msg.sender, estateCounter, block.timestamp, typeOfEstate(estateType));
    }
    function createAdv(uint estateId, uint sum) public estateExist(estateId) onlyEstateOwner(estateId) isActiveEstate(estateId) {
        require(sum > 0, "Sum must be more than 0");
        advCounter++;
        advs[estateId] =  Advertisement(msg.sender, address(0), sum, estateId, block.timestamp, AdvStatus.Opened, advCounter);
        advIds[advCounter] = estateId;
        emit advCreated(msg.sender, estateId, advCounter, block.timestamp, sum);
    }
    function changeStatusOfEstate(uint estateId) public estateExist(estateId) onlyEstateOwner(estateId) isActiveEstate(estateId) {
        estates[estateId].isActive = false;
        uint advId = 0;
        if (advs[estateId].seller != address(0)) {
            advId = advs[estateId].id;
            advs[estateId].isOpen = AdvStatus.Closed;
            emit advStatusChanged(advs[estateId].seller, estateId, block.timestamp, false);
        }
        emit estateStatusChanged(msg.sender, estateId, advId, block.timestamp, false);
    }
    function changeStatusOfAdv(uint advId) public advExist(advId) onlyEstateOwner(advIds[advId]) isActiveEstate(advIds[advId]) {
        uint estateId = advIds[advId];
        advs[estateId].isOpen = AdvStatus.Closed;
        emit advStatusChanged(advs[estateId].seller, estateId, block.timestamp, false);
    }

    function deposit() external payable  {
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint amount) public payable enoughMoney(balances[msg.sender], amount){
        require(amount <= balances[msg.sender] || amount > 0, "Not enough maoney to withdraw(");
        payable(msg.sender).transfer(amount);
        balances[msg.sender] -= amount;
        emit fundsBack(msg.sender, amount, block.timestamp);
    }

     function getBalance() external view returns(uint){
        return balances[msg.sender];
    }

    function buyEstate(uint advId) public payable advExist(advId) enoughMoney(balances[msg.sender], advs[advIds[advId]].sum) isOpenAdv(advIds[advId]){
        uint estateId = advIds[advId];
        require(estates[estateId].owner != msg.sender, "You already own the estate");
        advs[estateId].isOpen = AdvStatus.Closed;
        estatesOwners[msg.sender].push(estateId);
        uint price = advs[estateId].sum;
        balances[msg.sender] -= price;
        emit estatePurchased(advs[estateId].seller, msg.sender, advId, estateId, AdvStatus.Closed, block.timestamp, price);
    }

    function getEstates() public view returns(Estate[] memory) {
        Estate[] memory ests = new Estate[](estateCounter - 1);
        for (uint i = 1;i < estateCounter; i++) {
            ests[i - 1] = estates[i];
        }
        return ests;
    }

    function getAdvs() public view returns(Advertisement[] memory) {
        Advertisement[] memory advertisements = new Advertisement[](advCounter - 1);
        for (uint i = 1;i < advCounter; i++) {
            advertisements[i - 1] = advs[advIds[i]];
        }
        return advertisements;
    }

    function getMyEstates() public view returns(uint[] memory) {
        return estatesOwners[msg.sender];
    }
}