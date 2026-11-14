# «Тайнопись» — шифр Цезаря для русского алфавита (этап 5: модель данных)
# Меню (while) -> режим -> серия из N сообщений (for + range) -> история и поиск

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

# Кортеж: фиксированная связка «номер режима -> название», не меняется во время работы
MODE_NAMES = ("Выход", "Зашифровано", "Расшифровано")

# Список истории: каждая запись — словарь с одинаковыми ключами
history = []

# Словарь счётчиков: обновляется по ключу после каждого сообщения
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
        # История и анализ сдвигов
        if len(history) == 0:
            print("История пуста")
            continue
        print(f"Записей в истории: {len(history)}")
        shifts = []
        for record in history:
            print(f"{record['action']}: «{record['source']}» -> «{record['result']}» (сдвиг {record['shift']})")
            shifts.append(record["shift"])
        sorted_shifts = sorted(shifts)
        unique_shifts = set(shifts)
        print(f"Сдвиги: мин {min(shifts)}, макс {max(shifts)}, по возрастанию {sorted_shifts}")
        print(f"Разных сдвигов: {len(unique_shifts)}")
        print(f"Зашифровано: {counts['Зашифровано']}, расшифровано: {counts['Расшифровано']}, пропущено: {counts['Пропущено']}")
        continue

    elif mode == 4:
        # Поиск по истории без учёта регистра
        query = input("Что искать: ").strip().lower()
        if query == "":
            print("Ошибка: пустой запрос")
            continue
        found = []
        for record in history:
            if query in record["source"].lower() or query in record["result"].lower():
                found.append(record)
        print(f"Найдено: {len(found)}")
        for record in found:
            print(f"{record['action']}: «{record['source']}» -> «{record['result']}» (сдвиг {record['shift']})")
        continue

    # Режимы 1 и 2: серия из N сообщений
    action = MODE_NAMES[mode]
    n_str = input("Сколько сообщений обработать? ").strip()
    if not n_str.isdigit() or int(n_str) == 0:
        print("Ошибка: количество должно быть целым числом больше 0")
        continue
    n = int(n_str)

    done = 0
    for i in range(1, n + 1):
        print(f"--- Сообщение {i} из {n} ---")
        text = input("Введите текст: ").strip()
        shift_str = input("Введите сдвиг (целое число): ").strip()

        if not shift_str.removeprefix("-").isdigit():
            print("Ошибка: сдвиг должен быть целым числом, сообщение пропущено")
            counts["Пропущено"] += 1
            continue

        shift = int(shift_str)
        if mode == 1:
            k = shift % 33
        else:
            k = -shift % 33

        # Запись создаётся словарём, результат дописывается по ключу
        record = {"action": action, "source": text, "shift": shift, "result": ""}
        table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
        record["result"] = text.translate(table)
        print(f"{record['action']}: {record['result']}")

        history.append(record)
        counts[action] += 1
        done += 1

    print(f"Итог серии: обработано {done} из {n}, пропущено {n - done}")

    answer = input("Продолжить? (да/нет): ").strip().lower()
    if answer != "да":
        print("Выход по ответу «нет»")
        break

print("Конец работы")
