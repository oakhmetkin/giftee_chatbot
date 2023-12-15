from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from gpt_requester import ask_gpt, get_gift_names
import keyboards
from states import GiftRecState
from settings import TOKEN

from markets_parser import ParserWB


HTML_PM = ParseMode.HTML

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
parser = ParserWB()


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_help(message: Message, state: FSMContext):
    help_message = '''
Привет! Это чат-бот Giftee team. 
Мы поможем подобрать вам подарок
'''
    await GiftRecState.start.set()
    await message.answer(help_message, reply_markup=keyboards.start_markup, parse_mode=HTML_PM)


@dp.message_handler(state=GiftRecState.start)
async def quest1(message: Message, state: FSMContext):
    text = '''
<b>Расскажите, пожалуйста, о человеке, которому мы готовим подарок:</b>

1. Возраст и пол
2. Кто этот человек для вас (друг, член семьи, коллега, возлюбленный, просто знакомый)

<i>Примеры ответов: "Друг, 20 лет" или "Бабушка, 60 лет"</i>
'''
    await GiftRecState.base_quest.set()
    await message.answer(text, reply_markup=keyboards.none, parse_mode=HTML_PM)


@dp.message_handler(state=GiftRecState.base_quest)
async def quest2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['base_info'] = message.text

    text = '''
<b>Чтобы подобрать наилучший подарок, расскажите, что вы знаете об этом человеке:</b> 

1. Хобби и увлечения
2. Кем он работает?
3. На кого он учится?

<i>Пример ответа: "Хобби - коллекционировать монеты. Работает программистом. Учится на прикладного математика."</i>
'''
    await GiftRecState.next()
    await message.answer(text, parse_mode=HTML_PM)
    
    
@dp.message_handler(state=GiftRecState.deep_quest)
async def quest3(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['deep_info'] = message.text

    text = '''
<b>Какой у него образ жизни:</b> 

1. Активный образ жизни: Включает физическую активность, спорт, походы и заботу о здоровье. 
2. Спокойный образ жизни: Предпочтение уединению, чтению, расслаблению и тихим занятиям. 
3. Работящий образ жизни: Полная преданность работе, высокий уровень занятости и стремление к профессиональному росту. 
4. Эко-сознательный образ жизни: Забота о природе, экологические привычки, устойчивое потребленией 
5. Творческий образ жизни: Люди, посвятившие себя творчеству, искусству или музыке. 
6. Семейный образ жизни: Фокус на семье, забота о близких, время проведение в кругу родных и друзей. 
7. Путешественнический образ жизни: Люди, предпочитающие путешествия, новые культуры и приключения. 

<i>Пример ответа: "Активный"</i>
'''
    await GiftRecState.next()
    await message.answer(text, parse_mode=HTML_PM)
    
    
@dp.message_handler(state=GiftRecState.lifestyle_quest)
async def quest4(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['lifestyle_info'] = message.text

    text = '''
<b>Теперь давайте выберем подарок!!!</b>

1. На какой праздник подбираем подарок (Новый год, День рождения, др.) 
2. Какой тип подарка вы ищете (полезный, запоминающийся)

<i>Пример ответа: "Запоминающийся подарок на новый год"</i>
'''
    await GiftRecState.next()
    await message.answer(text, parse_mode=HTML_PM)
    
    
@dp.message_handler(state=GiftRecState.gift_desc)
async def quest5(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['gift_info'] = message.text

    text = '''
<b>Введите одно целое число - ваш бюджет</b>

<i>Пример ответа: "2500"</i>
'''
    await GiftRecState.next()
    await message.answer(text, parse_mode=HTML_PM)
    
    
@dp.message_handler(state=GiftRecState.budget)
async def quest6(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['budget_info'] = int(message.text)
        except:
            await message.answer('''
<b>Введите одно целое число - ваш бюджет</b>

<i>Пример ответа: "2500"</i>
''', parse_mode=HTML_PM)
            return

    query = f'''
Кому: {data['base_info']}
Интересы: {data['deep_info']}
Образ жизни: {data['lifestyle_info']}
Тип подарка: {data['gift_info']}
Бюджет: {data['budget_info']}
'''

    text = f'''
<b>Отлично! А теперь проверьте запрос:</b>
{query}
Если все верно, то нажмите "OK", иначе "Начать заново".
'''
    await GiftRecState.next()
    await message.answer(text, reply_markup=keyboards.check_markup, parse_mode=HTML_PM)
    
    
@dp.message_handler(state=GiftRecState.check)
async def quest_final(message: Message, state: FSMContext):
    msg = message.text

    if msg == 'OK':
        await message.answer('Ищу подарки...', reply_markup=keyboards.none, parse_mode=HTML_PM)
        
        query = { }
        async with state.proxy() as data:
            for key in ['base', 'deep', 'lifestyle', 'gift', 'budget']:
                query[key + '_info'] = data[key + '_info']

        try:
            gpt_answer = ask_gpt(query)
            gift_names = get_gift_names(gpt_answer)
            links = parser.get_links(gift_names)
            links_as_str = '\n'.join(links)
            answer = f'{gpt_answer}\n\nКупить подарки можно здесь:\n{links_as_str}'

            await message.answer(answer, parse_mode=HTML_PM)
        except:
            await message.answer('Не удалось получить подарки 😔\nПопробуйте позже')
        finally:
            await state.finish()
    else:
        await GiftRecState.start.set()
        await message.answer('Хорошо, начнем заново!', reply_markup=keyboards.none, parse_mode=HTML_PM)
        await send_help(message, state)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
