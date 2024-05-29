import asyncio
import logging

from environs import Env

from loader import dp, bot
from handlers.users.start import router
from utils.set_bot_commands import set_bot_commands

env = Env()
env.read_env()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(router=router)

    if env.str("MODE") == "DEBUG":
        logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
