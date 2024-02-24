import glob
import os
import sys
import zlib


class RepoError(Exception):
    pass


def getTreeParentId(commitId: str):
    with open(f".git/objects/{commitId[:2]}/{commitId[2:]}", "rb") as f:
        commit = zlib.decompress(f.read()).partition(b'\x00')[2]

    tree, _, commit = commit.partition(b'\n')
    treeId = tree.partition(b' ')[2].decode()
    parentId = commit[7:47].decode() if commit.startswith(b"parent") else None
    return treeId, parentId


def printSingleTreeObj(tree):
    attrXname, _, idXtree = tree.partition(b'\x00')
    name = attrXname.partition(b' ')[2].decode()
    id, tree = idXtree[:20].hex(), idXtree[20:]
    with open(f".git/objects/{id[:2]}/{id[2:]}", "rb") as f:
        _type = zlib.decompress(f.read()).partition(b' ')[0].decode()

    print(_type, id, name)
    return tree


def printTree(treeId: str):
    with open(f".git/objects/{treeId[:2]}/{treeId[2:]}", "rb") as f:
        tree = zlib.decompress(f.read()).partition(b'\x00')[2]

    if not tree:
        print("(empty)")
        return
    while tree := printSingleTreeObj(tree):
        pass


if len(sys.argv) == 1:
    raise RepoError("repo not provided")

os.chdir(sys.argv[1])
if ".git" not in glob.iglob("**", include_hidden=True):
    raise RepoError("not a repo")

branches = glob.glob("**", root_dir=".git/refs/heads")
if len(sys.argv) == 2:
    if branches:
        print(*branches, sep='\n')
    else:
        print("(no branches yet)")
    sys.exit(0)

if sys.argv[2] not in branches:
    raise RepoError(f"branch '{sys.argv[2]}' doesn't exist")

with open(f".git/refs/heads/{sys.argv[2]}") as f:
    sha = f.read(40)

print("TREE for commit", sha)
tree, sha = getTreeParentId(sha)
printTree(tree)

while sha is not None:
    print("TREE for commit", sha)
    tree, sha = getTreeParentId(sha)
    printTree(tree)
