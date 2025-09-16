"""
Эмулятор процессора с одноадресной архитектурой Фон-Неймана
Вариант №9: Поиск максимума в массиве и свертка двух массивов
"""

class Processor:
    def __init__(self):
        # Регистры процессора
        self.ACC = 0          # Аккумулятор (16 бит)
        self.PC = 0           # Счетчик команд (16 бит)
        self.IR = 0           # Регистр команд (16 бит)
        self.flags = {
            'ZF': False,      # Флаг нуля
            'SF': False,      # Флаг знака
            'CF': False,      # Флаг переноса
            'OF': False       # Флаг переполнения
        }
        
        # Память (4096 ячеек по 16 бит)
        self.memory = [0] * 4096
        
        # Состояние процессора
        self.halted = False
        self.step_count = 0
        
        # Коды операций
        self.opcodes = {
            'LOAD': 0x1,      # 0001
            'STORE': 0x2,     # 0010
            'ADD': 0x3,       # 0011
            'SUB': 0x4,       # 0100
            'CMP': 0x5,       # 0101
            'JMP': 0x6,       # 0110
            'JZ': 0x7,        # 0111
            'JNZ': 0x8,       # 1000
            'HALT': 0x0       # 0000
        }
        
        # Обратное соответствие кодов операций
        self.opcode_names = {v: k for k, v in self.opcodes.items()}
    
    def reset(self):
        """Сброс процессора в начальное состояние"""
        self.ACC = 0
        self.PC = 0
        self.IR = 0
        self.flags = {'ZF': False, 'SF': False, 'CF': False, 'OF': False}
        self.halted = False
        self.step_count = 0
        # НЕ очищаем память - программа должна остаться!
    
    def load_program(self, program, start_address=0):
        """Загрузка программы в память"""
        for i, instruction in enumerate(program):
            if start_address + i < len(self.memory):
                self.memory[start_address + i] = instruction
        self.PC = start_address
    
    def load_data(self, data, start_address=200):
        """Загрузка данных в память"""
        for i, value in enumerate(data):
            if start_address + i < len(self.memory):
                self.memory[start_address + i] = value
    
    def get_operand_value(self, operand, addressing_mode='direct'):
        """Получение значения операнда в зависимости от типа адресации"""
        if isinstance(operand, int):
            if addressing_mode == 'immediate':
                return operand
            elif addressing_mode == 'direct':
                return self.memory[operand] if operand < len(self.memory) else 0
            elif addressing_mode == 'indirect':
                addr = self.memory[operand] if operand < len(self.memory) else 0
                return self.memory[addr] if addr < len(self.memory) else 0
            else:
                return operand
        
        # Для ассемблера (строки)
        # Непосредственная адресация (#value)
        if operand.startswith('#'):
            return int(operand[1:])
        
        # Прямая адресация (address)
        if operand.isdigit():
            return self.memory[int(operand)]
        
        # Косвенно-регистровая адресация ((address))
        if operand.startswith('(') and operand.endswith(')'):
            addr = int(operand[1:-1])
            return self.memory[self.memory[addr]]
        
        # Регистровая адресация (R0 - аккумулятор)
        if operand == 'R0':
            return self.ACC
        
        return 0
    
    def set_operand_value(self, operand, value):
        """Установка значения операнда в зависимости от типа адресации"""
        if isinstance(operand, int):
            self.memory[operand] = value & 0xFFFF
            return
        
        # Прямая адресация (address)
        if operand.isdigit():
            self.memory[int(operand)] = value & 0xFFFF
            return
        
        # Косвенно-регистровая адресация ((address))
        if operand.startswith('(') and operand.endswith(')'):
            addr = int(operand[1:-1])
            self.memory[self.memory[addr]] = value & 0xFFFF
            return
        
        # Регистровая адресация (R0 - аккумулятор)
        if operand == 'R0':
            self.ACC = value & 0xFFFF
    
    def update_flags(self, result):
        """Обновление флагов после операции"""
        # Флаг нуля
        self.flags['ZF'] = (result == 0)
        
        # Флаг знака (старший бит)
        self.flags['SF'] = (result & 0x8000) != 0
        
        # Флаг переноса (выход за 16 бит)
        self.flags['CF'] = (result > 0xFFFF) or (result < -0x10000)
        
        # Флаг переполнения (знаковое переполнение)
        self.flags['OF'] = (result > 0x7FFF) or (result < -0x8000)
    
    def execute_instruction(self, opcode, operand):
        """Выполнение одной команды"""
        if opcode == self.opcodes['LOAD']:
            # Определяем тип адресации по диапазону операнда
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            else:  # 512+: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            self.ACC = value & 0xFFFF
            self.update_flags(self.ACC)
            
        elif opcode == self.opcodes['STORE']:
            self.memory[operand] = self.ACC & 0xFFFF
            
        elif opcode == self.opcodes['ADD']:
            # Определяем тип адресации по диапазону операнда
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            else:  # 512+: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            result = self.ACC + value
            self.ACC = result & 0xFFFF
            self.update_flags(self.ACC)
            
        elif opcode == self.opcodes['SUB']:
            # Определяем тип адресации по диапазону операнда
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            else:  # 512+: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            result = self.ACC - value
            self.ACC = result & 0xFFFF
            self.update_flags(self.ACC)
            
        elif opcode == self.opcodes['CMP']:
            # Определяем тип адресации по диапазону операнда
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            else:  # 512+: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            result = self.ACC - value
            self.update_flags(result)
            
        elif opcode == self.opcodes['JMP']:
            self.PC = operand
            
        elif opcode == self.opcodes['JZ']:
            if self.flags['ZF']:
                self.PC = operand
            else:
                self.PC += 1  # Увеличиваем PC, если переход НЕ выполняется
                
        elif opcode == self.opcodes['JNZ']:
            if not self.flags['ZF']:
                self.PC = operand
            else:
                self.PC += 1  # Увеличиваем PC, если переход НЕ выполняется
                
        elif opcode == self.opcodes['HALT']:
            self.halted = True
            return  # Не увеличиваем PC
    
    def step(self):
        """Выполнение одного шага программы"""
        if self.halted:
            return False
        
        # Загрузка команды
        if self.PC >= len(self.memory):
            self.halted = True
            return False
        
        self.IR = self.memory[self.PC]
        
        # Декодирование команды
        opcode = (self.IR >> 12) & 0xF
        operand = self.IR & 0xFFF
        
        # Выполнение команды
        self.execute_instruction(opcode, operand)
        
        # Переход к следующей команде (если не было перехода)
        # Команды переходов сами управляют PC через return
        if opcode not in [self.opcodes['JMP'], self.opcodes['JZ'], self.opcodes['JNZ'], self.opcodes['HALT']]:
            self.PC += 1
        
        self.step_count += 1
        return True
    
    def run(self, max_steps=10000):
        """Выполнение программы до завершения или максимального количества шагов"""
        steps = 0
        while not self.halted and steps < max_steps:
            if not self.step():
                break
            steps += 1
        return not self.halted
    
    def get_state(self):
        """Получение текущего состояния процессора"""
        return {
            'ACC': self.ACC,
            'PC': self.PC,
            'IR': self.IR,
            'flags': self.flags.copy(),
            'halted': self.halted,
            'step_count': self.step_count
        }
    
    def disassemble_instruction(self, instruction):
        """Диссемблирование команды"""
        opcode = (instruction >> 12) & 0xF
        operand = instruction & 0xFFF
        
        if opcode in self.opcode_names:
            op_name = self.opcode_names[opcode]
            if op_name == 'HALT':
                return f"{op_name}"
            else:
                return f"{op_name} {operand}"
        else:
            return f"UNKNOWN {opcode:04X} {operand:03X}"
    
    def get_memory_dump(self, start=0, count=100):
        """Получение дампа памяти"""
        result = []
        for i in range(start, min(start + count, len(self.memory))):
            if self.memory[i] != 0:  # Показываем только ненулевые ячейки
                disasm = self.disassemble_instruction(self.memory[i])
                result.append(f"{i:04X}: {self.memory[i]:04X} ({disasm})")
        return result
