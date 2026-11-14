# «Тайнопись» — шифр Цезаря для русского алфавита (этап 6: функции)
# Логика (проверка, расчёт, поиск) возвращает значения через return и ничего не печатает.
# Интерфейс (меню, серия, показ) спрашивает пользователя и печатает результат.

LOW = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
UP = LOW.upper()

# Кортеж: фиксированная связка «номер режима -> название»
MODE_NAMES = ("Выход", "Зашифровано", "Расшифровано")


# ---------- Логика: только параметры и return ----------

def is_int(value):
    """Проверяет, что строка — целое число (допускается один минус впереди)."""
    return value.removeprefix("-").isdigit()


def is_count(value):
    """Проверяет, что строка — целое число больше 0 (размер серии)."""
    return value.isdigit() and int(value) > 0


def caesar(text, k):
    """Сдвигает русские буквы текста на k позиций с сохранением регистра."""
    k = k % 33
    table = str.maketrans(LOW + UP, LOW[k:] + LOW[:k] + UP[k:] + UP[:k])
    return text.translate(table)


def make_record(mode, text, shift):
    """Создаёт словарь записи: режим 1 — сдвиг вперёд, режим 2 — назад."""
    record = {"action": MODE_NAMES[mode], "source": text, "shift": shift, "result": ""}
    if mode == 1:
        record["result"] = caesar(text, shift)
    else:
        record["result"] = caesar(text, -shift)
    return record


def shift_stats(history):
    """Считает по истории: минимальный и максимальный сдвиг, отсортированный список, число разных."""
    shifts = []
    for record in history:
        shifts.append(record["shift"])
    return min(shifts), max(shifts), sorted(shifts), len(set(shifts))


def search_history(history, query):
    """Возвращает записи, где запрос встречается в исходном тексте или результате."""
    found = []
    for record in history:
        if query in record["source"].lower() or query in record["result"].lower():
            found.append(record)
    return found


def format_record(record):
    """Превращает запись в строку для показа."""
    return f"{record['action']}: «{record['source']}» -> «{record['result']}» (сдвиг {record['shift']})"


# ---------- Интерфейс: ввод и печать ----------

def print_records(records):
    """Печатает список записей — общая функция для истории и поиска."""
    for record in records:
        print(format_record(record))


def run_series(mode, n, history, counts):
    """Пункты меню 1 и 2: серия из n сообщений. Дополняет history и counts, возвращает число обработанных."""
    done = 0
    for i in range(1, n + 1):
        print(f"--- Сообщение {i} из {n} ---")
        text = input("Введите текст: ").strip()
        shift_str = input("Введите сдвиг (целое число): ").strip()

        if not is_int(shift_str):
            print("Ошибка: сдвиг должен быть целым числом, сообщение пропущено")
            counts["Пропущено"] += 1
            continue

        record = make_record(mode, text, int(shift_str))
        print(f"{record['action']}: {record['result']}")
        history.append(record)
        counts[record["action"]] += 1
        done += 1

    print(f"Итог серии: обработано {done} из {n}, пропущено {n - done}")
    return done


def show_history(history, counts):
    """Пункт меню 3: история и статистика сдвигов."""
    if len(history) == 0:
        print("История пуста")
        return
    print(f"Записей в истории: {len(history)}")
    print_records(history)
    smallest, largest, sorted_shifts, unique_count = shift_stats(history)
    print(f"Сдвиги: мин {smallest}, макс {largest}, по возрастанию {sorted_shifts}")
    print(f"Разных сдвигов: {unique_count}")
    print(f"Зашифровано: {counts['Зашифровано']}, расшифровано: {counts['Расшифровано']}, пропущено: {counts['Пропущено']}")


def run_search(history):
    """Пункт меню 4: поиск по истории без учёта регистра."""
    query = input("Что искать: ").strip().lower()
    if query == "":
        print("Ошибка: пустой запрос")
        return
    found = search_history(history, query)
    print(f"Найдено: {len(found)}")
    print_records(found)


def main():
    """Главное меню: хранит историю и счётчики, вызывает функции пунктов меню."""
    history = []
    counts = {"Зашифровано": 0, "Расшифровано": 0, "Пропущено": 0}

    print("=== Тайнопись: шифр Цезаря ===")
    while True:
        print()
        print("1 — зашифровать, 2 — расшифровать, 3 — история, 4 — поиск, 0 — выход")
        mode_str = input("Выберите режим: ").strip()

        if not mode_str.isdigit():
            print("Неведомо сие: режим должен быть числом от 0 до 4")
            continue
        mode = int(mode_str)
        if mode == 0:
            print("Выход по команде 0")
            break
        elif mode > 4:
            print("Неведомо сие: такого режима нет, допустимы 0–4")
            continue
        elif mode == 3:
            show_history(history, counts)
            continue
        elif mode == 4:
            run_search(history)
            continue

        n_str = input("Сколько сообщений обработать? ").strip()
        if not is_count(n_str):
            print("Ошибка: количество должно быть целым числом больше 0")
            continue
        run_series(mode, int(n_str), history, counts)

        answer = input("Продолжить? (да/нет): ").strip().lower()
        if answer != "да":
            print("Выход по ответу «нет»")
            break

    print("Конец работы")


if __name__ == "__main__":
    main()
