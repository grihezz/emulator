; Сумма элементов массива с кэшированием адресов

START:
    LOAD #0
    STORE R1
    STORE R2
    
    LOAD #301
    STORE R12
    
    LOAD #300
    STORE 200
    LOAD (200)
    STORE R4

LOOP:
    LOAD R2
    CMP R4
    JZ END
    
    LOAD R12
    ADD R2
    STORE 104
    
    LOAD (104)
    ADD R1
    STORE R1
    
    LOAD R2
    ADD #1
    STORE R2
    JMP LOOP

END:
    LOAD R1
    STORE 100
    HALT
