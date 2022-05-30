# jupyter lab - для запуска файла с ТЗ
# поправил комиты
import datetime
import datetime as dt  # библиотека для работы с датой dt - для удобства обращения к ней далее в коде
from collections import defaultdict
# класс defaultdict который позволяет добавлять в словарь значения по несуществующим ключам без проверки и инициации
# т.е. если вы попытаетесь присвоить значение несуществующему ключу программа вылетит в ошибку, но при использовании данного
# класса такого не произойдет:
# Когда в цикле for ... in ключ k встречается в первый раз, то его еще нет в словаре d и запись d[k]
# создается автоматически с помощью функции default_factory, которая возвращает пустой список.
# Затем операция list.append() присоединяет значение к новому списку. Когда ключ словаря d
# встречаются снова, то возвращая список для этого ключа и операция list.append() добавляет другое значение в список.
# Этот метод проще и быстрее, чем эквивалентный метод словаря dict.setdefault()

import json            # библиотека для структурированного хранения данных в файле в формате json
import os.path         # библиотека работы с файлами операционной системы

def greet():
    print("Приветствуем вас в приложении")
    print("-----------------------------")
    print("------- Учёт финансов -------")
    print("-----------------------------")
    print("        Режимы работы:       ")
    print("-----------------------------")
    print("   1.  Добавить зачисление   ")
    print("   2.  Добавить трату        ")
    print("   3.  Получить статистику   ")
    print("   3.1 За все время учета    ")
    print("   3.2 Траты и поступления   ")
    print("   3.3 Баланс по месяцам     ")
    print("   3.4 Баланс по категориям  ")
    print("   3.5 За все время учета    ")
    print("   4.  Выйти из программы    ")
    print("-----------------------------")
    print(" Формат ввода даты: YY-MM-DD ")

def ask_mode():
    print("-----------------------------")
    return input("    Выберите режим работы:   ")

def wrong():
    print("-----------------------------")
    print(" Вы ввели некорректный режим ")

def ask_cost(ask_str):
    number = None
    while number is None:
        num_str =  input("  Введите сумму:             ")
        if num_str.isdigit():  # проверка - является ли числом строка
            number = int(num_str)
        else:
            print(" Вы ввели некорректное число!")
            continue
    return number

def ask_date(ask_str):
    date = None
    while date is None:
        date_str = input(ask_str)
        splitted = date_str.split("-")
        
        if len(splitted) != 3:
            print(" Введена некорректная дата!  ")
            continue
        
        check = []  # разделим дату на 3 числа и поместим вот в этот список для проверки
        for string in splitted:
            check.append(string.isdigit())
        
        if not(all(check)): #  проверим всели числа в списке-проверке числа
            print(" Часть даты- не число!       ")
            continue
        
        splitted[0] = "20"+splitted[0]
        year, month, day = map(int, splitted) # присвоим 3-м переменным значения из списка длиной 3 элемента
        date = dt.date(year, month, day) # преобразуем числа даты в формат даты питона для удобства работы
                                        # (сравнение сложение дат)
    return date

def ask_income():
    print("-----------------------------")
    cat = input("  Введите категорию:         ")
    cost = ask_cost("  Введите сумму поступления:")
    date = ask_date("  Введите дату поступления: ")
    return ["+", cat, date, cost]

def ask_spend():
    print("-----------------------------")
    cat = input("  Введите категорию:         ")
    cost = ask_cost("  Введите сумму траты:      ")
    date = ask_date("  Введите дату траты:       ")
    return ["-", cat, date, cost]

def ask_interval():
    date1 = ask_date("  Введите начало интервала:")
    date2 = ask_date("  Введите конец интервала: ")
    return (date1,date2)


# посчитаем за весь период
def ask_all_date(data_):
    date1 = data_[0][2]
    date2 = data_[1][2]
    for rec in data_:
        if rec[2] < date1:
            date1 = rec[2]
        if rec[2] > date2:
            date2 = rec[2]
    print(f'Период для статистики от {date1} до {date2}')
    return (date1,date2)

def stat(data, date1, date2):
    # для удобства используется специальный словарь, который по умолчанию содержит пустой список
    # в данном словаре будут храниться данные в виде КЛЮЧ-КАТЕГОРИЯ:[ЗНАЧЕНИЯ В ВИДЕ СПИСКА]
    income_stat = defaultdict(list)
    spend_stat = defaultdict(list)

    # data - список списков, один элемент списка это список из 4х элементов
    # чтобы продвигаться по такому списку в итераторе можно использовать 4 переменные
    for typ, cat, date, cost in data:
        if date >= date1 and date <= date2:
            if typ == "+":
                income_stat[cat].append(cost)
            if typ == "-":
                spend_stat[cat].append(cost)
    
    print("-----------------------------")
    print("  Статистика поступлений:    ")
    print("-----------------------------")
    for cat, cost_list in income_stat.items():
        print(f"  {cat:20} - {sum(cost_list)}")
    print("-----------------------------")
    print("  Статистика трат:           ")
    print("-----------------------------")
    for cat, cost_list in spend_stat.items():
        print(f"  {cat:20} - {sum(cost_list)}")


def all_income_cost(data, key_ = 1):
    # для удобства используется специальный словарь, который по умолчанию содержит пустой список
    # в данном словаре будут храниться данные в виде КЛЮЧ-КАТЕГОРИЯ:[ЗНАЧЕНИЯ В ВИДЕ СПИСКА]
    income_stat = defaultdict(list)
    spend_stat = defaultdict(list)
    sum_cost = 0
    sum_income = 0

    if key_ == 1:
        for typ, cat, date, cost in data:
            if typ == "+":
                income_stat[cat].append(cost)
            if typ == "-":
                spend_stat[cat].append(cost)

        print("-----------------------------")
        print("  Статистика поступлений:    ")
        print("-----------------------------")
        for cat, cost_list in income_stat.items():
            sum_income += sum(cost_list)
        print(f"Всего поступлений было: {sum_income}")
        print("-----------------------------")
        print("  Статистика трат:           ")
        print("-----------------------------")
        for cat, cost_list in spend_stat.items():
            sum_cost += sum(cost_list)
        print(f"Всего трат было:  {sum_cost}")
    elif key_ == 2:
#        d = datetime.date
        for typ, cat, date, cost in data:
            yy = date.year
            mm = date.month
            if typ == "+":
                income_stat[str(yy) + "-" + str(mm)].append(cost)
            if typ == "-":
                spend_stat[str(yy) + "-" + str(mm)].append(cost)
        else:
            print("Не правильно выбран ключ для функции статистики")

        print("------------------------------------")
        print("  Статистика поступлений по месяцам:")
        print("------------------------------------")
        for cat, cost_list in income_stat.items():
            print(f"  {cat:20} - {sum(cost_list)}")
        print("----------------------------------")
        print("  Статистика трат по месяцам :")
        print("----------------------------------")
        for cat, cost_list in spend_stat.items():
            print(f"  {cat:20} - {sum(cost_list)}")

def loop(data):
    greet()
    
    while True:
        mode = ask_mode()
        if mode == "1":
            data.append(ask_income())
        elif mode == "2":
            data.append(ask_spend())
        elif mode == "3":
            beg, end = ask_interval()
            stat(data, beg, end)
        elif mode == "3.1":
            beg, end = ask_all_date(data)
            stat(data, beg, end)
        elif mode == "3.2":
            all_income_cost(data, 1)
        elif mode == "3.3":
            all_income_cost(data, 2)
        elif mode == "3.4":
            beg, end = ask_all_date(data)
            stat(data, beg, end)
        elif mode == "4":
            break
        else:
            wrong()
    
    print("-----------------------------")
    print("      Данные сохранены!      ")
    print("-----------------------------")
    return data

def save(data, FILENAME, key_):
    # формат json не работает с форматом datetime, поэтому приходится перед сохранением списка в файл
    # преобразовывать элемент списка дата в строковый тип
    for rec in data:
        rec[2] = str(rec[2])  # преобразование делается в этой строке

    # шифруем
    for rec_clear in data:
        rec_clear[0] = my_crypt(str(rec_clear[0]), key_)
        rec_clear[1] = my_crypt(str(rec_clear[1]), key_)
        rec_clear[2] = my_crypt(str(rec_clear[2]), key_)
        rec_clear[3] = my_crypt(str(rec_clear[3]), key_)

    with open(FILENAME, "w") as f: # открываем файл с именем FILENAME и разрешаем туда запись через ключ "w"
        json.dump(data, f) # преобразуем список списков в формат json и отправляем данные в файл

def read(FILENAME, key_):
    # проверка - а есть ли на диске этот файл
    if os.path.isfile(FILENAME):
        with open(FILENAME) as f:
            data = json.load(f) # читаем формат json, преобразуем его и копируем в список data
    else:
        data = []

    # дешифруем
    for rec_clear in data:
        rec_clear[0] = my_decrypt(str(rec_clear[0]), key_)
        rec_clear[1] = my_decrypt(str(rec_clear[1]), key_)
        rec_clear[2] = my_decrypt(str(rec_clear[2]), key_)
        rec_clear[3] = int(my_decrypt(str(rec_clear[3]), key_))

    # данный код необходим чтобы вернуть правильный формат даты, чтобы можно было сравнивать даты между собой
    for rec in data:
        date_ints = map(int, rec[2].split("-")) # обратно преобразуем строку с датой в список чисел даты
        rec[2] = dt.date(*date_ints) #  преобразуем списко с числами в формат datetime и записываем с список
    return data

def check_user(usr, psw):
    users = {"admin": "qwe",
             "user1": "q45",
             "user2": "678"
         }
    if not(usr in users):
        return False
    else:
        if users[usr] != psw:
            return False
        else:
            return True


def my_crypt(str_, key_, mode_= 1):
# chr(x) - Возвращает односимвольную строку, код символа которой равен x.
# ord(с) - Код символа.
    # вариант 1 - простая замена символов на коды - простой способ
    if mode_ == 1:
        result = []
        mult_key = sum([ord(ch) for ch in key_])
        for sym in str_:
            result.append(ord(sym) + mult_key)
        return "/".join(map(str, result))
    else:
    #вариант 2 шифр цезаря для наименования файлов - посложнее
        s = str_
        steps = sum([ord(ch) for ch in key_])  # дешифровка указываем просто -
        result = ""

        for char in s:
            letter_number = ord(char) - ord('a')
            letter_number = (letter_number + steps) % 26  # 26 разность между кодами a и  z
            encoded_char = chr(ord('a') + letter_number)
            result += encoded_char
        return result


def my_decrypt(str_, key_, mode_=1):
# chr(x) - Возвращает односимвольную строку, код символа которой равен x.
# ord(с) - Код символа.
# Вариант 1 - простая замена смиволов кодами
    if mode_ == 1:
        result = []
        mult_key = sum([ord(ch) for ch in key_])
        list_ = str_.split("/")
        for sym in list_:
            result.append(chr(int(sym) - mult_key))
        return "".join(map(str, result))
    else:
# Вариант 2 - шифр Цезаря
        s = str_
        steps = sum([ord(ch) for ch in key_]) * -1# дешифровка указываем просто с минусом
        result = ""

        for char in s:
            letter_number = ord(char) - ord('a')
            letter_number = (letter_number + steps) % 26  # 26 разность между кодами a и  z
            encoded_char = chr(ord('a') + letter_number)
            result += encoded_char
        return result


def main(FILENAME, usr_key):
    data = read(FILENAME, usr_key)
    data = loop(data)
    save(data, FILENAME, usr_key)


usr = input('Введите имя пользователя:' )
psw = input('Введите пароль: ')
if check_user(usr, psw):
    main(my_crypt(usr, psw, 2).replace("/", "") + "_journal.json", psw)
else:
    print(f'Пользователь не прошел проверку, перезапустите программу')