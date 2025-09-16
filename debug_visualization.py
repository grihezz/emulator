#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from visual_gui import DataFlowVisualizer

# Создаем простое окно для тестирования визуализации
root = tk.Tk()
root.title("Тест визуализации")
root.geometry("800x600")

canvas = tk.Canvas(root, width=800, height=600, bg='white')
canvas.pack()

# Создаем визуализатор
visualizer = DataFlowVisualizer(canvas)

# Тестируем обновление компонентов
print("Тестируем обновление визуализации...")

# Обновляем ACC
visualizer.update_component('ACC', 42)
print("ACC обновлен на 42")

# Обновляем PC
visualizer.update_component('PC', 5)
print("PC обновлен на 5")

# Обновляем IR
visualizer.update_component('IR', 0x122A)
print("IR обновлен на 0x122A")

# Обновляем флаги
visualizer.update_component('FLAGS', 'Z---')
print("Флаги обновлены на Z---")

print("Проверьте визуализацию - ACC должен показывать 42")

root.mainloop()
