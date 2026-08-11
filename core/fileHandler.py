import config
from prosesor import run
from pathlib import Path

def readPath(p_path : str) -> None:
    namaBersih : str = ""
    if('"' in p_path):
        p_path = str(p_path).replace('"',"")
        
    namaBersih = Path(p_path).stem
        
    try:
        with open(p_path, "r") as fileOriginal:
            if(config.SYS_FILE_FORMAT in p_path):
                run(fileOriginal.read(), namaBersih)
                
            else:
                print("format file gak sesuai")

    except FileNotFoundError:
        print(f"file gak ketemu ({p_path}) ({namaBersih})")