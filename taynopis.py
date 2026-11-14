# «Тайнопись» — шифр Цезаря для русского алфавита (промежуточная защита, этапы 0–4)
# Меню (while) -> режим -> серия из N сообщений (for + range) -> итог -> «Продолжить?»

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

print("=== Тайнопись: шифр Цезаря ===")

# Основное меню: повторяется, пока пользователь не выберет выход
while True:
    print()
    print("1 — зашифровать, 2 — расшифровать, 0 — выход")
    mode_str = input("Выберите режим: ")

    # Проверка режима: сначала нечисловой ввод, потом диапазон 0..2
    if not mode_str.isdigit():
        print("Неведомо сие: режим должен быть числом 0, 1 или 2")
        continue
    mode = int(mode_str)
    if mode == 0:
        print("Выход по команде 0")
        break
    elif mode > 2:
        print("Неведомо сие: такого режима нет, допустимы 0, 1 и 2")
        continue
    elif mode == 1:
        action = "Зашифровано"
    else:
        action = "Расшифровано"

    # Размер серии N: сколько сообщений обработать за один раз
    n_str = input("Сколько сообщений обработать? ")
    if not n_str.isdigit() or int(n_str) == 0:
        print("Ошибка: количество должно быть целым числом больше 0")
        continue
    n = int(n_str)

    # Серия: обрабатываем N сообщений, считаем успешные
    done = 0
    for i in range(1, n + 1):
        print(f"--- Сообщение {i} из {n} ---")
        text = input("Введите текст: ")
        shift_str = input("Введите сдвиг (целое число): ")

        # Брак одного значения: пропускаем это сообщение, серия продолжается
        if not shift_str.removeprefix("-").isdigit():
            print("Ошибка: сдвиг должен быть целым числом, сообщение пропущено")
            continue

        shift = int(shift_str)
        if mode == 1:
            k = shift % 33
        else:
            k = -shift % 33
        table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
        result = text.translate(table)
        print(f"{action}: {result}")
        done += 1

    print(f"Итог серии: обработано {done} из {n}, пропущено {n - done}")

    answer = input("Продолжить? (да/нет): ").strip().lower()
    if answer != "да":
        print("Выход по ответу «нет»")
        break

print("Конец работы")
