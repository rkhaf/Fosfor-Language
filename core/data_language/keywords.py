import data_language.tataBahasa as tataBahasa

keywordList : dict[str, str] = {
    tataBahasa.KEYWORD_BKIN : "T_BKIN",
    tataBahasa.KEYWORD_VRBL : "T_VRBL",
    tataBahasa.KEYWORD_NMNY : "T_NMNY",
    tataBahasa.KEYWORD_TPNY : "T_TPNY",
    tataBahasa.KEYWORD_NLNY : "T_NLNY",
    tataBahasa.KEYWORD_DLMR : "T_DLMR",
}

literalList : dict[str, str] = {
    tataBahasa.KEYWORD_BOOL_TRUE : tataBahasa.T_LITERAL_BOOL,
    tataBahasa.KEYWORD_BOOL_FALSE : tataBahasa.T_LITERAL_BOOL,
    # tataBahasa.T_LITERAL_FLOAT : tataBahasa.T_LITERAL_FLOAT,
    # tataBahasa.T_LITERAL_INT : tataBahasa.T_LITERAL_INT,
    # tataBahasa.T_LITERAL_STR : tataBahasa.T_LITERAL_STR,
}

primitiveList : dict[str, str] = {
    tataBahasa.TIPEDATA_INT : tataBahasa.T_TIPE_INT,
    tataBahasa.TIPEDATA_FLOAT : tataBahasa.T_TIPE_FLT,
    tataBahasa.TIPEDATA_STR : tataBahasa.T_TIPE_STR,
    tataBahasa.TIPEDATA_BOOL : tataBahasa.T_TIPE_BOOL,
}

operatorList : dict[str, str] = {
    tataBahasa.OPERATOR_DIVE : "T_DIVE",
    tataBahasa.OPERATOR_MDLO : "T_MDLO",
    tataBahasa.OPERATOR_MINS : "T_MINS",
    tataBahasa.OPERATOR_MULT : "T_MULT",
    tataBahasa.OPERATOR_PLUS : "T_PLUS",
}

simbolList : set[str] = {
    tataBahasa.OPERATOR_PLUS,
    tataBahasa.OPERATOR_MINS,
    tataBahasa.OPERATOR_DIVE,
    tataBahasa.OPERATOR_MULT,
    tataBahasa.OPERATOR_MDLO,
    tataBahasa.KEYWORD_DLMR
}