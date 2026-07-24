from __future__ import annotations
import data_language.tataBahasa

class errorFormat:
    def __init__(self, p_baris:int=-1, p_kolom:int=-1, p_kelas:str="", p_token:str="", p_kodeError:int=-1):
        self.baris : int = p_baris
        self.kolom : int = p_kolom
        self.kelas : str = p_kelas
        self.bagian : str = p_token
        self.kodeError : int = p_kodeError
    
    def __eq__(self, p_baru : object)->bool:
        if isinstance(p_baru, errorFormat):
            return (self.baris, self.kolom, self.kelas, self.bagian, self.kodeError) == (p_baru.baris, p_baru.kolom, p_baru.kelas, p_baru.bagian, p_baru.kodeError)
        return False
    
    def __hash__(self) -> int:
        return hash((self.baris, self.kolom, self.kelas, self.bagian, self.kodeError))

class errorHandlerClass:
    def __init__(self) -> None:
        # self.errors : list[errorFormat] = []
        # self.errors : list[list[errorFormat]] = []
        self.errors : dict[int, list[errorFormat]] = {}
        # self.errors : set[errorFormat] = set()
        self.panjangGarisHeader : int = 100
        
        self.errorTerdaftar : dict[str, dict[int, str]] = {
            data_language.tataBahasa.MODUL_PATH_TOKN : {
                1 : ""
            },
            data_language.tataBahasa.MODUL_PATH_LEXR : {
                1 : "   input invalid, masa iya float ngisinya gitu"
            },
            data_language.tataBahasa.MODUL_PATH_PRSR : {
                1 : "nama variabelnya isiin dulu tu, kalo kosong gabisa dipanggil nntinya",
                2 : "namanya 1 aja jgn boros boros",
                3 : "tolong ngisi namanya jangan dari keyword, berisi simbol, diawalin numerik, ataupun berbentuk string",
                4 : "keywordnya ngeduplikat",
            },
        }
    
    def errorHeader(self)->None:
        msg : str = ""
        teksTengah : str = "ADA ERROR"
        for i in range(self.panjangGarisHeader):
            if(i<self.panjangGarisHeader/2 - int(len(teksTengah)/2)):
                msg+=" "
            elif(i==self.panjangGarisHeader/2 - int(len(teksTengah)/2)):
                msg+=teksTengah
                
        print("*"*self.panjangGarisHeader)
        print(msg)
        print("*"*self.panjangGarisHeader)
        # print("\n")
    
    def kirimError(self, p_kelas:str, p_kodeError:int, p_baris:int=-1, p_kolom:int=-1, p_bagian:str="") -> None:
        self.tambahinError(p_kelas, p_kodeError, p_baris, p_kolom, p_bagian)
        self.displayError()
        # self.errorHeader()
        # # baris+=1
        # # kolom+=1
        # pesanTemplate : str = "ada error dibaris: "+str(p_baris)+", kolom: "+str(p_kolom)+", dibagian: -> "+p_bagian+" <-'. erornya krna:"
        # pesanError : str = ""

        # getKelasError : dict[int, str] = self.errorTerdaftar.get(kelas, {})
        # if(len(getKelasError)!=0):
        #     getPesanError : str = getKelasError.get(kodeError, "ERROR")
            
        #     # pesanError
        #     pesanError+=getPesanError
            
        #     return pesanTemplate+"\n"+pesanError
        # else:
        #     # raise Exception("[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(baris)+str(kolom)+str(kelas))
        #     return "[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(baris)+", "+str(kolom)+", "+str(kelas)+", "+str(kodeError)

    def tambahinError(self, p_kelas:str, p_kodeError:int, p_baris:int=-1, p_kolom:int=-1, p_bagian:str="")->None:
        # if(not p_baris in self.errors.keys())
        # self.errors[p_baris].append(errorFormat(p_baris, p_kolom, p_kelas, p_bagian, p_kodeError))
        self.errors.setdefault(p_baris, []).append(errorFormat(p_baris, p_kolom, p_kelas, p_bagian, p_kodeError))
        pass
        # self.errors.add(errorFormat(p_baris, p_kolom, p_kelas, p_bagian, p_kodeError))
        
    def displayError(self)->None:
        self.errorHeader()
        
        if(len(self.errors)>0):
            for baris, listError in sorted(self.errors.items()):
                print("ada error dibaris: "+str(baris)+", erornya krna:")
                for eror in listError:
                    pesanTemplate : str = ""
                    pesanError : str = ""
                    getKelasError : dict[int, str] = self.errorTerdaftar.get(eror.kelas, {})
                    
                    # if(eror.baris!=-1):
                    #     pesanTemplate+= "ada error dibaris: "+str(eror.baris)+" "
                        
                    if(eror.kolom!=-1):
                        pesanTemplate+= "kolom: "+str(eror.kolom)+" "
                    
                    if(len(eror.bagian)>0):
                        pesanTemplate+= "dibagian: -> "+eror.bagian+" <-'"
                        
                    # pesanTemplate+= "erornya krna:"
                    
                    if(len(getKelasError)!=0):
                        getPesanError : str = getKelasError.get(eror.kodeError, "ERROR")
                        
                        # pesanError
                        if(len(pesanTemplate)>0):
                            pesanError+="\n"+getPesanError
                        else:
                            pesanError+=getPesanError
                        
                        # return pesanTemplate+"\n"+pesanError
                        print(" - ",pesanTemplate+pesanError)
                        # raise Exception(pesanTemplate+"\n"+pesanError)
                    else:
                        raise Exception("[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(eror.baris)+str(eror.kolom)+str(eror.kelas))
                print("\n")
        pass
    def adaError(self)->bool:
        return len(self.errors)>0