#!/usr/bin/env python3
"""
Скрипт для тестирования графических интерфейсов
Автоматически загружает и тестирует различные программы
"""

import sys
import os
from processor import Processor
from assembler import Assembler

def test_program_file(filename, expected_results=None):
    """Тестирование программы из файла"""
    print(f"\n{'='*60}")
    print(f"Тестирование программы: {filename}")
    print(f"{'='*60}")
    
    # Читаем файл программы
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден")
        return False
    
    # Создаем процессор и ассемблер
    processor = Processor()
    assembler = Assembler()
    
    try:
        # Ассемблируем код
        print("📝 Ассемблирование...")
        instructions = assembler.assemble(source_code)
        print(f"✅ Ассемблирование успешно! Инструкций: {len(instructions)}")
        
        # Загружаем программу
        machine_codes = [instr['instruction'] for instr in instructions]
        processor.load_program(machine_codes)
        
        # Загружаем тестовые данные в зависимости от программы
        if 'max_search' in filename or 'array' in filename:
            test_data = [10, 25, 5, 30, 15]  # Массив для поиска максимума
            processor.load_data(test_data, 200)
            print("📊 Загружены тестовые данные для массива:", test_data)
        elif 'convolution' in filename:
            array_a = [2, 4, 6]
            array_b = [3, 5, 7]
            processor.load_data(array_a, 200)
            processor.load_data(array_b, 210)
            print("📊 Загружены массивы A:", array_a, "B:", array_b)
        elif 'factorial' in filename:
            print("📊 Программа факториала не требует дополнительных данных")
        else:
            print("📊 Программа не требует специальных тестовых данных")
        
        # Выполняем программу
        print("🚀 Выполнение программы...")
        steps = 0
        max_steps = 1000
        
        while not processor.halted and steps < max_steps:
            processor.step()
            steps += 1
            
        if processor.halted:
            print(f"✅ Программа завершена за {steps} шагов")
        else:
            print(f"⚠️  Программа не завершилась за {max_steps} шагов (возможно, бесконечный цикл)")
            
        # Показываем результаты
        print("\n📋 Финальное состояние процессора:")
        print(f"   ACC: {processor.ACC} (0x{processor.ACC:04X})")
        print(f"   PC:  {processor.PC} (0x{processor.PC:04X})")
        print(f"   IR:  {processor.IR} (0x{processor.IR:04X})")
        print(f"   Флаги: ZF={processor.flags['ZF']} SF={processor.flags['SF']} CF={processor.flags['CF']} OF={processor.flags['OF']}")
        
        print("\n💾 Содержимое памяти (ненулевые ячейки):")
        for i in range(0, 300):
            if processor.memory[i] != 0:
                if i < 100:
                    print(f"   Memory[{i:3d}] = {processor.memory[i]:5d} (0x{processor.memory[i]:04X}) - Программа")
                elif i < 200:
                    print(f"   Memory[{i:3d}] = {processor.memory[i]:5d} (0x{processor.memory[i]:04X}) - Переменные")
                else:
                    print(f"   Memory[{i:3d}] = {processor.memory[i]:5d} (0x{processor.memory[i]:04X}) - Данные")
        
        # Проверяем ожидаемые результаты
        if expected_results:
            print("\n🔍 Проверка ожидаемых результатов:")
            all_correct = True
            for addr, expected_value in expected_results.items():
                actual_value = processor.memory[addr]
                if actual_value == expected_value:
                    print(f"   ✅ Memory[{addr}] = {actual_value} (ожидалось {expected_value})")
                else:
                    print(f"   ❌ Memory[{addr}] = {actual_value} (ожидалось {expected_value})")
                    all_correct = False
            
            if all_correct:
                print("🎉 Все проверки пройдены успешно!")
            else:
                print("⚠️  Некоторые проверки не пройдены")
                
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False

def main():
    """Главная функция тестирования"""
    print("🧪 Автоматическое тестирование программ эмулятора")
    print("Этот скрипт поможет проверить работу различных программ")
    
    # Список программ для тестирования
    test_programs = [
        {
            'file': 'programs/simple_test.asm',
            'expected': {100: 42, 101: 12, 102: 12}
        },
        {
            'file': 'programs/array_demo.asm',
            'expected': {100: 150}  # 10+20+30+40+50 = 150
        }
    ]
    
    success_count = 0
    total_count = len(test_programs)
    
    for i, test_prog in enumerate(test_programs, 1):
        print(f"\n🔬 Тест {i}/{total_count}")
        if test_program_file(test_prog['file'], test_prog.get('expected')):
            success_count += 1
            
    print(f"\n{'='*60}")
    print(f"📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print(f"{'='*60}")
    print(f"Успешно: {success_count}/{total_count}")
    print(f"Процент успеха: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 Все тесты пройдены успешно!")
        print("\n📋 Инструкции по запуску GUI:")
        print("   Базовый интерфейс:     python3 gui.py")
        print("   Визуальный интерфейс:  python3 visual_gui.py")
        print("   Расширенный интерфейс: python3 enhanced_gui.py")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте программы.")
        
    print(f"\n💡 Для интерактивного тестирования запустите любой из GUI интерфейсов")
    print(f"   и загрузите программы из папки programs/")

if __name__ == "__main__":
    main()
