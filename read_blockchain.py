import os
import json
from web3 import Web3, HTTPProvider
from eth_account import Account
from web3.middleware import construct_sign_and_send_raw_middleware
import asyncio
from typing import Tuple

PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = '0xca733a39b72DA72078DBc1c642e6C3836C5b424E'
PROVIDER_HTTP_ENDPOINT = "http://54.153.142.251:8545"

def get_votes_from_blochchain(spec_hash: str) -> Tuple[int,int]:
    """For interacting with the smart contract and getting the current vote counts of a ballot

    Args:
        spec_hash (str): A unique sha256 hash of the ballot info

    Returns:
        Tuple[int,int]: (yes count, no count)
    """
    w3 = Web3(Web3.HTTPProvider(PROVIDER_HTTP_ENDPOINT))
    acct = Account.from_key(PRIVATE_KEY)
    abi = json.load(open("voting.json"))
    VotingAlpha = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct.privateKey))
    p_id = VotingAlpha.functions.getProposalId(spec_hash.replace("0x0x","0x")).call()
    proposalInfo = VotingAlpha.functions.getProposal(p_id).call()
    return(proposalInfo[4], proposalInfo[3])