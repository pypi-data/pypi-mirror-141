import os
import re
from collections import Counter
from copy import copy
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Group:
    """連（同じ種類の並び）"""

    c: str  # 文字
    n: int  # 連続する数

    def __str__(self):
        return self.c * self.n


def to_groups(s: str):
    """連に分割"""
    n = len(s)
    last = n - 1
    for i in range(n - 1, -1, -1):
        if i < n - 1 and s[i] != s[i + 1]:
            yield Group(s[last], last - i)
            last = i
    if n:
        yield Group(s[last], last + 1)


@dataclass
class Column:
    """列（1本の串に相当）"""

    index: int  # 位置（表示用）
    groups: list[Group]  # 連のリスト
    space: int  # 空き

    def __init__(self, index: int, s: str):
        self.index = index
        self.groups = list(to_groups(s.strip("-")))
        self.space = 4 - sum(g.n for g in self.groups)

    def __str__(self):
        return "".join(map(str, self.groups)) + " " * self.space

    def ok(self):
        return self.space == 4 or (self.space == 0 and self.groups[0].n == 4)

    def canpush(self, group: Group):
        sp = self.space >= group.n
        return sp and (not self.groups or self.groups[-1].c == group.c)

    def push(self, column: "Column"):
        group = column.groups.pop()
        column.space += group.n
        if not self.groups:
            self.groups.append(copy(group))
        else:
            self.groups[-1].n += group.n
        self.space -= group.n
        return group

    def restore(self, column: "Column", group: Group):
        if self.groups[-1].n == group.n:
            self.groups.pop()
        else:
            self.groups[-1].n -= group.n
        self.space += group.n
        column.groups.append(group)
        column.space -= group.n


def show(columns):
    for column in columns:
        print(f"[{column}]")
    print()


@dataclass
class Table:
    columns: list[Column]

    def __init__(self, info: str):
        self.columns = [Column(i, s) for i, s in enumerate(info.split())]
        c = Counter(re.sub("[ -]+", "", info)).most_common()
        if not all(n == 4 for _, n in c):
            print(c)
            show(self.columns)
            raise

    def __hash__(self):
        return hash(" ".join(sorted(map(str, self.columns))))


def solve_logic(table: Table, cache: set[int], result: list[str]):
    if all(column.ok() for column in table.columns):
        return result
    for column1 in table.columns:
        if column1.ok():
            continue
        for column2 in table.columns:
            if column1 is column2 or not column2.canpush(column1.groups[-1]):
                continue
            group = column2.push(column1)
            h = hash(table)
            if h not in cache:
                cache.add(h)
                mes = f"move {group} from {column1.index} to {column2.index}"
                if r := solve_logic(table, cache, result + [mes]):
                    return r
            column2.restore(column1, group)


def get_game_str(fnam):
    import numpy as np
    from PIL import Image

    bst = " -bcehiknrstuy"
    bas = [
        [247, 231, 194],
        [215, 192, 149],
        [79, 152, 70],
        [240, 192, 85],
        [222, 142, 93],
        [201, 179, 105],
        [248, 212, 179],
        [207, 224, 139],
        [219, 112, 96],
        [237, 222, 186],
        [183, 141, 96],
        [232, 142, 110],
        [228, 219, 189],
        [183, 101, 60],
    ]
    with Image.open(fnam) as im:
        ar = np.array(im)

    ar = ar[:, (ar.mean(2).mean(0) > 235).argmin() :]
    dy = np.argmax(ar.mean(2).std(1) > 9)
    dx = np.argmax(ar.mean(2)[dy] < 200)
    ar = ar[dy + 45 :, dx - 18 :]
    ncols = [0, 0]
    for h in range(2):
        y = 330 + h * 599
        for i in range(13):
            x = 1000 * i // 12
            v = ar[y : y + 40, x : x + 40].reshape(-1, 3).mean(0)
            ncols[h] += np.linalg.norm(v - bas, axis=1).argmin() == 1
    hd = ncols[1] - ncols[0]
    rs = []
    for h, ncol in enumerate(ncols):
        for i in range(ncol):
            rrs = []
            x = 500 * (2 * i - h * hd) // 6
            for j in range(4):
                y = 90 * j + h * 599
                v = ar[y : y + 40, x : x + 40].reshape(-1, 3).mean(0)
                rrs.append(bst[np.linalg.norm(v - bas, axis=1).argmin()])
            rs.append("".join(rrs))
    return " ".join(rs)


def show_move(fnam):
    table = Table(get_game_str(fnam))
    print("\n".join(solve_logic(table, set(), []) or []))
    os.remove(fnam)


def main(dir=None):
    pth = Path(dir or f"{os.environ['HOME']}/Desktop/")
    fnam = max((f.stat().st_mtime, f) for f in pth.glob("*.jpg"))[1]
    show_move(fnam)
