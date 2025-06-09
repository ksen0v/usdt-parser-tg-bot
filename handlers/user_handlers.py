from aiogram.types import Message
from aiogram.filters import CommandObject
import asyncio

from config_loader import MESSAGES
from transaction import get_transaction_data
from wallet import isValidWallet, spy_start

# Словарь для хранения задач по user_id: {user_id: {address: task}}
active_tasks = {}

async def start(message: Message):
    await message.answer(MESSAGES['start'])

async def get(message: Message, command: CommandObject):
    hash = command.args
    if hash:
        try:
            transaction_data = await get_transaction_data(hash)
            await message.answer(
                str(MESSAGES['transaction_data']).format(
                    transaction_status=transaction_data.transaction_status,
                    chain_network=transaction_data.chain_network,
                    adress_from=transaction_data.address_from,
                    adress_to=transaction_data.address_to, 
                    utc_time=transaction_data.utc_time,
                    usdt_value=transaction_data.usdt_value
                )
            )
        except:
            await message.answer(MESSAGES['error_get_transaction'])
    else:
        await message.answer(MESSAGES['error_hash_isnull'])

async def spy(message: Message, command: CommandObject):
    user_id = message.from_user.id
    address = command.args
    
    if not address:
        await message.answer(MESSAGES['error_address_isnull'])
        return
    
    if not await isValidWallet(address):
        await message.answer(MESSAGES['error_get_wallet'])
        return
    
    # Инициализация словаря для пользователя, если его еще нет
    if user_id not in active_tasks:
        active_tasks[user_id] = {}
    
    # Проверяем, есть ли уже такая задача у пользователя
    if address in active_tasks[user_id]:
        await message.answer(MESSAGES['error_address_isactive'])
        return
    
    # Создаем новую задачу
    task = asyncio.create_task(spy_start(message, address))
    active_tasks[user_id][address] = task
    await message.answer(str(MESSAGES['monitoring_isrun']).format(address=address))

async def spy_stop(message: Message, command: CommandObject):
    user_id = message.from_user.id
    address = command.args
    
    if not address:
        await message.answer(MESSAGES['error_address_isnull'])
        return
    
    # Проверяем, есть ли задачи у пользователя
    if user_id not in active_tasks or address not in active_tasks[user_id]:
        await message.answer(MESSAGES['error_address_isnotactive'])
        return
    
    # Останавливаем задачу
    task = active_tasks[user_id].pop(address)
    task.cancel()
    
    # Если у пользователя больше нет задач, удаляем его из словаря
    if not active_tasks[user_id]:
        del active_tasks[user_id]
    
    await message.answer(str(MESSAGES['monitoring_isstop']).format(address=address))

async def spy_list(message: Message):
    user_id = message.from_user.id
    
    if user_id not in active_tasks or not active_tasks[user_id]:
        await message.answer(MESSAGES['no_active_tasks'])
        return
    
    tasks_list = "\n".join(active_tasks[user_id].keys())
    await message.answer(str(MESSAGES['tasks_list']).format(tasks_list=tasks_list))

async def spy_stop_all(message: Message):
    user_id = message.from_user.id
    
    if user_id not in active_tasks or not active_tasks[user_id]:
        await message.answer(MESSAGES['no_active_tasks'])
        return
    
    # Останавливаем все задачи пользователя
    for address, task in active_tasks[user_id].items():
        task.cancel()
    
    # Удаляем пользователя из словаря
    del active_tasks[user_id]
    
    await message.answer(MESSAGES['all_monitoring_isstop'])