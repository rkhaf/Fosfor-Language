from typing import NamedTuple

class Token(NamedTuple):
    baris:int
    kolom:int
    tipe:str
    nilai:str