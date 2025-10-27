; Свертка двух массивов с кэшированием адресов в регистрах
; Оптимизированная версия: R12 и R13 хранят адреса элементов

START:
    LOAD #0
    STORE R1
    STORE R2
    
    LOAD #301
    STORE R12
    
    LOAD #321
    STORE R13
    
    LOAD #300
    STORE 200
    LOAD (200)
    STORE R5

LOOP:
    LOAD R2
    CMP R5
    JZ END
    
    LOAD R12
    ADD R2
    STORE 104
    
    LOAD (104)
    STORE R7
    
    LOAD R13
    ADD R2
    STORE 105
    
    LOAD (105)
    STORE R9
    
    LOAD R9
    STORE R10
    LOAD #0
    STORE R11

MULT_LOOP:
    LOAD R10
    JZ MULT_DONE
    
    LOAD R11
    ADD R7
    STORE R11
    
    LOAD R10
    SUB #1
    STORE R10
    JMP MULT_LOOP

MULT_DONE:
    LOAD R1
    ADD R11
    STORE R1
    
    LOAD R2
    ADD #1
    STORE R2
    JMP LOOP

END:
    LOAD R1
    STORE 100
    HALT
