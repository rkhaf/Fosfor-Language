import data_language.tataBahasa as tataBahasa

keywordList : dict[str, str] = {
    tataBahasa.KEYWORD_BKIN : tataBahasa.T_BKIN,
    tataBahasa.KEYWORD_VRBL : tataBahasa.T_VRBL,
    tataBahasa.KEYWORD_NMNY : tataBahasa.T_NMNY,
    tataBahasa.KEYWORD_TPNY : tataBahasa.T_TPNY,    
    tataBahasa.KEYWORD_NLNY : tataBahasa.T_NLNY,
    tataBahasa.KEYWORD_PTER : tataBahasa.T_PTER,
    tataBahasa.KEYWORD_ALMT : tataBahasa.T_ALMT,
    tataBahasa.KEYWORD_DLMR : tataBahasa.T_DLMR,
    tataBahasa.KEYWORD_ISNY : tataBahasa.T_ISNY,
    tataBahasa.KEYWORD_AKHR : tataBahasa.T_AKHR,
    tataBahasa.KEYWORD_STRK : tataBahasa.T_STRK,
    tataBahasa.KEYWORD_FGSI : tataBahasa.T_FGSI,
    tataBahasa.KEYWORD_VOID : tataBahasa.T_VOID,
    tataBahasa.KEYWORD_RFSI : tataBahasa.T_RFSI,
    tataBahasa.KEYWORD_KLAU : tataBahasa.T_KLAU,
    tataBahasa.KEYWORD_PRSM : tataBahasa.T_PRSM,
    tataBahasa.KEYWORD_SAAT : tataBahasa.T_SAAT,
    tataBahasa.KEYWORD_LNJT : tataBahasa.T_LNJT,
    tataBahasa.KEYWORD_STOP : tataBahasa.T_STOP,
    tataBahasa.KEYWORD_LAIN : tataBahasa.T_LAIN,
    tataBahasa.KEYWORD_PMNY : tataBahasa.T_PMNY,
    tataBahasa.KEYWORD_BLKN : tataBahasa.T_BLKN,
    tataBahasa.KEYWORD_NGGK : tataBahasa.T_NGGK,
    tataBahasa.KEYWORD_NGLG : tataBahasa.T_NGLG,
    tataBahasa.KEYWORD_SLMA : tataBahasa.T_SLMA,
    tataBahasa.KEYWORD_LGKA_ATAU : tataBahasa.T_LGKA_ATAU,
    tataBahasa.KEYWORD_LGKA_DAN : tataBahasa.T_LGKA_DAN,
    tataBahasa.KEYWORD_LGKA_BKAN : tataBahasa.T_LGKA_BKAN
}

literalList : dict[str, str] = {
    tataBahasa.KEYWORD_BOOL_TRUE : tataBahasa.T_LITERAL_BOOL,
    tataBahasa.KEYWORD_BOOL_FALSE : tataBahasa.T_LITERAL_BOOL,
    tataBahasa.T_LITERAL_FLOAT : tataBahasa.T_LITERAL_FLOAT,
    tataBahasa.T_LITERAL_INT : tataBahasa.T_LITERAL_INT,
    tataBahasa.T_LITERAL_STR : tataBahasa.T_LITERAL_STR,
}

primitiveList : dict[str, str] = {
    tataBahasa.TIPEDATA_INT : tataBahasa.T_TIPE_INT,
    tataBahasa.TIPEDATA_FLOAT : tataBahasa.T_TIPE_FLT,
    tataBahasa.TIPEDATA_STR : tataBahasa.T_TIPE_STR,
    tataBahasa.TIPEDATA_BOOL : tataBahasa.T_TIPE_BOOL,
}

operatorList : dict[str, str] = {
    tataBahasa.OPERATOR_DIVE : tataBahasa.T_DIVE,
    tataBahasa.OPERATOR_MDLO : tataBahasa.T_MDLO,
    tataBahasa.OPERATOR_MINS : tataBahasa.T_MINS,
    tataBahasa.OPERATOR_MULT : tataBahasa.T_MULT,
    tataBahasa.OPERATOR_PLUS : tataBahasa.T_PLUS,
    tataBahasa.OPERATOR_ICRT : tataBahasa.T_ICRT,
    tataBahasa.OPERATOR_DCRT : tataBahasa.T_DCRT,
    tataBahasa.OPERATOR_SMDG : tataBahasa.T_SMDG
}

simbolList : dict[str, str] = {
    # tataBahasa.SYMBOL_PRTS_KNAN : tataBahasa.T_SYMBOL_,
    # tataBahasa.SYMBOL_PRTS_KIRI : tataBahasa.T_SYMBOL_,
    tataBahasa.SYMBOL_SERU : tataBahasa.T_SYMBOL_SERU,
    tataBahasa.SYMBOL_AT : tataBahasa.T_SYMBOL_AT,
    tataBahasa.SYMBOL_HSTG : tataBahasa.T_SYMBOL_HSTG,
    tataBahasa.SYMBOL_DLLR : tataBahasa.T_SYMBOL_DLLR,
    tataBahasa.SYMBOL_CRET : tataBahasa.T_SYMBOL_CRET,
    tataBahasa.SYMBOL_AMPD : tataBahasa.T_SYMBOL_AMPD,
    # tataBahasa.SYMBOL_TKMA : tataBahasa.SYMBOL_TKMA,
    tataBahasa.SYMBOL_TNYA : tataBahasa.T_SYMBOL_TNYA,
    # tataBahasa.SYMBOL_KCIL : tataBahasa.T_SYMBOL_KCIL,
    # tataBahasa.SYMBOL_BSAR : tataBahasa.T_SYMBOL_BSAR,
    tataBahasa.SYMBOL_GRLR : tataBahasa.T_SYMBOL_GRLR,
}

kurungList : dict[str, str] = {
    tataBahasa.SYMBOL_BRKT_KIRI : tataBahasa.T_SYMBOL_BRKT_KIRI,
    tataBahasa.SYMBOL_BRKT_KNAN : tataBahasa.T_SYMBOL_BRKT_KNAN,
    tataBahasa.SYMBOL_PRTS_KIRI : tataBahasa.T_PRTS_KIRI,
    tataBahasa.SYMBOL_PRTS_KNAN : tataBahasa.T_PRTS_KNAN,
}

punctuationList : dict[str, str] = {
    tataBahasa.SYMBOL_TKWA : tataBahasa.T_SYMBOL_TKWA,
    tataBahasa.SYMBOL_KOMA : tataBahasa.T_SYMBOL_KOMA,
    tataBahasa.SYMBOL_TTIK : tataBahasa.T_SYMBOL_TTIK
}

perbandinganList : dict[str, str] = {
    tataBahasa.CMPR_BSAR : tataBahasa.T_CMPR_BSAR,
    tataBahasa.CMPR_SBSR : tataBahasa.T_CMPR_SBSR,
    tataBahasa.CMPR_KCIL : tataBahasa.T_CMPR_KCIL,
    tataBahasa.CMPR_SKCL : tataBahasa.T_CMPR_SKCL,
    tataBahasa.CMPR_SAMA : tataBahasa.T_CMPR_SAMA,
    tataBahasa.CMPR_GSMA : tataBahasa.T_CMPR_GSMA,
}

# logikaList : dict[str, str] = {
#     tataBahasa.KEYWORD_LGKA_ATAU : tataBahasa.T_LGKA_ATAU,
#     tataBahasa.KEYWORD_LGKA_DAN : tataBahasa.T_LGKA_DAN,
#     tataBahasa.KEYWORD_LGKA_BKAN : tataBahasa.T_LGKA_BKAN
# }