    # Добавить защиту от блокировки API (Rate Limits)
    # Обработать таймауты
    # Реализовать retry-механизм с tenacity
from google import genai
import os
from dotenv import load_dotenv
import time
from requests import ReadTimeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
timeout_seconds = 10
client = genai.Client(api_key=api_key)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10),
       retry=retry_if_exception_type((ResourceExhausted, TimeoutError)))
def get_gemini_response(prompt):
    time.sleep(0.3)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        return response.text
    except (ResourceExhausted, TimeoutError) as e:
        raise
    except Exception as e:
        return f"An error occured {str(e)}"


if __name__ == "__main__":
    response = get_gemini_response("How old is the universe?")
    print(response)
