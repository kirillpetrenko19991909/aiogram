
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 НАСТРОЙКИ
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
ADMIN_USERNAME = "@kerilsnimaet"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- STATES ----------
class Form(StatesGroup):
    role = State()
    service = State()
    goal = State()
    brief = State()

# ---------- KEYBOARDS ----------
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Хочу съёмку", callback_data="start_form")],
        [InlineKeyboardButton(text="🤔 Подойдём ли мы?", callback_data="fit")],
        [InlineKeyboardButton(text="📎 Как мы работаем", callback_data="format")]
    ])

def role_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎤 Артист / музыкант", callback_data="role_artist")],
        [InlineKeyboardButton(text="📱 Инфлюенсер / блогер", callback_data="role_influencer")],
        [InlineKeyboardButton(text="🧠 Продюсер / менеджер", callback_data="role_manager")]
    ])

def service_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎶 Сниппеты", callback_data="srv_snippet")],
        [InlineKeyboardButton(text="🎬 Клип", callback_data="srv_clip")],
        [InlineKeyboardButton(text="📱 Контент для соцсетей", callback_data="srv_content")],
        [InlineKeyboardButton(text="❓ Нужна помощь", callback_data="srv_help")]
    ])

def goal_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Рост и охваты", callback_data="goal_growth")],
        [InlineKeyboardButton(text="🎭 Образ / стиль", callback_data="goal_image")],
        [InlineKeyboardButton(text="💿 Продвижение релиза", callback_data="goal_release")],
        [InlineKeyboardButton(text="🎥 Просто красивое видео", callback_data="goal_video")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться в начало", callback_data="back_start")]
    ])

# ---------- HANDLERS ----------
@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "Привет 👋\n"
        "Ты в Distortion Production.\n\n"
        "Мы снимаем:\n"
        "— сниппеты\n"
        "— клипы\n"
        "— видео для соцсетей\n\n"
        "Помогаем артистам и инфлюенсерам делать контент,\n"
        "который реально даёт рост, а не просто лежит в ленте.\n\n"
        "Давай посмотрим, подойдём ли мы друг другу 🙂",
        reply_markup=start_kb()
    )

@dp.callback_query(lambda c: c.data == "start_form")
async def start_form(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(
        "Для начала познакомимся 🙂\nКто ты?",
        reply_markup=role_kb()
    )
    await state.set_state(Form.role)
    await cb.answer()

@dp.callback_query(lambda c: c.data.startswith("role_"))
async def role(cb: types.CallbackQuery, state: FSMContext):
    await state.update_data(role=cb.data.replace("role_", ""))
    await cb.message.answer(
        "Что ты сейчас хочешь снять?\n(Можно выбрать то, что ближе)",
        reply_markup=service_kb()
    )
    await state.set_state(Form.service)
    await cb.answer()

@dp.callback_query(lambda c: c.data.startswith("srv_"))
async def service(cb: types.CallbackQuery, state: FSMContext):
    await state.update_data(service=cb.data.replace("srv_", ""))
    await cb.message.answer(
        "А теперь важный момент 👇\n"
        "Какой результат для тебя самый ценный?",
        reply_markup=goal_kb()
    )
    await state.set_state(Form.goal)
    await cb.answer()

@dp.callback_query(lambda c: c.data.startswith("goal_"))
async def goal(cb: types.CallbackQuery, state: FSMContext):
    goal = cb.data.replace("goal_", "")

    if goal == "video":
        await cb.message.answer(
            "Спасибо, что написал честно 🤍\n\n"
            "Мы сейчас работаем в проектах,\n"
            "где важен рост и развитие артиста.\n\n"
            "Если позже захочется большего —\n"
            "будем рады пообщаться 🙂",
            reply_markup=back_kb()
        )
        await state.clear()
    else:
        await state.update_data(goal=goal)
        await cb.message.answer(
            "Напиши, пожалуйста, пару строк:\n"
            "— ссылка на твои соцсети\n"
            "— город\n"
            "— есть ли дедлайн (если да — какой)\n\n"
            "Без формальностей 🙂"
        )
        await state.set_state(Form.brief)

    await cb.answer()

@dp.message(Form.brief)
async def brief(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    text = (
        "🤍 Новая заявка — Distortion Production\n\n"
        f"👤 Кто: {data['role']}\n"
        f"🎬 Формат: {data['service']}\n"
        f"🎯 Цель: {data['goal']}\n\n"
        f"📝 Бриф:\n{msg.text}\n\n"
        f"📩 От: @{msg.from_user.username or msg.from_user.id}"
    )

    await bot.send_message(ADMIN_USERNAME, text)

    await msg.answer(
        "Готово 🙌\n"
        "Спасибо, что поделился.\n\n"
        "Мы посмотрим заявку и напишем тебе лично.\n"
        "Если будут вопросы — всё обсудим.\n\n"
        "Distortion Production 🤍\n"
        "Работаем под цель."
    )

    await state.clear()

@dp.callback_query(lambda c: c.data == "fit")
async def fit(cb: types.CallbackQuery):
    await cb.message.answer(
        "Мы подходим тебе, если:\n"
        "— ты артист или инфлюенсер\n"
        "— хочешь расти, а не просто выкладывать видео\n"
        "— готов работать с образом и идеей\n\n"
        "Если чувствуешь, что это про тебя —\n"
        "жми «Хочу съёмку» 🙂"
    )
    await cb.answer()

@dp.callback_query(lambda c: c.data == "format")
async def format_work(cb: types.CallbackQuery):
    await cb.message.answer(
        "Коротко о нас 👇\n\n"
        "Мы:\n"
        "— думаем как зритель\n"
        "— понимаем алгоритмы\n"
        "— уважаем путь артиста\n\n"
        "Поэтому каждый проект — индивидуальный.\n"
        "Стоимость обсуждаем после понимания задачи."
    )
    await cb.answer()

@dp.callback_query(lambda c: c.data == "back_start")
async def back_start(cb: types.CallbackQuery):
    await start(cb.message)
    await cb.answer()

# ---------- RUN ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
