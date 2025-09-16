#!/usr/bin/env python3
"""
Тест программы свертки
"""

from pathlib import Path

from processor import Processor
from assembler import Assembler


def test_convolution():
    """Проверка программы свертки из набора Variant 9"""

    project_root = Path(__file__).resolve().parent
    program_path = project_root / 'programs' / 'variant9_convolution.asm'

    processor = Processor()
    assembler = Assembler()

    with open(program_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    instructions = assembler.assemble(source_code)
    machine_codes = [instr['instruction'] for instr in instructions]
    processor.load_program(machine_codes)

    array_a = [6, 1, 2, 3, 4, 5, 6]
    array_b = [6, 6, 5, 4, 3, 2, 1]
    processor.load_data(array_a, 300)
    processor.load_data(array_b, 320)

    processor.run(max_steps=20000)

    assert processor.halted
    assert processor.memory[100] == 56


if __name__ == "__main__":
    test_convolution()
