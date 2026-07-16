class errorHandlerClass:
    def __init__(self) -> None:
        
        self.errorTerdaftar : dict[str, dict[int, str]] = {
            "tokenizer" : {
                1 : ""
            },
            "lekser" : {
                1 : "input invalid, masa iya float ngisinya gitu"
            },
        }
    
    def kirimError(self, baris:int, kolom:int, kelas:str, token:str, kodeError:int) -> str:
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
            return "[ErrorHandlerClass] : errorcodenya gak sesuai, harap cek lagi pls"
