import subprocess
import time

# Ukur runtime main.exe
start_run = time.perf_counter()

# Jalankan executable-nya langsung lewat Python
subprocess.run(["./main.exe"]) 

end_run = time.perf_counter()

print(f"\n[Runtime Execution]: {(end_run - start_run) * 1000:.2f} ms")