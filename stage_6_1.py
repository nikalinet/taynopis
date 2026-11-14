"""«Тайнопись» - этап 6: рефакторинг проекта в функции.

Логика (проверки, расчёт, отбор) получает данные аргументами и отдаёт
результат через return. Интерфейс (меню, серия, показ) спрашивает через
input и печатает через print.
"""

LOW = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
UP = LOW.upper()
ALPHABET_SIZE = len(LOW)

# Кортеж: фиксированная связка «номер режима -> название»
MODE_NAMES = ("Откланяться", "Утаённое", "Явленное")

MENU = "1 - утаить, 2 - явить, 3 - летопись, 4 - отыскать, 0 - откланяться"

# Предел серии за один раз: защита от случайного ввода вроде 100000
MAX_SERIES = 100


# ---------- Логика: без input и print, результат через return ----------

def is_int(value):
    """Проверяет, что строка - целое число, допускается один минус впереди."""
    return value.removeprefix("-").isdigit()


def is_count(value):
    """Проверяет, что строка - целое число больше нуля."""
    return value.isdigit() and int(value) > 0


def caesar(text, k):
    """Сдвигает русские буквы на k позиций, сохраняя регистр."""
    k %= ALPHABET_SIZE
    table = str.maketrans(LOW + UP, LOW[k:] + LOW[:k] + UP[k:] + UP[:k])
    return text.translate(table)


def make_record(mode, text, shift):
    """Собирает запись летописи: режим 1 - сдвиг вперёд, режим 2 - назад."""
    k = shift if mode == 1 else -shift
    record = {"action": MODE_NAMES[mode], "source": text, "shift": shift, "result": ""}
    record["result"] = caesar(text, k)
    return record


def count_letters(text):
    """Возвращает пару: сколько в тексте букв и сколько прочих знаков."""
    letters = sum(1 for ch in text if ch in LOW or ch in UP)
    return letters, len(text) - letters


def shift_stats(history):
    """Возвращает минимум, максимум, список по возрастанию и число разных сдвигов."""
    shifts = [record["shift"] for record in history]
    return min(shifts), max(shifts), sorted(shifts), len(set(shifts))


def search_history(history, query):
    """Отбирает записи, где запрос есть в исходном тексте или в результате."""
    found = []
    for record in history:
        if query in record["source"].lower() or query in record["result"].lower():
            found.append(record)
    return found


def format_record(record):
    """Собирает строку для показа одной записи."""
    return f"{record['action']}: «{record['source']}» -> «{record['result']}» (шаг {record['shift']})"


# ---------- Интерфейс: спрашивает пользователя и печатает ----------

def ask_number(prompt, check, minimum=None, maximum=None):
    """Спрашивает число и проверяет его.

    Возвращает int или None, если ввод не прошёл проверку check
    либо вышел за границы minimum / maximum.
    """
    value = input(prompt).strip()
    if not check(value):
        return None
    number = int(value)
    if minimum is not None and number < minimum:
        return None
    if maximum is not None and number > maximum:
        return None
    return number


def ask_yes_no(prompt):
    """Спрашивает «да» или «нет», переспрашивая, пока ответ не станет понятным."""
    answer = input(prompt).strip().lower()
    while answer not in ("да", "нет"):
        print("Смутьян! Молви ясно: «да» али «нет» — иных речей не разумею.")
        answer = input(prompt).strip().lower()
    return answer == "да"


def print_records(records):
    """Печатает записи - общая функция для летописи и поиска."""
    for record in records:
        print(format_record(record))


def skip_message(counts, message):
    """Сообщает об отказе и учитывает пропущенное письмо."""
    print(message)
    counts["Не воротили"] += 1


def run_series(mode, n, history, counts):
    """Пункты меню 1 и 2: серия из n писем. Дополняет history и counts."""
    done = 0
    for i in range(1, n + 1):
        print(f"--- Письмецо {i} из {n} ---")
        text = input("Молви слово тайное: ").strip()

        if text == "":
            skip_message(counts, "Остолоп! Пустое слово не воротишь — молви письмо.")
            continue

        shift = ask_number("На сколько шагов воротить? ", is_int)
        if shift is None:
            skip_message(counts, "Беда: шаг не цельный, письмо сгинуло, аки камень в омуте.")
            continue

        record = make_record(mode, text, shift)
        letters, other = count_letters(text)
        print(f"{record['action']}: {record['result']}")
        print(f"Ворочено буквиц: {letters}, а прочей мелочи не тронуто: {other}")

        history.append(record)
        counts[record["action"]] += 1
        done += 1

    print(f"А как сочли: ворочено: {done} из {n}, а {n - done} не воротили — лежат, аки камни в омуте.")


def show_history(history, counts):
    """Пункт меню 3: летопись, статистика сдвигов и счётчики."""
    if len(history) == 0:
        print("Летопись не писана: ни былин, ни сказаний.")
        return

    print(f"Сказаний писано: {len(history)}")
    print_records(history)

    smallest, largest, sorted_shifts, unique_count = shift_stats(history)
    print(f"Шагов воротим: от мала {smallest}, до велика {largest}, "
          f"аки ручей от истока к устью {sorted_shifts}")
    print(f"Шагов всяких: {unique_count}")
    print(f"Утаённое: {counts['Утаённое']}, явленное: {counts['Явленное']}, не воротили: {counts['Не воротили']}")


def run_search(history):
    """Пункт меню 4: поиск по летописи без учёта регистра."""
    query = input("Чего изволишь отыскать в письменах минувшего? ").strip().lower()
    if query == "":
        print("Остолоп! Пустое слово не сыщешь — молви, чего искать")
        return

    found = search_history(history, query)
    print(f"Нашлось, письмо заветное: {len(found)}")
    print_records(found)


def main():
    """Главное меню: хранит историю и счётчики и передаёт их функциям аргументами."""
    history = []
    counts = {"Утаённое": 0, "Явленное": 0, "Не воротили": 0}

    print("=== Тайнопись: шифр Цезаря ===")
    while True:
        print()
        print(MENU)

        mode = ask_number("Чего изволишь, добрый молодец? ", is_int, 0, 4)
        if mode is None:
            print("Смутьян! Вразуми: мне цифирью молви, числом от ничто (0) до четырёх (4)")
            continue

        if mode == 0:
            print("Слово молвлено, дело сделано. Кланяюсь да ухожу, аки гость незваный.")
            break

        if mode == 3:
            show_history(history, counts)
            continue

        if mode == 4:
            run_search(history)
            continue

        n = ask_number("Сколько писем изволишь воротить? ", is_count, maximum=MAX_SERIES)
        if n is None:
            print(f"Горе-писарь! Молви, сколько писем воротить, "
                  f"числом целым от единицы до {MAX_SERIES}.")
            continue

        run_series(mode, n, history, counts)

        if not ask_yes_no("Продолжим воротить буковки, али откланяемся? (да / нет): "):
            print("Бывай, добрый молодец. Шаг береги аки зеницу ока — потеряешь, сам себя не прочтёшь.")
            break

    print("Коли не сработало — то не моя вина, а Цезаря окаянного.")


if __name__ == "__main__":
    main()
