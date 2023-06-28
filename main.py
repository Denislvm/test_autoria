from bs4 import BeautifulSoup
import requests
import time
import json

main_url = "https://auto.ria.com/uk/search/?categories.main.id=1&brand.id[0]=79&model.id[0]=2104&indexName=auto,order_auto,newauto_search&country.import.usa.not=0&damage.not=0"

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}


def get_soup(url):
    response = requests.get(url=url, headers=headers)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    return BeautifulSoup(response.text, 'html.parser')


# url2 = "https://auto.ria.com/uk/search/?categories.main.id=1&brand.id[0]=79&model.id[0]=2104&indexName=auto,order_auto,newauto_search&country.import.usa.not=0&damage.not=0&page=1"
def collect_cars():
    current_page = 1
    last_page = None
    current_url = main_url
    cars_list = []


    while True:

        # url = f"https://auto.ria.com/uk/search/?categories.main.id=1&brand.id[0]=79&model.id[0]=2104&indexName=auto,order_auto,newauto_search&country.import.usa.not=0&damage.not=0&page={current_page}"
        soup = get_soup(current_url)
        all_cars = soup.findAll('div', class_='content')
        for car in all_cars:
            link = car.find('a').get('href')
            # print(link)
            sub_car = get_soup(link)
            car_page = sub_car.findAll('div', class_='ticket-status-0')
            for car1 in car_page:
                mark = car1.find('h1', class_='head').text
                price = car1.find('div', class_='price_value').text
                mileage = car1.find('div', class_='base-information bold').text
                place = car1.find('div', class_='item_inner').text

                # print(link, '\n', mark, '\n', price, '\n', mileage, '\n', place, '\n')
                cars_dict = {
                            'link': link,
                            'mark': mark,
                            'price': price,
                            'mileage': mileage,
                            'place': place
                            }
                cars_list.append(cars_dict)


        if last_page is None:
            last_page_element = soup.find('span', class_='page-item.last')
            if last_page_element is not None:
                last_page = int(last_page_element.find('a').text)

        if current_url == main_url:
            current_url = f"{main_url}&page={current_page}"
        elif current_page == last_page:
            # Достигнута последняя страница
            break
        else:
            current_url = f"{main_url}&page={current_page}"

        current_page += 1
        # with open('result.json', 'w') as file:
        #     json.dump(cars_list, file, ensure_ascii=False, indent=4)

        # when project will over, this parametr will 600 millisec
        # time.sleep(600)


def main():
    collect_cars()


if __name__ == "__main__":
    main()
