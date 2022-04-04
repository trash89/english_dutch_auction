// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./console.sol";

contract DutchToken is ERC721, Ownable {
    constructor() ERC721("DutchToken", "DTK") {}

    function safeMint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
    }
}

contract DutchAuction {
    uint256 private constant DURATION = 30 seconds;

    IERC721 public immutable nft;
    uint256 public immutable nftId;

    address payable public immutable seller;
    uint256 public immutable startingPrice;
    uint256 public immutable startAt;
    uint256 public immutable expiresAt;
    uint256 public immutable discountRate;

    constructor(
        uint256 _startingPrice,
        uint256 _discountRate,
        address _nft,
        uint256 _nftId
    ) {
        seller = payable(msg.sender);
        startingPrice = _startingPrice;
        startAt = block.timestamp;
        expiresAt = block.timestamp + DURATION;
        discountRate = _discountRate;

        require(
            _startingPrice >= _discountRate * DURATION,
            "starting price < min"
        );
        nft = IERC721(_nft);
        nftId = _nftId;
    }

    function getPrice() public view returns (uint256) {
        uint256 timeElapsed = block.timestamp - startAt;
        uint256 discount = discountRate * timeElapsed;
        return startingPrice - discount;
    }

    function buy() external payable {
        require(block.timestamp < expiresAt, "auction expired");

        uint256 price = getPrice();
        require(msg.value >= price, "ETH < price");

        nft.transferFrom(seller, msg.sender, nftId);
        uint256 refund = msg.value - price;
        if (refund > 0) {
            console.log("buy(): refund %d to %s", refund, msg.sender);
            payable(msg.sender).transfer(refund);
        }
        console.log(
            "buy(): closing the auction(selfdestruct), sending %d to %s",
            address(this).balance,
            seller
        );
        selfdestruct(seller);
    }
}
