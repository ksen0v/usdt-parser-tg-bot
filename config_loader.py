import json
import os

def load_config():

    default_config = {
    "admin_id": 6993739453,
    "countdown": 10,
    "notifications": 0,
    "messages": {
        "startup_admin": "💎 TronScanner | Парсер транзакций 💎\n\nСтатус обновлен: Онлайн 🟢",
        "start": "Главное меню\n\nКоманды:\n/get [хэш] - получение данных о транзакции\n/spy [адресс кошелька] - запуск прослушивания транзакций кошелька с заданным кд\n/spy_list - список всех прослушиваемых кошельков\n/spy_stop [адресс кошелька] - остановка прослушивания транзакций кошелька\n/spy_stop_all - остановка всех прослушиваний транзакций кошельков ",
        "transaction_data": "Детали транзакции\n\nСтатус: {transaction_status}\nСеть: {chain_network}\nОткуда: {adress_from}\nКуда: {adress_to}\nВремя (UTC): {utc_time}\nСумма: {usdt_value} USDT",
        "error_get_transaction": "Ошибка получения транзакции",
        "error_hash_isnull": "Хэш не указан, команда /get [хэш]",
        "error_address_isnull": "Адрес кошелька не указан, команда /spy [адресс кошелька]",
        "error_get_wallet": "Ошибка получения кошелька",
        "wallet_details": "Детали кошелька\n\nАдрес: {address}\nСеть: {chain_network}\nБаланс: {balance} USDT\nПоследняя транзакция: {last_tx}", 
        "no_new_transactions": "Новых транзакций на кошельке {address} нет",
        "new_transaction": "Новая транзакция на кошельке {address}\n\nХэш: {hash}\nСеть: {network}\nВремя (UTC): {utc_time}\nОткуда: {wallet_from}\nСумма: {usdt_value} USDT",
        "error_address_isactive": "Адресс кошелька уже слушается",
        "error_address_isnotactive": "Адресс кошелька не слушается",
        "monitoring_isrun": "Мониторинг кошелька {address} запущен",
        "monitoring_isstop": "Мониторинг кошелька {address} остановлен",
        "tasks_list": "Список запущенных мониторингов\n\n{tasks_list}",
        "all_monitoring_isstop": "Все мониторинги остановлены"
    }
}

    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()
ADMIN_ID = config['admin_id']
MESSAGES = config['messages']
COUNTDOWN = int(config['countdown'])
NOTIFICATIONS = int(config['notifications'])
