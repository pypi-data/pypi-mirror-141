import os
import time
pid = os.getpid()
for i in range(20):
    print(pid, i)
    time.sleep(1)