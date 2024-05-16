from aiogram.filters.command import BotCommand


async def set_bot_commands(bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="order", description="Заказать")
    ])
