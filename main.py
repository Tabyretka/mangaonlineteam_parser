from sys import exit
from asyncio import create_task, gather, run
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from os import path, makedirs
from time import time


async def get_urls(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    try:
        async with ClientSession() as session:
            tasks = []
            response = await session.get(url=url, headers=headers)
            if response.ok:
                soup = BeautifulSoup(await response.text(), 'lxml')
                title = soup.find('h1', id='chapter-heading').text.split(' - ')
                div_list = soup.find_all('div', class_='page-break')
                pics_list = [i.find('img').get('src').strip(' \n ') for i in div_list]
                if len(pics_list):
                    for url in pics_list:
                        task = create_task(save_pictures(url, title, session))
                        tasks.append(task)
                    await gather(*tasks)
    except Exception as ex:
        print(f'{ex}')
        exit(0)


async def save_pictures(url, title, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    try:
        file_name = url.split('/')[-1]
        async with session.get(url=url, headers=headers) as response:
            if not path.exists(f'data/{title[0]}/{title[-1]}'):
                makedirs(f'data/{title[0]}/{title[-1]}')
            with open(f'data/{title[0]}/{title[-1]}/{file_name}', 'wb') as picture:
                if response.ok:
                    picture.write(await response.read())
    except Exception as ex:
        print(f'{ex}')
        exit(0)


def main():
    if not path.exists('data'):
        makedirs('data')
    url = input('Insert link to volume.\n')
    start_time = time()
    run(get_urls(url))
    print('successfully saved to data folder')
    print(f"--- {time() - start_time} seconds ---")


if __name__ == '__main__':
    main()
