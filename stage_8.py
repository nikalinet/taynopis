# «Тайнопись» - этап 8: классы
# Record - одно письмо, History - летопись и файл, App - меню.
# Связи: App содержит History, History содержит список Record.
# Наследования нет: вид сущности один, утаить и явить отличаются только режимом.

import json

low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = low.upper()

# Кортеж: фиксированная связка «номер режима -> название», не меняется во время работы
MODE_NAMES = ("Откланяться", "Утаённое", "Явленное")

# Файл летописи: создаётся программой при первом сохранении
DATA_FILE = "letopis.json"


# ---------- Функции без состояния: параметры и return ----------

# Годится ли строка как пункт меню (цифра от 0 до 5)
def is_mode(value):
    return value.isdigit() and int(value) <= 5


# Годится ли строка как число писем (целое от единицы)
def is_count(value):
    return value.isdigit() and int(value) > 0


# Годится ли строка как шаг (целое число, можно с минусом)
def is_shift(value):
    return value.removeprefix("-").isdigit()


# Сдвигает буквы текста на k шагов, прочие знаки не трогает
def shift_text(text, k):
    k = k % 33
    table = str.maketrans(low + up, low[k:] + low[:k] + up[k:] + up[:k])
    return text.translate(table)


# ---------- Record: одно письмо ----------

class Record:
    # Новое письмо: режим и слово, шаг пока 0
    def __init__(self, mode, text):
        self.mode = mode
        self.source = text
        self.shift = 0
        self.result = text

    # Меняет шаг с проверкой и сразу пересчитывает результат; False - шаг не принят
    def set_shift(self, value):
        if not is_shift(value):
            return False

        self.shift = int(value)
        if self.mode == 1:
            self.result = shift_text(self.source, self.shift)
        else:
            self.result = shift_text(self.source, -self.shift)
        return True

    # Название действия для показа
    def action(self):
        return MODE_NAMES[self.mode]

    # Сколько букв в письме
    def letters(self):
        count = 0
        for ch in self.source:
            if ch in low or ch in up:
                count += 1
        return count

    # Сколько в письме прочих знаков
    def others(self):
        return len(self.source) - self.letters()

    # Есть ли запрос в исходном слове или в результате
    def matches(self, query):
        return query in self.source.lower() or query in self.result.lower()

    # Краткий текст письма: то же имя метода есть у History
    def short(self):
        return f"{self.action()}: «{self.source}» -> «{self.result}» (шаг {self.shift})"

    # Словарь для записи в файл
    def to_dict(self):
        return {"action": self.action(), "source": self.source, "shift": self.shift, "result": self.result}


# ---------- History: летопись, счётчики и файл ----------

class History:
    # Новая летопись: имя файла, пустой список писем, счётчики с нуля
    def __init__(self, filename):
        self.filename = filename
        self.records = []
        self.counts = {"Утаённое": 0, "Явленное": 0, "Не воротили": 0}

    # Читает файл; если его ещё нет, летопись остаётся пустой
    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        self.counts = data["counts"]
        for item in data["history"]:
            record = Record(MODE_NAMES.index(item["action"]), item["source"])
            record.set_shift(str(item["shift"]))
            self.records.append(record)

    # Записывает файл: режим "w" заменяет старое содержимое целиком
    def save(self):
        items = []
        for record in self.records:
            items.append(record.to_dict())

        data = {"history": items, "counts": self.counts}
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    # Добавляет письмо и считает его
    def add(self, record):
        self.records.append(record)
        self.counts[record.action()] += 1

    # Считает письмо, которое не воротили
    def skip(self):
        self.counts["Не воротили"] += 1

    # Пуста ли летопись
    def is_empty(self):
        return len(self.records) == 0

    # Отбирает письма по запросу: проверку делает само письмо
    def search(self, query):
        found = []
        for record in self.records:
            if record.matches(query):
                found.append(record)
        return found

    # Считает меньший и больший шаг, шаги по возрастанию, число разных шагов
    def shift_stats(self):
        shifts = []
        for record in self.records:
            shifts.append(record.shift)
        return min(shifts), max(shifts), sorted(shifts), len(set(shifts))

    # Краткий текст летописи: то же имя метода есть у Record
    def short(self):
        return f"Сказаний писано: {len(self.records)}"

    # Строка со всеми счётчиками
    def counts_text(self):
        counts = self.counts
        return f"Утаённое: {counts['Утаённое']}, явленное: {counts['Явленное']}, не воротили: {counts['Не воротили']}"


# ---------- App: меню спрашивает, вызывает методы, печатает ----------

class App:
    # Приложение содержит летопись
    def __init__(self, filename):
        self.history = History(filename)

    # Печатает письма: общий метод для летописи и поиска
    def print_records(self, records):
        for record in records:
            print(record.short())

    # Одно письмо: спрашивает слово и шаг, показывает результат. True - письмо ворочено
    def run_letter(self, mode):
        text = input("Молви слово тайное: ").strip()

        # Пустое письмо в историю не попадает
        if text == "":
            print("Остолоп! Пустое слово не воротишь — молви письмо.")
            self.history.skip()
            return False

        record = Record(mode, text)

        if not record.set_shift(input("На сколько шагов воротить? ").strip()):
            print("Беда: шаг не цельный, письмо сгинуло, аки камень в омуте.")
            self.history.skip()
            return False

        print(f"{record.action()}: {record.result}")
        print(f"Ворочено буквиц: {record.letters()}, а прочей мелочи не тронуто: {record.others()}")
        self.history.add(record)
        return True

    # Пункты меню 1 и 2: серия из n писем, одна для обоих режимов
    def run_series(self, mode, n):
        done = 0
        for i in range(1, n + 1):
            print(f"--- Письмецо {i} из {n} ---")
            if self.run_letter(mode):
                done += 1

        print(f"А как сочли: ворочено: {done} из {n}, а {n - done} не воротили — лежат, аки камни в омуте.")

    # Пункт меню 3: летопись, шаги и счётчики
    def show_history(self):
        if self.history.is_empty():
            print("Летопись не писана: ни былин, ни сказаний.")
            return

        print(self.history.short())
        self.print_records(self.history.records)

        smallest, largest, sorted_shifts, unique_count = self.history.shift_stats()
        print(f"Шагов воротим: от мала {smallest}, до велика {largest}, "
              f"аки ручей от истока к устью {sorted_shifts}")
        print(f"Шагов всяких: {unique_count}")
        print(self.history.counts_text())

    # Пункт меню 4: поиск по истории без учёта регистра
    def run_search(self):
        query = input("Чего изволишь отыскать в письменах минувшего? ").strip().lower()

        if query == "":
            print("Остолоп! Пустое слово не сыщешь — молви, чего искать")
            return

        found = self.history.search(query)
        print(f"Нашлось, письмо заветное: {len(found)}")
        self.print_records(found)

    # Пункт меню 5 и выход: пишет в файл и сообщает об этом
    def run_save(self):
        self.history.save()
        print(f"Схоронено в {self.history.filename}. {self.history.short()}")

    # Спрашивает «да» или «нет», пока не ответят ясно, и возвращает ответ
    def ask_answer(self):
        answer = input("Продолжим воротить буковки, али откланяемся? (да / нет): ").strip().lower()

        while answer not in ("да", "нет"):
            print("Смутьян! Молви ясно: «да» али «нет» — иных речей не разумею.")
            answer = input("Продолжим воротить буковки, али откланяемся? (да / нет): ").strip().lower()

        return answer

    # Главное меню: читает файл до работы с меню, вызывает методы, пишет файл при выходе
    def run(self):
        print("=== Тайнопись: шифр Цезаря ===")

        self.history.load()
        print(f"Поднято из {self.history.filename}. {self.history.short()}")

        while True:
            print()
            print("1 - утаить, 2 - явить, 3 - летопись, 4 - отыскать, 5 - схоронить, 0 - откланяться")
            mode_str = input("Чего изволишь, добрый молодец? ").strip()

            if not is_mode(mode_str):
                print("Смутьян! Вразуми: мне цифирью молви, числом от ничто (0) до пяти (5)")
                continue

            mode = int(mode_str)

            if mode == 0:
                print("Слово молвлено, дело сделано. Кланяюсь да ухожу, аки гость незваный.")
                break
            elif mode == 3:
                self.show_history()
                continue
            elif mode == 4:
                self.run_search()
                continue
            elif mode == 5:
                self.run_save()
                continue

            n_str = input("Сколько писем изволишь воротить? ").strip()

            if not is_count(n_str):
                print("Горе-писарь! Молви, сколько писем воротить, числом целым от единицы.")
                continue

            self.run_series(mode, int(n_str))

            if self.ask_answer() != "да":
                print("Бывай, добрый молодец. Шаг береги аки зеницу ока — потеряешь, сам себя не прочтёшь.")
                break

        # Оба выхода (0 и «нет») приходят сюда, поэтому письма не потеряются
        self.run_save()
        print("Коли не сработало — то не моя вина, а Цезаря окаянного.")


app = App(DATA_FILE)
app.run()
