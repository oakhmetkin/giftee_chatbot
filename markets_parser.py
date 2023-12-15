from typing import List
import requests

class ParserWB:
    def __init__(self):
        self.params = {
            'TestGroup': 'no_test',
            'TestID': 'no_test',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '27',
            'suppressSpellcheck': 'false'
        }

    def parse(self, query, count, min_price=0, max_price=9999999):
        product_links = []
        page = 1
        while count > 0:
            params = self.params
            params['query'] = query
            if page != 1:
                params['page'] = str(page)

            if count >= 300:
                params['limit'] = '300'
            else:
                params['limit'] = str(count)

            # возможно надо подождать перед запросом

            response = requests.get(f'https://search.wb.ru/exactmatch/ru/common/v4/search?priceU={min_price*100};{max_price*100}', params=params)

            if response.status_code == 200:
                resp_json = response.json()
                products = resp_json['data']['products']
                for i in range(len(products)):
                    product_links.append((self.__create_link(products[i]['id']), products[i]['name'], int(products[i]['salePriceU']) // 100))
                count -= len(products)
            else:
                print("Ошибка при запросе к сайту WB")
            page += 1

        return product_links

    def get_links(self, names: List[str], min_price=0, max_price=9999999):
        '''
        Returns links to goods

        Params:
            names: list of goods names
        '''
        links = []
        for name in names:
            links += self.parse(name, 3, min_price, max_price)

        return links

    def __create_link(self, id):
        return f"https://www.wildberries.ru/catalog/{id}/detail.aspx"
