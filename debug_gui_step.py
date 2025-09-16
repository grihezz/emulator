#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from processor import Processor
from assembler import Assembler

# Тестируем простейшую программу пошагово
code = """
LOAD #42
STORE 100
HALT
"""

print("=== Тест пошагового выполнения ===")
print("Код:")
print(code)

try:
    # Ассемблируем
    asm = Assembler()
    instructions = asm.assemble(code)
    print(f"\n✅ Ассемблирование: {len(instructions)} инструкций")
    
    for i, instr in enumerate(instructions):
        print(f"{i:04X}: {instr['instruction']:04X} - {instr['mnemonic']}")
    
    # Загружаем в процессор
    proc = Processor()
    machine_codes = [instr['instruction'] for instr in instructions]
    proc.load_program(machine_codes)
    
    print(f"\n📊 Состояние после загрузки:")
    print(f"PC: {proc.PC}, ACC: {proc.ACC}, Halted: {proc.halted}")
    
    # Выполняем пошагово
    print(f"\n🔄 Выполнение пошагово:")
    step = 0
    while not proc.halted and step < 10:
        old_acc = proc.ACC
        old_pc = proc.PC
        success = proc.step()
        step += 1
        print(f"Шаг {step}: PC={old_pc}→{proc.PC}, ACC={old_acc}→{proc.ACC}, Halted={proc.halted}")
        if not success:
            print("❌ Ошибка выполнения!")
            break
    
    print(f"\n🎯 Результат:")
    print(f"Memory[100] = {proc.memory[100]}")
    print(f"Ожидается: 42")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
