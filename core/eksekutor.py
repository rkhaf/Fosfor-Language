from fileHandler import readPath
import sys

def main()->None:
    if(len(sys.argv)<2):
        print("error bg")
        
    input_file_path = sys.argv[1]
    readPath(input_file_path)
    
if __name__=="__main__":
    # main()
    
    input_file_path = str("main.fos")
    readPath(input_file_path)