from aiogram.types import Message
from aiogram.filters import CommandObject
import asyncio

from config_loader import MESSAGES
from transaction import get_transaction_data
from wallet import isValidWallet, spy_start

active_tasks = {}

async def start(message: Message):
    await message.answer(MESSAGES['start'])

async def get(message: Message, command: CommandObject):
    hash = command.args
    if hash:
        try:
            transaction_data = await get_transaction_data(hash)

            await message.answer(str(MESSAGES['transaction_data']).format(transaction_status = transaction_data.transaction_status,
                                                                        chain_network = transaction_data.chain_network,
                                                                        adress_from = transaction_data.address_from,
                                                                        adress_to = transaction_data.address_to, 
                                                                        utc_time = transaction_data.utc_time,
                                                                        usdt_value = transaction_data.usdt_value))
        except:
            await message.answer(MESSAGES['error_get_transaction'])
    else:
        await message.answer(MESSAGES['error_hash_isnull'])

async def spy(message: Message, command: CommandObject):
    address = command.args
    if address:
        if await isValidWallet(address):
            if address not in active_tasks:
                task = asyncio.create_task(spy_start(message, address))
                active_tasks[address] = task
                await message.answer(str(MESSAGES['monitoring_isrun']).format(address = address))
            else:
                await message.answer(MESSAGES['error_address_isactive'])
        else:
            await message.answer(MESSAGES['error_get_wallet'])
    else:
        await message.answer(MESSAGES['error_address_isnull'])

async def spy_stop(message: Message, command: CommandObject):
    address = command.args

    if address:
        if address in active_tasks:
            task = active_tasks[address]
            task.cancel()
            del active_tasks[address]

            await message.answer(str(MESSAGES['monitoring_isstop']).format(address = address))
        else:
            await message.answer(MESSAGES['error_address_isnotactive'])
    else:
        await message.answer(MESSAGES['error_address_isnull'])

async def spy_list(message: Message):
    await message.answer(str(MESSAGES['tasks_list']).format(tasks_list = " ".join(active_tasks)))

async def spy_stop_all(message: Message):
    for address in active_tasks:
        task = active_tasks[address]
        task.cancel()
    active_tasks.clear()
    await message.answer(MESSAGES['all_monitoring_isstop'])