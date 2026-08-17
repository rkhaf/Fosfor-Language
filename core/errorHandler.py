from __future__ import annotations
# import grammar.
from collections import defaultdict
from data_language import grammar

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
        self.errors : dict[int, set[errorFormat]] = {}
        # self.multilineErrors : dict[int, set[errorFormat]] = {}
        self.multilineErrors : defaultdict[tuple[str, str, int], list[tuple[int, int]]] = defaultdict(list)

        self.panjangGarisHeader : int = 100
        
        self.errorTerdaftar : dict[str, dict[int, str]] = {
            grammar.MODUL_PATH_TOKN : {
                1 : ""
            },
            grammar.MODUL_PATH_LEXR : {
                1 : "   input invalid, masa iya float ngisinya gitu",
                2 : "   stringnya blm ditutup",
                3 : "   commentnya blm ditutup"
            },
            grammar.MODUL_PATH_PRSR : {
                1 : "nama variabelnya isiin dulu tu, kalo kosong gabisa dipanggil nntinya",
                2 : "namanya 1 aja jgn boros boros",
                3 : "tolong ngisinya jangan dari keyword, berisi simbol, diawalin numerik, ataupun berbentuk string",
                4 : "keywordnya ngeduplikat",
                5 : "tipedatanya gk bener",
                6 : "tipedatanya ngeduplikat",
                7 : "ada yg nyasar, tolong cek lagi",
                8 : "parameternya invalid",
                9 : "kyknya fungsinya blm ditutup make ';' ",
                10 : "kyknya variabelnya blm ditutup make ';' ",
                11 : "klo mau ngisi value pake assignment '='",
                12 : "ekspresinya invalid",
                13 : "operand kanan invalid",
                14 : "kodenya invalid sih itu,selain impor sma deklarasi fungsi pastiin kodenya didalem fungsi yh",
                # 14 : "ngodonf nya didlm fungsi loh yh, jgn ditaroh diluar gtu",
                15 : "kodenya gaada entry point, nambahin fungsi main dulu sana",
                16 : "ekspresinya harap dikurung pke parantesis yh",
                17 : "kodenya invalid twin, cona cek lagi ada yg salah apa egk",
                18 : "inkrementalnya invalid, harap cek lgi",
                19 : "kyknya statementnya blm ditutup make ';' ",
                20 : "'kalau misal' tu bergantung sma 'kalau', jdi 'bikin' nya dibikin dulu coba",
            },
            grammar.MODUL_PATH_SMTK : {
                1 : "variabelnya ga ketemu, coba cek lagi udh dibikin apa blom",
                2 : "value yg dimasukin utk variabel tsb gacocok tipedatanya, coba cek lagi dh",
                3 : "operasi biner tpi tipedatanya gasama",
                4 : "parameter utk fungsi tsb inputnya kebanyakan, tolong sesuaiin lagi dh",
                5 : "variabel tsb tipedatanya gacocok sma parameter fungsi",
                6 : "fungsinya ga ketemu, coba cek lagi udh dibikin apa blom",
                7 : "utk parameter tsb harap langsung isi valuenya, jgn ngecalling variable / fungsi",
                8 : "klo ngisi parameter opsional (param yg punya nilai default) narohnya disebelah kanan parameter wajib, cb benerin lagi ",
                9 : "ada parameter yg harus diisi di fungsi tsb",
                10 : "value tsb tipedatanya gacocok sama parameter fungsi",
                11 : "value dri fungsi tsb tipedatanya gacocok sama parameter fungsi",
                12 : "fungsi tsb gak ngereturn apa apa (bertipedata void)",
                13 : "variabel tsb tipedatanya invalid",
                14 : "namanya udh kepake, ganti pke nama lain",
                15 : "value yg direturn ga sesuai sma tipedata fungsinya",
                16 : "fungsi tsb tipenya void, hrusnya ga ngebalikin apa apa",
                17 : "fungsi tsb gak ngereturn apa apa, coba balikin sesuatu di fungsi tsb",
                18 : "return fungsi tsb gak sesuai sama tipedatanya le, cek lg dh",
                19 : "operasi perbandingan tpi tipedatanya gasama",
                20 : "ekspresi kondisinya hrus bernilai boolean",
                21 : "member dalam modul tsb ga ketemu, coba cek ada gak didalem modulnya",
                22 : "modulenya ga ketemu, coba cek udh diimpor apa blm",
                23 : "utk skrg masih belom support nested module",
            },
            grammar.MODUL_PATH_CGEN : {
                1 : "tipedata input utk fungsi builtin tsb blom disupport wkwk"
            }
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
    
    def kirimError(self, p_kelas:str, p_kodeError:int, p_baris:int=-1, p_kolom:int=-1, p_bagian:str="") -> None:
        self.tambahinError(p_kelas, p_kodeError, p_baris, p_kolom, p_bagian)
        self.displayError()
        
    def tambahinError(self, p_kelas:str, p_kodeError:int, p_baris:int=-1, p_kolom:int=-1, p_bagian:str="")->None:
        self.errors.setdefault(p_baris, set()).add(errorFormat(p_baris, p_kolom, p_kelas, p_bagian, p_kodeError))

    def tambahinErrorMultibaris(self, p_kelas:str, p_kodeError:int, p_baris:int=-1, p_kolom:int=-1, p_bagian:str="")->None:
        key_error : tuple[str, str, int] = (p_bagian, p_kelas, p_kodeError)
        
        self.multilineErrors[key_error].append((p_baris, p_kolom))

        
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

        if(len(self.multilineErrors)>0):
            
            for (bagian, kelas, kodeError), posisi in self.multilineErrors.items():
                print(f"ada error utk identifier -> {bagian} <- yang ada diposisi:")
                listBaris : list[int] = []
                for baris, kolom in posisi:
                    # if(kolom!=-1):
                    listBaris.append(baris)
                    # print(f"    baris: {baris} kolom: {kolom}")
                    # else:
                    #     print(f"    baris: {baris}")
                        
                
                print(f"    baris: {listBaris}")
                # print("ada error krna:")
                getKelasError : dict[int, str] = self.errorTerdaftar.get(kelas, {})
                if(len(getKelasError)!=0):
                    getPesanError : str = getKelasError.get(kodeError, "ERROR")
                    
                    print("errornya krna:",getPesanError)
                    print("\n")
        pass
    
    def adaError(self)->bool:
        return len(self.errors)>0 or len(self.multilineErrors)>0