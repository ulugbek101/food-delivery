from aiogram import types

from loader import db
from localization.i18n import order_status
from router import router


@router.callback_query(lambda call: "check-order-status" in call.data)
async def show_order_status(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)
    order_id = int(call.data.split(":")[-1])
    order = db.get_user_order(order_id)
    await call.answer(text=f"{order_status.get(order.get('status')).get(lang)}", show_alert=True)
