; Вариант 9. Поиск максимума в массиве — регистровая версия
; Вход: в памяти по адресу 300 хранится размер N, элементы по 301..(300+N)
; Выход: максимальный элемент сохраняется в память по адресу 100 (и в R5)

START:
    ; База массива и размер
    LOAD #300
    STORE R1            ; R1 = base (адрес ячейки с размером)
    LOAD (R1)
    STORE R2            ; R2 = size

    ; Инициализация
    LOAD #0
    STORE R3            ; R3 = i
    LOAD #0
    STORE R5            ; R5 = max

LOOP:
    ; if i == size: END
    LOAD R3
    CMP R2
    JZ END

    ; addr = base + 1 + i
    LOAD R1
    ADD #1
    ADD R3
    STORE R6            ; R6 = адрес текущего элемента

    ; cur = M[R6]
    LOAD (R6)
    STORE R10           ; R10 = cur (оригинал)

    ; Сравнение cur > max через поэлементное декрементирование
    LOAD R10
    STORE R11           ; R11 = x (cur, будет уменьшаться)
    LOAD R5
    STORE R12           ; R12 = y (max, будет уменьшаться)
    LOAD #0
    STORE R13           ; R13 = флаг (cur > max)

CMP_LOOP:
    LOAD R11
    JZ CHECK_DONE       ; если x == 0 → не больше
    LOAD R12
    JZ CUR_GREATER      ; если y == 0 → x > y
    LOAD R11
    SUB #1
    STORE R11
    LOAD R12
    SUB #1
    STORE R12
    JMP CMP_LOOP

CUR_GREATER:
    LOAD #1
    STORE R13           ; отметить, что cur > max

CHECK_DONE:
    LOAD R13
    JZ SKIP_UPDATE

    LOAD R10            ; max = cur
    STORE R5

SKIP_UPDATE:
    ; i += 1
    LOAD R3
    ADD #1
    STORE R3
    JMP LOOP

END:
    ; сохранить результат для проверки
    LOAD R5
    STORE 100
    HALT

