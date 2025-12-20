from aiogram import Router, F, types

router = Router()


@router.message(F.text == "🆘 Поддержка")
async def support_handler(message: types.Message):
    await message.answer(
        "🆘 Поддержка\n\n"
        "Если у вас возникли вопросы — напишите администратору."
    )


@router.message(F.text == "📖 Инструкция")
async def instruction_handler(message: types.Message):
    await message.answer(
        "📖 Инструкция\n\n"
        "1. Установите Outline Client\n"
        "2. Получите VPN-ключ после оплаты\n"
        "3. Добавьте ключ в приложение\n"
        "4. Подключитесь к серверу"
    )