#!/usr/bin/env python3
"""
Главный файл для запуска эмулятора процессора
Вариант №9 - Одноадресная архитектура Фон-Неймана
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == "__main__":
    print("Запуск эмулятора процессора...")
    print("Вариант №9 - Одноадресная архитектура Фон-Неймана")
    print("Задания: Поиск максимума в массиве и свертка двух массивов")
    print("-" * 60)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


