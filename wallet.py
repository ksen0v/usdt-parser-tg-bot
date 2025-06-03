import json
from dataclasses import dataclass
from random import randint
from aiogram.types import Message
import asyncio

from utils import convert_utc_time, convert_usdt_value, fetch_data
from config_loader import MESSAGES, COUNTDOWN, NOTIFICATIONS

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
async def get_wallet_details(address):
    r = await fetch_data(API_WALLET_DETAILS + address)
    
    wallet_details = await parse_wallet_details(r)

    return wallet_details

async def parse_wallet_details(data_json):
    data = json.loads(data_json)

    last_transaction = await get_wallet_history(data['data'][0]['hash'], 1, 1)
    

    wallet = Wallet(data['data'][0]['hash'],
                    data['data'][0]['network'],
                    data['data'][0]['balance'],
                    data['data'][0]['txCount'],
                    last_transaction
                    )

    return wallet

#Wallet New Transactions
async def get_wallet_history(address, page_count, tx_count):
    r = await fetch_data(f'{API_WALLET_HISTORY}{address}/{page_count}/{tx_count}')

    wallet_history = await parse_wallet_history(r, tx_count)

    return wallet_history

async def parse_wallet_history(data_json, tx_count):
    data = json.loads(data_json)

    if tx_count == 1:
        last_transactions = data['data']['txs'][0]['txid']
    else:
        last_transactions = data['data']['txs']

    return last_transactions

async def isValidWallet(address):
    r = await fetch_data(API_WALLET_DETAILS + address)
    data = json.loads(r)
    return int(data['code']) != 404

async def spy_start(message: Message, address):
    wallet_details = await get_wallet_details(address)

    await message.answer(str(MESSAGES['wallet_details']).format(address = wallet_details.address, 
                                                                chain_network = wallet_details.network, 
                                                                balance = wallet_details.balance, 
                                                                last_tx = wallet_details.last_transaction_hash))
    
    last_transaction = wallet_details.last_transaction_hash

    new_transactions_all = []

    while True:
        wallet_details_new = await get_wallet_details(address)
        last_transaction_new = wallet_details_new.last_transaction_hash

        if last_transaction != last_transaction_new:
            page = 1
            new_transactions = []
            found_old = False

            while not found_old:
                current_transactions = await get_wallet_history(wallet_details.address, page, 48)
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
            
            for transaction in reversed(new_transactions):
                await message.answer(str(MESSAGES['new_transaction']).format(address = address, 
                                                                             hash = transaction['txid'], 
                                                                             network = transaction['network'], 
                                                                             utc_time = await convert_utc_time(transaction['time']),
                                                                             wallet_from = transaction['from'],
                                                                             usdt_value = await convert_usdt_value(int(transaction['value']))))
        else:
            if NOTIFICATIONS:
                await message.answer(str(MESSAGES['no_new_transactions']).format(address = address))

        delay = randint(COUNTDOWN + 5, COUNTDOWN + 10)
        await asyncio.sleep(delay)