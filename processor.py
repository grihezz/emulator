"""
Эмулятор процессора с одноадресной архитектурой Фон-Неймана
Вариант №9: Поиск максимума в массиве и свертка двух массивов
"""

class Processor:
    def __init__(self):
        self.ACC = 0          # Аккумулятор (16 бит)
        self.PC = 0           # Счетчик команд (16 бит)
        self.IR = 0           # Регистр команд (16 бит)
        self.registers = [0] * 16  # Регистры общего назначения R0-R15
        self.flags = {
            'ZF': False,      # Флаг нуля
            'SF': False,      # Флаг знака
            'CF': False,      # Флаг переноса
            'OF': False       # Флаг переполнения
        }

        self.memory = [0] * 4096
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

        self.opcode_names = {v: k for k, v in self.opcodes.items()}
    
    def reset(self):
        self.ACC = 0
        self.PC = 0
        self.IR = 0
        self.registers = [0] * 16
        self.flags = {'ZF': False, 'SF': False, 'CF': False, 'OF': False}
        self.halted = False
        self.step_count = 0
    
    def load_program(self, program, start_address=0):
        for i, instruction in enumerate(program):
            if start_address + i < len(self.memory):
                self.memory[start_address + i] = instruction
        self.PC = start_address
    
    def load_data(self, data, start_address=200):
        for i, value in enumerate(data):
            if start_address + i < len(self.memory):
                self.memory[start_address + i] = value
    
    def get_operand_value(self, operand, addressing_mode='direct'):
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

        # Непосредственная адресация (#value)
        if operand.startswith('#'):
            return int(operand[1:])
        
        # Прямая адресация (address)
        if operand.isdigit():
            return self.memory[int(operand)]

        
        # Регистровая адресация (R0-R7)
        if operand.startswith('R') and len(operand) >= 2:
            # Поддержка R0-R15
            reg_str = operand[1:]
            reg_num = int(reg_str) if reg_str.isdigit() else -1
            if 0 <= reg_num <= 15:
                return self.registers[reg_num] & 0xFFFF
        
        return 0
    
    def set_operand_value(self, operand, value):
        if isinstance(operand, int):
            self.memory[operand] = value & 0xFFFF
            return

        if operand.isdigit():
            self.memory[int(operand)] = value & 0xFFFF
            return

        # Регистровая адресация (R0-R7)
        if operand.startswith('R') and len(operand) >= 2:
            # Поддержка R0-R15
            reg_str = operand[1:]
            reg_num = int(reg_str) if reg_str.isdigit() else -1
            if 0 <= reg_num <= 15:
                self.registers[reg_num] = value & 0xFFFF
    
    def update_flags(self, result):
        self.flags['ZF'] = (result == 0)
        self.flags['SF'] = (result & 0x8000) != 0
        self.flags['CF'] = (result > 0xFFFF) or (result < -0x10000)
        self.flags['OF'] = (result > 0x7FFF) or (result < -0x8000)
    
    def execute_instruction(self, opcode, operand):
        if opcode == self.opcodes['LOAD']:
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            elif operand < 1024:  # 512-1023: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            elif operand >= 1024 and operand < 1040:  # 1024-1039: регистровая адресация (R0-R15)
                reg_num = operand - 1024
                value = self.registers[reg_num] & 0xFFFF
            elif operand >= 1040 and operand < 1056:
                reg_num = operand - 1040
                addr = self.registers[reg_num] & 0xFFFF
                value = self.memory[addr] if addr < len(self.memory) else 0
            elif operand >= 1040 and operand < 1056:
                reg_num = operand - 1040
                addr = self.registers[reg_num] & 0xFFFF
                value = self.memory[addr] if addr < len(self.memory) else 0
            elif operand >= 1040 and operand < 1056:
                reg_num = operand - 1040
                addr = self.registers[reg_num] & 0xFFFF
                value = self.memory[addr] if addr < len(self.memory) else 0
            elif operand >= 1040 and operand < 1056:
                reg_num = operand - 1040
                addr = self.registers[reg_num] & 0xFFFF
                value = self.memory[addr] if addr < len(self.memory) else 0
            else:
                value = 0
            self.ACC = value & 0xFFFF
            self.update_flags(self.ACC)
            
        elif opcode == self.opcodes['STORE']:
            if operand >= 1024 and operand < 1040:
                reg_num = operand - 1024
                self.registers[reg_num] = self.ACC & 0xFFFF
            elif operand >= 1040 and operand < 1056:
                # store via register-indirect (Rk)
                reg_num = operand - 1040
                addr = self.registers[reg_num] & 0xFFFF
                if addr < len(self.memory):
                    self.memory[addr] = self.ACC & 0xFFFF
            elif operand >= 256 and operand < 512:
                # store via memory-indirect ((addr))
                base = operand - 256
                if base < len(self.memory):
                    addr = self.memory[base]
                    if addr < len(self.memory):
                        self.memory[addr] = self.ACC & 0xFFFF
            else:
                self.memory[operand] = self.ACC & 0xFFFF
            
        elif opcode == self.opcodes['ADD']:
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            elif operand < 1024:  # 512-1023: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            elif operand >= 1024 and operand < 1040:  # 1024-1039: регистровая адресация (R0-R15)
                reg_num = operand - 1024
                value = self.registers[reg_num] & 0xFFFF
            else:
                value = 0
            result = self.ACC + value
            self.ACC = result & 0xFFFF
            self.update_flags(self.ACC)
            
        elif opcode == self.opcodes['SUB']:
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            elif operand < 1024:  # 512-1023: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            elif operand >= 1024 and operand < 1040:  # 1024-1039: регистровая адресация (R0-R15)
                reg_num = operand - 1024
                value = self.registers[reg_num] & 0xFFFF
            else:
                value = 0
            result = self.ACC - value
            self.ACC = result & 0xFFFF
            self.update_flags(self.ACC)
            
        elif opcode == self.opcodes['CMP']:
            if operand < 256:  # 0-255: прямая адресация
                value = self.get_operand_value(operand, 'direct')
            elif operand < 512:  # 256-511: косвенная адресация
                addr = operand - 256
                value = self.get_operand_value(addr, 'indirect')
            elif operand < 1024:  # 512-1023: непосредственная адресация
                value = self.get_operand_value(operand - 512, 'immediate')
            elif operand >= 1024 and operand < 1040:  # 1024-1039: регистровая адресация (R0-R15)
                reg_num = operand - 1024
                value = self.registers[reg_num] & 0xFFFF
            else:
                value = 0
            result = self.ACC - value
            self.update_flags(result)
            
        elif opcode == self.opcodes['JMP']:
            self.PC = operand
            
        elif opcode == self.opcodes['JZ']:
            if self.flags['ZF']:
                self.PC = operand
            else:
                self.PC += 1
                
        elif opcode == self.opcodes['JNZ']:
            if not self.flags['ZF']:
                self.PC = operand
            else:
                self.PC += 1
                
        elif opcode == self.opcodes['HALT']:
            self.halted = True
            return
    
    def step(self):
        if self.halted:
            return False

        if self.PC >= len(self.memory):
            self.halted = True
            return False
        
        self.IR = self.memory[self.PC]

        opcode = (self.IR >> 12) & 0xF
        operand = self.IR & 0xFFF

        self.execute_instruction(opcode, operand)
        if opcode not in [self.opcodes['JMP'], self.opcodes['JZ'], self.opcodes['JNZ'], self.opcodes['HALT']]:
            self.PC += 1
        
        self.step_count += 1
        return True
    
    def run(self, max_steps=10000):
        steps = 0
        while not self.halted and steps < max_steps:
            if not self.step():
                break
            steps += 1
        return not self.halted
    
    def get_state(self):
        return {
            'ACC': self.ACC,
            'PC': self.PC,
            'IR': self.IR,
            'registers': self.registers.copy(),
            'flags': self.flags.copy(),
            'halted': self.halted,
            'step_count': self.step_count
        }
    
    def disassemble_instruction(self, instruction):
        opcode = (instruction >> 12) & 0xF
        operand = instruction & 0xFFF
        
        if opcode in self.opcode_names:
            op_name = self.opcode_names[opcode]
            if op_name == 'HALT':
                return f"{op_name}"
            else:
                # Определяем тип адресации и форматируем операнд
                if operand >= 1024 and operand < 1040:
                    reg_num = operand - 1024
                    return f"{op_name} R{reg_num}"
                elif operand >= 1040 and operand < 1056:
                    reg_num = operand - 1040
                    return f"{op_name} (R{reg_num})"
                elif operand >= 512 and operand < 1024:
                    value = operand - 512
                    return f"{op_name} #{value}"
                elif operand >= 256 and operand < 512:
                    addr = operand - 256
                    return f"{op_name} ({addr})"
                else:
                    return f"{op_name} {operand}"
        else:
            return f"UNKNOWN {opcode:04X} {operand:03X}"

