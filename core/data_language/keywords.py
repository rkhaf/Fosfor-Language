import data_language.tataBahasa as tataBahasa

keywordList : dict[str, str] = {
    tataBahasa.KEYWORD_BKIN : tataBahasa.T_BKIN,
    tataBahasa.KEYWORD_VRBL : tataBahasa.T_VRBL,
    tataBahasa.KEYWORD_NMNY : tataBahasa.T_NMNY,
    tataBahasa.KEYWORD_TPNY : tataBahasa.T_TPNY,    
    tataBahasa.KEYWORD_NLNY : tataBahasa.T_NLNY,
    tataBahasa.KEYWORD_DLMR : tataBahasa.T_DLMR,
    tataBahasa.SYMBOL_PRTS_KIRI : tataBahasa.T_PRTS_KIRI,
    tataBahasa.SYMBOL_PRTS_KNAN : tataBahasa.T_PRTS_KNAN,
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
}

simbolList : dict[str, str] = {
    # tataBahasa.SYMBOL_PRTS_KNAN : tataBahasa.T_SYMBOL_,
    # tataBahasa.SYMBOL_PRTS_KIRI : tataBahasa.T_SYMBOL_,
    tataBahasa.SYMBOL_SERU : tataBahasa.T_SYMBOL_SERU,
    tataBahasa.SYMBOL_AT : tataBahasa.T_SYMBOL_AT,
    tataBahasa.SYMBOL_HSTG : tataBahasa.SYMBOL_HSTG,
    tataBahasa.SYMBOL_DLLR : tataBahasa.SYMBOL_DLLR,
    tataBahasa.SYMBOL_CRET : tataBahasa.SYMBOL_CRET,
    tataBahasa.SYMBOL_AMPD : tataBahasa.SYMBOL_AMPD,
    tataBahasa.SYMBOL_TKMA : tataBahasa.SYMBOL_TKMA,
    tataBahasa.SYMBOL_TKWA : tataBahasa.SYMBOL_TKWA,
    tataBahasa.SYMBOL_TNYA : tataBahasa.SYMBOL_TNYA,
    tataBahasa.SYMBOL_KCIL : tataBahasa.SYMBOL_KCIL,
    tataBahasa.SYMBOL_BSAR : tataBahasa.SYMBOL_BSAR,
    tataBahasa.SYMBOL_SMDG : tataBahasa.SYMBOL_SMDG,
    tataBahasa.SYMBOL_GRLR : tataBahasa.SYMBOL_GRLR,
}

# simbolList : set[str] = {
#     # tataBahasa.OPERATOR_PLUS,
#     # tataBahasa.OPERATOR_MINS,
#     # tataBahasa.OPERATOR_DIVE,
#     # tataBahasa.OPERATOR_MULT,
#     # tataBahasa.OPERATOR_MDLO,
#     # tataBahasa.KEYWORD_DLMR,
#     tataBahasa.SYMBOL_PRTS_KIRI,
#     tataBahasa.SYMBOL_PRTS_KNAN,
#     tataBahasa.SYMBOL_SERU,
#     tataBahasa.SYMBOL_AT,
#     tataBahasa.SYMBOL_HSTG,
#     tataBahasa.SYMBOL_DLLR,
#     tataBahasa.SYMBOL_CRET,
#     tataBahasa.SYMBOL_AMPD,
#     tataBahasa.SYMBOL_TKMA,
#     tataBahasa.SYMBOL_TKWA,
#     tataBahasa.SYMBOL_TNYA,
#     tataBahasa.SYMBOL_KCIL,
#     tataBahasa.SYMBOL_BSAR,
#     tataBahasa.SYMBOL_SMDG,
#     tataBahasa.SYMBOL_GRLR,
# }