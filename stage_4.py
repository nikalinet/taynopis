# «Тайнопись» - этап 4

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

print("=== Тайнопись: шифр Цезаря ===")

# Основное меню: повторяется, пока не выберут выход
while True: #1
    print()
    print("1 - утаить, 2 - явить, 0 - откланяться")
    mode_str = input("Чего изволишь, добрый молодец? ")

    if not mode_str.isdigit() or int(mode_str) > 2: #2
        print("Смутьян! Вразуми: ничто (0), един (1) али два (2) - иных чисел не ведаю.")
        continue

    mode = int(mode_str)
    if mode == 0:
        print("Слово молвлено, дело сделано. Кланяюсь да ухожу, аки гость незваный.")
        break

    text = input("Молви слово тайное: ")

    shift_str = input("На сколько шагов воротить? ")
    while not shift_str.removeprefix("-").isdigit(): #3
        print("Бестолочь! Шаг воротить цифирью целой молви, а не смуту наводи.")
        shift_str = input("На сколько шагов воротить? ")
    shift = int(shift_str)

    if mode == 1:
        k = shift
        action = "Утаённое"  # Шифрованное
    else:
        k = -shift
        action = "Явленное"  # Дешифрованное

    result = ""
    kept = 0
    for i in range(len(text)): #4
        ch = text[i]

        # Не буква (пробел, цифра, знак) - оставляем как есть и идём к следующему знаку
        if ch not in low and ch not in up:
            result += ch
            kept += 1
            continue

        if ch in low:
            result += low[(low.index(ch) + k) % 33]
        else:
            result += up[(up.index(ch) + k) % 33]

    print(f"{action} письмецо: {result}")
    print(f"Букв сдвинуто: {len(text) - kept}, прочих знаков не тронуто: {kept}")

    answer = input("Продолжим воротить буковки, али откланяемся? (да / нет): ")
    while answer not in ("да", "нет"):
        print("Смутьян! Молви ясно: 'да' али 'нет' — иных речей не разумею.")
        answer = input("Продолжим воротить буковки, али откланяемся? (да / нет): ")

    if answer != "да":
        print("Бывай, добрый молодец. Шаг береги аки зеницу ока - потеряешь, сам себя не прочтёшь.")
        break

print("Коли не сработало — то не моя вина, а Цезаря окаянного.")
