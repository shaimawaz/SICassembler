SUM      START   2000
FIRST    LDX     LOOP              LOAD X REGISTER WITH 0
         LDA     LOOP              LOAD ACCUMULATOR WITH 0
         LDA     =C'EOFHYT'
         LTORG
LOOP     ADD     TABLE
         ADD     TABLE2, X
         TIX     COUNT
         JLT     LOOP
         RSUB                      RETURN TO CALLER
         RSUB                      RETURN TO CALLER
         LDA     =C'EOFHYT'
         LDA     =X'0512'
. This is a comment
.
         LTORG
         LDA     =C'EOFJH'
         LDA     =X'0512'
         LDA     =X'0512'
NUM2     WORD    X'7x75'
CHAR     WORD    C'FFF'
CHA      WORD    -1
CH       BYTE    X'323'
COUNT    RESB    1
TABLE    RESW    200               2000-WORD TABLE AREA
TABLE2   RESW    2000              2000-WORD TABLE2 AREA
TOTAL    RESW    1
         END     FIRST
         