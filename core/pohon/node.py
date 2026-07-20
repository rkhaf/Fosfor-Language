from llvmFolder.library import LLVM_PRIMITIVE_TYPES

class nodeClass:
    """
    node sepuh yg jadi tumpuan seluruh node
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        self.baris : int = p_baris
        self.kolom : int = p_kolom
        pass

class nodeEkspresi(nodeClass):
    """
    nodeParent buat node yg bisa ngereturn di kodenya
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        super().__init__(p_baris, p_kolom)
        pass

class nodeStatement(nodeClass):
    """
    nodeParent buat node yg gak return apa2 di kodenya
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        super().__init__(p_baris, p_kolom)
        pass

class nodeBlock(nodeStatement):
    """
    node container utk contain node
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaVariabel : str, p_tipedataVariabel : str)->None:
        super().__init__(p_baris, p_kolom)
        self.isiBlock : list[nodeClass] = []

class nodeBikinVariabel(nodeStatement):
    """
    node representasi utk bikin variabel
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaVariabel : str, p_tipedataVariabel : str)->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaVariabel : str = ""
        self.tipedataVariabel : str = ""
        self.nilaiVariabel : nodeEkspresi
        

class nodeBikinFungsi(nodeStatement):
    """
    node representasi utk bikin fungsi
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaFungsi : str, p_tipedataFungsi : str)->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaVariabel : str = ""
        self.namaFungsi : str = p_namaFungsi
        self.tipedataFungsi : str = p_tipedataFungsi
        self.isiFungsi : nodeBlock