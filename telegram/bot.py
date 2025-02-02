from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Токен, который ты получила от BotFather
TOKEN = '7410371015:AAHmxJzeg__QGnndUDzx5EOkdwGl4w9TPck'

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я твой новый бот. Как дела?')

# Обработчик текстовых сообщений
async def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    await update.message.reply_text(f'Вы сказали: {user_message}')

# Функция запуска бота
def main() -> None:
    # Создаем Application и передаем ему токен бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
