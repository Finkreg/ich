#     Напишите функцию extract_emails(text), которая извлекает все адреса электронной почты из заданного текста и возвращает их в виде списка.
# Пример использования:
# text = "Contact us at info@example.com or support@example.com for assistance."
# emails = extract_emails(text)
# print(emails)  # Вывод: ['info@example.com', 'support@example.com']

import re

def extract_emails(data):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_adresses = re.findall(email_pattern, data)
    return email_adresses

text = "Contact us at info@example.com or support@example.com for assistance."
emails = extract_emails(text)
print(emails)  



#     Напишите функцию highlight_keywords(text, keywords), которая выделяет все вхождения заданных ключевых слов в тексте, окружая их символами *. 
# Функция должна быть регистронезависимой при поиске ключевых слов.

# Пример использования:
# text = "This is a sample text. We need to highlight Python and programming."
# keywords = ["python", "programming"]
# highlighted_text = highlight_keywords(text, keywords)
# print(highlighted_text)
# # Вывод: "This is a sample text. We need to highlight *Python* and *programming*."


def highlight_keywords(text, keywords):
    pattern = r'(' + '|'.join(re.escape(word) for word in keywords) + r')'
    print(pattern)
    highlighted_text = re.sub(pattern, r'*\1*', text, flags=re.IGNORECASE)
    return highlighted_text



text = "This is a sample text. We need to highlight Python and programming."
keywords = ["python", "programming"]
highlighted_text = highlight_keywords(text, keywords)
print(highlighted_text)