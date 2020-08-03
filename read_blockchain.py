import os
import json
from web3 import Web3, HTTPProvider
from eth_account import Account
from web3.middleware import construct_sign_and_send_raw_middleware
import asyncio


private_key = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = '0xca733a39b72DA72078DBc1c642e6C3836C5b424E'
PROVIDER_HTTP_ENDPOINT = "http://54.153.142.251:8545"

w3 = Web3(Web3.HTTPProvider(PROVIDER_HTTP_ENDPOINT))
acct = Account.from_key(private_key)
abi = json.load(open("voting.json"))

VotingAlpha = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct.privateKey))
p_id = VotingAlpha.functions.getProposalId("0x389ec27d697e0412dbe51df0e5ae0f70b0de4be63a36de8e04646e8ef4b779f8").call()
print(p_id)
proposalInfo = VotingAlpha.functions.getProposal(p_id).call()
print("No votes:", proposalInfo[3])
print("Yes votes:", proposalInfo[4])


for i in range(1, 400):
    proposalInfo = VotingAlpha.functions.getProposal(i).call()
    if proposalInfo[3] or proposalInfo[4]:
        print(i, proposalInfo[3], proposalInfo[4])


