import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import adafruit_dht

class TelegramBot:
    def __init__(self, token, bot_username):
        self.TOKEN = token
        self.BOT_USERNAME = bot_username
        self.app = Application.builder().token(self.TOKEN).build()

        self.app.add_handler(CommandHandler('start', self.start_command))
        self.app.add_handler(CommandHandler('help', self.help_command))
        self.app.add_handler(CommandHandler('custom', self.custom_command))

        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        self.app.add_error_handler(self.error)

    async def start_command(self, update, context):
        await update.message.reply_text('StartTest')

    async def help_command(self, update, context):
        await update.message.reply_text('helpTest')

    async def custom_command(self, update, context):
        await update.message.reply_text('customTest')

    def handle_response(self, text):
        processed = text.lower()

        if 'hello' in processed:
            return 'Hey there!'
        if 'how are you' in processed:
            return 'I am good'

        return 'I do not understand what you wrote...'

    async def handle_message(self, update, context):
        message_type = update.message.chat.type
        text = update.message.text

        print(f'User({update.message.id}) in {message_type}: {text}"')

        if message_type == 'group':
            if self.BOT_USERNAME in text:
                new_text = text.replace(self.BOT_USERNAME, '').strip()
                response = self.handle_response(new_text)
                print('Bot:', response)
                await update.message.reply_text(response)

    async def error(self, update, context):
        print(f'Update {update} caused error {context.error}')

    def run(self):
        print('Starting bot...')
        self.app.run_polling(poll_interval=1)

class Sensor:
    def __init__(self, gpio_pin):
        self.GPIO_PIN = gpio_pin
        self.am2302 = adafruit_dht.DHT22(self.GPIO_PIN)

    async def read_humidity(self):
        while True:
            try:
                humidity_percent = self.am2302.humidity
                print(f"Luftfeuchtigkeit: {humidity_percent}%")
            except RuntimeError as e:
                print(f"Fehler beim Lesen des Sensors: {e}")

            await asyncio.sleep(1)

async def main():
    TOKEN = 'DeinTelegramBotToken'
    BOT_USERNAME = 'DeinBotUsername'
    GPIO_PIN = 17

    bot = TelegramBot(TOKEN, BOT_USERNAME)
    sensor = Sensor(GPIO_PIN)

    await asyncio.gather(
        bot.run(),
        sensor.read_humidity()
    )

if __name__ == '__main__':
    asyncio.run(main())







