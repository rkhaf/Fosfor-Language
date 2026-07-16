import config
from prosesor import run

def readPath(p_path : str) -> None:
    
    if('"' in p_path):
        p_path = str(p_path).replace('"',"")
        
    try:
        with open(p_path, "r") as fileOriginal:
            if(config.formatFile in p_path):
                run(fileOriginal.read())
                
            else:
                print("format file gak sesuai")

    except FileNotFoundError:
        print("gak nemu")