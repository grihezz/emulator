; Вариант 9. Поиск максимума - АЛЬТЕРНАТИВНАЯ ВЕРСИЯ
; Отличия: используем #301 вместо вычисления 300+1
; Результат: memory[100]

START:
    LOAD #0
    STORE 100        ; max = 0
    STORE 101        ; i = 0
    
    LOAD (300)       ; читаем размер напрямую (без 102)
    STORE 104        ; size

LOOP:
    LOAD 101         ; i
    CMP 104          ; сравниваем с size
    JZ END
    
    ; Вычисляем адрес элемента (используем #301 вместо 300+1)
    LOAD 101         ; индекс
    ADD #301         ; базовый адрес элементов (300 + 1)
    STORE 103        ; адрес элемента
    LOAD (103)       ; читаем элемент
    STORE 105        ; текущий элемент
    
    ; Копируем для сравнения
    LOAD 105
    STORE 106        ; элемент для уменьшения
    LOAD 100
    STORE 107        ; максимум для уменьшения
    
    ; Флаг "элемент больше"
    LOAD #0
    STORE 108

COMPARE:
    LOAD 106
    JZ ELEMENT_SMALLER   ; элемент обнулился -> элемент <= max
    
    LOAD 107
    JZ ELEMENT_BIGGER    ; максимум обнулился -> элемент > max
    
    LOAD 106
    SUB #1
    STORE 106            ; уменьшаем элемент
    
    LOAD 107
    SUB #1
    STORE 107            ; уменьшаем максимум
    
    JMP COMPARE

ELEMENT_SMALLER:
    ; Элемент <= максимум, ничего не делаем
    JMP NEXT

ELEMENT_BIGGER:
    ; Элемент > максимума
    LOAD #1
    STORE 108            ; флаг = true
    JMP NEXT

NEXT:
    LOAD 108
    JZ SKIP_UPDATE
    
    LOAD 105
    STORE 100            ; обновляем максимум

SKIP_UPDATE:
    LOAD 101
    ADD #1
    STORE 101            ; i += 1
    JMP LOOP

END:
    HALT

