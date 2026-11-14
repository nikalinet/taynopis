"""«Тайнопись» — шифр Цезаря для русского алфавита (33 буквы).

Модуль инициализации (этап 2): меню, ввод, приведение типов, вывод.
Сценарий соответствует паспорту проекта (этап 0) и блок-схеме (этап 1).
"""

ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_UPPER = ALPHABET_LOWER.upper()
ALPHABET_SIZE = len(ALPHABET_LOWER)  # 33


def shift_text(text, k):
    """Сдвигает каждую русскую букву на k позиций, сохраняя регистр.

    Пробелы, цифры и знаки препинания остаются без изменений.
    """
    result = ""
    for ch in text:
        if ch in ALPHABET_LOWER:
            result += ALPHABET_LOWER[(ALPHABET_LOWER.index(ch) + k) % ALPHABET_SIZE]
        elif ch in ALPHABET_UPPER:
            result += ALPHABET_UPPER[(ALPHABET_UPPER.index(ch) + k) % ALPHABET_SIZE]
        else:
            result += ch
    return result


def main():
    print("=== Тайнопись: шифр Цезаря ===")

    while True:
        # Вывод меню, ввод режима
        print()
        print("1 — зашифровать")
        print("2 — расшифровать")
        print("0 — выход")
        try:
            mode = int(input("Выберите режим: "))
        except ValueError:
            print("Неведомо сие: режим должен быть числом 0, 1 или 2.")
            continue

        if mode == 0:
            break
        if mode not in (1, 2):
            print("Неведомо сие: такого режима нет.")
            continue

        # Ввод текста
        text = input("Введите текст: ")

        # Ввод сдвига (повторяется до тех пор, пока не введено целое число)
        while True:
            try:
                shift = int(input("Введите сдвиг (целое число): "))
                break
            except ValueError:
                print("Ошибка: сдвиг должен быть целым числом. Попробуйте снова.")

        # Выбор направления сдвига
        k = shift if mode == 1 else -shift

        # Преобразование и вывод результата
        result = shift_text(text, k)
        action = "Зашифрованный" if mode == 1 else "Расшифрованный"
        print(f"{action} текст (сдвиг {shift}): {result}")

        # Продолжить?
        answer = input("Продолжить? (да/нет): ").strip().lower()
        if answer not in ("да", "д", "yes", "y"):
            break

    print("Конец работы. До свидания!")


if __name__ == "__main__":
    main()
