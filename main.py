from bs4 import BeautifulSoup
import requests
import time

main_url = "https://auto.ria.com/uk/search/?categories.main.id=1&brand.id[0]=79&model.id[0]=2104&indexName=auto,order_auto,newauto_search&country.import.usa.not=0&damage.not=0"

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}


def get_soup(url):
    response = requests.get(url=url, headers=headers)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    return BeautifulSoup(response.text, 'html.parser')


def parse_process():
    while True:
        page = get_soup(main_url)
        all_cars = page.findAll('div', _class='content')
        for car in all_cars:
            link = car.find('a', _class='js-newAutoInformerLink address')

            print(link)

        # when project will over, this parametr will be 600 millisec
        # time.sleep(600)


n = parse_process()
print(n)



