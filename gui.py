"""
Графический интерфейс для эмулятора процессора
Отображает регистры, флаги, память и позволяет управлять выполнением
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from processor import Processor
from assembler import Assembler

class ProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Эмулятор процессора - Вариант №9")
        self.root.geometry("1200x800")
        
        # Инициализация компонентов
        self.processor = Processor()
        self.assembler = Assembler()
        
        # Создание интерфейса
        self.create_widgets()
        self.update_display()
        
        # Автообновление каждые 100мс
        self.auto_update()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель - регистры и управление
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Правая панель - память и код
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # === ЛЕВАЯ ПАНЕЛЬ ===
        
        # Регистры
        reg_frame = ttk.LabelFrame(left_frame, text="Регистры", padding=10)
        reg_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Аккумулятор
        ttk.Label(reg_frame, text="Аккумулятор (ACC):").pack(anchor=tk.W)
        self.acc_var = tk.StringVar()
        acc_entry = ttk.Entry(reg_frame, textvariable=self.acc_var, state="readonly", width=15)
        acc_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Счетчик команд
        ttk.Label(reg_frame, text="Счетчик команд (PC):").pack(anchor=tk.W)
        self.pc_var = tk.StringVar()
        pc_entry = ttk.Entry(reg_frame, textvariable=self.pc_var, state="readonly", width=15)
        pc_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Регистр команд
        ttk.Label(reg_frame, text="Регистр команд (IR):").pack(anchor=tk.W)
        self.ir_var = tk.StringVar()
        ir_entry = ttk.Entry(reg_frame, textvariable=self.ir_var, state="readonly", width=15)
        ir_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Флаги
        flags_frame = ttk.LabelFrame(left_frame, text="Флаги", padding=10)
        flags_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.flag_vars = {}
        flag_names = ['ZF', 'SF', 'CF', 'OF']
        flag_descriptions = ['Ноль', 'Знак', 'Перенос', 'Переполнение']
        
        for i, (name, desc) in enumerate(zip(flag_names, flag_descriptions)):
            var = tk.BooleanVar()
            self.flag_vars[name] = var
            cb = ttk.Checkbutton(flags_frame, text=f"{name} ({desc})", variable=var, state="disabled")
            cb.pack(anchor=tk.W, pady=2)
        
        # Управление
        control_frame = ttk.LabelFrame(left_frame, text="Управление", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопки управления
        ttk.Button(control_frame, text="Сброс", command=self.reset_processor).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Шаг", command=self.step_processor).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Запуск", command=self.run_processor).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Остановка", command=self.stop_processor).pack(fill=tk.X, pady=2)
        
        # Статус
        status_frame = ttk.LabelFrame(left_frame, text="Статус", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.status_var).pack(anchor=tk.W)
        
        self.step_count_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.step_count_var).pack(anchor=tk.W)
        
        # === ПРАВАЯ ПАНЕЛЬ ===
        
        # Вкладки
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка "Память"
        memory_frame = ttk.Frame(notebook)
        notebook.add(memory_frame, text="Память")
        
        # Память команд
        ttk.Label(memory_frame, text="Память команд:").pack(anchor=tk.W)
        self.memory_text = scrolledtext.ScrolledText(memory_frame, height=15, width=60)
        self.memory_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Память данных
        ttk.Label(memory_frame, text="Память данных:").pack(anchor=tk.W)
        self.data_text = scrolledtext.ScrolledText(memory_frame, height=10, width=60)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка "Ассемблер"
        asm_frame = ttk.Frame(notebook)
        notebook.add(asm_frame, text="Ассемблер")
        
        # Редактор кода
        ttk.Label(asm_frame, text="Исходный код:").pack(anchor=tk.W)
        self.code_text = scrolledtext.ScrolledText(asm_frame, height=20, width=80)
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Кнопки ассемблера
        asm_buttons = ttk.Frame(asm_frame)
        asm_buttons.pack(fill=tk.X)
        
        ttk.Button(asm_buttons, text="Ассемблировать", command=self.assemble_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(asm_buttons, text="Загрузить в процессор", command=self.load_assembled_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(asm_buttons, text="Загрузить файл", command=self.load_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(asm_buttons, text="Сохранить файл", command=self.save_file).pack(side=tk.LEFT)
        
        # Результат ассемблирования
        ttk.Label(asm_frame, text="Результат ассемблирования:").pack(anchor=tk.W)
        self.asm_result_text = scrolledtext.ScrolledText(asm_frame, height=10, width=80, state="disabled")
        self.asm_result_text.pack(fill=tk.BOTH, expand=True)
        
        # Загружаем примеры программ
        self.load_example_programs()
    
    def load_example_programs(self):
        """Загрузка примеров программ"""
        # Программа поиска максимума
        max_search_code = """; Поиск максимума в массиве
; Массив: [5, 3, 8, 1, 9, 2, 7]
; Результат: 9

START:
    LOAD #0          ; Загружаем 0 в аккумулятор (текущий максимум)
    STORE 100        ; Сохраняем в переменную max
    LOAD #0          ; Загружаем 0 (индекс)
    STORE 101        ; Сохраняем в переменную i
    LOAD #7          ; Загружаем размер массива
    STORE 102        ; Сохраняем в переменную size

LOOP:
    LOAD 101         ; Загружаем i
    CMP 102          ; Сравниваем с size
    JZ END           ; Если i == size, переходим к END
    
    LOAD 101         ; Загружаем i
    ADD #200         ; Добавляем адрес начала массива
    STORE 103        ; Сохраняем адрес элемента в temp
    
    LOAD (103)       ; Загружаем элемент массива
    CMP 100          ; Сравниваем с текущим максимумом
    JZ NEXT          ; Если меньше, переходим к NEXT
    
    STORE 100        ; Сохраняем новый максимум
    STORE 104        ; Сохраняем индекс максимума

NEXT:
    LOAD 101         ; Загружаем i
    ADD #1           ; Увеличиваем на 1
    STORE 101        ; Сохраняем обратно
    JMP LOOP         ; Переходим к началу цикла

END:
    HALT
"""
        
        # Программа свертки массивов
        convolution_code = """; Свертка двух массивов по 6 элементов
; A = [1, 2, 3, 4, 5, 6]
; B = [2, 3, 4, 5, 6, 7]
; Результат: 1*2 + 2*3 + 3*4 + 4*5 + 5*6 + 6*7 = 112

START:
    LOAD #0          ; Инициализируем сумму
    STORE 100        ; Сохраняем в переменную sum
    LOAD #0          ; Инициализируем индекс
    STORE 101        ; Сохраняем в переменную i
    LOAD #6          ; Размер массивов
    STORE 102        ; Сохраняем в переменную size

LOOP:
    LOAD 101         ; Загружаем i
    CMP 102          ; Сравниваем с size
    JZ END           ; Если i == size, переходим к END
    
    ; Загружаем A[i]
    LOAD 101         ; Загружаем i
    ADD #200         ; Добавляем адрес начала массива A
    STORE 103        ; Сохраняем адрес A[i]
    LOAD (103)       ; Загружаем A[i]
    STORE 104        ; Сохраняем A[i]
    
    ; Загружаем B[i]
    LOAD 101         ; Загружаем i
    ADD #210         ; Добавляем адрес начала массива B
    STORE 105        ; Сохраняем адрес B[i]
    LOAD (105)       ; Загружаем B[i]
    
    ; Умножаем A[i] * B[i] (простое сложение в цикле)
    STORE 106        ; Сохраняем B[i]
    LOAD #0          ; Инициализируем произведение
    STORE 107        ; Сохраняем в переменную product
    
MULT_LOOP:
    LOAD 106         ; Загружаем B[i]
    CMP #0           ; Сравниваем с 0
    JZ MULT_END      ; Если 0, заканчиваем умножение
    
    LOAD 107         ; Загружаем product
    ADD 104          ; Добавляем A[i]
    STORE 107        ; Сохраняем product
    
    LOAD 106         ; Загружаем B[i]
    SUB #1           ; Уменьшаем на 1
    STORE 106        ; Сохраняем обратно
    JMP MULT_LOOP    ; Переходим к началу цикла умножения

MULT_END:
    LOAD 107         ; Загружаем произведение
    ADD 100          ; Добавляем к сумме
    STORE 100        ; Сохраняем новую сумму
    
    LOAD 101         ; Загружаем i
    ADD #1           ; Увеличиваем на 1
    STORE 101        ; Сохраняем обратно
    JMP LOOP         ; Переходим к началу цикла

END:
    HALT
"""
        
        # Загружаем первую программу по умолчанию
        self.code_text.insert(tk.END, max_search_code)
    
    def update_display(self):
        """Обновление отображения"""
        # Обновляем регистры
        self.acc_var.set(f"{self.processor.ACC} (0x{self.processor.ACC:04X})")
        self.pc_var.set(f"{self.processor.PC} (0x{self.processor.PC:04X})")
        self.ir_var.set(f"{self.processor.IR} (0x{self.processor.IR:04X})")
        
        # Обновляем флаги
        for flag, var in self.flag_vars.items():
            var.set(self.processor.flags[flag])
        
        # Обновляем статус
        if self.processor.halted:
            self.status_var.set("Остановлен")
        else:
            self.status_var.set("Выполняется")
        
        self.step_count_var.set(f"Шагов выполнено: {self.processor.step_count}")
        
        # Обновляем память команд
        self.update_memory_display()
        
        # Обновляем память данных
        self.update_data_display()
    
    def update_memory_display(self):
        """Обновление отображения памяти команд"""
        self.memory_text.delete(1.0, tk.END)
        
        # Показываем только ненулевые ячейки памяти
        for i in range(0, min(256, len(self.processor.memory))):
            if self.processor.memory[i] != 0:
                disasm = self.processor.disassemble_instruction(self.processor.memory[i])
                line = f"{i:04X}: {self.processor.memory[i]:04X} - {disasm}\n"
                self.memory_text.insert(tk.END, line)
    
    def update_data_display(self):
        """Обновление отображения памяти данных"""
        self.data_text.delete(1.0, tk.END)
        
        # Показываем данные начиная с адреса 200
        for i in range(200, min(300, len(self.processor.memory))):
            if self.processor.memory[i] != 0:
                line = f"{i:04X}: {self.processor.memory[i]:04X} ({self.processor.memory[i]})\n"
                self.data_text.insert(tk.END, line)
    
    def reset_processor(self):
        """Сброс процессора"""
        self.processor.reset()
        self.update_display()
    
    def step_processor(self):
        """Выполнение одного шага"""
        if not self.processor.halted:
            self.processor.step()
            self.update_display()
    
    def run_processor(self):
        """Запуск выполнения программы"""
        if not self.processor.halted:
            self.processor.run()
            self.update_display()
    
    def stop_processor(self):
        """Остановка выполнения"""
        self.processor.halted = True
        self.update_display()
    
    def assemble_code(self):
        """Ассемблирование кода"""
        try:
            source_code = self.code_text.get(1.0, tk.END)
            instructions = self.assembler.assemble(source_code)
            
            # Отображаем результат
            self.asm_result_text.config(state="normal")
            self.asm_result_text.delete(1.0, tk.END)
            
            formatted = self.assembler.format_program(instructions)
            for line in formatted:
                self.asm_result_text.insert(tk.END, line + "\n")
            
            self.asm_result_text.config(state="disabled")
            
            # Сохраняем инструкции для загрузки
            self.assembled_instructions = instructions
            
            messagebox.showinfo("Успех", "Код успешно ассемблирован!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка ассемблирования:\n{str(e)}")
    
    def load_assembled_code(self):
        """Загрузка ассемблированного кода в процессор"""
        try:
            if hasattr(self, 'assembled_instructions'):
                # Извлекаем машинные коды
                machine_codes = [instr['instruction'] for instr in self.assembled_instructions]
                
                # Загружаем в процессор
                self.processor.load_program(machine_codes)
                
                # Загружаем тестовые данные
                self.load_test_data()
                
                self.update_display()
                messagebox.showinfo("Успех", "Программа загружена в процессор!")
            else:
                messagebox.showwarning("Предупреждение", "Сначала ассемблируйте код!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки:\n{str(e)}")
    
    def load_test_data(self):
        """Загрузка тестовых данных"""
        # Данные для поиска максимума: [5, 3, 8, 1, 9, 2, 7]
        max_data = [7, 5, 3, 8, 1, 9, 2, 7]  # Первый элемент - размер
        self.processor.load_data(max_data, 200)
        
        # Данные для свертки: A = [1, 2, 3, 4, 5, 6], B = [2, 3, 4, 5, 6, 7]
        array_a = [6, 1, 2, 3, 4, 5, 6]  # Первый элемент - размер
        array_b = [6, 2, 3, 4, 5, 6, 7]  # Первый элемент - размер
        self.processor.load_data(array_a, 200)
        self.processor.load_data(array_b, 210)
    
    def load_file(self):
        """Загрузка файла с кодом"""
        filename = filedialog.askopenfilename(
            title="Загрузить файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(1.0, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки файла:\n{str(e)}")
    
    def save_file(self):
        """Сохранение файла с кодом"""
        filename = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if filename:
            try:
                content = self.code_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Успех", "Файл сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения файла:\n{str(e)}")
    
    def auto_update(self):
        """Автоматическое обновление интерфейса"""
        self.update_display()
        self.root.after(100, self.auto_update)

def main():
    root = tk.Tk()
    app = ProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


