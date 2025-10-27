START:
    LOAD #300
    STORE 200
    LOAD (200)
    STORE R2
    
    LOAD #301
    STORE 201
    LOAD (201)
    STORE R3
    
    LOAD #302
    STORE 202
    LOAD (202)
    STORE R4
    
    LOAD #303
    STORE 203
    LOAD (203)
    STORE R5
    
    LOAD #304
    STORE 204
    LOAD (204)
    STORE R6
    
    LOAD #0
    STORE R1
    
    LOAD R3
    ADD R1
    STORE R1
    
    LOAD R4
    ADD R1
    STORE R1
    
    LOAD R5
    ADD R1
    STORE R1
    
    LOAD R6
    ADD R1
    STORE R1
    
    LOAD R1
    STORE 100
    HALT
