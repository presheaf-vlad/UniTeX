import unicodeitplus
import hashlib
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hlink

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6812363457:AAEG8Uq9q9pO0HtHsx-36fUCZ_7j5rrl2J8")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    photo=FSInputFile('input.png')
    await message.answer("Салют! \nЯ бот, который умеет конвертировать ваш TeX-код в обычный unicode-текст. С моей помощью ты можешь отправлять несложные формулы в любом чате! Для этого вызови меня и напиши что-то вроде этого:")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('И получится вот что:\n' + unicodeitplus.parse('Рассмотрим $f: X\\to Y$ $-$ гладкое отображение'))

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer("<b>1</b>. Если я не хочу обрабатывать ваш текст, то проверьте корректность формулы, в частности, количество знаков '$'."
                         +"\n\n<b>2</b>. Я не умею генерировать текст или pdf-файлы, для этого используйте @InLaTeXbot."
                         +"\n\n<b>3</b>. Список всевозможных символов, которые я могу обработать <b><a href='https://en.wikipedia.org/wiki/Mathematical_operators_and_symbols_in_Unicode'>тут</a></b>.", parse_mode='html')

@dp.message(Command("examples"))
async def cmd_examples(message: types.Message):
    await message.answer("<b>Вот несколько примеров</b>:\n"
                         +"\n <I>Ввод</I>: \nПредпучком множеств $\mathcal{F}$ на категории $\mathcal{C}$ называют контравариантный функтор $\mathcal{F}: \mathcal{C}\\to Sets$" 
                         +"\n <I>Вывод</I>:\n"+unicodeitplus.parse('Предпучком множеств $\mathcal{F}$ на категории $\mathcal{C}$ называют контравариантный функтор $\mathcal{F}: \mathcal{C}\\to$ Sets')
                         +"\n\n <I>Ввод</I>:\nСкорость света равна $c=3\\times 10^{8}$"
                         +"\n <I>Вывод</I>:\n"+unicodeitplus.parse('Скорость света равна $c=3\\times 10^{8}$')
                         +"\n\n <I>Ввод</I>: \n Последовательность пучков $0 \\to \mathcal{F} \\to \\mathcal{G} \\to \\mathcal{H} \\to 0$ на $X$ точна $\Leftrightarrow$ $0 \\to \mathcal{F}_x \\to \\mathcal{G}_x \\to mathcal{H}_x \\to 0$ точна $\\forall x \\in X$"
                         +"\n <I>Вывод</I>:\n"+unicodeitplus.parse('Последовательность пучков $0 \\to \mathcal{F} \\to \\mathcal{G} \\to \\mathcal{H} \\to 0$ на $X$ точна $\Leftrightarrow$ $0 \\to \mathcal{F}_x \\to \\mathcal{G}_x \\to \\mathcal{H}_x \\to 0$ точна $\\forall x \\in X$'), parse_mode='html')
    
@dp.message(Command("links"))
async def cmd_links(message: types.Message):
    await message.answer("<b>Полезные ссылки:</b>\n"
                         +"\n 1. <b><a href='https://en.wikipedia.org/wiki/Mathematical_operators_and_symbols_in_Unicode'>Доступные символы в Unicode</a></b>" 
                         +"\n 2. <b><a href='https://detexify.kirelabs.org/classify.html'>Распознать знак</a></b>"
                         +"\n 3. @InLaTeXbot - бот, который умеет делать pdf-файлы и картинки из вашего кода"
                         +"\n 4. <b><a href='https://old.mccme.ru//free-books//llang/newllang.pdf'>Книжка о ТеХе</a></b>", parse_mode='html')

async def main():
    await dp.start_polling(bot)

@dp.message()
async def UniTeX(message: types.Message):
    await message.answer(unicodeitplus.parse(message.text))

@dp.inline_query()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'UniTeX'
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id = result_id,
        title = unicodeitplus.parse(text),
        input_message_content=types.InputTextMessageContent(message_text=unicodeitplus.parse(text)))]
    await query.answer(articles, cache_time=1, is_personal=True)


if __name__ == "__main__":
    asyncio.run(main())