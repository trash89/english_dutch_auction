// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./console.sol";

contract EnglishToken is ERC721, Ownable {
    constructor() ERC721("EnglishToken", "ETK") {}

    function safeMint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
    }
}

contract EnglishAuction {
    IERC721 public immutable nft;
    uint256 public immutable nftId;

    address payable public immutable seller;
    uint32 public endAt;
    bool public started;
    bool public ended;

    address public highestBidder;
    uint256 public highestBid;
    mapping(address => uint256) public bids;

    event Start();
    event Bid(address indexed sender, uint256 amount);
    event Withdraw(address indexed bidder, uint256 amount);
    event End(address winner, uint256 amount);

    constructor(
        address _nft,
        uint256 _nftId,
        uint256 _startingBid
    ) {
        nft = IERC721(_nft);
        nftId = _nftId;
        seller = payable(msg.sender);
        highestBid = _startingBid;
    }

    function start() external {
        require(msg.sender == seller, "not seller");
        require(!started, "started");
        started = true;
        endAt = uint32(block.timestamp) + 10 seconds;
        console.log(
            "start() : msg.sender is %s, address(this) is %s",
            msg.sender,
            address(this)
        );
        nft.transferFrom(msg.sender, address(this), nftId);
        //nft.safeTransferFrom(msg.sender, address(this), nftId);
        emit Start();
    }

    function bid() external payable {
        require(started, "not started");
        require(uint32(block.timestamp) < endAt, "ended");
        require(msg.value > highestBid, "value < highest");

        if (highestBidder != address(0)) {
            bids[highestBidder] += highestBid;
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
        console.log(
            "bid() : highestBidder is %s, with %d",
            highestBidder,
            highestBid
        );
        emit Bid(msg.sender, msg.value);
    }

    function withdraw() external {
        uint256 bal = bids[msg.sender];
        bids[msg.sender] = 0;
        console.log("withdraw() :msg.sender is %s, bal is %d", msg.sender, bal);
        payable(msg.sender).transfer(bal);
        emit Withdraw(msg.sender, bal);
    }

    function end() external {
        require(started, "not started");
        require(uint32(block.timestamp) >= endAt, "not ended");
        require(!ended, "ended");
        ended = true;
        if (highestBidder != address(0)) {
            nft.safeTransferFrom(address(this), highestBidder, nftId);
            seller.transfer(highestBid);
            console.log(
                "end() : transfer %d to %s and the ownership of NFT %d",
                highestBid,
                highestBidder,
                nftId
            );
        } else {
            nft.safeTransferFrom(address(this), seller, nftId);
            console.log("end() : transfer to %s for NFT %d", seller, nftId);
        }

        emit End(highestBidder, highestBid);
    }
}
