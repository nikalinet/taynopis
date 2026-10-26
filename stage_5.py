# «Тайнопись» - этап 5: модель данных

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

# Кортеж: фиксированная связка «номер режима -> название», не меняется во время работы
MODE_NAMES = ("Откланяться", "Утаённое", "Явленное")  # 1

history = []

counts = {"Утаённое": 0, "Явленное": 0, "Не воротили": 0}

print("=== Тайнопись: шифр Цезаря ===")

while True:
    print()
    print("1 - утаить, 2 - явить, 3 - летопись, 4 - отыскать, 0 - откланяться")
    mode_str = input("Чего изволишь, добрый молодец? ").strip()

    # Проверка режима: только цифра от 0 до 4
    if not mode_str.isdigit() or int(mode_str) > 4:
        print("Смутьян! Вразуми: мне цифирью молви, числом от ничто (0) до четырёх (4)")
        continue

    mode = int(mode_str)

    if mode == 0:
        print("Слово молвлено, дело сделано. Кланяюсь да ухожу, аки гость незваный.")
        break

    # Режим 3: летопись - печать истории, сдвигов и счётчиков
    elif mode == 3:
        if len(history) == 0:
            print("Летопись не писана: ни былин, ни сказаний.")
            continue

        print(f"Сказаний писано: {len(history)}")
        shifts = []

        for record in history:
            print(f"{record['action']}: «{record['source']}» -> «{record['result']}» (шаг {record['shift']})")
            shifts.append(record["shift"])

        sorted_shifts = sorted(shifts)
        unique_shifts = set(shifts)

        print(f"Шагов воротим: от мала {min(shifts)}, до велика {max(shifts)}, "
              f"аки ручей от истока к устью {sorted_shifts}")
        print(f"Шагов всяких: {len(unique_shifts)}")
        print(f"Утаённое: {counts['Утаённое']}, явленное: {counts['Явленное']}, не воротили: {counts['Не воротили']}")
        continue

    # Режим 4: поиск по истории без учёта регистра
    elif mode == 4:
        query = input("Чего изволишь отыскать в письменах минувшего? ").strip().lower()

        if query == "":
            print("Остолоп! Пустое слово не сыщешь — молви, чего искать")
            continue

        found = []
        for record in history:
            if query in record["source"].lower() or query in record["result"].lower():
                found.append(record)

        print(f"Нашлось, письмо заветное: {len(found)}")
        for record in found:
            print(f"{record['action']}: «{record['source']}» -> «{record['result']}» (шаг {record['shift']})")
        continue

    # Режимы 1 и 2: серия из N сообщений
    action = MODE_NAMES[mode]
    n_str = input("Сколько писем изволишь воротить? ").strip()

    if not n_str.isdigit() or int(n_str) == 0:
        print("Горе-писарь! Молви, сколько писем воротить, числом целым от единицы.")
        continue

    n = int(n_str)

    done = 0

    for i in range(1, n + 1):  # 2
        print(f"--- Письмецо {i} из {n} ---")
        text = input("Молви слово тайное: ").strip()

        # Пустое письмо в историю не попадает
        if text == "":
            print("Остолоп! Пустое слово не воротишь — молви письмо.")
            counts["Не воротили"] += 1
            continue

        shift_str = input("На сколько шагов воротить? ").strip()

        if not shift_str.removeprefix("-").isdigit():
            print("Беда: шаг не цельный, письмо сгинуло, аки камень в омуте.")
            counts["Не воротили"] += 1
            continue

        shift = int(shift_str)

        if mode == 1:
            k = shift % 33
        else:
            k = -shift % 33

        record = {"action": action, "source": text, "shift": shift, "result": ""}  # 3
        table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
        record["result"] = text.translate(table)

        print(f"{record['action']}: {record['result']}")
        letters = sum(1 for ch in text if ch in low or ch in up)
        print(f"Ворочено буквиц: {letters}, а прочей мелочи не тронуто: {len(text) - letters}")

        history.append(record)
        counts[action] += 1
        done += 1

    print(f"А как сочли: ворочено: {done} из {n}, а {n - done} не воротили — лежат, аки камни в омуте.")

    answer = input("Продолжим воротить буковки, али откланяемся? (да / нет): ").strip().lower()

    while answer not in ("да", "нет"):
        print("Смутьян! Молви ясно: «да» али «нет» — иных речей не разумею.")
        answer = input("Продолжим воротить буковки, али откланяемся? (да / нет): ").strip().lower()

    if answer != "да":
        print("Бывай, добрый молодец. Шаг береги аки зеницу ока — потеряешь, сам себя не прочтёшь.")
        break

print("Коли не сработало — то не моя вина, а Цезаря окаянного.")
