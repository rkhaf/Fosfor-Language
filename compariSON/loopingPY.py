import time

def main():
    start = time.perf_counter()
    
    i = 0
    total = 0
    
    # Loop 100 Juta Kali
    while i < 100_000_000:
        total = total + i
        i = i + 1
        
    end = time.perf_counter()
    
    print(f"Hasil Total : {total}")
    print(f"Waktu Python: {end - start:.4f} detik")

if __name__ == "__main__":
    main()