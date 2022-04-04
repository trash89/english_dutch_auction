from brownie import accounts, DutchToken, DutchAuction
import time

DECIMALS = 10**18


def main():
    alice = accounts[0]
    bob = accounts[1]

    nft, nftId = deploy_and_mint_nft(alice)

    startingPrice = 1000000
    discountRate = 10
    dutchAuction = deploy_dutchAuction(
        alice, nft, nftId, startingPrice, discountRate)
    print(f"Owner of NFT {nftId} is {nft.ownerOf(nftId)}")

    print(
        f"{alice} approves the transfer of NFT {nftId} to the DutchAuction contract")
    tx = nft.approve(dutchAuction.address, nftId, {"from": alice})
    tx.wait(1)
    print("Approved!")

    currentPrice = dutchAuction.getPrice()
    print(f"The price is now : {currentPrice}")
    print_balances()

    amount = currentPrice
    print(f"Bob buys for {amount}...")
    tx = dutchAuction.buy({"from": bob, "amount": amount})
    tx.wait(1)
    print(f"Bob buyed for {amount}!")
    print_balances()


def deploy_and_mint_nft(deploy_from):
    print("Deploying the NFT contract and generating 1 NFT")
    nft = DutchToken.deploy({"from": deploy_from})
    print(f"The NFT contract is deployed at {nft}")
    nftId = 100
    tx = nft.safeMint(deploy_from.address, nftId, {"from": deploy_from})
    tx.wait(1)
    print(f"Owner of NFT {nftId} is {nft.ownerOf(nftId)}")
    return nft, nftId


def deploy_dutchAuction(deploy_from, _nft, _nftId, _startingPrice, _discountRate):
    print("Deploying the DutchAuction contract...")
    ea = DutchAuction.deploy(
        _startingPrice, _discountRate, _nft, _nftId,  {"from": deploy_from})
    print(f"The DutchAuction contract is deployed at {ea}")
    return ea


def print_balances():
    print(
        f"Alice : {accounts[0].balance()/DECIMALS}, Bob : {accounts[1].balance()/DECIMALS}")
    print(f"DutchAuction : {DutchAuction[-1].balance()/DECIMALS}")
