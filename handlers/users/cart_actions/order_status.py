from aiogram import types

from loader import db
from localization.i18n import order_status
from router import router


@router.callback_query(lambda call: "check-status" in call.data)
async def show_order_status(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)
    user = db.get_user(call.from_user.id)
    order = db.get_user_order(user.get("id"))
    await call.answer(text=f"{order_status.get(order.get('status')).get(lang)}", show_alert=True)
