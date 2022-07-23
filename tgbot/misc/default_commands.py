from aiogram import types, Dispatcher


async def setup_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        commands=[
            types.BotCommand("start", "\U0001F504 Botni qayta yuklash"),  # Emoji ":arrows_counterclockwise:"
            types.BotCommand("help", "\U0001F198 Yordam"),  # Emoji "sos"
        ]
    )
