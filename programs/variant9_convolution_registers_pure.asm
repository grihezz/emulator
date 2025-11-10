; Вариант 9. Свертка (скалярное произведение) — регистровая версия
; Вход: массив A по адресам 301..306, массив B по адресам 321..326 (длина 6)
; Выход: сумма сохраняется по адресу 100 и в R5

START:
    ; Базы массивов
    LOAD #300
    STORE R1            ; R1 = base A (размер ожидается в 300, элементы с 301)
    LOAD #320
    STORE R2            ; R2 = base B (размер ожидается в 320, элементы с 321)

    ; size = 6 (жестко задано)
    LOAD #6
    STORE R3            ; R3 = size

    ; Инициализация
    LOAD #0
    STORE R4            ; R4 = i
    LOAD #0
    STORE R5            ; R5 = sum

LOOP:
    ; if i == size: END
    LOAD R4
    CMP R3
    JZ END

    ; addrA = baseA + 1 + i
    LOAD R1
    ADD #1
    ADD R4
    STORE R6            ; R6 = адрес A[i]
    LOAD (R6)
    STORE R7            ; R7 = A[i]

    ; addrB = baseB + 1 + i
    LOAD R2
    ADD #1
    ADD R4
    STORE R8            ; R8 = адрес B[i]
    LOAD (R8)
    STORE R9            ; R9 = B[i]

    ; product = A[i] * B[i] (повторным сложением)
    LOAD #0
    STORE R10           ; R10 = product
    LOAD R9
    STORE R0            ; R0 = счетчик (B[i])

MUL_LOOP:
    LOAD R0
    JZ MUL_DONE
    LOAD R10
    ADD R7
    STORE R10
    LOAD R0
    SUB #1
    STORE R0
    JMP MUL_LOOP

MUL_DONE:
    LOAD R5
    ADD R10
    STORE R5            ; sum += product

    ; i += 1
    LOAD R4
    ADD #1
    STORE R4
    JMP LOOP

END:
    LOAD R5
    STORE 100
    HALT

