import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, Canvas
import time
import threading
from processor import Processor
from assembler import Assembler

class DataFlowVisualizer:
    def __init__(self, canvas, width=800, height=600):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.animations = []
        self.components = {}
        # Настройки скорости анимации
        self.animation_steps = 10  # Было 20, стало 10 (в 2 раза быстрее)
        self.animation_delay = 25  # Было 50ms, стало 25ms (в 2 раза быстрее)
        self.create_components()
        
    def create_components(self):
        """Создание визуальных компонентов процессора"""
        # Цвета компонентов
        colors = {
            'register': '#E3F2FD',
            'memory': '#FFF3E0',
            'alu': '#E8F5E8',
            'control': '#FCE4EC',
            'bus': '#F3E5F5'
        }
        
        # Аккумулятор
        self.components['ACC'] = {
            'rect': self.canvas.create_rectangle(50, 50, 150, 100, fill=colors['register'], outline='black', width=2),
            'text': self.canvas.create_text(100, 75, text='ACC\n0', font=('Arial', 10, 'bold')),
            'x': 100, 'y': 75
        }
        
        # Счетчик команд
        self.components['PC'] = {
            'rect': self.canvas.create_rectangle(200, 50, 300, 100, fill=colors['register'], outline='black', width=2),
            'text': self.canvas.create_text(250, 75, text='PC\n0', font=('Arial', 10, 'bold')),
            'x': 250, 'y': 75
        }
        
        # Регистр команд
        self.components['IR'] = {
            'rect': self.canvas.create_rectangle(350, 50, 450, 100, fill=colors['register'], outline='black', width=2),
            'text': self.canvas.create_text(400, 75, text='IR\n0000', font=('Arial', 10, 'bold')),
            'x': 400, 'y': 75
        }
        
        # АЛУ
        self.components['ALU'] = {
            'rect': self.canvas.create_rectangle(150, 150, 300, 220, fill=colors['alu'], outline='black', width=2),
            'text': self.canvas.create_text(225, 185, text='АЛУ', font=('Arial', 12, 'bold')),
            'x': 225, 'y': 185
        }
        
        # Блок управления
        self.components['CU'] = {
            'rect': self.canvas.create_rectangle(350, 150, 500, 220, fill=colors['control'], outline='black', width=2),
            'text': self.canvas.create_text(425, 185, text='Блок\nУправления', font=('Arial', 10, 'bold')),
            'x': 425, 'y': 185
        }
        
        # Память
        self.components['MEM'] = {
            'rect': self.canvas.create_rectangle(50, 280, 200, 400, fill=colors['memory'], outline='black', width=2),
            'text': self.canvas.create_text(125, 340, text='ОЗУ\n4096 ячеек', font=('Arial', 10, 'bold')),
            'x': 125, 'y': 340
        }
        
        # Шина данных
        self.components['DATA_BUS'] = {
            'rect': self.canvas.create_rectangle(250, 280, 500, 320, fill=colors['bus'], outline='black', width=2),
            'text': self.canvas.create_text(375, 300, text='Шина данных', font=('Arial', 10, 'bold')),
            'x': 375, 'y': 300
        }
        
        # Флаги
        self.components['FLAGS'] = {
            'rect': self.canvas.create_rectangle(520, 50, 620, 150, fill=colors['register'], outline='black', width=2),
            'text': self.canvas.create_text(570, 100, text='Флаги\nZF SF CF OF', font=('Arial', 9, 'bold')),
            'x': 570, 'y': 100
        }
        
        # Регистры общего назначения R0-R15
        register_gp_y = 200  # Y-позиция для общей группы регистров
        register_gp_x_start = 600  # Начало X-позиции
        
        for i in range(16):
            x_start = register_gp_x_start + (i % 4) * 60  # 4 регистра в ряду
            y_start = register_gp_y + (i // 4) * 60  # 4 ряда
            x_end = x_start + 50
            y_end = y_start + 45
            
            reg_name = f'R{i}'
            self.components[reg_name] = {
                'rect': self.canvas.create_rectangle(x_start, y_start, x_end, y_end, 
                                                     fill=colors['register'], outline='black', width=2),
                'text': self.canvas.create_text(x_start + 25, y_start + 22, 
                                                text=f'R{i}\n0', font=('Arial', 9, 'bold')),
                'x': x_start + 25, 'y': y_start + 22
            }
        
        # Соединительные линии
        self.create_connections()
        
    def create_connections(self):
        """Создание соединительных линий между компонентами"""
        # ACC -> ALU
        self.canvas.create_line(100, 100, 175, 150, width=2, fill='gray', dash=(5, 5))
        
        # ALU -> ACC
        self.canvas.create_line(175, 150, 100, 100, width=2, fill='gray', dash=(5, 5))
        
        # IR -> CU
        self.canvas.create_line(400, 100, 425, 150, width=2, fill='gray', dash=(5, 5))
        
        # MEM -> DATA_BUS
        self.canvas.create_line(200, 340, 250, 300, width=2, fill='gray', dash=(5, 5))
        
        # DATA_BUS -> ACC
        self.canvas.create_line(300, 280, 100, 100, width=2, fill='gray', dash=(5, 5))
        
        # ALU -> FLAGS
        self.canvas.create_line(300, 185, 520, 100, width=2, fill='gray', dash=(5, 5))
        
        # Регистры общего назначения -> ALU (пунктирные линии для показа возможности)
        for i in range(16):
            reg_name = f'R{i}'
            if reg_name in self.components:
                reg_comp = self.components[reg_name]
                # Тонкая линия от регистра к АЛУ
                self.canvas.create_line(reg_comp['x'], reg_comp['y'] - 22, 175, 150, 
                                       width=1, fill='lightgray', dash=(3, 3))
        
    def update_component(self, component, value):
        """Обновление значения компонента"""
        if component in self.components:
            comp = self.components[component]
            if component == 'ACC':
                self.canvas.itemconfig(comp['text'], text=f'ACC\n{value}')
            elif component == 'PC':
                self.canvas.itemconfig(comp['text'], text=f'PC\n{value}')
            elif component == 'IR':
                self.canvas.itemconfig(comp['text'], text=f'IR\n{value:04X}')
            elif component == 'FLAGS':
                self.canvas.itemconfig(comp['text'], text=f'Флаги\n{value}')
            elif component.startswith('R'):  # R0-R15
                self.canvas.itemconfig(comp['text'], text=f'{component}\n{value}')
                
    def animate_data_flow(self, from_comp, to_comp, data_value, color='red'):
        if from_comp not in self.components or to_comp not in self.components:
            return
            
        from_x = self.components[from_comp]['x']
        from_y = self.components[from_comp]['y']
        to_x = self.components[to_comp]['x']
        to_y = self.components[to_comp]['y']

        data_circle = self.canvas.create_oval(from_x-10, from_y-10, from_x+10, from_y+10, 
                                            fill=color, outline='black', width=2)
        data_text = self.canvas.create_text(from_x, from_y, text=str(data_value), 
                                          font=('Arial', 8, 'bold'), fill='white')

        steps = self.animation_steps
        dx = (to_x - from_x) / steps
        dy = (to_y - from_y) / steps
        
        def animate_step(step):
            if step < steps:
                self.canvas.move(data_circle, dx, dy)
                self.canvas.move(data_text, dx, dy)
                self.canvas.after(self.animation_delay, lambda: animate_step(step + 1))
            else:
                self.canvas.delete(data_circle)
                self.canvas.delete(data_text)
                
        animate_step(0)
        
    def highlight_component(self, component, color='yellow', duration=500):
        if component in self.components:
            comp = self.components[component]
            original_color = self.canvas.itemcget(comp['rect'], 'fill')
            self.canvas.itemconfig(comp['rect'], fill=color)
            self.canvas.after(duration, lambda: self.canvas.itemconfig(comp['rect'], fill=original_color))

class VisualProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Эмулятор процессора с визуализацией - Вариант №9")
        self.root.geometry("1600x900")
        self.processor = Processor()
        self.assembler = Assembler()
        self.running = False
        self.step_mode = False
        self.create_widgets()
        # Применяем настройки анимации
        self.update_animation_settings()
        self.update_display()
        
    def create_widgets(self):
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=2)
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)

        vis_title = ttk.Label(left_frame, text="Визуализация потока данных", font=('Arial', 14, 'bold'))
        vis_title.pack(pady=(0, 10))

        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = Canvas(canvas_frame, bg='white', width=1000, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        self.visualizer = DataFlowVisualizer(self.canvas)

        vis_control_frame = ttk.LabelFrame(left_frame, text="Управление визуализацией", padding=10)
        vis_control_frame.pack(fill=tk.X, pady=(10, 0))
        
        vis_buttons = ttk.Frame(vis_control_frame)
        vis_buttons.pack(fill=tk.X)
        
        ttk.Button(vis_buttons, text="Сброс", command=self.reset_processor).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(vis_buttons, text="Шаг", command=self.step_with_animation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(vis_buttons, text="Запуск", command=self.run_with_animation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(vis_buttons, text="Пауза", command=self.pause_execution).pack(side=tk.LEFT, padx=(0, 5))

        speed_frame = ttk.Frame(vis_control_frame)
        speed_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(speed_frame, text="Скорость:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=2.0)  # По умолчанию 2x скорость
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=3.0, variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(speed_frame, text="3x").pack(side=tk.RIGHT)
        
        # Чекбокс для отключения анимации
        self.animation_enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(vis_control_frame, text="Включить анимацию", 
                       variable=self.animation_enabled_var).pack(pady=(5, 0))
        
        # Привязываем изменение скорости к обновлению настроек
        speed_scale.configure(command=self.update_animation_settings)
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        reg_frame = ttk.Frame(notebook)
        notebook.add(reg_frame, text="Регистры")
        
        self.create_register_panel(reg_frame)

        asm_frame = ttk.Frame(notebook)
        notebook.add(asm_frame, text="Ассемблер")
        
        self.create_assembler_panel(asm_frame)

        mem_frame = ttk.Frame(notebook)
        notebook.add(mem_frame, text="Память")
        
        self.create_memory_panel(mem_frame)
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Логи")
        
        self.create_log_panel(log_frame)
        
    def create_register_panel(self, parent):
        state_frame = ttk.LabelFrame(parent, text="Текущее состояние", padding=10)
        state_frame.pack(fill=tk.X, pady=(0, 10))
        self.acc_var = tk.StringVar()
        self.pc_var = tk.StringVar()
        self.ir_var = tk.StringVar()
        
        # Системные регистры
        ttk.Label(state_frame, text="Аккумулятор:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(state_frame, textvariable=self.acc_var, font=('Courier', 10)).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(state_frame, text="Счетчик команд:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(state_frame, textvariable=self.pc_var, font=('Courier', 10)).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(state_frame, text="Регистр команд:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(state_frame, textvariable=self.ir_var, font=('Courier', 10)).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Регистры общего назначения
        reg_frame = ttk.LabelFrame(parent, text="Регистры общего назначения (R0-R15)", padding=10)
        reg_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.reg_vars = {}
        for i in range(16):
            var = tk.StringVar()
            self.reg_vars[f'R{i}'] = var
            row = i // 4
            col = (i % 4) * 2
            ttk.Label(reg_frame, text=f"R{i}:").grid(row=row, column=col, sticky=tk.W, padx=(0, 5))
            ttk.Label(reg_frame, textvariable=var, font=('Courier', 9)).grid(row=row, column=col+1, sticky=tk.W, padx=(0, 10))

        flags_frame = ttk.LabelFrame(parent, text="Флаги", padding=10)
        flags_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.flag_vars = {}
        flag_names = ['ZF', 'SF', 'CF', 'OF']
        flag_descriptions = ['Ноль', 'Знак', 'Перенос', 'Переполнение']
        
        for i, (name, desc) in enumerate(zip(flag_names, flag_descriptions)):
            var = tk.BooleanVar()
            self.flag_vars[name] = var
            cb = ttk.Checkbutton(flags_frame, text=f"{name} ({desc})", variable=var, state="disabled")
            cb.pack(anchor=tk.W, pady=2)

        stats_frame = ttk.LabelFrame(parent, text="Статистика", padding=10)
        stats_frame.pack(fill=tk.X)
        
        self.step_count_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
        ttk.Label(stats_frame, text="Статус:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.status_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Шагов:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.step_count_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
    def create_assembler_panel(self, parent):
        ttk.Label(parent, text="Исходный код:").pack(anchor=tk.W)
        self.code_text = scrolledtext.ScrolledText(parent, height=15, width=50)
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Ассемблировать", command=self.assemble_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Загрузить", command=self.load_assembled_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Примеры", command=self.load_examples).pack(side=tk.LEFT)

        ttk.Label(parent, text="Машинный код:").pack(anchor=tk.W)
        self.asm_result_text = scrolledtext.ScrolledText(parent, height=8, width=50, state="disabled")
        self.asm_result_text.pack(fill=tk.BOTH, expand=True)
        self.load_default_example()
        
    def create_memory_panel(self, parent):
        ttk.Label(parent, text="Память команд:").pack(anchor=tk.W)
        self.memory_text = scrolledtext.ScrolledText(parent, height=10, width=50)
        self.memory_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        ttk.Label(parent, text="Память данных:").pack(anchor=tk.W)
        self.data_text = scrolledtext.ScrolledText(parent, height=10, width=50)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
    def create_log_panel(self, parent):
        ttk.Label(parent, text="Лог выполнения:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(parent, height=20, width=50)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        ttk.Button(parent, text="Очистить логи", command=self.clear_logs).pack()
        
    def load_default_example(self):
        example_code = """; Вариант 9: Свертка двух массивов (6 элементов, целые без знака)
; Массив A начинается по адресу 300, массив B — по адресу 320.
; Формат хранения: [размер, элемент0, элемент1, ...]
; Результат сохраняется в ячейке 100.

START:
    LOAD #0
    STORE 100        ; сумма свертки
    STORE 101        ; индекс i

    LOAD #300
    STORE 102        ; база массива A
    LOAD #320
    STORE 103        ; база массива B

    LOAD (102)
    STORE 110        ; размер массивов

LOOP:
    LOAD 101
    CMP 110
    JZ END

    LOAD 102
    ADD #1
    ADD 101
    STORE 104
    LOAD (104)
    STORE 106        ; A[i]

    LOAD 103
    ADD #1
    ADD 101
    STORE 105
    LOAD (105)
    STORE 107        ; B[i]

    LOAD 107
    STORE 109        ; счётчик для умножения
    LOAD #0
    STORE 108        ; произведение

MULT_LOOP:
    LOAD 109
    JZ MULT_DONE

    LOAD 108
    ADD 106
    STORE 108

    LOAD 109
    SUB #1
    STORE 109
    JMP MULT_LOOP

MULT_DONE:
    LOAD 100
    ADD 108
    STORE 100

    LOAD 101
    ADD #1
    STORE 101
    JMP LOOP

END:
    HALT
"""
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, example_code)
        
    def step_with_animation(self):
        if not self.processor.halted:
            old_state = self.get_processor_state()
            success = self.processor.step()
            new_state = self.get_processor_state()
            
            if success:
                if self.animation_enabled_var.get():
                    self.animate_instruction_execution(old_state, new_state)
                else:
                    self.visualizer.update_component('ACC', new_state['ACC'])
                    self.visualizer.update_component('PC', new_state['PC'])
                    self.visualizer.update_component('IR', new_state['IR'])
                    flags_str = f"{'Z' if new_state['flags']['ZF'] else '-'}{'S' if new_state['flags']['SF'] else '-'}{'C' if new_state['flags']['CF'] else '-'}{'O' if new_state['flags']['OF'] else '-'}"
                    self.visualizer.update_component('FLAGS', flags_str)
                self.log_instruction(old_state, new_state)
                
            self.update_display()
            
            if self.processor.halted:
                result = self.processor.memory[100]
                messagebox.showinfo("Программа завершена", 
                    f"Результат сохранен в ячейке 100: {result}")
            
    def run_with_animation(self):
        if not self.running and not self.processor.halted:
            self.running = True
            self.animate_continuous_execution()
            
    def animate_continuous_execution(self):
        if self.running and not self.processor.halted:
            # Защита от бесконечного выполнения
            if self.processor.step_count > 10000:
                self.running = False
                messagebox.showwarning("Превышен лимит", 
                    f"Программа выполнила {self.processor.step_count} шагов и остановлена.\n"
                    f"Результат в ячейке 100: {self.processor.memory[100]}")
                return
            
            old_state = self.get_processor_state()
            self.processor.step()
            new_state = self.get_processor_state()
            
            if self.animation_enabled_var.get():
                self.animate_instruction_execution(old_state, new_state)
            else:
                self.visualizer.update_component('ACC', new_state['ACC'])
                self.visualizer.update_component('PC', new_state['PC'])
                self.visualizer.update_component('IR', new_state['IR'])
                flags_str = f"{'Z' if new_state['flags']['ZF'] else '-'}{'S' if new_state['flags']['SF'] else '-'}{'C' if new_state['flags']['CF'] else '-'}{'O' if new_state['flags']['OF'] else '-'}"
                self.visualizer.update_component('FLAGS', flags_str)
            
            self.log_instruction(old_state, new_state)
            self.update_display()
            
            # Быстрое выполнение без анимации для производительности
            delay = 0  # Минимальная задержка
            self.root.after(delay, self.animate_continuous_execution)
        else:
            self.running = False
            if self.processor.halted:
                result = self.processor.memory[100]
                messagebox.showinfo("Программа завершена", 
                    f"Результат сохранен в ячейке 100: {result}")
            
    def pause_execution(self):
        self.running = False
    
    def update_animation_settings(self, *args):
        """Обновление настроек анимации на основе слайдера скорости"""
        speed = self.speed_var.get()
        
        # Применяем скорость: чем выше значение, тем быстрее анимация
        # speed=1.0 → нормальная скорость
        # speed=3.0 → 3x быстрее
        if self.animation_enabled_var.get():
            self.visualizer.animation_steps = max(3, int(15 / speed))
            self.visualizer.animation_delay = max(5, int(50 / speed))
        else:
            self.visualizer.animation_steps = 1
            self.visualizer.animation_delay = 1
        
    def animate_instruction_execution(self, old_state, new_state):
        ir = new_state['IR']
        opcode = (ir >> 12) & 0xF
        operand = ir & 0xFFF

        speed = self.speed_var.get()
        delay_1 = max(10, int(100 / speed))
        delay_2 = max(20, int(200 / speed))
        delay_3 = max(40, int(400 / speed))
        delay_4 = max(60, int(600 / speed))
        delay_5 = max(80, int(800 / speed))
        delay_short = max(5, int(50 / speed))

        self.visualizer.highlight_component('PC', 'lightblue', delay_5)
        self.visualizer.highlight_component('IR', 'lightgreen', delay_4)
        
        # Handle STORE early to ensure proper register animations
        if opcode == 0x2:
            if 1040 <= operand < 1056:  # (Rk)
                reg_num = operand - 1040
                self.visualizer.highlight_component(f'R{reg_num}', 'lightyellow', delay_short)
                self.visualizer.animate_data_flow('ACC', 'DATA_BUS', old_state['ACC'], 'red')
                self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'MEM', f'M[R{reg_num}]', 'red'))
            elif 1024 <= operand < 1040:  # Rk
                reg_num = operand - 1024
                self.visualizer.highlight_component(f'R{reg_num}', 'lightyellow', delay_short)
                self.visualizer.animate_data_flow('ACC', f'R{reg_num}', old_state['ACC'], 'red')
            elif 256 <= operand < 512:  # (addr)
                addr = operand - 256
                self.visualizer.animate_data_flow('ACC', 'DATA_BUS', old_state['ACC'], 'red')
                self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'MEM', f'M[M[{addr}]]', 'red'))
            else:  # direct addr
                self.visualizer.animate_data_flow('ACC', 'DATA_BUS', old_state['ACC'], 'red')
                self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'MEM', f'M[{operand}]', 'red'))

            # Update components and exit
            self.root.after(delay_short, lambda: self.visualizer.update_component('ACC', new_state['ACC']))
            self.root.after(delay_1, lambda: self.visualizer.update_component('PC', new_state['PC']))
            self.root.after(delay_2, lambda: self.visualizer.update_component('IR', new_state['IR']))
            flags_str = f"{'Z' if new_state['flags']['ZF'] else '-'}{'S' if new_state['flags']['SF'] else '-'}{'C' if new_state['flags']['CF'] else '-'}{'O' if new_state['flags']['OF'] else '-'}"
            self.root.after(delay_3, lambda: self.visualizer.update_component('FLAGS', flags_str))
            return

        if opcode == 0x1:
            if operand >= 1040 and operand < 1056:
                reg_num = operand - 1040
                self.visualizer.highlight_component(f'R{reg_num}', 'lightyellow', delay_short)
                self.visualizer.animate_data_flow('MEM', 'DATA_BUS', f'M[R{reg_num}]', 'green')
                self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'ACC', new_state['ACC'], 'green'))
            elif operand >= 1024 and operand < 1040:
                reg_num = operand - 1024
                self.visualizer.highlight_component(f'R{reg_num}', 'lightyellow', delay_short)
                self.visualizer.animate_data_flow(f'R{reg_num}', 'ACC', self.processor.registers[reg_num], 'blue')
            elif operand >= 512:
                value = operand - 512
                self.visualizer.animate_data_flow('CU', 'ACC', value, 'blue')
            elif operand >= 256:
                addr = operand - 256
                self.visualizer.animate_data_flow('MEM', 'DATA_BUS', f'M[{addr}]', 'green')
                self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'ACC', new_state['ACC'], 'green'))
            else:
                self.visualizer.animate_data_flow('MEM', 'DATA_BUS', f'M[{operand}]', 'green')
                self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'ACC', new_state['ACC'], 'green'))
                
        elif opcode == 0x2:
            self.visualizer.animate_data_flow('ACC', 'DATA_BUS', old_state['ACC'], 'red')
            self.root.after(delay_1, lambda: self.visualizer.animate_data_flow('DATA_BUS', 'MEM', f'→M[{operand}]', 'red'))
            
        elif opcode == 0x3 or opcode == 0x4:  # ADD/SUB
            self.visualizer.highlight_component('ALU', 'yellow', delay_5)
            self.visualizer.animate_data_flow('ACC', 'ALU', old_state['ACC'], 'purple')
            if operand >= 1040 and operand < 1056:
                reg_num = operand - 1040
                self.visualizer.highlight_component(f'R{reg_num}', 'lightyellow', delay_short)
                self.root.after(delay_2, lambda: self.visualizer.animate_data_flow('MEM', 'ALU', f'M[R{reg_num}]', 'purple'))
            elif operand >= 1024 and operand < 1040:
                reg_num = operand - 1024
                self.visualizer.highlight_component(f'R{reg_num}', 'lightyellow', delay_short)
                self.root.after(delay_2, lambda: self.visualizer.animate_data_flow(f'R{reg_num}', 'ALU', self.processor.registers[reg_num], 'purple'))
            elif operand >= 512:
                value = operand - 512
                self.root.after(delay_2, lambda: self.visualizer.animate_data_flow('CU', 'ALU', value, 'purple'))
            elif operand >= 256:
                addr = operand - 256
                self.root.after(delay_2, lambda: self.visualizer.animate_data_flow('MEM', 'ALU', f'M[{addr}]', 'purple'))
            else:
                self.root.after(delay_2, lambda: self.visualizer.animate_data_flow('MEM', 'ALU', f'M[{operand}]', 'purple'))
            self.root.after(delay_3, lambda: self.visualizer.animate_data_flow('ALU', 'ACC', new_state['ACC'], 'purple'))
            self.root.after(delay_4, lambda: self.visualizer.animate_data_flow('ALU', 'FLAGS', 'flags', 'orange'))
            
        elif opcode == 0x5:  # CMP
            self.visualizer.highlight_component('ALU', 'yellow', delay_5)
            self.visualizer.animate_data_flow('ACC', 'ALU', old_state['ACC'], 'cyan')
            self.root.after(delay_2, lambda: self.visualizer.animate_data_flow('ALU', 'FLAGS', 'cmp', 'orange'))
            
        # Обновляем визуальные компоненты
        self.root.after(delay_short, lambda: self.visualizer.update_component('ACC', new_state['ACC']))
        self.root.after(delay_1, lambda: self.visualizer.update_component('PC', new_state['PC']))
        self.root.after(delay_2, lambda: self.visualizer.update_component('IR', new_state['IR']))
        flags_str = f"{'Z' if new_state['flags']['ZF'] else '-'}{'S' if new_state['flags']['SF'] else '-'}{'C' if new_state['flags']['CF'] else '-'}{'O' if new_state['flags']['OF'] else '-'}"
        self.root.after(delay_3, lambda: self.visualizer.update_component('FLAGS', flags_str))
        
    def get_processor_state(self):
        """Получение состояния процессора"""
        return {
            'ACC': self.processor.ACC,
            'PC': self.processor.PC,
            'IR': self.processor.IR,
            'flags': self.processor.flags.copy(),
            'step_count': self.processor.step_count
        }
        
    def log_instruction(self, old_state, new_state):
        """Логирование выполненной инструкции"""
        ir = new_state['IR']
        opcode = (ir >> 12) & 0xF
        operand = ir & 0xFFF
        
        # Определяем мнемонику
        opcodes = {0x0: 'HALT', 0x1: 'LOAD', 0x2: 'STORE', 0x3: 'ADD', 0x4: 'SUB', 0x5: 'CMP', 0x6: 'JMP', 0x7: 'JZ', 0x8: 'JNZ'}
        mnemonic = opcodes.get(opcode, f'UNK({opcode})')
        
        # Формируем строку лога
        log_entry = f"Шаг {new_state['step_count']:3d}: PC={old_state['PC']:3d} | {mnemonic:5s} {operand:3d} | ACC: {old_state['ACC']:5d}→{new_state['ACC']:5d}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def clear_logs(self):
        """Очистка логов"""
        self.log_text.delete(1.0, tk.END)
        
    def reset_processor(self):
        """Сброс процессора (сохраняет программу в памяти)"""
        self.running = False
        self.processor.reset()
        self.clear_logs()
        self.update_display()
        
        # Сброс визуализации (включая регистры)
        self.visualizer.update_component('ACC', 0)
        self.visualizer.update_component('PC', 0)
        self.visualizer.update_component('IR', 0)
        self.visualizer.update_component('FLAGS', '----')
        for i in range(16):
            self.visualizer.update_component(f'R{i}', 0)
        
    def full_reset_processor(self):
        """Полный сброс процессора (очищает память)"""
        self.running = False
        self.processor.ACC = 0
        self.processor.PC = 0
        self.processor.IR = 0
        self.processor.flags = {'ZF': False, 'SF': False, 'CF': False, 'OF': False}
        self.processor.halted = False
        self.processor.step_count = 0
        self.processor.memory = [0] * 4096
        self.clear_logs()
        self.update_display()
        
        # Сброс визуализации (включая регистры)
        self.visualizer.update_component('ACC', 0)
        self.visualizer.update_component('PC', 0)
        self.visualizer.update_component('IR', 0)
        self.visualizer.update_component('FLAGS', '----')
        for i in range(16):
            self.visualizer.update_component(f'R{i}', 0)
        
    def assemble_code(self):
        """Ассемблирование кода"""
        try:
            source_code = self.code_text.get(1.0, tk.END)
            
            # Используем основной ассемблер из assembler.py
            from assembler import Assembler
            main_assembler = Assembler()
            instructions = main_assembler.assemble(source_code)
            
            # Отображаем результат
            self.asm_result_text.config(state="normal")
            self.asm_result_text.delete(1.0, tk.END)
            
            for i, instr in enumerate(instructions):
                line = f"{i:04X}: {instr['instruction']:04X} - {instr['mnemonic']}\n"
                self.asm_result_text.insert(tk.END, line)
            
            self.asm_result_text.config(state="disabled")
            
            # Сохраняем инструкции
            self.assembled_instructions = instructions
            
            messagebox.showinfo("Успех", f"Код успешно ассемблирован! {len(instructions)} инструкций.")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка ассемблирования:\n{str(e)}")
            
    def load_assembled_code(self):
        """Загрузка ассемблированного кода"""
        try:
            if hasattr(self, 'assembled_instructions'):
                machine_codes = [instr['instruction'] for instr in self.assembled_instructions]
                self.processor.load_program(machine_codes)
                
                # Загружаем тестовые данные в зависимости от программы
                source_code = self.code_text.get(1.0, tk.END)
                if "сверт" in source_code.lower() or "convolution" in source_code.lower():
                    # Данные для свертки с указанием длины массивов
                    array_a = [6, 1, 2, 3, 4, 5, 6]
                    array_b = [6, 6, 5, 4, 3, 2, 1]
                    self.processor.load_data(array_a, 300)
                    self.processor.load_data(array_b, 320)
                    data_info = (
                        "Данные для свертки: "
                        f"A={array_a} (адреса 300-306), "
                        f"B={array_b} (адреса 320-326)"
                    )
                elif "максимум" in source_code.lower() or "max" in source_code.lower():
                    # Данные для поиска максимума (первый элемент — размер)
                    test_data = [6, 12, 3, 27, 9, 1, 18]
                    self.processor.load_data(test_data, 300)
                    data_info = (
                        "Данные для поиска максимума: "
                        f"{test_data} (адреса 300-306)"
                    )
                else:
                    # Данные по умолчанию
                    default_data = [4, 10, 20, 30, 40]
                    self.processor.load_data(default_data, 300)
                    data_info = (
                        "Данные по умолчанию (формат [N, ...]): "
                        f"{default_data} (адреса 300-304)"
                    )
                
                self.update_display()
                messagebox.showinfo("Успех", f"Программа загружена! {len(machine_codes)} инструкций.\n{data_info}")
            else:
                messagebox.showwarning("Предупреждение", "Сначала ассемблируйте код!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки:\n{str(e)}")
            
    def load_examples(self):
        """Загрузка примеров"""
        # Можно добавить диалог выбора примеров
        pass
        
    def update_display(self):
        """Обновление отображения"""
        # Обновляем регистры
        self.acc_var.set(f"{self.processor.ACC} (0x{self.processor.ACC:04X})")
        self.pc_var.set(f"{self.processor.PC} (0x{self.processor.PC:04X})")
        self.ir_var.set(f"{self.processor.IR} (0x{self.processor.IR:04X})")
        
        # Обновляем регистры общего назначения
        for i, reg_var in enumerate(self.reg_vars.values()):
            if hasattr(self.processor, 'registers'):
                reg_val = self.processor.registers[i] if i < len(self.processor.registers) else 0
                reg_var.set(f"{reg_val} (0x{reg_val:04X})")
            else:
                reg_var.set("0 (0x0000)")
        
        # Обновляем флаги
        for flag, var in self.flag_vars.items():
            var.set(self.processor.flags[flag])
            
        # Обновляем статус
        if self.processor.halted:
            self.status_var.set("Остановлен")
        elif self.running:
            self.status_var.set("Выполняется")
        else:
            self.status_var.set("Готов")
            
        self.step_count_var.set(str(self.processor.step_count))
        
        # Обновляем визуализацию
        self.visualizer.update_component('ACC', self.processor.ACC)
        self.visualizer.update_component('PC', self.processor.PC)
        self.visualizer.update_component('IR', self.processor.IR)
        flags_str = f"{'Z' if self.processor.flags['ZF'] else '-'}{'S' if self.processor.flags['SF'] else '-'}{'C' if self.processor.flags['CF'] else '-'}{'O' if self.processor.flags['OF'] else '-'}"
        self.visualizer.update_component('FLAGS', flags_str)
        
        # Обновляем регистры общего назначения в визуализации
        if hasattr(self.processor, 'registers'):
            for i in range(16):
                reg_name = f'R{i}'
                reg_val = self.processor.registers[i] if i < len(self.processor.registers) else 0
                self.visualizer.update_component(reg_name, reg_val)
        
        # Обновляем память
        self.update_memory_display()
        self.update_data_display()
        
    def update_memory_display(self):
        """Обновление отображения памяти команд"""
        self.memory_text.delete(1.0, tk.END)
        
        for i in range(min(50, len(self.processor.memory))):
            if self.processor.memory[i] != 0:
                disasm = self.processor.disassemble_instruction(self.processor.memory[i])
                line = f"{i:04X}: {self.processor.memory[i]:04X} - {disasm}\n"
                if i == self.processor.PC and not self.processor.halted:
                    line = ">>> " + line
                self.memory_text.insert(tk.END, line)
                
    def update_data_display(self):
        """Обновление отображения памяти данных"""
        self.data_text.delete(1.0, tk.END)
        
        for i in range(200, min(250, len(self.processor.memory))):
            if self.processor.memory[i] != 0:
                line = f"{i:04X}: {self.processor.memory[i]:04X} ({self.processor.memory[i]})\n"
                self.data_text.insert(tk.END, line)

def main():
    root = tk.Tk()
    app = VisualProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
