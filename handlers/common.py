
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="**Сгенерируйте портрет эпохи указав фильтры для открыток:**\n\n"
             "/help - показать помощь и информацию о боте\n"
             # "/date - указать временной период (в годах)\n"
             # "/place - откуда или куда прибыло письмо\n"
             # "/aspect - указать соотношение сторон\n"
             "/generate - сгенерировать портрет эпохи\n\n"
             'Также возможно написать "отмена" для отмены текущей команды.',
             # "*Если вы не указали какие-либо фильтры,\n"
             # "они будут спрошены при вызове* /generate",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="/generate - создать портрет эпохи\n\n"
        "Этот бот был создан для хакатона Почтовое: Digital\n"
        "[Исходный код](https://github.com/egoros7/postalbot)\n"
        "Использованы данные Цифрового корпуса почтовых открыток «Пишу тебе». URL: https://pishutebe.ru/",
        reply_markup=ReplyKeyboardRemove()
    )

# Нетрудно догадаться, что следующие два хэндлера можно
# спокойно объединить в один, но для полноты картины оставим так

# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )