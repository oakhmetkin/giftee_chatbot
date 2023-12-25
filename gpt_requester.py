from openai import OpenAI
import re
from datetime import datetime, timedelta

from settings import OPENAI_API_KEY


__TWENTY_SECONDS = timedelta(seconds=20)

GPT_STATUSES = {
    0: 'OK',
    1: 'MINUTE_LIMIT_EXCEEDED',
    2: 'DAY_LIMIT_EXCEEDED',
}

MAX_DAY_REQUESTS_COUNT = 200

__li = re.compile(r'\[(.+)\]')

__client = OpenAI(
  api_key=OPENAI_API_KEY,
)

__last_call = datetime.now()
__day_calls = []


def ask_gpt(data: dict) -> (bool, str):
    global __last_call, __day_calls

    if len(__day_calls) >= MAX_DAY_REQUESTS_COUNT:
        __day_calls = [
            c for c in __day_calls if __last_call - c > timedelta(days=1)
        ]
        if len(__day_calls) >= MAX_DAY_REQUESTS_COUNT:
            return 2, ''
        else:
            return ask_gpt(data)
    elif datetime.now() - __last_call < __TWENTY_SECONDS:
        return 1, ''
    
    __last_call = datetime.now()

    completion = __client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты - мастер подбора подарков! Ты выдаешь все ответы в виде нумерованного списка (всегда 5 пунктов). Название подарка ты заключаешь в квадратные скобки."},
            {"role": "user", "content": f'''Сейчас я расскажу тебе о человеке, твоей задачей будет подобрать идеальный подарок для него.

Кому: {data['base_info']}
Интересы: {data['deep_info']}
Образ жизни: {data['lifestyle_info']}
Тип подарка: {data['gift_info']}
'''}
        ]
    )

    __last_call = datetime.now()
    __day_calls.append(__last_call)

    return 0, completion.choices[0].message.content


def get_gift_names(text: str):
    result = []

    for line in text.split('\n'):
        subs = __li.findall(line)

        if subs:
            result.append(subs[0])
    
    return result
