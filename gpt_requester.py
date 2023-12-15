from openai import OpenAI
import re

from settings import OPENAI_API_KEY


__li = re.compile(r'\[(.+)\]')

client = OpenAI(
  api_key=OPENAI_API_KEY,
)


def ask_gpt(data):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты - мастер подбора подарков. Ты выдаешь все ответы в виде нумерованного списка (всегда 5 пунктов). Название подарка ты заключаешь в квадратные скобки."},
            {"role": "user", "content": f'''Сейчас я расскажу тебе о человеке, твоей задачей будет подобрать идеальный подарок для него.

Кому: {data['base_info']}
Интересы: {data['deep_info']}
Образ жизни: {data['lifestyle_info']}
Тип подарка: {data['gift_info']}
'''}
        ]
    )

    return completion.choices[0].message.content


def get_gift_names(text: str):
    result = []

    for line in text.split('\n'):
        subs = __li.findall(line)

        if subs:
            result.append(subs[0])
    
    return result
