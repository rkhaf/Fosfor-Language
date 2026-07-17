import data_language.tataBahasa as tataBahasa

keywordList : dict[str, str] = {
    tataBahasa.KEYWORD_BKIN : "T_BKIN",
    tataBahasa.KEYWORD_VRBL : "T_VRBL",
    tataBahasa.KEYWORD_NMNY : "T_NMNY",
    tataBahasa.KEYWORD_TPNY : "T_TPNY",
    tataBahasa.KEYWORD_NLNY : "T_NLNY",
    tataBahasa.KEYWORD_SYS_DLMR : "T_DLMR",
    
}

primitiveList : dict[str, str] = {
    tataBahasa.TIPEDATA_INT : "PRIM_INT",
    tataBahasa.TIPEDATA_FLOAT : "PRIM_FLT",
    tataBahasa.TIPEDATA_STR : "PRIM_STR",
    tataBahasa.TIPEDATA_BOOL : "PRIM_BOOL",
}