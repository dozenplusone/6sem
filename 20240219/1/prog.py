import glob
import os
import sys


class RepoError(Exception):
    pass


if len(sys.argv) == 1:
    raise RepoError("repo not provided")
os.chdir(sys.argv[1])

if len(sys.argv) == 2:
    if ".git" not in glob.iglob("**", include_hidden=True):
        raise RepoError("not a repo")

    print(*glob.iglob("**", root_dir=".git/refs/heads"))
    sys.exit(0)
