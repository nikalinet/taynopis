# «Тайнопись» - этап 3

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

print("=== Тайнопись: шифр Цезаря ===")
print("1 - утаить, 2 - явить, 0 - откланяться")
mode_str = input("Чего изволишь, добрый молодец? ")

# Без цикла, как по заданию
if not mode_str.isdigit() or int(mode_str) > 2:
    print("Смутьян! Вразуми: ничто (0), един (1) али два (2) - иных чисел не ведаю.")

elif int(mode_str) == 0:
    print("Слово молвлено, дело сделано. Кланяюсь да ухожу, аки гость незваный.") 
else:
    mode = int(mode_str)
    text = input("Молви слово тайное: ")
    shift_str = input("На сколько шагов воротить? ")

    if not shift_str.removeprefix("-").isdigit():
        print("Бестолочь! Шаг воротить цифирью целой молви, а не смуту наводи.") # Сдвиг должен быть целым числом
    else:
        shift = int(shift_str)

        if mode == 1:
            k = shift
            action = "Утаённое" # Шифрованное
        else:
            k = -shift
            action = "Явленное" # Дешифрованное

        k = k % 33
        table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
        result = text.translate(table)
        print(f"{action} письмецо заморское, а шаг не потеряй - сам себя не прочтёшь:  {result}")
