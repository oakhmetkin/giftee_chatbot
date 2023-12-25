import json


__FILENAME = 'data.jsonl'


def save_answer(data, gpt_answer, products):
    try:
        obj = {
            'query': {
                'for': data['base_info'],
                'interests': data['deep_info'],
                'lifestyle': data['lifestyle_info'],
                'gift_type': data['gift_info'],
            },

            'gpt_answer': gpt_answer,

            'products': products,
        }

        with open(__FILENAME, 'a', encoding='utf-8') as f:
            f.write(json.dumps(obj))
            f.write('\n')
    except:
        pass
