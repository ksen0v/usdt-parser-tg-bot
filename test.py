import requests
import json
from dataclasses import dataclass
from utils import convert_utc_time, convert_usdt_value

import time
from random import randint

API_WALLET_HISTORY = 'https://usdt.tokenview.io/api/usdt/addresstxlist/'
API_WALLET_DETAILS = 'https://usdt.tokenview.io/api/usdtsearch/'

@dataclass
class Transaction:
    transaction_status: str
    chain_network: str
    adress_from: str
    adress_to: str
    utc_time: str
    usdt_value: int

@dataclass
class Wallet:
    address: str
    network: str
    balance: int
    tx_count: int
    last_transaction_hash: str 

#Wallet Details (adress, network, balance, history)
def get_wallet_details(address):
    r = requests.get(API_WALLET_DETAILS + address)
    
    wallet_details = parse_wallet_details(r.text)

    return wallet_details

def parse_wallet_details(data_json):
    data = json.loads(data_json)

    last_transaction = get_wallet_history(data['data'][0]['hash'], 1, 1)
    

    wallet = Wallet(data['data'][0]['hash'],
                    data['data'][0]['network'],
                    data['data'][0]['balance'],
                    data['data'][0]['txCount'],
                    last_transaction
                    )

    return wallet

#Wallet New Transactions
def get_new_transactions(wallet_details):
    last_transaction = wallet_details.last_transaction_hash

    new_transactions_all = []

    while True:
        wallet_details = get_wallet_details('0xf89d7b9c864f589bbf53a82105107622b35eaa40')
        last_transaction_new = wallet_details.last_transaction_hash

        if last_transaction != last_transaction_new:
            page = 1
            new_transactions = []
            found_old = False

            while not found_old:
                current_transactions = get_wallet_history(wallet_details.address, page, 48)
                page += 1

                for transaction in current_transactions:
                    if transaction['txid'] != last_transaction:
                        new_transactions.append(transaction)
                    else:
                        found_old = True
                        break

                if found_old or len(current_transactions) < 48:
                    break

            if new_transactions:
                new_transactions_all.extend(new_transactions)
                last_transaction = new_transactions[0]['txid']
            
            return reversed(new_transactions)
            #for tx in reversed(new_transactions):
            #    print(f'New tx: {tx["txid"]}')

        else:
            return []

        #delay = randint(5, 10)
        #print(f"Delay: {delay}")
        #time.sleep(delay)

def get_wallet_history(address, page_count, tx_count):
    r = requests.get(f'{API_WALLET_HISTORY}{address}/{page_count}/{tx_count}')

    wallet_history = parse_wallet_history(r.text, tx_count)

    return wallet_history

def parse_wallet_history(data_json, tx_count):
    data = json.loads(data_json)

    if tx_count == 1:
        last_transactions = data['data']['txs'][0]['txid']
    else:
        last_transactions = data['data']['txs']

    return last_transactions

