from aiogram import Router, types
from aiogram.filters import CommandStart
from src.vibe_tracker_bot.database.models import User

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    if not message.from_user:
        return

    telegram_id = message.from_user.id
    username = message.from_user.username

    # Create user if not exists
    user, created = await User.get_or_create(
        telegram_id=telegram_id, defaults={"username": username}
    )

    # If user existed but username changed, update it
    if not created and user.username != username:
        user.username = username
        await user.save()

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я Vibe Tracker — помогаю следить за твоим настроением и энергией.\n\n"
        "Используй команду /log, чтобы отметить своё состояние."
    )
