from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="local", timeout=120.0)

MODELS = {
    "before (llama3.1 Q4_0)": "llama3.1",
    "after_int8 (llama3.1 Q8_0)": "llama3.1:8b-instruct-q8_0",
}

SYSTEM_PROMPT = (
    "Ти — ASTRA-8, бортовий інженерний ШІ-аналітик космічної місії. "
    "Відповідай чітко, технічно грамотною українською мовою."
)

PROMPTS_10 = [
    "1. Поясни в 3 реченнях причину виникнення ефекту Джанібекова на орбітальній станції.",
    "2. Напиши Python-функцію для переведення тиску з кілопаскалів (кПа) у міліметри ртутного стовпа та атмосфери.",
    "3. Розшифруй помилку телеметрії: [ERR_THERMAL_LOOP_B: ΔT = +14.2K over 120s, coolant flow 0.4 L/min]. Які дії екіпажу?",
    "4. Переклади українською: 'Attitude control thrusters fired for 3.2 seconds to compensate for solar radiation pressure torque.'",
    "5. Склади чек-лист перевірки герметичності перехідного шлюзу перед виходом у відкритий космос (5 пунктів).",
    "6. Сонячні панелі станції генерують 12 кВт, але ККД впав на 15% через деградацію. Скільки енергії (у кВт·год) вони вироблять за 4 години освітленої частини орбіти?",
    "7. Напиши JSON-структуру для звіту про стан трьох систем: живлення (норма), зв'язок (попередження), навігація (норма).",
    "8. Чим відрізняється апогей від перигею еліптичної орбіти? Відповідь дай коротко.",
    "9. Напиши регулярний вираз (regex) на Python для пошуку кодів помилок формату ERR_XXX_000 у логах корабля.",
    "10. Зроби коротке резюме для командира: тиск у відсіку 101.3 кПа, рівень CO2 — 0.04%, температура — 21.5°C, заряд батарей — 94%.",
]

with open("quality_comparison.md", "w", encoding="utf-8") as f:
    f.write("# Порівняння якості відповідей на 10 контрольних промптах (Пункти 1.4 та 1.5)\n\n")
    for prompt in PROMPTS_10:
        print(f"Обробка: {prompt[:50]}...")
        f.write(f"## {prompt}\n\n")
        for label, model_name in MODELS.items():
            resp = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=350,
                temperature=0,
                seed=1,
            )
            answer = (resp.choices[0].message.content or "").strip()
            f.write(f"### {label}\n{answer}\n\n")
        f.write("---\n\n")

print("Готово! Всі 10 пар відповідей збережено у файл quality_comparison.md")