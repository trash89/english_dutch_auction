from brownie import accounts, EnglishToken, EnglishAuction
import time

DECIMALS = 10**18


def main():
    alice = accounts[0]
    bob = accounts[1]
    charlie = accounts[2]

    nft, nftId = deploy_and_mint_nft(alice)

    startingBid = "1 wei"
    englishAuction = deploy_englishAuction(alice, nft, nftId, startingBid)
    print(f"Owner of NFT {nftId} is {nft.ownerOf(nftId)}")

    print(
        f"{alice} approves the transfer of NFT {nftId} to the EnglishAuction contract")
    tx = nft.approve(englishAuction.address, nftId, {"from": alice})
    tx.wait(1)
    print("Approved!")

    print("Alice is starting the auction...")
    tx = englishAuction.start({"from": alice})
    tx.wait(1)
    print("Auction started!")

    print_balances()
    amount = "2 wei"
    print(f"Alice bids for {amount}...")
    tx = englishAuction.bid({"from": alice, "amount": amount})
    tx.wait(1)
    print(f"Alice bidded for {amount}!")
    print_balances()

    amount = "3 wei"
    print(f"Bob bids for {amount}...")
    tx = englishAuction.bid({"from": bob, "amount": amount})
    tx.wait(1)
    print(f"Bob bidded for {amount}!")
    print_balances()

    amount = "4 wei"
    print(f"Charlie bids for {amount}...")
    tx = englishAuction.bid({"from": charlie, "amount": amount})
    tx.wait(1)
    print(f"Charlie bidded for {amount}!")
    print_balances()

    print("Waiting 10 secs to finish the auction...")
    time.sleep(10)
    print("Alice calls end()...")
    tx = englishAuction.end({"from": alice})
    tx.wait(1)
    print("Alice ended the auction!")
    print_balances()

    print("Bob calls withdraw()...")
    tx = englishAuction.withdraw({"from": bob})
    tx.wait(1)
    print("Bob withdrawn from the auction!")
    print_balances()

    print("Charlie calls withdraw()...")
    tx = englishAuction.withdraw({"from": charlie})
    tx.wait(1)
    print("Charlie withdrawn from the auction!")
    print_balances()

    print("Alice calls withdraw()...")
    tx = englishAuction.withdraw({"from": alice})
    tx.wait(1)
    print("Alice withdrawn from the auction!")
    print_balances()


def deploy_and_mint_nft(deploy_from):
    print("Deploying the NFT contract and generating 1 NFT")
    nft = EnglishToken.deploy({"from": deploy_from})
    print(f"The NFT contract is deployed at {nft}")
    nftId = 100
    tx = nft.safeMint(deploy_from.address, nftId, {"from": deploy_from})
    tx.wait(1)
    print(f"Owner of NFT {nftId} is {nft.ownerOf(nftId)}")
    return nft, nftId


def deploy_englishAuction(deploy_from, _nft, _nftId, _startingBid):
    print("Deploying the EnglishAuction contract...")
    englishAuction = EnglishAuction.deploy(
        _nft, _nftId, _startingBid, {"from": deploy_from})
    print(f"The EnglishAuction contract is deployed at {englishAuction}")
    return englishAuction


def print_balances():
    print(
        f"Alice : {accounts[0].balance()/DECIMALS}, Bob : {accounts[1].balance()/DECIMALS}, Charlie : {accounts[2].balance()/DECIMALS}")
    print(f"EnglishAuction : {EnglishAuction[-1].balance()/DECIMALS}")
