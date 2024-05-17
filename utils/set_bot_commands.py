from aiogram.filters.command import BotCommand


async def set_bot_commands(bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="order", description="Заказать"),
        BotCommand(command="cart", description="Корзина"),
        BotCommand(command="contacts", description="Контакты"),
        BotCommand(command="help", description="Помощь"),
    ])
