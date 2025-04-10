# 1. Напишите функцию get_response(url), которая отправляет GET-запрос по заданному URL-адресу и 
# возвращает объект ответа. Затем выведите следующую информацию об ответе:
# - Код состояния (status code)
# - Текст ответа (response text)
# - Заголовки ответа (response headers)

# Пример использования:

# url = "https://api.example.com"
# response = get_response(url)
# print("Status Code:", response.status_code)
# print("Response Text:", response.text)
# print("Response Headers:", response.headers)

import requests

def get_response(link):
    try:
        response = requests.get(link)
        return response
    except requests.exceptions.RequestException as e:
        print(f"There was an ERROR: {e}")


# url = "https://api.example.com"
url = "https://httpbin.org/"
response = get_response(url)

if response:
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print("Response Headers:", response.headers)







# 2. Напишите функцию find_common_words(url_list), которая принимает список URL-адресов и 
# возвращает список наиболее часто встречающихся слов на веб-страницах. Для каждого URL-адреса 
# функция должна получить содержимое страницы с помощью запроса GET и использовать регулярные 
# выражения для извлечения слов. Затем функция должна подсчитать количество вхождений каждого 
# слова и вернуть наиболее часто встречающиеся слова в порядке убывания частоты.

import re
from collections import Counter
def find_common_words(url_list, top_n = 10):
    all_words = []
    for url in url_list:
        response = requests.get(url)

        text = re.sub(r'<script.*?</script>', '', response.text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'&[a-zA-Z0-9]+;', '', text) # Удаление HTML-сущностей


        words = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]+\b', text.lower())
        all_words.extend(words)
    
    word_counts = Counter(all_words)

    most_common = word_counts.most_common(top_n)
    return most_common

urls_to_analyze = [
    "https://www.example.com",
    "https://ru.wikipedia.org/wiki/%D0%9F%D0%B8%D1%82%D0%BE%D0%BD_(%D1%8F%D0%B7%D1%8B%D0%BA_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)"
]
common_words = find_common_words(urls_to_analyze, top_n=10)
print("Наиболее часто встречающиеся слова на указанных веб-страницах:")
for word, count in common_words:
    print(f"- {word}: {count}")
