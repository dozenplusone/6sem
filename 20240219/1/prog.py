import glob
import os
import sys
import zlib


class RepoError(Exception):
    pass


if len(sys.argv) == 1:
    raise RepoError("repo not provided")

os.chdir(sys.argv[1])
branches = glob.glob("**", root_dir=".git/refs/heads")

if len(sys.argv) == 2:
    if ".git" not in glob.iglob("**", include_hidden=True):
        raise RepoError("not a repo")

    print(*branches)
    sys.exit(0)

if sys.argv[2] not in branches:
    raise RepoError(f"branch '{sys.argv[2]}' doesn't exist")

with open(f".git/refs/heads/{sys.argv[2]}") as f:
    sha = f.read(40)
with open(f".git/objects/{sha[:2]}/{sha[2:]}", "rb") as f:
    commit = zlib.decompress(f.read()).partition(b'\x00')[2].decode().rstrip()
print(commit)
