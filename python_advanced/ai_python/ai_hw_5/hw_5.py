    # Создайте простую цепочку LangChain для суммаризации текста из URL веб-страницы.
    # Зарегистрируйтесь на PromptHub и изучите его интерфейс. Найдите и опишите 3 интересных промпта.
    # (Дополнительно) Создайте цепочку "вопрос-ответ по документам" для небольшого текстового файла.

# Функция для создания цепочки, которая объединяет документы и обрабатывает их с помощью LLM.
from langchain.chains.combine_documents import create_stuff_documents_chain
# Класс для создания шаблонов промптов для чата.
from langchain_core.prompts import ChatPromptTemplate
# Класс для работы с генеративной моделью от Google.
from langchain_google_genai import ChatGoogleGenerativeAI
# Класс для загрузки документов (в данном случае – веб-страницы).
from langchain_community.document_loaders import WebBaseLoader
# Модуль для работы с переменными окружения (из файла .env).
from dotenv import load_dotenv
# Модуль для работы с операционной системой (например, для получения переменных окружения).
import os

# Загружаем переменные окружения из файла .env. Это нужно, чтобы получить секретные ключи, не прописывая их в коде.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Инициализируем генеративную модель Google с указанной моделью "gemini-2.0-flash" и передаём ей API-ключ.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# Создаем загрузчик, который скачает содержимое указанного веб-адреса.
loader = WebBaseLoader("https://habr.com/ru/articles/883604/")

# Загружаем документ с веб-страницы. В переменной docs будет храниться текст или структура полученного документа.
docs = loader.load()

# Создаем шаблон для промптов, который будет использоваться для генерации ответа.
# Здесь {context} - это место, куда подставится загруженный документ.
prompt = ChatPromptTemplate.from_template("Напишите краткое изложение следующего текста: {context}")

# Создаем цепочку, которая объединяет документы и передает их в LLM вместе с подсказкой.
chain = create_stuff_documents_chain(llm, prompt)

# Запускаем цепочку, передавая загруженный документ в качестве параметра "context".
# Функция invoke обрабатывает входные данные и возвращает результат от модели.
result = chain.invoke({"context": docs})

# Выводим полученный результат (например, краткое изложение текста) на экран.
print(result)