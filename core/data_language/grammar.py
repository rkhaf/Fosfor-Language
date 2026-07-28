from data_language.tokens import tokenType

MODUL_PATH_LEXR : str = "modul_baca.lekser"
MODUL_PATH_TOKN : str = "modul_baca.tokenizer"
MODUL_PATH_PRSR : str = "modul_parsing.parser"

SYS_ERR : str = "ERROR"

TIPEDATA_INT : str = "integer"
TIPEDATA_FLOAT : str = "float"
TIPEDATA_BOOL : str = "boolean"
TIPEDATA_STR : str = "string"

OPERATOR_PLUS : str = "+"
OPERATOR_MINS : str = "-"
OPERATOR_DIVE : str = "/"
OPERATOR_MULT : str = "*"
OPERATOR_MDLO : str = "%"
OPERATOR_ICRT : str = "++"
OPERATOR_DCRT : str = "--"
OPERATOR_SMDG : str = "="

CMPR_KCIL : str = "<"
CMPR_BSAR : str = ">"
CMPR_SBSR : str = ">="
CMPR_SKCL : str = "<="
CMPR_SAMA : str = "=="
CMPR_GSMA : str = "!="

CMNT_SNGL : str = "//"
CMNT_MLTI_OPEN : str = "/*"
CMNT_MLTI_CLSD : str = "*/"

SYMBOL_PRTS_KIRI : str = "("
SYMBOL_PRTS_KNAN : str = ")"

SYMBOL_KRWL_KIRI : str = "{"
SYMBOL_KRWL_KNAN : str = "}"

SYMBOL_BRKT_KIRI : str = "["
SYMBOL_BRKT_KNAN : str = "]"

SYMBOL_SERU : str = "!"
SYMBOL_AT : str = "@"
SYMBOL_HSTG : str = "#"
SYMBOL_DLLR : str = "$"
SYMBOL_CRET : str = "^"
SYMBOL_AMPD : str = "&"
SYMBOL_TKMA : str = ";"
SYMBOL_TKWA : str = ":"
SYMBOL_TNYA : str = "?"
SYMBOL_GRLR : str = "|"
SYMBOL_KOMA : str = ","
SYMBOL_TTIK : str = "."

KEYWORD_BOOL_TRUE : str = "benar"
KEYWORD_BOOL_FALSE : str = "salah"

KEYWORD_BKIN : str = "bikin"
KEYWORD_VRBL : str = "variabel"
KEYWORD_NMNY : str = "namanya"
KEYWORD_TPNY : str = "tipenya"
KEYWORD_NLNY : str = "nilainya"
KEYWORD_PNTR : str = "pointer"
KEYWORD_ALMT : str = "alamatnya"
KEYWORD_PTER : str = "pointer"
KEYWORD_AKHR : str = "akhir"
KEYWORD_ISNY : str = "isinya"
KEYWORD_STRK : str = "struktur"
KEYWORD_FGSI : str = "fungsi"
KEYWORD_VOID : str = "void"
KEYWORD_RFSI : str = "referensi"
KEYWORD_KLAU : str = "kalau"
KEYWORD_PRSM : str = "persamaan"
KEYWORD_SAAT : str = "saat"
KEYWORD_STOP : str = "stop"
KEYWORD_LNJT : str = "lanjut"
KEYWORD_LAIN : str = "lain"
KEYWORD_PMNY : str = "parameternya"
KEYWORD_BLKN : str = "balikin"
KEYWORD_NGGK : str = "nggak"
KEYWORD_NGLG : str = "ngulangin"
KEYWORD_SLMA : str = "selama"
KEYWORD_DLMR : str = ";"

KEYWORD_LGKA_BKAN : str = "bukan"
KEYWORD_LGKA_ATAU : str = "atau"
KEYWORD_LGKA_DAN : str = "dan"

T_LITERAL_INT : str = "T_LTRL_INT"
T_LITERAL_FLOAT : str = "T_LTRL_FLOAT"
T_LITERAL_BOOL : str = "T_LTRL_BOOL"
T_LITERAL_STR : str = "T_LTRL_STR"

T_IVTF : str = "T_IVTF"

keywordList : dict[str, tokenType] = {
    KEYWORD_BKIN : tokenType.T_BKIN,
    KEYWORD_VRBL : tokenType.T_VRBL,
    KEYWORD_NMNY : tokenType.T_NMNY,
    KEYWORD_TPNY : tokenType.T_TPNY,
    KEYWORD_NLNY : tokenType.T_NLNY,
    KEYWORD_PTER : tokenType.T_PTER,
    KEYWORD_ALMT : tokenType.T_ALMT,
    KEYWORD_DLMR : tokenType.T_DLMR,
    KEYWORD_ISNY : tokenType.T_ISNY,
    KEYWORD_AKHR : tokenType.T_AKHR,
    KEYWORD_STRK : tokenType.T_STRK,
    KEYWORD_FGSI : tokenType.T_FGSI,
    KEYWORD_VOID : tokenType.T_VOID,
    KEYWORD_RFSI : tokenType.T_RFSI,
    KEYWORD_KLAU : tokenType.T_KLAU,
    KEYWORD_PRSM : tokenType.T_PRSM,
    KEYWORD_SAAT : tokenType.T_SAAT,
    KEYWORD_LNJT : tokenType.T_LNJT,
    KEYWORD_STOP : tokenType.T_STOP,
    KEYWORD_LAIN : tokenType.T_LAIN,
    KEYWORD_PMNY : tokenType.T_PMNY,
    KEYWORD_BLKN : tokenType.T_BLKN,
    KEYWORD_NGGK : tokenType.T_NGGK,
    KEYWORD_NGLG : tokenType.T_NGLG,
    KEYWORD_SLMA : tokenType.T_SLMA,
    KEYWORD_LGKA_ATAU : tokenType.T_LGKA_ATAU,
    KEYWORD_LGKA_DAN : tokenType.T_LGKA_DAN,
    KEYWORD_LGKA_BKAN : tokenType.T_LGKA_BKAN
}

literalList : dict[str, tokenType] = {
    KEYWORD_BOOL_TRUE : tokenType.T_LITERAL_BOOL,
    KEYWORD_BOOL_FALSE : tokenType.T_LITERAL_BOOL,
    T_LITERAL_FLOAT : tokenType.T_LITERAL_FLOAT,
    T_LITERAL_INT : tokenType.T_LITERAL_INT,
    T_LITERAL_STR : tokenType.T_LITERAL_STR,
}

primitiveList : dict[str, tokenType] = {
    TIPEDATA_INT : tokenType.T_TIPE_INT,
    TIPEDATA_FLOAT : tokenType.T_TIPE_FLT,
    TIPEDATA_STR : tokenType.T_TIPE_STR,
    TIPEDATA_BOOL : tokenType.T_TIPE_BOOL,
}

operatorList : dict[str, tokenType] = {
    OPERATOR_DIVE : tokenType.T_DIVE,
    OPERATOR_MDLO : tokenType.T_MDLO,
    OPERATOR_MINS : tokenType.T_MINS,
    OPERATOR_MULT : tokenType.T_MULT,
    OPERATOR_PLUS : tokenType.T_PLUS,
    OPERATOR_ICRT : tokenType.T_ICRT,
    OPERATOR_DCRT : tokenType.T_DCRT,
    OPERATOR_SMDG : tokenType.T_SMDG
}

simbolList : dict[str, tokenType] = {
    # SYMBOL_PRTS_KNAN : T_SYMBOL_,
    # SYMBOL_PRTS_KIRI : T_SYMBOL_,
    SYMBOL_SERU : tokenType.T_SYMBOL_SERU,
    SYMBOL_AT : tokenType.T_SYMBOL_AT,
    SYMBOL_HSTG : tokenType.T_SYMBOL_HSTG,
    SYMBOL_DLLR : tokenType.T_SYMBOL_DLLR,
    SYMBOL_CRET : tokenType.T_SYMBOL_CRET,
    SYMBOL_AMPD : tokenType.T_SYMBOL_AMPD,
    # SYMBOL_TKMA : SYMBOL_TKMA,
    SYMBOL_TNYA : tokenType.T_SYMBOL_TNYA,
    # SYMBOL_KCIL : T_SYMBOL_KCIL,
    # SYMBOL_BSAR : T_SYMBOL_BSAR,
    SYMBOL_GRLR : tokenType.T_SYMBOL_GRLR,
}

kurungList : dict[str, tokenType] = {
    SYMBOL_BRKT_KIRI : tokenType.T_SYMBOL_BRKT_KIRI,
    SYMBOL_BRKT_KNAN : tokenType.T_SYMBOL_BRKT_KNAN,
    SYMBOL_PRTS_KIRI : tokenType.T_PRTS_KIRI,
    SYMBOL_PRTS_KNAN : tokenType.T_PRTS_KNAN,
}

punctuationList : dict[str, tokenType] = {
    SYMBOL_TKWA : tokenType.T_SYMBOL_TKWA,
    SYMBOL_KOMA : tokenType.T_SYMBOL_KOMA,
    SYMBOL_TTIK : tokenType.T_SYMBOL_TTIK
}

perbandinganList : dict[str, tokenType] = {
    CMPR_BSAR : tokenType.T_CMPR_BSAR,
    CMPR_SBSR : tokenType.T_CMPR_SBSR,
    CMPR_KCIL : tokenType.T_CMPR_KCIL,
    CMPR_SKCL : tokenType.T_CMPR_SKCL,
    CMPR_SAMA : tokenType.T_CMPR_SAMA,
    CMPR_GSMA : tokenType.T_CMPR_GSMA,
}