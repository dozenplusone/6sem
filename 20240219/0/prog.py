import glob
import sys
import zlib

for p in glob.iglob(sys.argv[1] + "/??/*"):
    with open(p, "rb") as f:
        print('-' * 16, zlib.decompress(f.read()), sep='\n')
