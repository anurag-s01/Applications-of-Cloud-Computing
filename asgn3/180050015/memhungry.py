
import time
f = open("./data.dat", "rb")
data = ""

i = 0
for i in range(200):
    data += str(f.read(1000000))
    i += 1
    print(i)
    
