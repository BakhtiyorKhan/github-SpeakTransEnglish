
import logging
from oxfordLookUp import getDefinitions
from googletrans import Translator


from aiogram import Bot, Dispatcher, executor, types

translator = Translator()

API_TOKEN = '5399002324:AAHNF8oGlWGUi0wKJ41yrgbOdzbvmhs2ilc'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):

    await message.reply("Speak English botiga xush kelibsiz.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Speak English botida siz zo'zlarni topishingiz mumkin!")


@dp.message_handler()
async def tarjimon(message: types.Message):

    lang = translator.detect(message.text).lang
    # Bu yerda ikki so'zdan ko'pligi tekshiriladi
    if len(message.text.split()) > 2:
        dest = 'uz' if lang =='en' else 'en'
        await message.reply(translator.translate(message.text,dest).text)
    else:
        if lang =='en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text,dest='en').text
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)