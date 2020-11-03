Terminals = {INSTRUCTION , VALUE , CASES , DECLARER , ID_PARAMETERS , PARAMETERS , DATA , BREAK}

No Terminals = {if , while , foreach , id , in , switch , case , default , break , \, , ; , : , ( , ) , { , } , = , => , boolean , let , const , var , string , number}

S_0 = Instruction

INSTRUCTION     → if (VALUE){INSTRUCTION}  INSTRUCTION
                | while (VALUE){INSTRUCTION}  INSTRUCTION
                | foreach(id in id){INSTRUCTION} INSTRUCTION
                | switch (id){CASES}  INSTRUCTION
                | DECLARER id = COMPLEMENT INSTRUCTION
                | id(PARAMETERS);INSTRUCTION
                | λ

CASES           → case DATA∶INSTRUCTIONS BREAK CASES
                | default:INSTRUCTIONS BREAK CASES
                | λ

BREAK           → break;
                | λ

VALUE           → boolean
                | id

DECLARER        → let
                | const
                | var

ID_PARAMETERS   → id ID_PARAMETERS
                | ,ID_PARAMETERS
                | λ

PARAMETERS      → DATA PARAMETERS
                | ,PARAMETERS
                | λ

DATA            → number
                | boolean
                | string
                | id

COMPLEMENT      → (ID_PARAMETERS)=>{INSTRUCTION}
                | DATA;