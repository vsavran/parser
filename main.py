import requests
from bs4 import BeautifulSoup
import json

class HtmlData():
    def __init__(self, headers, host):
        self.headers = headers
        self.host = host

    def get_data(self, url, params={'page': 1}):
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code == 200:
            self._html = res.text
        else:
            print('Error Happened')


class Soup(HtmlData):
    def __init__(self, headers, hosr):
        super().__init__(headers, hosr)

    def create_soup(self):
        self.soup = BeautifulSoup(self._html, 'html.parser')

    def get_pages_count(self):
        max_num = 0
        if hasattr(self, 'soup'):
            for item in self.soup.find_all('a', class_='page-link'):
                found_number = item.get_text()
                if (found_number.isdigit() and int(found_number) > max_num):
                    max_num = int(found_number)
            self.max_num = max_num
        else:
            print('Please call get_data method')


class Parser(Soup):
    def parseHtml(self, tag, className, params):
        self.get_data(URL)
        self.create_soup()
        self.get_pages_count()
        new_list = []
        for item in range(1, self.max_num + 1):
            print(f'Parsing page: {item}')
            self.get_data(URL, {'page': item})
            self.create_soup()
            data = self.soup.find_all(tag, class_=className)
            for item in data:
                new_list.append(params(item, self))
            self.parsed_list = new_list


URL = 'https://auto.ria.com/uk/newauto/marka-mitsubishi/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
    'accept': '*/*'
}
HOST = 'https://auto.ria.com'


def new_params(item, self):
    return {
        'title': item.find('h3', class_='proposition_name').get_text(strip=True),
        'usd_price': item.find('div', class_='mt-5 proposition_bottom').find_next('span').get_text(
            strip=True),
        'ua_price': item.find('span', class_='grey size13').get_text(),
        'link': self.host + item.find('h3', class_='proposition_name').find_next('a').get('href'),
        'city': item.find('div', class_='proposition_region size13').find_next('strong').get_text(
            strip=True)
    }


parser = Parser(HEADERS, HOST)
parser.parseHtml('div', "proposition_area", new_params)
print(parser.parsed_list)

with open('personal.json', 'w') as json_file:
    json.dump(parser.parsed_list, json_file)
