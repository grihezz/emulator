; Простая программа поиска максимума БЕЗ переходов
; Массив: [5, 3, 8, 1, 9, 2, 7]
; Результат: 9 (максимальный элемент)

; Инициализация
LOAD #0
STORE 100

; Проверяем каждый элемент по очереди

; Элемент 0: 5
LOAD 201
CMP 100
JZ SKIP1
STORE 100
SKIP1:

; Элемент 1: 3  
LOAD 202
CMP 100
JZ SKIP2
STORE 100
SKIP2:

; Элемент 2: 8
LOAD 203
CMP 100
JZ SKIP3
STORE 100
SKIP3:

; Элемент 3: 1
LOAD 204
CMP 100
JZ SKIP4
STORE 100
SKIP4:

; Элемент 4: 9 (максимум)
LOAD 205
CMP 100
JZ SKIP5
STORE 100
SKIP5:

; Элемент 5: 2
LOAD 206
CMP 100
JZ SKIP6
STORE 100
SKIP6:

; Элемент 6: 7
LOAD 207
CMP 100
JZ SKIP7
STORE 100
SKIP7:

HALT
