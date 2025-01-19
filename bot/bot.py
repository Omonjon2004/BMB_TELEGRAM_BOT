import asyncio
import logging
import os
import sys
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.dispatcher.router import Router
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

lang_data = {
    "uz": {
        "start": "Xush kelibsiz BMB Holding ga! Quyida menyudan kerakli bo‘limni tanlang:",
        "product_info": "🛍️ Mahsulot haqida ma’lumot",
        "company_info": "🏢 Kompaniya haqida",
        "order_product": "📦 Buyurtma berish",
        "view_cart": "🛒 Savatni ko‘rish",
        "language_choice": "Iltimos, tilni tanlang:",
        "uzbek": "🇺🇿 O‘zbekcha",
        "russian": "🇷🇺 Русский",
        "english": "🇬🇧 English",
        "company_details": "BMB Holding zamonaviy biznes markazi bo‘lib, turli xizmatlarni taklif qiladi. Batafsil ma’lumot uchun havolani bosing.",
        "web_link": "🌐 Kompaniya web-sayti",
        "back": "🔙 Orqaga"
    },
    "ru": {
        "start": "Добро пожаловать в BMB Holding! Выберите нужный раздел из меню ниже:",
        "product_info": "🛍️ Информация о продукции",
        "company_info": "🏢 О компании",
        "order_product": "📦 Оформить заказ",
        "view_cart": "🛒 Просмотр корзины",
        "language_choice": "Пожалуйста, выберите язык:",
        "uzbek": "🇺🇿 O‘zbekcha",
        "russian": "🇷🇺 Русский",
        "english": "🇬🇧 English",
        "company_details": "BMB Holding - современный бизнес-центр, предлагающий широкий спектр услуг. Нажмите на ссылку, чтобы узнать больше.",
        "web_link": "🌐 Сайт компании",
        "back": "🔙 Назад"
    },
    "en": {
        "start": "Welcome to BMB Holding! Choose the desired section from the menu below:",
        "product_info": "🛍️ Product Information",
        "company_info": "🏢 About the Company",
        "order_product": "📦 Place an Order",
        "view_cart": "🛒 View Cart",
        "language_choice": "Please choose a language:",
        "uzbek": "🇺🇿 O‘zbekcha",
        "russian": "🇷🇺 Русский",
        "english": "🇬🇧 English",
        "company_details": "BMB Holding is a modern business center offering various services. Click the link to learn more.",
        "web_link": "🌐 Company Website",
        "back": "🔙 Back"
    }
}

user_language = {}
user_state = defaultdict(list)  # Foydalanuvchi holatini saqlash

# Foydalanuvchi holatini yangilash
def update_user_state(user_id, new_state):
    if user_state[user_id] and user_state[user_id][-1] == new_state:
        return
    user_state[user_id].append(new_state)

# Foydalanuvchini oldingi holatga qaytarish
def go_back(user_id):
    if user_state[user_id]:
        user_state[user_id].pop()
    return user_state[user_id][-1] if user_state[user_id] else "language_choice"

# Tilni tanlash klaviaturasi
def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang_data["uz"]["uzbek"], callback_data="lang_uz")],
        [InlineKeyboardButton(text=lang_data["uz"]["russian"], callback_data="lang_ru")],
        [InlineKeyboardButton(text=lang_data["uz"]["english"], callback_data="lang_en")]
    ])

# Asosiy menyu klaviaturasi
def menu_keyboard(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang_data[lang]["product_info"], callback_data="product_info")],
        [InlineKeyboardButton(text=lang_data[lang]["company_info"], callback_data="company_info")],
        [InlineKeyboardButton(text=lang_data[lang]["order_product"], callback_data="order_product")],
        [InlineKeyboardButton(text=lang_data[lang]["view_cart"], callback_data="view_cart")],
        [InlineKeyboardButton(text=lang_data[lang]["back"], callback_data="back_to_main")]
    ])

@router.message(CommandStart())
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name or "Foydalanuvchi"
    welcome_message = f"Assalomu alaykum, {user_name}! {lang_data['uz']['language_choice']}"
    update_user_state(message.from_user.id, "language_choice")
    await message.answer(welcome_message, reply_markup=language_keyboard())

@router.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    lang = user_language.get(user_id, "uz")

    if data.startswith("lang_"):
        selected_lang = data.split("_")[1]
        user_language[user_id] = selected_lang
        lang = selected_lang
        update_user_state(user_id, "main_menu")
        welcome_text = lang_data[lang]["start"]
        keyboard = menu_keyboard(lang)
        await callback_query.message.edit_text(welcome_text, reply_markup=keyboard)

    elif data == "back_to_main":
        previous_state = go_back(user_id)
        if previous_state == "language_choice":
            welcome_text = lang_data["uz"]["language_choice"]
            keyboard = language_keyboard()
        elif previous_state == "main_menu":
            welcome_text = lang_data[lang]["start"]
            keyboard = menu_keyboard(lang)
        await callback_query.message.edit_text(welcome_text, reply_markup=keyboard)

    elif data == "company_info":
        update_user_state(user_id, "company_info")
        url_mapping = {
            "uz": "https://bmb-holding.uz/kompaniya-haqida/",
            "ru": "https://bmb-holding.uz/o-kompanii/",
            "en": "https://bmb-holding.uz/about-us/"
        }
        url = url_mapping.get(lang, "https://bmb-holding.uz/")
        web_link_text = lang_data[lang]["web_link"]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=web_link_text, url=url)],
            [InlineKeyboardButton(text=lang_data[lang]["back"], callback_data="back_to_main")]
        ])
        company_details = lang_data[lang]["company_details"]
        await callback_query.message.edit_text(company_details, reply_markup=keyboard)

    await callback_query.answer()

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.include_router(router)
    await bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam olish")
    ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
