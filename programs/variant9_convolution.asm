; Вариант 9. Свертка двух массивов по 6 элементов (целые без знака)
; Массив A начинается с адреса 300, массив B — с адреса 320.
; Формат хранения: [размер, элемент0, элемент1, ...].
; Итоговая сумма произведений сохраняется в ячейке 100.

START:
    LOAD #0
    STORE 100        ; накопленная сумма
    STORE 101        ; индекс i = 0

    LOAD #300
    STORE 102        ; базовый адрес массива A
    LOAD #320
    STORE 103        ; базовый адрес массива B

    LOAD (102)
    STORE 110        ; размер массива (ожидается 6)

LOOP:
    LOAD 101
    CMP 110
    JZ END           ; если i == size, завершаем

    LOAD 102
    ADD #1
    ADD 101
    STORE 104        ; адрес A[i]
    LOAD (104)
    STORE 106        ; значение A[i]

    LOAD 103
    ADD #1
    ADD 101
    STORE 105        ; адрес B[i]
    LOAD (105)
    STORE 107        ; значение B[i]

    LOAD 107
    STORE 109        ; счётчик повторений для умножения
    LOAD #0
    STORE 108        ; произведение A[i] * B[i]

MULT_LOOP:
    LOAD 109
    JZ MULT_DONE     ; если счётчик 0, заканчиваем умножение

    LOAD 108
    ADD 106
    STORE 108        ; product += A[i]

    LOAD 109
    SUB #1
    STORE 109        ; уменьшаем счётчик
    JMP MULT_LOOP

MULT_DONE:
    LOAD 100
    ADD 108
    STORE 100        ; суммируем произведение

    LOAD 101
    ADD #1
    STORE 101        ; i += 1
    JMP LOOP

END:
    HALT
