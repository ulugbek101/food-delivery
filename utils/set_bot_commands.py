from aiogram.filters.command import BotCommand


async def set_bot_commands(bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Launch a bot"),
        BotCommand(command="help", description="Get help"),
    ])
