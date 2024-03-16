from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, BufferedInputFile

import base64

from keyboards.simple_row import make_row_keyboard
from data import generate

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_aspect = ["16:9", "1:1", "9:16"]
available_places = ["куда", "откуда"]

class Generate(StatesGroup):
    choosing_date = State()
    choosing_wof = State()
    choosing_place = State()
    choosing_aspect = State()
    generating = State()


@router.message(StateFilter(None), Command("generate"))
async def cmd_generate(message: Message, state: FSMContext):
    await message.answer(
        text="Пожалуйста, напишите год\n",
        reply_markup=ReplyKeyboardRemove()
    )
    # Устанавливаем пользователю состояние "выбирает дату"
    await state.set_state(Generate.choosing_date)

@router.message(Generate.choosing_date)
async def date_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_date=message.text.lower())
    await message.answer(
        text="Выберите откуда или куда идёт письмо",
        reply_markup=make_row_keyboard(available_places)
    )
    await state.set_state(Generate.choosing_wof)


@router.message(Generate.choosing_wof, F.text.lower().in_(available_places))
async def wof_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_wof=message.text.lower())
    await message.answer(
        text="Теперь, пожалуйста, выберите населенный пункт",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Generate.choosing_place)

# В целом, никто не мешает указывать стейты полностью строками
# Это может пригодиться, если по какой-то причине
# ваши названия стейтов генерируются в рантайме (но зачем?)
@router.message(StateFilter("Generate:choosing_wof"))
async def date_chosen_incorrectly(message: Message):
    await message.answer(
        text='Вы неправильно ответили. Возможными ответами являются только "куда" и "откуда"',
        reply_markup=make_row_keyboard(available_places)
    )

@router.message(StateFilter("Generate:choosing_place"))
async def place_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_place=message.text)
    await message.answer(
        text="Выберите соотношение сторон",
        reply_markup=make_row_keyboard(available_aspect)
    )
    await state.set_state(Generate.choosing_aspect)

@router.message(Generate.choosing_aspect, F.text.in_(available_aspect))
async def aspect_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text="Генерация... Пожалуйста подождите.",
        reply_markup=ReplyKeyboardRemove()
    )
    ans = await generate(user_data['chosen_date'], user_data['chosen_wof'], user_data['chosen_place'], message.text)
    
    file = BufferedInputFile(base64.b64decode(ans[0]), 'image.png')

    await message.answer_photo(file)
    
    await state.clear()
    # await state.set_state(Generate.generating)

@router.message(StateFilter("Generate:choosing_aspect"))
async def aspect_chosen_incorrectly(message: Message):
    await message.answer(
        text='Вы некорректно ответили. Выберете ответы снизу:',
        reply_markup=make_row_keyboard(available_aspect)
    )

# @router.message(Generate.generating)
# async def generation_func(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     ans = generate(user_data['chosen_date'], user_data['chosen_wof'], user_data['chosen_place'], user_data['chosen_aspect'])
#     await message.answer(
#         text=ans,
#         reply_markup=ReplyKeyboardRemove()
#     )
#     # Сброс состояния и сохранённых данных у пользователя
#     await state.clear()
