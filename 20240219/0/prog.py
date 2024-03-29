import glob
import sys
import zlib

for p in glob.iglob(sys.argv[1] + "/??/*"):
    with open(p, "rb") as f:
        obj = zlib.decompress(f.read())
    _typesize, _, obj = obj.partition(b'\x00')
    _type, size = _typesize.split()
    match _type:
        case b"commit":
            print("--- C O M M I T ---")
            print(obj.decode().rstrip())
        case b"tree":
            print("--- T R E E ---")
            namesize, _, obj = obj.partition(b'\x00')
            sha, obj = obj[:20], obj[20:]
            print(namesize.decode(), sha.hex())
        case _:
            print("--- <other> ---")
            print(obj)
