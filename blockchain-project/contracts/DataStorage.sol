pragma solidity ^0.8.20;

contract DataStorage {
    struct DataRecord {
        uint256 id;
        string data;
        address creator;
        uint256 timestamp;
        bool isActive;
    }
    
    mapping(uint256 => DataRecord) private records;
    uint256 private recordCount;
    
    event DataStored(uint256 indexed id, address indexed creator, uint256 timestamp);
    event DataUpdated(uint256 indexed id, address indexed updater, uint256 timestamp);
    event DataDeleted(uint256 indexed id, address indexed deleter, uint256 timestamp);
    
    function storeData(string memory _data) public returns (uint256) {
        recordCount++;
        records[recordCount] = DataRecord({
            id: recordCount,
            data: _data,
            creator: msg.sender,
            timestamp: block.timestamp,
            isActive: true
        });
        
        emit DataStored(recordCount, msg.sender, block.timestamp);
        return recordCount;
    }
    
    function getData(uint256 _id) public view returns (
        uint256 id,
        string memory data,
        address creator,
        uint256 timestamp,
        bool isActive
    ) {
        require(_id > 0 && _id <= recordCount, "Invalid record ID");
        DataRecord memory record = records[_id];
        return (record.id, record.data, record.creator, record.timestamp, record.isActive);
    }
    
    function updateData(uint256 _id, string memory _newData) public returns (bool) {
        require(_id > 0 && _id <= recordCount, "Invalid record ID");
        require(records[_id].isActive, "Record is not active");
        require(records[_id].creator == msg.sender, "Only creator can update");
        
        records[_id].data = _newData;
        records[_id].timestamp = block.timestamp;
        
        emit DataUpdated(_id, msg.sender, block.timestamp);
        return true;
    }
    
    function deleteData(uint256 _id) public returns (bool) {
        require(_id > 0 && _id <= recordCount, "Invalid record ID");
        require(records[_id].isActive, "Record already deleted");
        require(records[_id].creator == msg.sender, "Only creator can delete");
        
        records[_id].isActive = false;
        
        emit DataDeleted(_id, msg.sender, block.timestamp);
        return true;
    }
    
    function getDataCount() public view returns (uint256) {
        return recordCount;
    }
    
    function getAllActiveRecords() public view returns (uint256[] memory) {
        uint256 activeCount = 0;
        for (uint256 i = 1; i <= recordCount; i++) {
            if (records[i].isActive) {
                activeCount++;
            }
        }
        
        uint256[] memory activeIds = new uint256[](activeCount);
        uint256 index = 0;
        for (uint256 i = 1; i <= recordCount; i++) {
            if (records[i].isActive) {
                activeIds[index] = i;
                index++;
            }
        }
        
        return activeIds;
    }
    
    function verifyData(uint256 _id, string memory _data) public view returns (bool) {
        require(_id > 0 && _id <= recordCount, "Invalid record ID");
        return keccak256(bytes(records[_id].data)) == keccak256(bytes(_data));
    }
}
