// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract NFTTicket is ERC721Full {
    struct Ticket {
        uint256 tokenId;
        uint256 price;
        uint256 copies;
    }

    Ticket[] public tickets;
    mapping(uint256 => address[]) public ownershipHistory;
    mapping(uint256 => uint256[]) public priceHistory;

    event TicketCreated(uint256 indexed tokenId, address indexed owner, uint256 price, uint256 copies);
    event TicketTransferred(uint256 indexed tokenId, address indexed from, address indexed to, uint256 price);

    constructor() public ERC721Full("NFTTicket", "TICKET") {}

    function registerTicket(address owner, string memory tokenURI, uint256 price, uint256 copies) public returns (uint256) {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);
        tickets.push(Ticket(tokenId, price, copies));
        ownershipHistory[tokenId].push(owner);
        priceHistory[tokenId].push(price);
        emit TicketCreated(tokenId, owner, price, copies);
        return tokenId;
    }

    function buyTicket(uint256 tokenId) public payable {
        Ticket storage ticket = tickets[tokenId];
        require(msg.value >= ticket.price, "Insufficient funds");
        require(ticket.copies > 0, "No more copies available");

        address previousOwner = ownerOf(tokenId);
        address newOwner = msg.sender;

        _transferFrom(previousOwner, newOwner, tokenId);

        ownershipHistory[tokenId].push(newOwner);
        priceHistory[tokenId].push(msg.value);

        ticket.copies--;

        address(uint160(previousOwner)).transfer(msg.value);

        emit TicketTransferred(tokenId, previousOwner, newOwner, msg.value);
    }

    function getOwnershipHistory(uint256 tokenId) public view returns (address[] memory) {
        return ownershipHistory[tokenId];
    }

    function getPriceHistory(uint256 tokenId) public view returns (uint256[] memory) {
        return priceHistory[tokenId];
    }

    function getCopies(uint256 tokenId) public view returns (uint256) {
        return tickets[tokenId].copies;
    }
} 
