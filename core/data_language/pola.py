# from data_language import tataBahasa as tb
# from data_language import grammar
from data_language.tokens import tokenType

POLA_BIKIN_VARIABEL = [tokenType.T_BKIN, tokenType.T_VRBL]
POLA_BIKIN_FUNGSI = [tokenType.T_BKIN, tokenType.T_FGSI]
# POLA_PANGGIL_FUNGSI = [tokenType.T_FGSI, tokenType.T_IDTF]
POLA_ENTRY_POINT = [tokenType.T_FGSI, tokenType.T_IDTF]
POLA_PANGGIL_FUNGSI = [tokenType.T_IDTF, tokenType.T_PRTS_KIRI]
POLA_KALAU_BRANCH = [tokenType.T_KLAU, tokenType.T_PRTS_KIRI]