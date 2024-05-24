from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext

from localization.i18n import main_menu_title, settings_title, back_button_text
from router import router
from loader import db, bot
from keyboards.reply.main_menu import generate_main_menu
from keyboards.reply.settings_menu import generate_settings_menu
from keyboards.inline.subcategories_menu import generate_subcategories_menu
from keyboards.inline.categories_menu import generate_categories_menu
from keyboards.inline.root_menu import generate_root_menu
from handlers.users.cart_actions.cart_overall import show_cart
from handlers.users.buy import start_shipping


@router.message(F.text.in_(back_button_text.values()))
async def back(message: types.Message, state: FSMContext):
    # Clear any state before returning user back to his/her last step
    await state.clear()

    user = db.get_user(message.from_user.id)
    lang = user.get("language_code")
    last_visited_place = user.get("last_visited_place")

    if last_visited_place == "main_menu":
        await message.answer(f"<b>{main_menu_title.get(lang)}</b>", reply_markup=generate_main_menu(lang))

    elif last_visited_place == "settings_menu":
        await message.answer(f"<b>{settings_title.get(lang)}</b>", reply_markup=generate_settings_menu(lang))
        db.update_last_step(message.from_user.id, "main_menu")

    elif last_visited_place == "cart":
        message_id = message.message_id
        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id - 1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id - 2)
        await message.answer(text=f"<b>{main_menu_title.get(lang)}</b>", reply_markup=generate_main_menu(lang))
        await message.answer_photo(
            photo="https://static.vecteezy.com/system/resources/previews/017/722/096/non_2x/cooking-cuisine-cookery-logo-restaurant-menu-cafe-diner-label-logo-design-illustration-free-vector.jpg",
            reply_markup=generate_root_menu(lang)
        )
        db.update_last_step(message.from_user.id, "main_menu")

    elif last_visited_place == "cart_overall":
        await show_cart(message)


@router.callback_query(lambda call: "back" in call.data)
async def inline_back(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)
    action = call.data.split(":")
    destination = action[1]

    await call.message.delete()

    if destination == "to-cat":
        category_id = action[-1]
        category = db.get_category(category_id)

        if category.get('category_id'):
            subcategories = db.get_subcategories(category.get('category_id'))
            photo = db.get_category(category.get('category_id')).get('photo')
            await call.message.answer_photo(photo=f"{photo}",
                                            reply_markup=generate_subcategories_menu(lang=lang,
                                                                                     subcategories=subcategories,
                                                                                     category_id=category[
                                                                                         'category_id']))
        else:
            categories = db.get_categories(target=category.get("belongs_to"))
            await call.message.answer_photo(
                photo="https://static.vecteezy.com/system/resources/previews/017/722/096/non_2x/cooking-cuisine-cookery-logo-restaurant-menu-cafe-diner-label-logo-design-illustration-free-vector.jpg",
                reply_markup=generate_categories_menu(lang=lang, categories_list=categories))
