import json
from dataclasses import dataclass
from utils import convert_utc_time, convert_usdt_value, fetch_data

URL = 'https://usdt.tokenview.io/api/search/'

@dataclass
class Transaction:
    transaction_status: str
    chain_network: str
    address_from: str
    address_to: str
    utc_time: str
    usdt_value: int

async def get_transaction_data(hash):
    r = await fetch_data(URL + hash)
    
    transaction_data = await parse_requests(r)

    return transaction_data

async def parse_requests(data_json):
    data = json.loads(data_json)

    transaction = Transaction(transaction_status = data['enMsg'], 
                              chain_network = data['data'][0]['network'], 
                              address_from = data['data'][0]['from'], 
                              address_to = data['data'][0]['to'], 
                              utc_time = await convert_utc_time(data['data'][0]['time']), 
                              usdt_value = await convert_usdt_value(int(data['data'][0]['tokenTransfer'][0]['value']), 
                                                 int(data['data'][0]['tokenTransfer'][0]['tokenDecimals']))) 

    return transaction