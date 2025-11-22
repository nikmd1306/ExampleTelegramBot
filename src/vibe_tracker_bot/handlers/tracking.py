from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..database.models import User, MoodLog

tracking_router = Router()


class TrackingState(StatesGroup):
    waiting_for_note = State()


def get_rating_keyboard() -> InlineKeyboardMarkup:
    """Creates a 1-10 rating keyboard."""
    # 2 rows of 5 buttons
    buttons = []
    row1 = [
        InlineKeyboardButton(text=str(i), callback_data=f"rate:{i}")
        for i in range(1, 6)
    ]
    row2 = [
        InlineKeyboardButton(text=str(i), callback_data=f"rate:{i}")
        for i in range(6, 11)
    ]
    buttons.append(row1)
    buttons.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_skip_keyboard() -> InlineKeyboardMarkup:
    """Creates a skip button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_note")]
        ]
    )


@tracking_router.message(Command("log"))
async def cmd_log(message: types.Message, state: FSMContext):
    """Starts the tracking flow."""
    await state.clear()
    await message.answer(
        "Оцени свой уровень энергии/вайба от 1 до 10:",
        reply_markup=get_rating_keyboard(),
    )


@tracking_router.callback_query(F.data.startswith("rate:"))
async def process_rating(callback: types.CallbackQuery, state: FSMContext):
    """Handles rating selection."""
    rating = int(callback.data.split(":")[1])
    await state.update_data(rating=rating)
    await state.set_state(TrackingState.waiting_for_note)

    await callback.message.edit_text(
        f"Принято: {rating}/10.\n\n"
        "Хочешь добавить заметку? Напиши её или нажми кнопку:",
        reply_markup=get_skip_keyboard(),
    )
    await callback.answer()


@tracking_router.message(TrackingState.waiting_for_note)
async def process_note(message: types.Message, state: FSMContext):
    """Handles the text note."""
    data = await state.get_data()
    rating = data.get("rating")
    note = message.text

    user, _ = await User.get_or_create(
        telegram_id=message.from_user.id,
        defaults={"username": message.from_user.username},
    )

    await MoodLog.create(user=user, value=rating, note=note)

    await state.clear()
    await message.answer("✅ Запись сохранена!")


@tracking_router.callback_query(F.data == "skip_note", TrackingState.waiting_for_note)
async def process_skip_note(callback: types.CallbackQuery, state: FSMContext):
    """Handles skipping the note."""
    data = await state.get_data()
    rating = data.get("rating")

    user, _ = await User.get_or_create(
        telegram_id=callback.from_user.id,
        defaults={"username": callback.from_user.username},
    )

    await MoodLog.create(user=user, value=rating, note=None)

    await state.clear()
    await callback.message.edit_text(
        f"Принято: {rating}/10.\n✅ Запись сохранена (без заметки)."
    )
    await callback.answer()
