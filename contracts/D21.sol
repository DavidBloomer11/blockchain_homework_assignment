pragma solidity ^0.8.7;

import "./IVoteD21.sol";

contract D21 is IVoteD21 {
    // VoterData structure
    struct VoterData{
        int8 positive;
        int8 negative;
        int8 flag;
        address[] voted;
    }

    // Added attributes
    mapping (address => Subject) private subjectMapping;
    address[] private subjectAddressList;
    mapping (address => VoterData) private voterRegistry;
    uint private votingDeadline;
    address private owner;

    constructor () {
        votingDeadline = block.timestamp + 604800; //604800 = 7 days
        owner = msg.sender;
    }
    

    function addSubject(string memory name) external {
        // We need to check if the sender (one that called the function) has allready added a subject.
        require(subjectMapping[msg.sender].flag < 1, "Address has allready added a subject!");

        Subject memory newSubject = Subject(name,0,1);

        // Require that there is still time to add a new subject
        require(this.getRemainingTime() > 0, "No time left to vote!");

        // Add subject to our hastable and to our registry
        subjectMapping[msg.sender] = newSubject;
        subjectAddressList.push(msg.sender);
    }

    function addVoter(address addr) external {
        // Checks if voter (address) is allready registered, if it is
        // it will pass an error that the voter is allready registered and therefore cant be
        // registered again
        require(voterRegistry[addr].flag <1, "Voter allready added");

        // Require that owner is adding the voter
        require(msg.sender == owner, "Only the owner can add new voters");

        // Require that there is still time to add voters
        require(this.getRemainingTime() > 0, "No time left to vote!");

        address[] memory votedOn;  

        VoterData memory voter = VoterData(2,1,1,votedOn);

        voterRegistry[addr] = voter;
    }

    function getSubjects() external view returns(address[] memory) {
        return subjectAddressList;
    }

    function getSubject(address addr) external view returns(Subject memory) {
        return subjectMapping[addr];
    }

    function votePositive(address addr) external {
        VoterData storage voterData = voterRegistry[msg.sender];

        //Perform checks:

        // Require that there is still time left to vote
        require(this.getRemainingTime() > 0, "No time left to vote!");

        //Require that voter hasn't allready voted on this subject
        require(checkIfAllreadyVoted(addr,voterData.voted)==false,"Voter has allready voted");

        //Require that voter has votes left, Require that voter is registered
        require(voterData.positive > 0,"Voter has no positive votes left or isn't registered");

        // Perform voting:
        subjectMapping[addr].votes += 1;

        voterData.positive -= 1;
        voterData.voted.push(addr);       

    }

    function voteNegative(address addr) external {
        VoterData storage voterData = voterRegistry[msg.sender];

        // Perform checks:

        // Require that there is time left to vote
        require(this.getRemainingTime() > 0, "No time left to vote!");

        // Require that hasn't allready voted on this subject
        require(checkIfAllreadyVoted(addr,voterData.voted)==false,"Voter has allready voted");

        //Require that has no positive votes left, Require that voter is registered
        require(voterData.positive == 0,"Voter still has positive votes or isn't registered.");

        //Require that has negative votes left
        require(voterData.negative > 0,"Voter has no positive votes left.");


        // Perform voting:
        subjectMapping[addr].votes -= 1;

        voterData.negative -= 1;  
        voterData.voted.push(addr);
    }

    function getRemainingTime() external view returns(uint) {
        if(votingDeadline > block.timestamp) {
            return votingDeadline - block.timestamp;
        }
        else {
            return 0;
        }

    }
    
    function getResults() external view returns(Subject[] memory) {
        uint length = subjectAddressList.length;
        Subject[] memory subjectList = new Subject[](length);
        for(uint i=0; i < subjectAddressList.length; i++) {
            Subject memory sub= subjectMapping[subjectAddressList[i]];
            subjectList[i] = sub;
        }

        quickSort(subjectList,int(0),int(length - 1));

        return subjectList;
    }

    function test() external view returns(uint) {
        return block.timestamp;
    }

    function getOwner() external view returns(address){
        return owner;
    } 


    // Functions to help
    function checkIfAllreadyVoted(address addr,address[] storage list) view private returns(bool response) {
        response = false;
        for(uint i = 0; i < list.length; i++) {
            if(addr == list[i]) {
                response = true;
            }
        }
        return response;
    }

    function quickSort(Subject[] memory arr, int left, int right) private pure  {
        Subject[] memory sorted = arr;

        int i = left;
        int j = right;
        if (i == j)
            return;
        int pivot = arr[uint(left + (right - left) / 2)].votes;
        while (i <= j) {
            while (arr[uint(i)].votes < pivot) i++;
            while (pivot < arr[uint(j)].votes) j--;
            if (i <= j) {
                (arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
                i++;
                j--;
            }
        }
        if (left < j)
            quickSort(arr, left, j);
        if (i < right)
            quickSort(arr, i, right);
    }


}