# from data_language import tataBahasa as tb
# from data_language import grammar
from data_language.tokens import tokenType

POLA_BIKIN_VARIABEL : list[tokenType] = [tokenType.T_BKIN, tokenType.T_VRBL]
POLA_BIKIN_FUNGSI : list[tokenType] = [tokenType.T_BKIN, tokenType.T_FGSI]
# POLA_PANGGIL_FUNGSI = [tokenType.T_FGSI, tokenType.T_IDTF]
POLA_ENTRY_POINT : list[tokenType] = [tokenType.T_FGSI, tokenType.T_IDTF]
POLA_PANGGIL_FUNGSI : list[tokenType] = [tokenType.T_IDTF, tokenType.T_PRTS_KIRI]
# POLA_KALAU_BRANCH = [tokenType.T_KLAU, tokenType.T_PRTS_KIRI]
POLA_PERULANGAN_SELAMA : list[tokenType] = [tokenType.T_NGLG, tokenType.T_SLMA]
POLA_IMPOR_MODUL : list[tokenType] = [tokenType.T_IMPR, tokenType.T_MDUL]