# «Тайнопись» - этап 7: файл

import json

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

# Кортеж: фиксированная связка «номер режима -> название», не меняется во время работы
MODE_NAMES = ("Откланяться", "Утаённое", "Явленное")

# Файл летописи: создаётся программой при первом сохранении
DATA_FILE = "letopis.json"


def empty_counts():
    return {"Утаённое": 0, "Явленное": 0, "Не воротили": 0}


def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        history = data["history"]
        counts = data["counts"]

        if not isinstance(history, list) or not isinstance(counts, dict):
            raise TypeError
        if not {"Утаённое", "Явленное", "Не воротили"} <= counts.keys():
            raise KeyError

        return history, counts, "ok"
    except FileNotFoundError:
        return [], empty_counts(), "missing"
    except (json.JSONDecodeError, KeyError, TypeError):
        return [], empty_counts(), "broken"


# Записывает летопись и счётчики: режим "w" заменяет старое содержимое целиком
# и создаёт файл, если его ещё нет
def save_data(filename, history, counts):
    data = {"history": history, "counts": counts}
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# Логика


def is_mode(value):
    return value.isdecimal() and int(value) <= 5


def is_count(value):
    return value.isdecimal() and int(value) > 0


def is_shift(value):
    return value.removeprefix("-").isdecimal()


def shift_text(text, k):
    k = k % 33
    table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
    return text.translate(table)


def count_letters(text):
    letters = 0
    for ch in text:
        if ch in low or ch in up:
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


def shift_stats(history):
    if not history:
        return None, None, [], 0

    shifts = []
    for record in history:
        shifts.append(record["shift"])
    return min(shifts), max(shifts), sorted(shifts), len(set(shifts))


def search_history(history, query):
    found = []
    for record in history:
        if query in record["source"].lower() or query in record["result"].lower():
            found.append(record)
    return found


def format_record(record):
    return f"{record['action']}: «{record['source']}» -> «{record['result']}» (шаг {record['shift']})"


# Интерфейс


def print_records(records):
    for record in records:
        print(format_record(record))


def run_letter(mode, history, counts):
    text = input("Молви слово тайное: ").strip()

    if text == "":
        print("Остолоп! Пустое слово не воротишь - молви письмо.")
        counts["Не воротили"] += 1
        return False

    shift_str = input("На сколько шагов воротить? ").strip()

    if not is_shift(shift_str):
        print("Беда: шаг не цельный, письмо сгинуло, аки камень в омуте.")
        counts["Не воротили"] += 1
        return False
    record = make_record(mode, text, int(shift_str))
    print(f"{record['action']}: {record['result']}")
    letters = count_letters(text)
    print(
        f"Ворочено буквиц: {letters}, а прочей мелочи не тронуто: {len(text) - letters}"
    )

    history.append(record)
    counts[record["action"]] += 1
    return True


def run_series(mode, n, history, counts):
    done = 0
    for i in range(1, n + 1):
        print(f"--- Письмецо {i} из {n} ---")
        if run_letter(mode, history, counts):
            done += 1

    print(
        f"А как сочли: ворочено: {done} из {n}, а {n - done} не воротили - лежат, аки камни в омуте."
    )


def show_history(history, counts):
    if len(history) == 0:
        print("Летопись не писана: ни былин, ни сказаний.")
        return

    print(f"Сказаний писано: {len(history)}")
    print_records(history)

    smallest, largest, sorted_shifts, unique_count = shift_stats(history)
    print(
        f"Шагов воротим: от мала {smallest}, до велика {largest}, "
        f"аки ручей от истока к устью {sorted_shifts}"
    )
    print(f"Шагов всяких: {unique_count}")
    print(
        f"Утаённое: {counts['Утаённое']}, явленное: {counts['Явленное']}, не воротили: {counts['Не воротили']}"
    )


def run_search(history):
    query = input("Чего изволишь отыскать в письменах минувшего? ").strip().lower()

    if query == "":
        print("Остолоп! Пустое слово не сыщешь - молви, чего искать")
        return

    found = search_history(history, query)
    print(f"Нашлось, письмо заветное: {len(found)}")
    print_records(found)


def run_save(history, counts):
    save_data(DATA_FILE, history, counts)
    print(f"Летопись в {DATA_FILE} запечатлена. Сказаний в ней: {len(history)}")


def ask_answer():
    answer = (
        input("Продолжим воротить буковки, али откланяемся? (да / нет): ")
        .strip()
        .lower()
    )

    while answer not in ("да", "нет"):
        print("Смутьян! Молви ясно: «да» али «нет» - иных речей не разумею.")
        answer = (
            input("Продолжим воротить буковки, али откланяемся? (да / нет): ")
            .strip()
            .lower()
        )

    return answer


def main():
    print("=== Тайнопись: шифр Цезаря ===")

    history, counts, status = load_data(DATA_FILE)

    if status == "ok":
        print(f"Летопись из {DATA_FILE} прочитана. Сказаний в ней: {len(history)}")
    elif status == "missing":
        print(f"Летопись в {DATA_FILE} не сыскана. Начинаем с пустой истории.")
    else:
        print(f"Летопись в {DATA_FILE} попорчена. Начинаем с пустой истории.")

    while True:
        print()
        print(
            "1 - утаить, 2 - явить, 3 - летопись, 4 - отыскать, 5 - запечатлеть, 0 - откланяться"
        )
        mode_str = input("Чего изволишь, добрый молодец? ").strip()

        if not is_mode(mode_str):
            print(
                "Смутьян! Вразуми: мне цифирью молви, числом от ничто (0) до пяти (5)"
            )
            continue

        mode = int(mode_str)

        if mode == 0:
            print(
                "Слово молвлено, дело сделано. Кланяюсь да ухожу, аки гость незваный."
            )
            break
        elif mode == 3:
            show_history(history, counts)
            continue
        elif mode == 4:
            run_search(history)
            continue
        elif mode == 5:
            run_save(history, counts)
            continue

        n_str = input("Сколько писем изволишь воротить? ").strip()

        if not is_count(n_str):
            print(
                "Горе-писарь! Молви, сколько писем воротить, числом целым от единицы."
            )
            continue

        run_series(mode, int(n_str), history, counts)

        if ask_answer() != "да":
            print(
                "Бывай, добрый молодец. Шаг береги аки зеницу ока - потеряешь, сам себя не прочтёшь."
            )
            break

    run_save(history, counts)
    print("Коли не сработало - то не моя вина, а Цезаря окаянного.")


if __name__ == "__main__":
    main()
