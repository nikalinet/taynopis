# «Тайнопись» - этап 6: логика в функциях, ввод и печать в интерфейсе

LOW = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
UP = LOW.upper()
ALPHABET_SIZE = len(LOW)

# Ключ - номер режима, значение - название для летописи
MODE_NAMES = {1: "Утаённое", 2: "Явленное"}

MENU = "1 - утаить, 2 - явить, 3 - летопись, 4 - отыскать, 0 - откланяться"
ANSWER_PROMPT = "Продолжим воротить буковки, али откланяемся? (да / нет): "

# Отдельный ключ: отказы считаем отдельно от режимов 1 и 2
SKIPPED = "skipped"


# Логика

def is_menu_choice(value):
    return value.isdecimal() and int(value) <= 4


def is_count(value):
    return value.isdecimal() and int(value) > 0


# Направление задаёт режим, а шаг приводится по модулю в shift_text
def is_shift(value):
    return value.removeprefix("-").isdecimal()


def shift_text(text, k):
    k %= ALPHABET_SIZE
    table = str.maketrans(
        LOW + UP, LOW[k:] + LOW[:k] + UP[k:] + UP[:k]
    )
    return text.translate(table)


def count_letters(text):
    letters = 0
    for ch in text:
        if ch in LOW or ch in UP:
            letters += 1
    return letters


def make_record(mode, text, shift):
    if mode == 1:
        k = shift
    else:
        k = -shift
    return {
        "action": MODE_NAMES[mode],
        "source": text,
        "shift": shift,
        "result": shift_text(text, k),
    }


# Защита на будущее: пустая история не должна ронять min() и max()
def shift_stats(history):
    if not history:
        return None, None, [], 0
    shifts = [record["shift"] for record in history]
    return min(shifts), max(shifts), sorted(shifts), len(set(shifts))


# Регистр не важен: запрос и тексты приводятся к нижнему внутри
def search_history(history, query):
    query = query.lower()
    found = []
    for record in history:
        source = record["source"].lower()
        result = record["result"].lower()
        if query in source or query in result:
            found.append(record)
    return found


def format_record(record):
    return (
        f"{record['action']}: «{record['source']}» -> "
        f"«{record['result']}» (шаг {record['shift']})"
    )


# Интерфейс

def print_records(records):
    for record in records:
        print(format_record(record))


def read_text():
    text = input("Молви слово тайное: ").strip()
    if text == "":
        print("Остолоп! Пустое слово не воротишь — молви письмо.")
        return None
    return text


def read_shift():
    value = input("На сколько шагов воротить? ").strip()
    if not is_shift(value):
        print("Беда: шаг не цельный, письмо сгинуло, аки камень в омуте.")
        return None
    return int(value)


# True - письмо ворочено и записано в летопись
def process_letter(mode, history, counts):
    text = read_text()
    shift = None if text is None else read_shift()
    if text is None or shift is None:
        counts[SKIPPED] += 1
        return False

    record = make_record(mode, text, shift)
    print(f"{record['action']}: {record['result']}")
    letters = count_letters(text)
    print(f"Ворочено буквиц: {letters}, "
          f"а прочей мелочи не тронуто: {len(text) - letters}")

    history.append(record)
    counts[mode] += 1
    return True


# Возвращает число вороченных писем
def run_series(mode, n, history, counts):
    done = 0
    for i in range(1, n + 1):
        print(f"--- Письмецо {i} из {n} ---")
        if process_letter(mode, history, counts):
            done += 1
    return done


# Пункт 3: история, шаги и счётчики
def show_history(history, counts):
    if not history:
        print("Летопись не писана: ни былин, ни сказаний.")
        return

    print(f"Сказаний писано: {len(history)}")
    print_records(history)

    smallest, largest, sorted_shifts, unique_count = shift_stats(history)
    print(f"Шагов воротим: от мала {smallest}, до велика {largest}, "
          f"аки ручей от истока к устью {sorted_shifts}")
    print(f"Шагов всяких: {unique_count}")
    print(f"Утаённое: {counts[1]}, явленное: {counts[2]}, "
          f"не воротили: {counts[SKIPPED]}")


# Пункт 4: поиск по истории
def run_search(history):
    prompt = "Чего изволишь отыскать в письменах минувшего? "
    query = input(prompt).strip()

    if query == "":
        print("Остолоп! Пустое слово не сыщешь — молви, чего искать")
        return

    found = search_history(history, query)
    print(f"Нашлось, письмо заветное: {len(found)}")
    print_records(found)


def ask_answer():
    answer = input(ANSWER_PROMPT).strip().lower()

    while answer not in ("да", "нет"):
        print("Смутьян! Молви ясно: «да» али «нет» — иных речей не разумею.")
        answer = input(ANSWER_PROMPT).strip().lower()

    return answer


def main():
    history = []
    counts = {1: 0, 2: 0, SKIPPED: 0}

    print("=== Тайнопись: шифр Цезаря ===")

    while True:
        print()
        print(MENU)
        mode_str = input("Чего изволишь, добрый молодец? ").strip()

        if not is_menu_choice(mode_str):
            print("Смутьян! Вразуми: мне цифирью молви, "
                  "числом от ничто (0) до четырёх (4)")
            continue

        mode = int(mode_str)

        if mode == 0:
            print("Слово молвлено, дело сделано. "
                  "Кланяюсь да ухожу, аки гость незваный.")
            break
        elif mode == 3:
            show_history(history, counts)
            continue
        elif mode == 4:
            run_search(history)
            continue

        n_str = input("Сколько писем изволишь воротить? ").strip()

        if not is_count(n_str):
            print("Горе-писарь! Молви, сколько писем воротить, "
                  "числом целым от единицы.")
            continue

        n = int(n_str)
        done = run_series(mode, n, history, counts)
        print(f"А как сочли: ворочено: {done} из {n}, "
              f"а {n - done} не воротили — лежат, аки камни в омуте.")

        if ask_answer() != "да":
            print("Бывай, добрый молодец. Шаг береги аки зеницу ока — "
                  "потеряешь, сам себя не прочтёшь.")
            break

    print("Коли не сработало — то не моя вина, а Цезаря окаянного.")


if __name__ == "__main__":
    main()
