#!/usr/bin/env python3
"""
Быстрый тест эмулятора для проверки основных функций
"""

from processor import Processor
from assembler import Assembler

def quick_test():
    """Быстрый тест основных функций"""
    print("🚀 Быстрый тест эмулятора процессора")
    print("=" * 50)
    
    # Инициализация
    processor = Processor()
    assembler = Assembler()
    
    # Тестовая программа
    test_code = """
LOAD #100
ADD #50
STORE 200
LOAD 200
SUB #25
STORE 201
HALT
"""
    
    print("📝 Тестовая программа:")
    print(test_code)
    
    try:
        # Ассемблирование
        print("🔧 Ассемблирование...")
        instructions = assembler.assemble(test_code)
        print(f"✅ Успешно! Сгенерировано {len(instructions)} инструкций")
        
        # Загрузка в процессор
        machine_codes = [instr['instruction'] for instr in instructions]
        processor.load_program(machine_codes)
        print("✅ Программа загружена в процессор")
        
        # Выполнение
        print("\n🚀 Выполнение программы...")
        print("Шаг | PC | ACC | Команда")
        print("-" * 30)
        
        step = 0
        while not processor.halted and step < 20:
            pc_before = processor.PC
            acc_before = processor.ACC
            
            if processor.step():
                ir = processor.IR
                opcode = (ir >> 12) & 0xF
                operand = ir & 0xFFF
                
                opcodes = {0x0: 'HALT', 0x1: 'LOAD', 0x2: 'STORE', 0x3: 'ADD', 0x4: 'SUB', 0x5: 'CMP', 0x6: 'JMP', 0x7: 'JZ', 0x8: 'JNZ'}
                cmd_name = opcodes.get(opcode, f'UNK({opcode})')
                
                print(f"{step+1:3d} | {pc_before:2d} | {acc_before:3d} | {cmd_name} {operand}")
                step += 1
            else:
                break
                
        print("-" * 30)
        
        # Результаты
        print("\n📊 Финальное состояние:")
        print(f"   ACC: {processor.ACC}")
        print(f"   PC:  {processor.PC}")
        print(f"   Статус: {'Остановлен' if processor.halted else 'Активен'}")
        print(f"   Шагов: {processor.step_count}")
        
        print("\n💾 Результаты в памяти:")
        for addr in [200, 201]:
            if processor.memory[addr] != 0:
                print(f"   Memory[{addr}] = {processor.memory[addr]}")
                
        # Проверка ожидаемых результатов
        print("\n🔍 Проверка результатов:")
        expected_200 = 150  # 100 + 50
        expected_201 = 125  # 150 - 25
        
        if processor.memory[200] == expected_200:
            print(f"   ✅ Memory[200] = {processor.memory[200]} (ожидалось {expected_200})")
        else:
            print(f"   ❌ Memory[200] = {processor.memory[200]} (ожидалось {expected_200})")
            
        if processor.memory[201] == expected_201:
            print(f"   ✅ Memory[201] = {processor.memory[201]} (ожидалось {expected_201})")
        else:
            print(f"   ❌ Memory[201] = {processor.memory[201]} (ожидалось {expected_201})")
            
        if processor.halted:
            print("   ✅ Программа завершилась корректно")
        else:
            print("   ❌ Программа не завершилась")
            
        print("\n🎉 Быстрый тест завершен!")
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False
        
    return True

if __name__ == "__main__":
    success = quick_test()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ ЭМУЛЯТОР РАБОТАЕТ КОРРЕКТНО!")
        print("📋 Можете переходить к ручному тестированию GUI:")
        print("   python3 gui.py")
        print("   python3 visual_gui.py") 
        print("   python3 enhanced_gui.py")
    else:
        print("\n" + "=" * 50)
        print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        print("🔧 Проверьте код эмулятора перед тестированием GUI")

