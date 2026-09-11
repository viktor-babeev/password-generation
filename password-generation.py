#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
password-generation.py
Автоматическая генерация паролей с проверкой надежности по списку ФИО.
Automatic password generation with strength checking against a list of full names.

(c) 2025 Viktor Sergeevich Babeev <babeev.v.s@gmail.com>
Repository: https://github.com/viktor-babeev

Terms of Use:
This code is licensed under CC BY-NC 4.0.
Commercial use of this software is strictly PROHIBITED 
without prior written permission from the author
"""


from random import randint


# Производит генерацию пароля
def gen_passwd():
    random_lenght = randint(12, 12)   # задается длина пароля
    result = ''
    for i in range(random_lenght):
        random_char = chr(randint(33, 126))
        result += random_char
    return result


# Производит проверку стойкости пароля
def check(s):
    rs = s
    if len(s) >= 8:  # если пароль больше N символов
        sch, sch_low, sch_up, sch_num, sch_not = 0, 0, 0, 0, 0
        while sch < len(rs) or (sch_low == 0 and sch_up == 0 and sch_num == 0):
            i = rs[sch]
            if i >= 'a' and i <= 'z':
                sch_low += 1
            elif i >= 'A' and i <= 'Z':
                sch_up += 1
            elif i >= '0' and i <= '9':
                sch_num += 1
            elif i == '`' or i == '~' or i == '|' or i == "'":
                sch_not += 1
            sch += 1
        if sch_low == 3 and sch_up == 3 and sch_num == 3 and len(rs) == len(set(rs)) and sch_not == 0:
            return True
    return False


# Пром.функция. Содержит цикл для формирования 1-го пароля.
def passwd_gen_cycle():
    rs = False
    sch = 0
    passwd = ''
    while not rs:
        passwd = gen_passwd()   # генерация пароля.
        rs = check(passwd)      # проверка пароля по условиям.
        # счетчик количества попыток формирования пароля удовлетворяющего условиям.
        sch += 1
    return passwd


def main():
    # открытие файлов.
    file_passwd = open("PasswdFile.txt", "w+")
    file_fio = open("FioLatinica.txt", "r")
    # В цикле проходим по файлу с ФИО и записываем новый файл с паролями.
    for line in file_fio:
        line = line.strip()
        if not line:
            break
        file_passwd.write(line)
        file_passwd.write(f'   |   ')
        res_passwd = str(passwd_gen_cycle())   # сформированный пароль.
        file_passwd.write(res_passwd)
        file_passwd.write(f'\n==========================================\n')
    file_passwd.close()                               # закрытие файла.


if __name__ == '__main__':
    main()
