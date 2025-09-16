#!/usr/bin/env python3
"""Автоматические проверки программ для графических интерфейсов."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pytest

from processor import Processor
from assembler import Assembler


PROJECT_ROOT = Path(__file__).resolve().parent


ProgramSpec = Dict[str, object]


PROGRAM_SPECS: List[ProgramSpec] = [
    {
        "name": "variant9_max",
        "path": PROJECT_ROOT / "programs" / "variant9_max.asm",
        "data": [(300, [6, 12, 3, 27, 9, 1, 18])],
        "expected": {100: 27},
        "max_steps": 20000,
    },
    {
        "name": "variant9_convolution",
        "path": PROJECT_ROOT / "programs" / "variant9_convolution.asm",
        "data": [
            (300, [6, 1, 2, 3, 4, 5, 6]),
            (320, [6, 6, 5, 4, 3, 2, 1]),
        ],
        "expected": {100: 56},
        "max_steps": 20000,
    },
]


def _run_program(path: Path, data_blocks: Iterable[Tuple[int, List[int]]], max_steps: int) -> Processor:
    processor = Processor()
    assembler = Assembler()

    source_code = path.read_text(encoding="utf-8")
    instructions = assembler.assemble(source_code)
    machine_codes = [instr["instruction"] for instr in instructions]
    processor.load_program(machine_codes)

    for start_address, values in data_blocks:
        processor.load_data(values, start_address)

    processor.run(max_steps=max_steps)
    return processor


@pytest.mark.parametrize("spec", PROGRAM_SPECS, ids=lambda spec: spec["name"])
def test_program_file(spec: ProgramSpec) -> None:
    processor = _run_program(
        path=spec["path"],
        data_blocks=spec.get("data", []),
        max_steps=spec.get("max_steps", 1000),
    )

    assert processor.halted

    for address, expected_value in spec.get("expected", {}).items():
        assert processor.memory[address] == expected_value


def main() -> None:
    """Простой запускатель тестов для ручной проверки."""

    for spec in PROGRAM_SPECS:
        processor = _run_program(
            path=spec["path"],
            data_blocks=spec.get("data", []),
            max_steps=spec.get("max_steps", 1000),
        )

        status = "успех" if processor.halted else "ошибка"
        print(f"{spec['name']}: {status}")
        for address, expected_value in spec.get("expected", {}).items():
            actual = processor.memory[address]
            print(f"  Memory[{address}] = {actual} (ожидалось {expected_value})")


if __name__ == "__main__":
    main()
