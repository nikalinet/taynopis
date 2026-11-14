# «Тайнопись» — модуль со сценариями (этап 3)
# Сценарий: меню -> проверка режима -> текст -> проверка сдвига -> преобразование -> вывод

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

print("=== Тайнопись: шифр Цезаря ===")
print("1 — зашифровать, 2 — расшифровать, 0 — выход")
mode_str = input("Выберите режим: ")

# Проверка режима: сначала нечисловой ввод, потом диапазон 0..2
if not mode_str.isdigit():
    print("Неведомо сие: режим должен быть числом 0, 1 или 2")
elif int(mode_str) > 2:
    print("Неведомо сие: такого режима нет, допустимы 0, 1 и 2")
elif int(mode_str) == 0:
    print("Выход. До свидания!")
else:
    mode = int(mode_str)
    text = input("Введите текст: ")
    shift_str = input("Введите сдвиг (целое число): ")

    # Проверка сдвига: допускаем знак «минус» перед цифрами
    if not shift_str.removeprefix("-").isdigit():
        print("Ошибка: сдвиг должен быть целым числом")
    else:
        shift = int(shift_str)

        if mode == 1:
            k = shift
            action = "Зашифрованный"
        else:
            k = -shift
            action = "Расшифрованный"

        k = k % 33
        table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
        result = text.translate(table)
        print(f"{action} текст: {result}")
