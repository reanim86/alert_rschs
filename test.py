import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота от @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = '@belgorod01'  # ID канала


async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка постов из канала"""
    if update.channel_post:
        message = update.channel_post

        print(f"\nНовый пост в канале:")
        print(f"ID сообщения: {message.message_id}")
        print(f"Дата: {message.date}")
        print(f"Текст: {message.text}")

        # Сохраняем сообщение в файл
        with open('channel_messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"ID: {message.message_id}\n")
            f.write(f"Дата: {message.date}\n")
            f.write(f"Текст: {message.text}\n")
            f.write("-" * 50 + "\n")


async def get_channel_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о канале по команде"""
    try:
        chat = await context.bot.get_chat(CHANNEL_ID)
        print(f"Информация о канале:")
        print(f"Название: {chat.title}")
        print(f"ID: {chat.id}")
        print(f"Тип: {chat.type}")
        print(f"Описание: {chat.description}")

        await update.message.reply_text(f"Информация о канале получена, проверьте консоль")

    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {e}")


def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(MessageHandler(filters.UpdateType._ChannelPost, handle_channel_post))

    # Команда для получения информации о канале
    from telegram.ext import CommandHandler
    application.add_handler(CommandHandler("channel_info", get_channel_info))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()