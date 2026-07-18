import data_language.tataBahasa

class errorHandlerClass:
    def __init__(self) -> None:
        self.panjangGarisHeader : int = 100
        
        self.errorTerdaftar : dict[str, dict[int, str]] = {
            data_language.tataBahasa.MODUL_PATH_TOKN : {
                1 : ""
            },
            data_language.tataBahasa.MODUL_PATH_LEXR : {
                1 : "input invalid, masa iya float ngisinya gitu"
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
        baris+=1
        kolom+=1
        pesanTemplate : str = "ada error dibaris: "+str(baris)+", kolom: "+str(kolom)+", dibagian: -> "+token+" <-'. erornya krna:"
        pesanError : str = ""

        getKelasError : dict[int, str] = self.errorTerdaftar.get(kelas, {})
        if(len(getKelasError)!=0):
            getPesanError : str = getKelasError.get(kodeError, "ERROR")
            
            # pesanError
            pesanError+=getPesanError
            
            return pesanTemplate+"\n"+pesanError
        else:
            return "[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls "+str(baris)+str(kolom)+str(kelas)
