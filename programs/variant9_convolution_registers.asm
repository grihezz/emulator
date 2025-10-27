START:
    LOAD #301
    STORE 200
    LOAD #302
    STORE 201
    LOAD #303
    STORE 202
    LOAD #304
    STORE 203
    LOAD #305
    STORE 204
    LOAD #306
    STORE 205
    
    LOAD #321
    STORE 206
    LOAD #322
    STORE 207
    LOAD #323
    STORE 208
    LOAD #324
    STORE 209
    LOAD #325
    STORE 210
    LOAD #326
    STORE 211
    
    LOAD (200)
    STORE R2
    
    LOAD (201)
    STORE R3
    
    LOAD (202)
    STORE R4
    
    LOAD (203)
    STORE R5
    
    LOAD (204)
    STORE R6
    
    LOAD (205)
    STORE R7
    
    LOAD (206)
    STORE R8
    
    LOAD (207)
    STORE R9
    
    LOAD (208)
    STORE R10
    
    LOAD (209)
    STORE R11
    
    LOAD (210)
    STORE R12
    
    LOAD (211)
    STORE R13
    
    LOAD #0
    STORE R1
    
    LOAD R8
    STORE R0
    LOAD #0
    STORE R14
MULT0:
    LOAD R0
    JZ NEXT0
    LOAD R14
    ADD R2
    STORE R14
    LOAD R0
    SUB #1
    STORE R0
    JMP MULT0
NEXT0:
    LOAD R1
    ADD R14
    STORE R1
    
    LOAD R9
    STORE R0
    LOAD #0
    STORE R14
MULT1:
    LOAD R0
    JZ NEXT1
    LOAD R14
    ADD R3
    STORE R14
    LOAD R0
    SUB #1
    STORE R0
    JMP MULT1
NEXT1:
    LOAD R1
    ADD R14
    STORE R1
    
    LOAD R10
    STORE R0
    LOAD #0
    STORE R14
MULT2:
    LOAD R0
    JZ NEXT2
    LOAD R14
    ADD R4
    STORE R14
    LOAD R0
    SUB #1
    STORE R0
    JMP MULT2
NEXT2:
    LOAD R1
    ADD R14
    STORE R1
    
    LOAD R11
    STORE R0
    LOAD #0
    STORE R14
MULT3:
    LOAD R0
    JZ NEXT3
    LOAD R14
    ADD R5
    STORE R14
    LOAD R0
    SUB #1
    STORE R0
    JMP MULT3
NEXT3:
    LOAD R1
    ADD R14
    STORE R1
    
    LOAD R12
    STORE R0
    LOAD #0
    STORE R14
MULT4:
    LOAD R0
    JZ NEXT4
    LOAD R14
    ADD R6
    STORE R14
    LOAD R0
    SUB #1
    STORE R0
    JMP MULT4
NEXT4:
    LOAD R1
    ADD R14
    STORE R1
    
    LOAD R13
    STORE R0
    LOAD #0
    STORE R14
MULT5:
    LOAD R0
    JZ NEXT5
    LOAD R14
    ADD R7
    STORE R14
    LOAD R0
    SUB #1
    STORE R0
    JMP MULT5
NEXT5:
    LOAD R1
    ADD R14
    STORE R1
    
    LOAD R1
    STORE 100
    HALT
