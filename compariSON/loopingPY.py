import time

total = 0
i = 1

print("Mulai perulangan 100 juta...")

start = time.time()

while i <= 100000000:
    total += 1

    if i % 20000000 == 0:
        print(f"iterasi ke: {i}")

    i += 1

end = time.time()

print(f"\n[Python] Waktu eksekusi: {end - start:.6f} detik")
print(f"Hasil total: {total}")