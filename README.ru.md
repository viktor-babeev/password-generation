# password-generation

Скрипт на Python для **автоматической генерации надежных паролей** по заданным критериям, с привязкой к списку ФИО. 

Программа работает в фоновом режиме, считывает входные данные из текстового файла, генерирует уникальные пароли методом контролируемого подбора и сохраняет результат в отдельный отчет/файл.

## ✨ Особенности и критерии пароля

Каждый сгенерированный пароль строго соответствует следующим правилам:
* ✨ **Длина:** ровно 12 символов.
* 🔠 **Заглавные буквы:** ровно 3 (только латиница `A-Z`).
* 🔡 **Строчные буквы:** ровно 3 (только латиница `a-z`).
* 🔢 **Цифры:** ровно 3 (`0-9`).
* 🔣 **Спецсимволы:** ровно 3 (исключая системные/проблемные знаки вроде `` ` ``, `~`, `|`, `'`).
* 🛡️ **Уникальность:** все 12 символов в пароле уникальны (нет повторяющихся знаков).

## 📁 Структура проекта

Для работы скрипта в одной директории должны находиться следующие файлы:
* `password-generation.py` — основной файл программы с логикой генерации.
* `FioLatinica.txt` — исходный файл со списком ФИО (создается вручную).
* `PasswdFile.txt` — результирующий файл с готовыми парами ФИО-Пароль (создается автоматически).

## 🚀 Инструкция по использованию

### 1. Подготовка входных данных
Создайте в папке с проектом файл `FioLatinica.txt`. Заполните его именами в формате `IvanovVL`, каждое имя с новой строки:
```text
IvanovVL
PetrovIA
SidorovAK
```

### 2. Запуск программы
Программа не требует внешних библиотек и работает на чистом Python 3.

**Обычный запуск:**
* **Для Windows**
  ```bash
  python password-generation.py
  ```
* **Для Linux / macOS:**
  ```bash
  python3 password-generation.py
  ```

### 3. Результат работы
После выполнения в папке появится файл `PasswdFile.txt` следующего вида:
```text
IvanovVL   |   hB:6#5FQo8)q
==========================================
PetrovIA   |   kn4Gt9/O+1#V
==========================================
SidorovAK   |   zP@bOX9l03/*
==========================================
```

## 🛠️ Технологии
* **Language:** Python 3.x
* **Core Modules:** `random` (randint)

## 📜 Лицензия / License

This project is licensed under the **CC BY-NC 4.0** License.
*   **Allowed:** free copying, modifying, and personal/educational/non-commercial use.
*   **🚫 PROHIBITED:** any commercial use of the source code or its derivatives without prior written permission from the author.

---

This project is licensed under the **CC BY-NC 4.0** License.
*   **Allowed:** free copying, modifying, and personal/educational/non-commercial use.
*   **🚫 PROHIBITED:** any commercial use of the source code or its derivatives without prior written permission from the author.
