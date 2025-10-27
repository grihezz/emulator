"""
Расширенный графический интерфейс с улучшенной визуализацией
Включает диаграммы, графики производительности и детальную визуализацию
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from processor import Processor
from assembler import Assembler

class PerformanceMonitor:
    def __init__(self):
        self.instruction_counts = {}
        self.memory_access_history = []
        self.execution_time_history = []
        self.register_value_history = {'ACC': [], 'PC': [], 'IR': []}
        
    def record_instruction(self, opcode):
        """Записывает выполненную инструкцию"""
        opcodes = {0x0: 'HALT', 0x1: 'LOAD', 0x2: 'STORE', 0x3: 'ADD', 0x4: 'SUB', 0x5: 'CMP', 0x6: 'JMP', 0x7: 'JZ', 0x8: 'JNZ'}
        mnemonic = opcodes.get(opcode, f'UNK({opcode})')
        
        if mnemonic in self.instruction_counts:
            self.instruction_counts[mnemonic] += 1
        else:
            self.instruction_counts[mnemonic] = 1
            
    def record_memory_access(self, address, access_type):
        """Записывает обращение к памяти"""
        self.memory_access_history.append({'address': address, 'type': access_type, 'time': len(self.memory_access_history)})
        
    def record_register_values(self, acc, pc, ir):
        """Записывает значения регистров"""
        self.register_value_history['ACC'].append(acc)
        self.register_value_history['PC'].append(pc)
        self.register_value_history['IR'].append(ir)
        
    def reset(self):
        """Сброс статистики"""
        self.instruction_counts.clear()
        self.memory_access_history.clear()
        self.execution_time_history.clear()
        for key in self.register_value_history:
            self.register_value_history[key].clear()

class EnhancedProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Расширенный эмулятор процессора - Вариант №9")
        self.root.geometry("1600x1000")
        
        # Инициализация компонентов
        self.processor = Processor()
        self.assembler = Assembler()
        self.performance_monitor = PerformanceMonitor()
        self.running = False
        
        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        
        # Создание интерфейса
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главное меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть программу", command=self.open_program)
        file_menu.add_command(label="Сохранить программу", command=self.save_program)
        file_menu.add_separator()
        file_menu.add_command(label="Экспорт статистики", command=self.export_stats)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню "Вид"
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Сброс графиков", command=self.reset_charts)
        view_menu.add_command(label="Полноэкранный режим", command=self.toggle_fullscreen)
        
        # Главный контейнер с разделителями
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Левая панель - код и управление
        left_panel = ttk.Frame(main_paned)
        main_paned.add(left_panel, weight=1)
        
        # Центральная панель - состояние процессора
        center_panel = ttk.Frame(main_paned)
        main_paned.add(center_panel, weight=1)
        
        # Правая панель - графики и анализ
        right_panel = ttk.Frame(main_paned)
        main_paned.add(right_panel, weight=1)
        
        # Создаем содержимое панелей
        self.create_left_panel(left_panel)
        self.create_center_panel(center_panel)
        self.create_right_panel(right_panel)
        
    def create_left_panel(self, parent):
        """Создание левой панели - код и управление"""
        # Заголовок
        title = ttk.Label(parent, text="Редактор и управление", font=('Arial', 12, 'bold'))
        title.pack(pady=(0, 10))
        
        # Редактор кода
        code_frame = ttk.LabelFrame(parent, text="Исходный код", padding=10)
        code_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.code_text = scrolledtext.ScrolledText(code_frame, height=20, width=50, font=('Courier', 10))
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Кнопки управления кодом
        code_buttons = ttk.Frame(code_frame)
        code_buttons.pack(fill=tk.X)
        
        ttk.Button(code_buttons, text="Ассемблировать", command=self.assemble_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(code_buttons, text="Загрузить", command=self.load_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(code_buttons, text="Примеры", command=self.show_examples).pack(side=tk.LEFT)
        
        # Панель управления выполнением
        exec_frame = ttk.LabelFrame(parent, text="Управление выполнением", padding=10)
        exec_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Основные кнопки
        main_buttons = ttk.Frame(exec_frame)
        main_buttons.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(main_buttons, text="🔄 Сброс", command=self.reset_processor).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(main_buttons, text="▶️ Шаг", command=self.step_execution).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(main_buttons, text="⏯️ Запуск", command=self.toggle_execution).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(main_buttons, text="⏹️ Стоп", command=self.stop_execution).pack(side=tk.LEFT)
        
        # Настройки выполнения
        settings_frame = ttk.Frame(exec_frame)
        settings_frame.pack(fill=tk.X)
        
        ttk.Label(settings_frame, text="Скорость:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(settings_frame, from_=0.1, to=5.0, variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.speed_label = ttk.Label(settings_frame, text="1.0x")
        self.speed_label.pack(side=tk.RIGHT)
        
        # Привязываем обновление метки скорости
        speed_scale.configure(command=self.update_speed_label)
        
        # Машинный код
        machine_frame = ttk.LabelFrame(parent, text="Машинный код", padding=10)
        machine_frame.pack(fill=tk.BOTH, expand=True)
        
        self.machine_text = scrolledtext.ScrolledText(machine_frame, height=10, width=50, font=('Courier', 9), state="disabled")
        self.machine_text.pack(fill=tk.BOTH, expand=True)
        
        # Загружаем пример по умолчанию
        self.load_default_example()
        
    def create_center_panel(self, parent):
        """Создание центральной панели - состояние процессора"""
        # Заголовок
        title = ttk.Label(parent, text="Состояние процессора", font=('Arial', 12, 'bold'))
        title.pack(pady=(0, 10))
        
        # Notebook для вкладок
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка "Регистры"
        reg_frame = ttk.Frame(notebook)
        notebook.add(reg_frame, text="Регистры")
        self.create_registers_tab(reg_frame)
        
        # Вкладка "Память"
        mem_frame = ttk.Frame(notebook)
        notebook.add(mem_frame, text="Память")
        self.create_memory_tab(mem_frame)
        
        # Вкладка "Стек вызовов"
        stack_frame = ttk.Frame(notebook)
        notebook.add(stack_frame, text="Трассировка")
        self.create_trace_tab(stack_frame)
        
    def create_registers_tab(self, parent):
        """Создание вкладки регистров"""
        # Основные регистры
        main_reg_frame = ttk.LabelFrame(parent, text="Основные регистры", padding=10)
        main_reg_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Создаем переменные для регистров
        self.acc_var = tk.StringVar()
        self.pc_var = tk.StringVar()
        self.ir_var = tk.StringVar()
        
        # Сетка для регистров
        reg_grid = ttk.Frame(main_reg_frame)
        reg_grid.pack(fill=tk.X)
        
        # Заголовки
        ttk.Label(reg_grid, text="Регистр", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(reg_grid, text="Значение (Dec)", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        ttk.Label(reg_grid, text="Значение (Hex)", font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        ttk.Label(reg_grid, text="Значение (Bin)", font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Аккумулятор
        ttk.Label(reg_grid, text="ACC", font=('Courier', 10, 'bold')).grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.acc_dec_label = ttk.Label(reg_grid, text="0", font=('Courier', 10))
        self.acc_dec_label.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.acc_hex_label = ttk.Label(reg_grid, text="0x0000", font=('Courier', 10))
        self.acc_hex_label.grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.acc_bin_label = ttk.Label(reg_grid, text="0000000000000000", font=('Courier', 10))
        self.acc_bin_label.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Счетчик команд
        ttk.Label(reg_grid, text="PC", font=('Courier', 10, 'bold')).grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.pc_dec_label = ttk.Label(reg_grid, text="0", font=('Courier', 10))
        self.pc_dec_label.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        self.pc_hex_label = ttk.Label(reg_grid, text="0x0000", font=('Courier', 10))
        self.pc_hex_label.grid(row=2, column=2, padx=5, pady=2, sticky=tk.W)
        self.pc_bin_label = ttk.Label(reg_grid, text="0000000000000000", font=('Courier', 10))
        self.pc_bin_label.grid(row=2, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Регистр команд
        ttk.Label(reg_grid, text="IR", font=('Courier', 10, 'bold')).grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        self.ir_dec_label = ttk.Label(reg_grid, text="0", font=('Courier', 10))
        self.ir_dec_label.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        self.ir_hex_label = ttk.Label(reg_grid, text="0x0000", font=('Courier', 10))
        self.ir_hex_label.grid(row=3, column=2, padx=5, pady=2, sticky=tk.W)
        self.ir_bin_label = ttk.Label(reg_grid, text="0000000000000000", font=('Courier', 10))
        self.ir_bin_label.grid(row=3, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Декодирование текущей команды
        decode_frame = ttk.LabelFrame(parent, text="Декодирование команды", padding=10)
        decode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.decode_text = scrolledtext.ScrolledText(decode_frame, height=4, width=50, font=('Courier', 10), state="disabled")
        self.decode_text.pack(fill=tk.BOTH, expand=True)
        
        # Флаги
        flags_frame = ttk.LabelFrame(parent, text="Флаги состояния", padding=10)
        flags_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.flag_vars = {}
        flag_info = [
            ('ZF', 'Ноль', 'Результат операции равен нулю'),
            ('SF', 'Знак', 'Результат операции отрицательный'),
            ('CF', 'Перенос', 'Произошел перенос из старшего разряда'),
            ('OF', 'Переполнение', 'Произошло переполнение')
        ]
        
        for i, (flag, name, desc) in enumerate(flag_info):
            frame = ttk.Frame(flags_frame)
            frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar()
            self.flag_vars[flag] = var
            
            cb = ttk.Checkbutton(frame, text=f"{flag} ({name})", variable=var, state="disabled")
            cb.pack(side=tk.LEFT)
            
            ttk.Label(frame, text=desc, font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))
        
        # Статистика выполнения
        stats_frame = ttk.LabelFrame(parent, text="Статистика", padding=10)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar()
        self.step_count_var = tk.StringVar()
        self.cycle_count_var = tk.StringVar()
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        ttk.Label(stats_grid, text="Статус:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(stats_grid, textvariable=self.status_var, font=('Courier', 10)).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(stats_grid, text="Шагов выполнено:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(stats_grid, textvariable=self.step_count_var, font=('Courier', 10)).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
    def create_memory_tab(self, parent):
        """Создание вкладки памяти"""
        # Разделяем на две части
        mem_paned = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        mem_paned.pack(fill=tk.BOTH, expand=True)
        
        # Память команд
        cmd_mem_frame = ttk.LabelFrame(mem_paned, text="Память команд", padding=10)
        mem_paned.add(cmd_mem_frame, weight=1)
        
        self.memory_text = scrolledtext.ScrolledText(cmd_mem_frame, height=15, font=('Courier', 9))
        self.memory_text.pack(fill=tk.BOTH, expand=True)
        
        # Память данных
        data_mem_frame = ttk.LabelFrame(mem_paned, text="Память данных", padding=10)
        mem_paned.add(data_mem_frame, weight=1)
        
        self.data_text = scrolledtext.ScrolledText(data_mem_frame, height=15, font=('Courier', 9))
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
    def create_trace_tab(self, parent):
        """Создание вкладки трассировки"""
        trace_frame = ttk.LabelFrame(parent, text="Трассировка выполнения", padding=10)
        trace_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.trace_text = scrolledtext.ScrolledText(trace_frame, height=20, font=('Courier', 9))
        self.trace_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        trace_buttons = ttk.Frame(trace_frame)
        trace_buttons.pack(fill=tk.X)
        
        ttk.Button(trace_buttons, text="Очистить", command=self.clear_trace).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(trace_buttons, text="Сохранить", command=self.save_trace).pack(side=tk.LEFT)
        
    def create_right_panel(self, parent):
        """Создание правой панели - графики и анализ"""
        # Заголовок
        title = ttk.Label(parent, text="Анализ производительности", font=('Arial', 12, 'bold'))
        title.pack(pady=(0, 10))
        
        # Notebook для графиков
        charts_notebook = ttk.Notebook(parent)
        charts_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка "Статистика команд"
        instr_frame = ttk.Frame(charts_notebook)
        charts_notebook.add(instr_frame, text="Команды")
        self.create_instruction_chart(instr_frame)
        
        # Вкладка "Регистры"
        reg_chart_frame = ttk.Frame(charts_notebook)
        charts_notebook.add(reg_chart_frame, text="Регистры")
        self.create_register_chart(reg_chart_frame)
        
        # Вкладка "Память"
        mem_chart_frame = ttk.Frame(charts_notebook)
        charts_notebook.add(mem_chart_frame, text="Память")
        self.create_memory_chart(mem_chart_frame)
        
    def create_instruction_chart(self, parent):
        """Создание графика статистики команд"""
        self.instr_fig, self.instr_ax = plt.subplots(figsize=(6, 4))
        self.instr_canvas = FigureCanvasTkAgg(self.instr_fig, parent)
        self.instr_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.instr_ax.set_title('Статистика выполненных команд')
        self.instr_ax.set_xlabel('Команды')
        self.instr_ax.set_ylabel('Количество')
        
    def create_register_chart(self, parent):
        """Создание графика изменения регистров"""
        self.reg_fig, self.reg_ax = plt.subplots(figsize=(6, 4))
        self.reg_canvas = FigureCanvasTkAgg(self.reg_fig, parent)
        self.reg_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.reg_ax.set_title('История изменения регистров')
        self.reg_ax.set_xlabel('Шаги выполнения')
        self.reg_ax.set_ylabel('Значение')
        
    def create_memory_chart(self, parent):
        """Создание графика обращений к памяти"""
        self.mem_fig, self.mem_ax = plt.subplots(figsize=(6, 4))
        self.mem_canvas = FigureCanvasTkAgg(self.mem_fig, parent)
        self.mem_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.mem_ax.set_title('Карта обращений к памяти')
        self.mem_ax.set_xlabel('Адрес памяти')
        self.mem_ax.set_ylabel('Время обращения')
        
    def load_default_example(self):
        """Загрузка примера по умолчанию"""
        example = """; Демонстрационная программа
; Вычисление факториала числа 5

START:
    LOAD #5          ; Загружаем число 5
    STORE 100        ; Сохраняем в переменную n
    LOAD #1          ; Загружаем 1 (результат)
    STORE 101        ; Сохраняем в переменную result

LOOP:
    LOAD 100         ; Загружаем n
    CMP #0           ; Сравниваем с 0
    JZ END           ; Если n = 0, завершаем
    
    LOAD 101         ; Загружаем result
    STORE 102        ; Временно сохраняем
    LOAD 100         ; Загружаем n
    STORE 103        ; Сохраняем множитель
    
    ; Умножение result * n (через сложение)
    LOAD #0          ; Обнуляем result
    STORE 101
    
MULT:
    LOAD 103         ; Загружаем счетчик
    CMP #0           ; Сравниваем с 0
    JZ NEXT          ; Если 0, переходим к следующему
    
    LOAD 101         ; Загружаем result
    ADD 102          ; Добавляем временное значение
    STORE 101        ; Сохраняем result
    
    LOAD 103         ; Загружаем счетчик
    SUB #1           ; Уменьшаем на 1
    STORE 103        ; Сохраняем счетчик
    JMP MULT         ; Повторяем умножение
    
NEXT:
    LOAD 100         ; Загружаем n
    SUB #1           ; Уменьшаем на 1
    STORE 100        ; Сохраняем n
    JMP LOOP         ; Переходим к началу цикла

END:
    HALT             ; Результат в переменной 101
"""
        self.code_text.insert(tk.END, example)
        
    def update_speed_label(self, value):
        """Обновление метки скорости"""
        self.speed_label.config(text=f"{float(value):.1f}x")
        
    def assemble_code(self):
        """Ассемблирование кода"""
        try:
            source = self.code_text.get(1.0, tk.END)
            instructions = self.assembler.assemble(source)
            
            # Показываем машинный код
            self.machine_text.config(state="normal")
            self.machine_text.delete(1.0, tk.END)
            
            for instr in instructions:
                line = f"{instr['address']:04X}: {instr['instruction']:04X} - {instr['mnemonic']} {instr.get('operand', '')}\n"
                self.machine_text.insert(tk.END, line)
                
            self.machine_text.config(state="disabled")
            
            self.assembled_instructions = instructions
            messagebox.showinfo("Успех", f"Код ассемблирован успешно!\nИнструкций: {len(instructions)}")
            
        except Exception as e:
            messagebox.showerror("Ошибка ассемблирования", str(e))
            
    def load_code(self):
        """Загрузка кода в процессор"""
        try:
            if hasattr(self, 'assembled_instructions'):
                machine_codes = [instr['instruction'] for instr in self.assembled_instructions]
                self.processor.load_program(machine_codes)
                
                # Загружаем тестовые данные
                test_data = [5, 4, 3, 2, 1]
                self.processor.load_data(test_data, 200)
                
                self.update_display()
                messagebox.showinfo("Успех", "Программа загружена в процессор!")
            else:
                messagebox.showwarning("Предупреждение", "Сначала ассемблируйте код!")
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))
            
    def step_execution(self):
        """Выполнение одного шага"""
        if not self.processor.halted:
            # Записываем состояние до выполнения
            old_ir = self.processor.IR
            old_pc = self.processor.PC
            
            # Выполняем шаг
            success = self.processor.step()
            
            if success:
                # Записываем статистику
                opcode = (self.processor.IR >> 12) & 0xF
                self.performance_monitor.record_instruction(opcode)
                self.performance_monitor.record_register_values(
                    self.processor.ACC, self.processor.PC, self.processor.IR
                )
                
                # Логируем выполнение
                self.log_execution_step(old_pc, old_ir)
                
            self.update_display()
            self.update_charts()
            
    def toggle_execution(self):
        """Переключение режима выполнения"""
        if self.running:
            self.running = False
        else:
            self.running = True
            self.run_continuous()
            
    def run_continuous(self):
        """Непрерывное выполнение"""
        if self.running and not self.processor.halted:
            self.step_execution()
            delay = int(1000 / self.speed_var.get())
            self.root.after(delay, self.run_continuous)
        else:
            self.running = False
            
    def stop_execution(self):
        """Остановка выполнения"""
        self.running = False
        
    def reset_processor(self):
        """Сброс процессора"""
        self.running = False
        self.processor.reset()
        self.performance_monitor.reset()
        self.clear_trace()
        self.update_display()
        self.update_charts()
        
    def log_execution_step(self, old_pc, old_ir):
        """Логирование шага выполнения"""
        opcode = (self.processor.IR >> 12) & 0xF
        operand = self.processor.IR & 0xFFF
        
        opcodes = {0x0: 'HALT', 0x1: 'LOAD', 0x2: 'STORE', 0x3: 'ADD', 0x4: 'SUB', 0x5: 'CMP', 0x6: 'JMP', 0x7: 'JZ', 0x8: 'JNZ'}
        mnemonic = opcodes.get(opcode, f'UNK({opcode})')
        
        log_entry = f"[{self.processor.step_count:4d}] PC:{old_pc:3d} | {mnemonic:5s} {operand:3d} | ACC:{self.processor.ACC:5d} | Flags: {'Z' if self.processor.flags['ZF'] else '-'}{'S' if self.processor.flags['SF'] else '-'}{'C' if self.processor.flags['CF'] else '-'}{'O' if self.processor.flags['OF'] else '-'}\n"
        
        self.trace_text.insert(tk.END, log_entry)
        self.trace_text.see(tk.END)
        
    def clear_trace(self):
        """Очистка трассировки"""
        self.trace_text.delete(1.0, tk.END)
        
    def save_trace(self):
        """Сохранение трассировки"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.trace_text.get(1.0, tk.END))
                messagebox.showinfo("Успех", f"Трассировка сохранена в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
                
    def update_display(self):
        """Обновление отображения"""
        # Обновляем регистры в разных форматах
        acc = self.processor.ACC
        pc = self.processor.PC
        ir = self.processor.IR
        
        self.acc_dec_label.config(text=str(acc))
        self.acc_hex_label.config(text=f"0x{acc:04X}")
        self.acc_bin_label.config(text=f"{acc:016b}")
        
        self.pc_dec_label.config(text=str(pc))
        self.pc_hex_label.config(text=f"0x{pc:04X}")
        self.pc_bin_label.config(text=f"{pc:016b}")
        
        self.ir_dec_label.config(text=str(ir))
        self.ir_hex_label.config(text=f"0x{ir:04X}")
        self.ir_bin_label.config(text=f"{ir:016b}")
        
        # Декодирование текущей команды
        self.decode_text.config(state="normal")
        self.decode_text.delete(1.0, tk.END)
        
        if ir != 0:
            opcode = (ir >> 12) & 0xF
            operand = ir & 0xFFF
            disasm = self.processor.disassemble_instruction(ir)
            
            decode_info = f"Команда: {disasm}\n"
            decode_info += f"Код операции: {opcode} (0x{opcode:X})\n"
            decode_info += f"Операнд: {operand} (0x{operand:03X})\n"
            
            # Определяем тип адресации
            if operand >= 512:
                decode_info += f"Тип адресации: Непосредственная (#{operand - 512})\n"
            elif operand >= 256:
                decode_info += f"Тип адресации: Косвенная (({operand - 256}))\n"
            else:
                decode_info += f"Тип адресации: Прямая ({operand})\n"
                
            self.decode_text.insert(tk.END, decode_info)
            
        self.decode_text.config(state="disabled")
        
        # Обновляем флаги
        for flag, var in self.flag_vars.items():
            var.set(self.processor.flags[flag])
            
        # Обновляем статус
        if self.processor.halted:
            self.status_var.set("ОСТАНОВЛЕН")
        elif self.running:
            self.status_var.set("ВЫПОЛНЯЕТСЯ")
        else:
            self.status_var.set("ГОТОВ")
            
        self.step_count_var.set(str(self.processor.step_count))
        
        # Обновляем память
        self.update_memory_display()
        
    def update_memory_display(self):
        """Обновление отображения памяти"""
        # Память команд
        self.memory_text.delete(1.0, tk.END)
        for i in range(min(100, len(self.processor.memory))):
            if self.processor.memory[i] != 0:
                disasm = self.processor.disassemble_instruction(self.processor.memory[i])
                line = f"{i:04X}: {self.processor.memory[i]:04X} - {disasm}"
                if i == self.processor.PC and not self.processor.halted:
                    line = ">>> " + line
                line += "\n"
                self.memory_text.insert(tk.END, line)
                
        # Память данных
        self.data_text.delete(1.0, tk.END)
        for i in range(100, min(300, len(self.processor.memory))):
            if self.processor.memory[i] != 0:
                line = f"{i:04X}: {self.processor.memory[i]:04X} ({self.processor.memory[i]})\n"
                self.data_text.insert(tk.END, line)
                
    def update_charts(self):
        """Обновление графиков"""
        # График команд
        if self.performance_monitor.instruction_counts:
            self.instr_ax.clear()
            commands = list(self.performance_monitor.instruction_counts.keys())
            counts = list(self.performance_monitor.instruction_counts.values())
            
            bars = self.instr_ax.bar(commands, counts, color='skyblue', edgecolor='navy')
            self.instr_ax.set_title('Статистика выполненных команд')
            self.instr_ax.set_xlabel('Команды')
            self.instr_ax.set_ylabel('Количество')
            
            # Добавляем значения на столбцы
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                self.instr_ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                 f'{count}', ha='center', va='bottom')
                                 
            self.instr_canvas.draw()
            
        # График регистров
        history = self.performance_monitor.register_value_history
        if history['ACC']:
            self.reg_ax.clear()
            steps = range(len(history['ACC']))
            
            self.reg_ax.plot(steps, history['ACC'], label='ACC', marker='o', markersize=3)
            self.reg_ax.plot(steps, history['PC'], label='PC', marker='s', markersize=3)
            
            self.reg_ax.set_title('История изменения регистров')
            self.reg_ax.set_xlabel('Шаги выполнения')
            self.reg_ax.set_ylabel('Значение')
            self.reg_ax.legend()
            self.reg_ax.grid(True, alpha=0.3)
            
            self.reg_canvas.draw()
            
        # График памяти
        if self.performance_monitor.memory_access_history:
            self.mem_ax.clear()
            addresses = [access['address'] for access in self.performance_monitor.memory_access_history]
            times = [access['time'] for access in self.performance_monitor.memory_access_history]
            
            self.mem_ax.scatter(addresses, times, alpha=0.6, s=20)
            self.mem_ax.set_title('Карта обращений к памяти')
            self.mem_ax.set_xlabel('Адрес памяти')
            self.mem_ax.set_ylabel('Время обращения')
            self.mem_ax.grid(True, alpha=0.3)
            
            self.mem_canvas.draw()
            
    def reset_charts(self):
        """Сброс графиков"""
        for ax in [self.instr_ax, self.reg_ax, self.mem_ax]:
            ax.clear()
        for canvas in [self.instr_canvas, self.reg_canvas, self.mem_canvas]:
            canvas.draw()
            
    def show_examples(self):
        """Показать примеры программ"""
        # Можно реализовать диалог выбора примеров
        examples = {
            "Факториал": self.load_default_example,
            "Поиск максимума": lambda: self.load_example("max_search"),
            "Свертка массивов": lambda: self.load_example("convolution")
        }
        
        # Простая реализация - загружаем пример поиска максимума
        self.code_text.delete(1.0, tk.END)
        max_example = """; Поиск максимума в массиве
START:
    LOAD 200         ; Загружаем первый элемент
    STORE 100        ; Сохраняем как максимум
    
    LOAD 201         ; Второй элемент
    CMP 100          ; Сравниваем с максимумом
    JZ CHECK3        ; Если меньше, пропускаем
    STORE 100        ; Иначе обновляем максимум
    
CHECK3:
    LOAD 202         ; Третий элемент
    CMP 100          ; Сравниваем с максимумом
    JZ CHECK4        ; Если меньше, пропускаем
    STORE 100        ; Иначе обновляем максимум
    
CHECK4:
    LOAD 203         ; Четвертый элемент
    CMP 100          ; Сравниваем с максимумом
    JZ CHECK5        ; Если меньше, пропускаем
    STORE 100        ; Иначе обновляем максимум
    
CHECK5:
    LOAD 204         ; Пятый элемент
    CMP 100          ; Сравниваем с максимумом
    JZ END           ; Если меньше, завершаем
    STORE 100        ; Иначе обновляем максимум
    
END:
    HALT             ; Результат в адресе 100
"""
        self.code_text.insert(tk.END, max_example)
        
    def load_example(self, example_name):
        """Загрузка конкретного примера"""
        # Заглушка для загрузки примеров
        pass
        
    def open_program(self):
        """Открытие программы из файла"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("Assembly files", "*.asm"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(1.0, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
                
    def save_program(self):
        """Сохранение программы в файл"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".asm",
            filetypes=[("Assembly files", "*.asm"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                content = self.code_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Успех", f"Программа сохранена в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
                
    def export_stats(self):
        """Экспорт статистики"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Статистика выполнения программы\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(f"Шагов выполнено: {self.processor.step_count}\n")
                    f.write(f"Состояние процессора: {'ОСТАНОВЛЕН' if self.processor.halted else 'АКТИВЕН'}\n\n")
                    
                    f.write("Статистика команд:\n")
                    for cmd, count in self.performance_monitor.instruction_counts.items():
                        f.write(f"  {cmd}: {count}\n")
                        
                    f.write("\nТрассировка выполнения:\n")
                    f.write(self.trace_text.get(1.0, tk.END))
                    
                messagebox.showinfo("Успех", f"Статистика экспортирована в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать статистику:\n{str(e)}")
                
    def toggle_fullscreen(self):
        """Переключение полноэкранного режима"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)

def main():
    root = tk.Tk()
    app = EnhancedProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

