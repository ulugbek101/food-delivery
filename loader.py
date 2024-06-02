from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, PAYMENT_PROVIDER_TOKEN
from utils.db_api.db import Database

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database(db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT)
branches_locations = [
    [41.324691689658856, 69.21545814154231],
]

db.create_users_table()
db.create_categories_table()
db.create_products_table()
db.create_cart_table()
db.create_locations_table()
db.create_user_orders_table()
db.create_orders_table()
