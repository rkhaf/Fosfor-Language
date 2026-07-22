import data_language.tataBahasa

class errorFormat:
    def __init__(self, p_baris:int, p_kolom:int, p_kelas:str, p_token:str, p_kodeError:int):
        self.baris : int = p_baris
        self.kolom : int = p_kolom
        self.kelas : str = p_kelas
        self.token : str = p_token
        self.kodeError : int = p_kodeError

class errorHandlerClass:
    def __init__(self) -> None:
        self.errors : list[errorFormat] = []
        self.panjangGarisHeader : int = 100
        
        self.errorTerdaftar : dict[str, dict[int, str]] = {
            data_language.tataBahasa.MODUL_PATH_TOKN : {
                1 : ""
            },
            data_language.tataBahasa.MODUL_PATH_LEXR : {
                1 : "input invalid, masa iya float ngisinya gitu"
            },
            data_language.tataBahasa.MODUL_PATH_PRSR : {
                1 : "nama variabelnya isiin dulu njr, kalo kosong gabisa dipanggil ntar"
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
    
    def kirimError(self, baris:int, kolom:int, kelas:str, token:str, kodeError:int) -> str:
        self.errorHeader()
        # baris+=1
        # kolom+=1
        pesanTemplate : str = "ada error dibaris: "+str(baris)+", kolom: "+str(kolom)+", dibagian: -> "+token+" <-'. erornya krna:"
        pesanError : str = ""

        getKelasError : dict[int, str] = self.errorTerdaftar.get(kelas, {})
        if(len(getKelasError)!=0):
            getPesanError : str = getKelasError.get(kodeError, "ERROR")
            
            # pesanError
            pesanError+=getPesanError
            
            return pesanTemplate+"\n"+pesanError
        else:
            # raise Exception("[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(baris)+str(kolom)+str(kelas))
            return "[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(baris)+", "+str(kolom)+", "+str(kelas)+", "+str(kodeError)

    def tambahinError(self, p_baris:int, p_kolom:int, p_kelas:str, p_token:str, p_kodeError:int)->None:
        self.errors.append(errorFormat(p_baris, p_kolom, p_kelas, p_token, p_kodeError))
        
    def displayError(self)->None:
        self.errorHeader()
        
        if(len(self.errors)>0):
            for eror in self.errors:
                pesanTemplate : str = "ada error dibaris: "+str(eror.baris)+", kolom: "+str(eror.kolom)+", dibagian: -> "+eror.token+" <-'. erornya krna:"
                pesanError : str = ""
                getKelasError : dict[int, str] = self.errorTerdaftar.get(eror.kelas, {})
                if(len(getKelasError)!=0):
                    getPesanError : str = getKelasError.get(eror.kodeError, "ERROR")
                    
                    # pesanError
                    pesanError+=getPesanError
                    
                    # return pesanTemplate+"\n"+pesanError
                    raise Exception(pesanTemplate+"\n"+pesanError)
                else:
                    raise Exception("[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(eror.baris)+str(eror.kolom)+str(eror.kelas))