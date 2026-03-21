import aiohttp
import bs4
import asyncio
import time
from googletrans import Translator

# Возвращает перевод слова с wooordhunt или None
async def get_translate_wooo(word):
    # Возвращает всю страницу с wooordhunt
    async def fetch_page(word):
        url = f'https://wooordhunt.ru/word/{word}'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    text = await response.text()
                    return bs4.BeautifulSoup(text, 'lxml')
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None
    # Парсит перевод со страницы
    def translate(soup):
        content = soup.find(class_='t_inline_en')
        if content: return content.text
        block = soup.find(class_='t_inline')
        if block: return block.text
        return None

    # Логика проверки
    if ' ' in word: return None
    word_page = await fetch_page(word)
    return translate(word_page)


# Возвращает перевод слова от google или None
async def get_translate_google(wood):
    translator = Translator()
    # Т.к язык не определен, то переводитья стразу на 2 языка
    resultEN = await translator.translate(wood, dest="en") # Русский -> Английский
    resultRU = await translator.translate(wood, dest="ru") # Английский -> Русский
    for translare in (resultEN.text, resultRU.text):
        # Возвращает не совпавший с вводом перевод
        if translare.lower() != wood.lower(): 
            return translare.lower()

# Основная функция перевода
async def get_translate(word):
    wooo_translate = await get_translate_wooo(word) # wooordhunt
    google_translate = await get_translate_google(word) # google
    return wooo_translate, google_translate

async def benchmark_async():
    words = ["hello", "world", "python", "test", "speed", "benchmark", "async", "parallel", "translate"]
    start_time = time.time()
    
    # Запускаем все переводы параллельно
    tasks = [get_translate(word) for word in words]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")
    return results

async def main():
    while True:
        word = input('Слово: ')
        res = await get_translate(word)
        print(res)

if __name__ == '__main__':
    asyncio.run(main())