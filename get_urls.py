import requests
from bs4 import BeautifulSoup as bs

url = 'https://minecraftrating.ru'


def get_max_pages():
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    pagination = soup.find('ul', {'class': 'pagination'})
    all_pages = pagination.find_all('li')
    max_pages = int(all_pages[len(all_pages) - 2].text)
    get_servers(max_pages)


def get_servers(max_pages):
    with open('urls.txt', 'w') as f:
        r = requests.get(url)
        print(str(r.status_code) + f'[{1}]')
        soup = bs(r.text, 'html.parser')
        links = soup.find_all('a', {'itemprop': 'url'})
        for link in links:
            f.write(url + link['href'] + '\n')
        for i in range(2, max_pages+1):
            r = requests.get(url + f'/page/{str(i)}/')
            print(str(r.status_code) + f'[{str(i)}]')
            soup = bs(r.text, 'html.parser')
            links = soup.find_all('a', {'itemprop': 'url'})
            for link in links:
                f.write(url + link['href'] + '\n')


if __name__ == "__main__":
    get_max_pages()
