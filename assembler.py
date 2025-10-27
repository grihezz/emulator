"""
Ассемблер для процессора с одноадресной архитектурой
Поддерживает различные типы адресации
"""

import re

class Assembler:
    def __init__(self):
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

        self.labels = {}
        self.variables = {}
        self.address_counter = 0
    
    def reset(self):
        self.labels = {}
        self.variables = {}
        self.address_counter = 0
    
    def parse_operand(self, operand_str):
        operand_str = operand_str.strip()
        if operand_str.startswith('#'):
            value = int(operand_str[1:])
            return value, 'immediate'
        
        # Косвенно-регистровая адресация ((address))
        if operand_str.startswith('(') and operand_str.endswith(')'):
            addr_str = operand_str[1:-1].strip()
            if addr_str.isdigit():
                return int(addr_str), 'indirect'
            elif addr_str in self.labels:
                return self.labels[addr_str], 'indirect'
            else:
                raise ValueError(f"Неизвестная метка: {addr_str}")

        if operand_str == 'R0':
            return 0, 'register'

        if operand_str.isdigit():
            return int(operand_str), 'direct'
        elif operand_str in self.labels:
            return self.labels[operand_str], 'direct'
        elif operand_str in self.variables:
            return self.variables[operand_str], 'direct'
        else:
            try:
                return int(operand_str), 'direct'
            except ValueError:
                raise ValueError(f"Неизвестный операнд: {operand_str}")
    
    def encode_instruction(self, opcode, operand, operand_type):
        """Кодирование команды в машинный код"""
        # Кодируем тип адресации в операнде
        if operand_type == 'immediate':
            # Непосредственная адресация: добавляем 512
            encoded_operand = (operand + 512) & 0xFFF
        elif operand_type == 'indirect':
            # Косвенная адресация: добавляем 256
            encoded_operand = (operand + 256) & 0xFFF
        else:
            # Прямая адресация: операнд как есть
            encoded_operand = operand & 0xFFF
            
        # Формат команды: [15:12] - код операции, [11:0] - операнд
        instruction = (opcode << 12) | encoded_operand
        return instruction
    
    def parse_line(self, line):
        """Парсинг одной строки ассемблера"""
        line = line.strip()
        
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith(';'):
            return None
        
        # Удаляем комментарии
        if ';' in line:
            line = line[:line.index(';')].strip()
        
        # Проверяем на метку
        label = None
        if ':' in line:
            parts = line.split(':', 1)
            label = parts[0].strip()
            line = parts[1].strip()
            
            # Сохраняем метку
            self.labels[label] = self.address_counter
        
        # Пропускаем строки только с метками
        if not line:
            return None
        
        # Разбор команды
        parts = line.split()
        if not parts:
            return None
        
        mnemonic = parts[0].upper()
        operand_str = parts[1] if len(parts) > 1 else None
        
        # Проверяем код операции
        if mnemonic not in self.opcodes:
            raise ValueError(f"Неизвестная команда: {mnemonic}")
        
        opcode = self.opcodes[mnemonic]
        
        # Обработка команд без операндов
        if mnemonic == 'HALT':
            operand = 0
            operand_type = 'none'
        else:
            if operand_str is None:
                raise ValueError(f"Команда {mnemonic} требует операнд")
            
            operand, operand_type = self.parse_operand(operand_str)
        
        # Кодирование команды
        instruction = self.encode_instruction(opcode, operand, operand_type)
        
        # Увеличиваем счетчик адресов
        self.address_counter += 1
        
        return {
            'instruction': instruction,
            'mnemonic': mnemonic,
            'operand': operand,
            'operand_type': operand_type,
            'label': label,
            'address': self.address_counter - 1
        }
    
    def assemble(self, source_code):
        """Ассемблирование исходного кода"""
        self.reset()
        
        lines = source_code.split('\n')
        instructions = []
        errors = []
        
        # Первый проход: сбор меток
        self.address_counter = 0
        for line_num, line in enumerate(lines, 1):
            try:
                # Простой парсинг только для сбора меток
                line = line.strip()
                if not line or line.startswith(';'):
                    continue
                    
                if ';' in line:
                    line = line[:line.index(';')].strip()
                    
                if ':' in line:
                    parts = line.split(':', 1)
                    label = parts[0].strip()
                    self.labels[label] = self.address_counter
                    line = parts[1].strip()
                    
                if line:  # Если есть команда после метки
                    self.address_counter += 1
                    
            except Exception as e:
                # Игнорируем ошибки в первом проходе
                pass
        
        # Сброс счетчика для второго прохода
        self.address_counter = 0
        
        # Второй проход: генерация кода
        for line_num, line in enumerate(lines, 1):
            try:
                result = self.parse_line(line)
                if result:
                    instructions.append(result)
            except Exception as e:
                errors.append(f"Строка {line_num}: {str(e)}")
        
        if errors:
            raise ValueError("Ошибки ассемблирования:\n" + "\n".join(errors))
        
        return instructions
    
    def disassemble(self, instruction):
        """Диссемблирование машинной команды"""
        opcode = (instruction >> 12) & 0xF
        operand = instruction & 0xFFF
        
        # Поиск мнемоники
        mnemonic = None
        for name, code in self.opcodes.items():
            if code == opcode:
                mnemonic = name
                break
        
        if mnemonic is None:
            return f"UNKNOWN {opcode:04X} {operand:03X}"
        
        if mnemonic == 'HALT':
            return mnemonic
        
        # Определение типа операнда
        if operand == 0:
            return f"{mnemonic} R0"
        elif operand < 256:  # Предполагаем, что это прямой адрес
            return f"{mnemonic} {operand}"
        else:
            return f"{mnemonic} #{operand}"
    
    def format_program(self, instructions):
        """Форматирование программы для вывода"""
        result = []
        for instr in instructions:
            addr = instr['address']
            code = instr['instruction']
            mnemonic = instr['mnemonic']
            operand = instr['operand']
            operand_type = instr['operand_type']
            label = instr['label']
            
            # Форматирование операнда
            if operand_type == 'immediate':
                operand_str = f"#{operand}"
            elif operand_type == 'indirect':
                operand_str = f"({operand})"
            elif operand_type == 'register':
                operand_str = "R0"
            elif operand_type == 'direct':
                operand_str = str(operand)
            else:
                operand_str = ""
            
            # Формирование строки
            line = f"{addr:04X}: {code:04X} "
            if label:
                line += f"{label:10s} "
            else:
                line += "          "
            
            if operand_str:
                line += f"{mnemonic:5s} {operand_str}"
            else:
                line += mnemonic
            
            result.append(line)
        
        return result
