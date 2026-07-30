from errorHandler import errorHandlerClass
from modul_parsing.AST import ASTClass

class semantikClass:
    def __init__(self, p_errorHandlerRef : errorHandlerClass) -> None:
        self.errorHandlerObjek = p_errorHandlerRef
        pass

    def proses(self, p_tree : ASTClass)->None:
        p_tree.printTree()
        print("printed")
        pass