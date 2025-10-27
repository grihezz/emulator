; Вариант 9. Сортировка пузырьком (с использованием регистров)
; Массив начинается с адреса 300, формат: [размер, элемент0, элемент1, ...]
; Результат: отсортированный массив на месте

START:
    LOAD #300        ; базовый адрес
    STORE R1
    LOAD (R1)        ; читаем размер
    STORE R2         ; size (используем R2)
    STORE R3         ; outer loop counter (используем R3)

OUTER_LOOP:
    LOAD R3
    SUB #1           ; outer loop: size-1 итераций
    STORE R3
    JZ END
    
    LOAD R3          ; подготовка к внутреннему циклу
    STORE R4         ; j = size-1 (используем R4)
    LOAD #0
    STORE R5         ; swapped flag (используем R5)

INNER_LOOP:
    LOAD R4
    JZ CHECK_SWAPPED  ; если j == 0, проверяем были ли обмены
    
    ; Вычисляем адреса arr[j] и arr[j-1]
    LOAD R1          ; база массива
    ADD #1           ; пропускаем размер
    ADD R4           ; j
    STORE R6         ; адрес arr[j] (используем R6)
    
    LOAD R4          ; j
    SUB #1           ; j-1
    STORE R7         ; j-1 (используем R7)
    
    LOAD R1          ; база массива
    ADD #1
    ADD R7           ; j-1
    STORE R8         ; адрес arr[j-1] (используем R8)
    
    ; Сравниваем arr[j] и arr[j-1]
    LOAD (R6)
    STORE R9         ; arr[j] (используем R9)
    
    LOAD (R8)
    STORE R10        ; arr[j-1] (используем R10)
    
    ; Копируем для сравнения
    LOAD R9
    STORE R11        ; копия arr[j]
    LOAD R10
    STORE R12        ; копия arr[j-1]
    
    LOAD #0
    STORE R13        ; флаг "arr[j] > arr[j-1]"

COMPARE:
    LOAD R11
    JZ NO_SWAP       ; если arr[j] стал 0
    
    LOAD R12
    JZ SWAP           ; если arr[j-1] стал 0, arr[j] > arr[j-1]
    
    LOAD R11
    SUB #1
    STORE R11
    
    LOAD R12
    SUB #1
    STORE R12
    
    JMP COMPARE

SWAP:
    ; Меняем местами arr[j] и arr[j-1]
    LOAD R10         ; arr[j-1]
    STORE (R6)       ; arr[j] = arr[j-1]
    
    LOAD R9          ; arr[j]
    STORE (R8)       ; arr[j-1] = arr[j]
    
    LOAD #1
    STORE R5         ; swapped = true
    
NO_SWAP:
    ; Уменьшаем j
    LOAD R4
    SUB #1
    STORE R4
    JMP INNER_LOOP

CHECK_SWAPPED:
    ; Проверяем, были ли обмены
    LOAD R5
    JZ END           ; если swapped == 0, массив отсортирован
    
    ; Уменьшаем outer counter
    JMP OUTER_LOOP

END:
    HALT

