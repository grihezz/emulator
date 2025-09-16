; Рабочая программа свертки двух массивов
; A = [1, 2, 3, 4, 5, 6] и B = [2, 3, 4, 5, 6, 7]
; Результат: 1*2 + 2*3 + 3*4 + 4*5 + 5*6 + 6*7 = 112

; Инициализация суммы
LOAD #0
STORE 100

; 1*2 = 2
LOAD 201
STORE 101
LOAD 211
STORE 102
; Умножение 1 * 2 = 2 (2 раза добавляем 1)
LOAD #0
ADD 101
ADD 101
STORE 103
; Добавляем к сумме
LOAD 100
ADD 103
STORE 100

; 2*3 = 6
LOAD 202
STORE 101
LOAD 212
STORE 102
; Умножение 2 * 3 = 6 (3 раза добавляем 2)
LOAD #0
ADD 101
ADD 101
ADD 101
STORE 103
; Добавляем к сумме
LOAD 100
ADD 103
STORE 100

; 3*4 = 12
LOAD 203
STORE 101
LOAD 213
STORE 102
; Умножение 3 * 4 = 12 (4 раза добавляем 3)
LOAD #0
ADD 101
ADD 101
ADD 101
ADD 101
STORE 103
; Добавляем к сумме
LOAD 100
ADD 103
STORE 100

; 4*5 = 20
LOAD 204
STORE 101
LOAD 214
STORE 102
; Умножение 4 * 5 = 20 (5 раз добавляем 4)
LOAD #0
ADD 101
ADD 101
ADD 101
ADD 101
ADD 101
STORE 103
; Добавляем к сумме
LOAD 100
ADD 103
STORE 100

; 5*6 = 30
LOAD 205
STORE 101
LOAD 215
STORE 102
; Умножение 5 * 6 = 30 (6 раз добавляем 5)
LOAD #0
ADD 101
ADD 101
ADD 101
ADD 101
ADD 101
ADD 101
STORE 103
; Добавляем к сумме
LOAD 100
ADD 103
STORE 100

; 6*7 = 42
LOAD 206
STORE 101
LOAD 216
STORE 102
; Умножение 6 * 7 = 42 (7 раз добавляем 6)
LOAD #0
ADD 101
ADD 101
ADD 101
ADD 101
ADD 101
ADD 101
ADD 101
STORE 103
; Добавляем к сумме
LOAD 100
ADD 103
STORE 100

HALT
