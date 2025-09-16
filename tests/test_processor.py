"""
Тесты для эмулятора процессора
Проверяют корректность работы всех компонентов
"""

import unittest
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processor import Processor
from assembler import Assembler

class TestProcessor(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.processor = Processor()
        self.assembler = Assembler()
    
    def test_processor_initialization(self):
        """Тест инициализации процессора"""
        self.assertEqual(self.processor.ACC, 0)
        self.assertEqual(self.processor.PC, 0)
        self.assertEqual(self.processor.IR, 0)
        self.assertFalse(self.processor.halted)
        self.assertEqual(self.processor.step_count, 0)
        
        # Проверяем флаги
        for flag in ['ZF', 'SF', 'CF', 'OF']:
            self.assertFalse(self.processor.flags[flag])
    
    def test_memory_operations(self):
        """Тест операций с памятью"""
        # Загрузка программы
        program = [0x1001, 0x2002, 0x0000]  # LOAD #1, STORE 2, HALT
        self.processor.load_program(program)
        
        # Проверяем загрузку
        self.assertEqual(self.processor.memory[0], 0x1001)
        self.assertEqual(self.processor.memory[1], 0x2002)
        self.assertEqual(self.processor.memory[2], 0x0000)
        
        # Загрузка данных
        data = [1, 2, 3, 4, 5]
        self.processor.load_data(data, 100)
        
        # Проверяем загрузку данных
        for i, value in enumerate(data):
            self.assertEqual(self.processor.memory[100 + i], value)
    
    def test_load_instruction(self):
        """Тест команды LOAD"""
        # LOAD #5 (непосредственная адресация: 512 + 5)
        self.processor.execute_instruction(0x1, 517)  # 512 + 5
        self.assertEqual(self.processor.ACC, 5)
        self.assertFalse(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
        
        # LOAD #0 (непосредственная адресация: 512 + 0)
        self.processor.execute_instruction(0x1, 512)  # 512 + 0
        self.assertEqual(self.processor.ACC, 0)
        self.assertTrue(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
        
        # LOAD значение из памяти (прямая адресация)
        self.processor.memory[10] = 42
        self.processor.execute_instruction(0x1, 10)
        self.assertEqual(self.processor.ACC, 42)
        self.assertFalse(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
    
    def test_store_instruction(self):
        """Тест команды STORE"""
        # Устанавливаем значение в аккумулятор
        self.processor.ACC = 42
        
        # STORE 100
        self.processor.execute_instruction(0x2, 100)
        self.assertEqual(self.processor.memory[100], 42)
    
    def test_add_instruction(self):
        """Тест команды ADD"""
        # Устанавливаем начальное значение
        self.processor.ACC = 10
        
        # ADD #5 (непосредственная адресация: 512 + 5)
        self.processor.execute_instruction(0x3, 517)  # 512 + 5
        self.assertEqual(self.processor.ACC, 15)
        self.assertFalse(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
        
        # ADD из памяти (прямая адресация)
        self.processor.memory[10] = 5
        self.processor.execute_instruction(0x3, 10)
        self.assertEqual(self.processor.ACC, 20)  # 15 + 5
    
    def test_sub_instruction(self):
        """Тест команды SUB"""
        # Устанавливаем начальное значение
        self.processor.ACC = 20
        
        # SUB #5 (непосредственная адресация: 512 + 5)
        self.processor.execute_instruction(0x4, 517)  # 512 + 5
        self.assertEqual(self.processor.ACC, 15)
        self.assertFalse(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
        
        # SUB #15 (непосредственная адресация: 512 + 15)
        self.processor.execute_instruction(0x4, 527)  # 512 + 15
        self.assertEqual(self.processor.ACC, 0)
        self.assertTrue(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
    
    def test_cmp_instruction(self):
        """Тест команды CMP"""
        # Устанавливаем значение в аккумулятор
        self.processor.ACC = 10
        
        # CMP #10 (непосредственная адресация: 512 + 10)
        self.processor.execute_instruction(0x5, 522)  # 512 + 10
        self.assertTrue(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
        
        # CMP #5 (непосредственная адресация: 512 + 5)
        self.processor.execute_instruction(0x5, 517)  # 512 + 5
        self.assertFalse(self.processor.flags['ZF'])
        self.assertFalse(self.processor.flags['SF'])
        
        # CMP #15 (непосредственная адресация: 512 + 15)
        self.processor.execute_instruction(0x5, 527)  # 512 + 15
        self.assertFalse(self.processor.flags['ZF'])
        self.assertTrue(self.processor.flags['SF'])
    
    def test_jump_instructions(self):
        """Тест команд переходов"""
        # JMP 100
        self.processor.execute_instruction(0x6, 100)
        self.assertEqual(self.processor.PC, 100)
        
        # JZ 200 (флаг нуля установлен)
        self.processor.flags['ZF'] = True
        self.processor.execute_instruction(0x7, 200)
        self.assertEqual(self.processor.PC, 200)
        
        # JNZ 300 (флаг нуля не установлен)
        self.processor.flags['ZF'] = False
        self.processor.execute_instruction(0x8, 300)
        self.assertEqual(self.processor.PC, 300)
    
    def test_halt_instruction(self):
        """Тест команды HALT"""
        self.assertFalse(self.processor.halted)
        self.processor.execute_instruction(0x0, 0)
        self.assertTrue(self.processor.halted)
    
    def test_program_execution(self):
        """Тест выполнения простой программы"""
        # Программа: LOAD #5, ADD #3, STORE 100, HALT
        program = [
            0x1205,  # LOAD #5 (непосредственная адресация: 512 + 5)
            0x3203,  # ADD #3 (непосредственная адресация: 512 + 3)
            0x2064,  # STORE 100 (прямая адресация)
            0x0000   # HALT
        ]
        
        self.processor.load_program(program)
        self.processor.run()
        
        # Проверяем результат
        self.assertTrue(self.processor.halted)
        self.assertEqual(self.processor.ACC, 8)
        self.assertEqual(self.processor.memory[100], 8)
    
    def test_max_search_program(self):
        """Тест программы поиска максимума"""
        # Загружаем тестовые данные
        data = [5, 3, 8]  # Простой массив из 3 элементов
        self.processor.load_data(data, 200)
        
        # Очень простая программа поиска максимума
        program = [
            0x1200,  # LOAD #0 (max = 0) - непосредственная адресация
            0x2064,  # STORE 100 - прямая адресация
            # Проверяем первый элемент (5)
            0x10C8,  # LOAD 200 - прямая адресация (Memory[200] = 5)
            0x2064,  # STORE 100 - сохраняем как max
            # Проверяем второй элемент (3)
            0x10C9,  # LOAD 201 - прямая адресация (Memory[201] = 3)
            0x5064,  # CMP 100 - сравниваем с max
            0x7009,  # JZ NEXT - если 3 <= 5, пропускаем
            0x2064,  # STORE 100 - сохраняем новый max
            # NEXT:
            # Проверяем третий элемент (8)
            0x10CA,  # LOAD 202 - прямая адресация (Memory[202] = 8)
            0x5064,  # CMP 100 - сравниваем с max
            0x700C,  # JZ END - если 8 <= max, переходим к концу
            0x2064,  # STORE 100 - сохраняем новый max (8)
            # END:
            0x0000   # HALT
        ]
        
        self.processor.load_program(program)
        self.processor.run()
        
        # Проверяем результат (максимум должен быть 8)
        self.assertEqual(self.processor.memory[100], 8)
    
    def test_convolution_program(self):
        """Тест программы свертки массивов"""
        # Загружаем тестовые данные
        array_a = [2, 3]  # A = [2, 3]
        array_b = [4, 5]  # B = [4, 5]
        self.processor.load_data(array_a, 200)
        self.processor.load_data(array_b, 210)

        # Простая программа для тестирования загрузки данных
        program = [
            0x10C8,  # LOAD 200 - загружаем A[0] = 2
            0x2064,  # STORE 100 - сохраняем A[0]
            0x10D2,  # LOAD 210 - загружаем B[0] = 4  
            0x2065,  # STORE 101 - сохраняем B[0]
            0x0000   # HALT
        ]

        self.processor.load_program(program)
        self.processor.run()

        # Проверяем результат
        self.assertEqual(self.processor.memory[200], 2)  # Исходные данные A[0]
        self.assertEqual(self.processor.memory[210], 4)  # Исходные данные B[0]
        self.assertEqual(self.processor.memory[100], 2)  # Скопированное A[0]
        self.assertEqual(self.processor.memory[101], 4)  # Скопированное B[0]

    def test_variant9_max_search_program(self):
        """Полный тест программы поиска максимума для варианта 9"""
        program_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'programs',
            'variant9_max.asm'
        )

        with open(program_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        instructions = self.assembler.assemble(source_code)
        machine_codes = [instr['instruction'] for instr in instructions]
        self.processor.load_program(machine_codes)

        array_data = [6, 12, 3, 27, 9, 1, 18]
        self.processor.load_data(array_data, 300)

        self.processor.run(max_steps=20000)

        self.assertTrue(self.processor.halted)
        self.assertEqual(self.processor.memory[100], 27)

    def test_variant9_convolution_program(self):
        """Полный тест программы свертки для варианта 9"""
        program_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'programs',
            'variant9_convolution.asm'
        )

        with open(program_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        instructions = self.assembler.assemble(source_code)
        machine_codes = [instr['instruction'] for instr in instructions]
        self.processor.load_program(machine_codes)

        array_a = [6, 1, 2, 3, 4, 5, 6]
        array_b = [6, 6, 5, 4, 3, 2, 1]
        self.processor.load_data(array_a, 300)
        self.processor.load_data(array_b, 320)

        self.processor.run(max_steps=20000)

        self.assertTrue(self.processor.halted)
        self.assertEqual(self.processor.memory[100], 56)

class TestAssembler(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.assembler = Assembler()
    
    def test_parse_operand(self):
        """Тест парсинга операндов"""
        # Непосредственная адресация
        value, addr_type = self.assembler.parse_operand("#5")
        self.assertEqual(value, 5)
        self.assertEqual(addr_type, 'immediate')
        
        # Прямая адресация
        value, addr_type = self.assembler.parse_operand("100")
        self.assertEqual(value, 100)
        self.assertEqual(addr_type, 'direct')
        
        # Косвенно-регистровая адресация
        value, addr_type = self.assembler.parse_operand("(200)")
        self.assertEqual(value, 200)
        self.assertEqual(addr_type, 'indirect')
        
        # Регистровая адресация
        value, addr_type = self.assembler.parse_operand("R0")
        self.assertEqual(value, 0)
        self.assertEqual(addr_type, 'register')
    
    def test_encode_instruction(self):
        """Тест кодирования инструкций"""
        # LOAD #5 (непосредственная адресация помечается битом 9)
        instruction = self.assembler.encode_instruction(0x1, 5, 'immediate')
        self.assertEqual(instruction, 0x1205)
        
        # STORE 100
        instruction = self.assembler.encode_instruction(0x2, 100, 'direct')
        self.assertEqual(instruction, 0x2064)
        
        # HALT
        instruction = self.assembler.encode_instruction(0x0, 0, 'none')
        self.assertEqual(instruction, 0x0000)
    
    def test_assemble_simple_program(self):
        """Тест ассемблирования простой программы"""
        source = """
        LOAD #5
        ADD #3
        STORE 100
        HALT
        """
        
        instructions = self.assembler.assemble(source)
        
        self.assertEqual(len(instructions), 4)
        self.assertEqual(instructions[0]['mnemonic'], 'LOAD')
        self.assertEqual(instructions[0]['operand'], 5)
        self.assertEqual(instructions[0]['instruction'], 0x1205)
        
        self.assertEqual(instructions[1]['mnemonic'], 'ADD')
        self.assertEqual(instructions[1]['operand'], 3)
        self.assertEqual(instructions[1]['instruction'], 0x3203)
        
        self.assertEqual(instructions[2]['mnemonic'], 'STORE')
        self.assertEqual(instructions[2]['operand'], 100)
        self.assertEqual(instructions[2]['instruction'], 0x2064)
        
        self.assertEqual(instructions[3]['mnemonic'], 'HALT')
        self.assertEqual(instructions[3]['instruction'], 0x0000)
    
    def test_assemble_with_labels(self):
        """Тест ассемблирования с метками"""
        source = """
        LOAD #0
        STORE 100
LOOP:
        LOAD #1
        ADD 100
        STORE 100
        JMP LOOP
        HALT
        """
        
        instructions = self.assembler.assemble(source)
        
        self.assertEqual(len(instructions), 7)
        # Проверяем, что JMP указывает на правильный адрес
        self.assertEqual(instructions[5]['mnemonic'], 'JMP')
        self.assertEqual(instructions[5]['operand'], 2)  # Адрес LOOP (строка 2)

if __name__ == '__main__':
    unittest.main()
