import os
from openai import OpenAI, APIConnectionError, APITimeoutError
from openai.types.chat import ChatCompletionMessageParam

os.system("")

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="local",
    timeout=60.0,
)

MODEL_NAME = "llama3.1:8b-instruct-q8_0"

GREEN = "\033[92m"
LIGHT_ORANGE = "\033[38;5;214m"
RESET = "\033[0m"

SYSTEM_PROMPT = (
    "Ти — ASTRA-8, бортовий інженерний ШІ-аналітик космічної місії. "
    "Твоє завдання: аналізувати логи телеметрії, діагностувати несправності систем корабля "
    "та допомагати екіпажу з інженерними розрахунками. "
    "Відповідай чітко, технічно грамотною українською мовою. "
    "У фізичних формулах обов'язково зводь усі величини до системи СІ (метри, кілограми, секунди). "
    "Для будь-яких розрахунків або логічних задач спершу міркуй крок за кроком, а потім давай фінальний висновок."
)


def stream_assistant_reply(messages: list[ChatCompletionMessageParam]) -> str | None:
    """Надсилає історію повідомлень до моделі та виводить відповідь стрімінгом."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=600,
            temperature=0.3,
            stream=True,
        )

        print(f"{LIGHT_ORANGE}ASTRA-8:{RESET} ", end="", flush=True)
        full_response = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print("\n")
        return full_response

    except APITimeoutError:
        print("\n[Помилка таймауту]: Сервер занадто довго обробляє запит. Спробуйте скоротити вхідні дані.\n")
    except APIConnectionError:
        print("\n[Помилка зв'язку]: Не вдалося підключитися до сервера Ollama (http://localhost:11434). Перевірте, чи запущено 'ollama serve'.\n")
    except Exception as e:
        print(f"\n[Системний збій]: {e}\n")
    return None


def mission_assistant() -> None:
    print("=========================================================")
    print("   ASTRA-8 | Бортовий AI-аналітик космічної місії")
    print("   Модель: llama3.1:8b-instruct-q8_0 (локальний вузол)")
    print("   Команди: '/clear' — очистити контекст, 'вихід' — вийти.")
    print("=========================================================\n")

    messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input(f"{GREEN}Інженер:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nСеанс зв'язку завершено.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("вихід", "exit", "quit"):
            print(f"{LIGHT_ORANGE}ASTRA-8:{RESET} Системи переведено в режим очікування. Кінець зв'язку.")
            break
        if user_input.lower() == "/clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print(f"{LIGHT_ORANGE}ASTRA-8:{RESET} Пам'ять діалогу очищено.\n")
            continue

        messages.append({"role": "user", "content": user_input})
        reply = stream_assistant_reply(messages)

        if reply is not None:
            messages.append({"role": "assistant", "content": reply})
        else:
            messages.pop()


if __name__ == "__main__":
    mission_assistant()