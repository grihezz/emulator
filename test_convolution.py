#!/usr/bin/env python3
"""
Тест программы свертки
"""

from processor import Processor
from assembler import Assembler

def test_convolution():
    """Тест программы свертки"""
    print("🧮 Тест программы свертки массивов")
    print("=" * 50)
    
    # Читаем программу
    with open('programs/convolution_simple.asm', 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    print("📝 Программа свертки:")
    print("A = [2, 3], B = [4, 5]")
    print("Ожидаемый результат: 2*4 + 3*5 = 8 + 15 = 23")
    
    # Инициализация
    processor = Processor()
    assembler = Assembler()
    
    try:
        # Ассемблирование
        print("\n🔧 Ассемблирование...")
        instructions = assembler.assemble(source_code)
        print(f"✅ Успешно! Инструкций: {len(instructions)}")
        
        # Загрузка программы
        machine_codes = [instr['instruction'] for instr in instructions]
        processor.load_program(machine_codes)
        
        # Загрузка тестовых данных
        array_a = [2, 3]  # A = [2, 3]
        array_b = [4, 5]  # B = [4, 5]
        processor.load_data(array_a, 200)
        processor.load_data(array_b, 210)
        
        print("📊 Загружены данные:")
        print(f"   A = {array_a} (адреса 200-201)")
        print(f"   B = {array_b} (адреса 210-211)")
        
        # Выполнение
        print("\n🚀 Выполнение программы...")
        processor.run(max_steps=100)
        
        # Результаты
        print(f"\n📊 Результаты:")
        print(f"   ACC: {processor.ACC}")
        print(f"   Статус: {'Остановлен' if processor.halted else 'Выполняется'}")
        print(f"   Шагов: {processor.step_count}")
        
        print(f"\n💾 Результат свертки:")
        result = processor.memory[100]
        print(f"   Memory[100] = {result}")
        
        # Проверка
        expected = 23  # 2*4 + 3*5 = 8 + 15 = 23
        if result == expected:
            print(f"   ✅ ПРАВИЛЬНО! Ожидалось {expected}, получено {result}")
        else:
            print(f"   ❌ ОШИБКА! Ожидалось {expected}, получено {result}")
            
        print(f"\n🔍 Промежуточные данные:")
        for addr in range(200, 220):
            if processor.memory[addr] != 0:
                print(f"   Memory[{addr}] = {processor.memory[addr]}")
                
        return result == expected
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_convolution()
    
    if success:
        print("\n🎉 Программа свертки работает корректно!")
        print("📋 Теперь можете загрузить ее в GUI:")
        print("   1. Скопируйте содержимое programs/convolution_simple.asm")
        print("   2. Вставьте в поле 'Исходный код' в GUI")
        print("   3. Нажмите 'Ассемблировать' → 'Загрузить'")
        print("   4. Нажмите 'Сброс' → 'Запуск'")
        print("   5. Результат должен быть в Memory[100] = 23")
    else:
        print("\n❌ Программа свертки требует доработки")
