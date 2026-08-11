from pathlib import Path
import sys

SYS_FILE_FORMAT : str = "fos"


# def getBaseDir()->Path:
        
#     if("__compiled__" in globals()):
#         return Path(sys.argv[0]).resolve.parent
    
#     elif(getattr(sys, "frozen", False)):
#         return Path(sys.executable).resolve.parent
    
#     else:
#         return Path(__name__).resolve()

coreDir : Path = Path(__file__).resolve().parent
path_runtimeCPP  = coreDir / "runtime" / "runtime.o"
pass