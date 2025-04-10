#     Напишите программу, которая запрашивает у пользователя URL-адрес веб-страницы, использует библиотеку 
# Beautiful Soup для парсинга HTML и выводит список всех ссылок на странице.
from bs4 import BeautifulSoup
import requests

def print_links(url = "https://www.wikipedia.org/"):
    response = requests.get(url)  #с помощью библиотеки requests обрабатываем полученные данные
    soup = BeautifulSoup(response.text, 'html.parser') #Варим суп :) на основе HTML текста
    for link in soup.find_all('a'): #используем цикл и метод find_all чтобы найти все гиперссылки
        href = link.get('href')
        if href.startswith('//'): #обрабатываем ссылки которые начинаются с // чтобы в консоли они начинались с https и правильно отображались
            href = 'https:' + href
            print(href)  # Выводим ссылку

        

# webpage = input("enter the URL: ") # просим юзера ввести вдрем вебсайта
# print_links(webpage)
print_links()


#     Напишите программу, которая запрашивает у пользователя URL-адрес веб-страницы и уровень заголовков, а 
# затем использует библиотеку Beautiful Soup для парсинга HTML и извлекает заголовки нужного уровня 
# (теги h1, h2, h3 и т.д.) с их текстом.



def select_headers(url, header_lvl = 'h1'): 
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, 'html.parser') 
    for header in soup.find_all(header_lvl): 
        print(header.get_text())


link = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
select_headers(link)

# link = input(f"enter the URL: ")
# header = input(f"enter the header level: ")
# select_headers(link, header)
