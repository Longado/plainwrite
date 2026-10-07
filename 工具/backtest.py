#!/usr/bin/env python3
"""人话 · 回测。backtest.py 词...:每个词在两份材料里每万字出现几次。

两份材料:
- Claude 写的交付物:~/.claude/plainwrite-dirs 里列的目录下、汉字不少于 200 的 .md(隐藏目录不进)。
- 作者写的提示:~/.claude/projects/*/*.jsonl 里真人打的提示,汉字不少于 150,去掉以 < 开头、带代码块的和重复的。

收进避免词表的门槛(见 DESIGN.md):作者提过意见,或这里 Claude 明显多、作者少。作者自己常用的不收。
代码、链接、路径、「」里的不算(和 check.py 一样抹掉)。
"""
import glob
import json
import os
import re
import sys
import unicodedata

from check import mask

DIRS_FILE = os.path.expanduser("~/.claude/plainwrite-dirs")
cjk = lambda t: len(re.findall(r"[一-鿿]", t))


def claude_docs():
    try:
        dirs = open(DIRS_FILE, encoding="utf-8").read().split()
    except OSError:
        sys.exit(f"读不到 {DIRS_FILE}:一行一个目录,列出 Claude 写交付物的地方")
    for d in dirs:
        for f in glob.glob(f"{d}/**/*.md", recursive=True):
            if any(p.startswith(".") for p in os.path.relpath(f, d).split(os.sep)):
                continue
            try:
                t = open(f, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            if cjk(t) >= 200:
                yield t


def eddie_prompts():
    seen = set()
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        for line in open(f, encoding="utf-8", errors="ignore"):
            if '"user"' not in line:
                continue
            try:
                o = json.loads(line)
            except ValueError:
                continue
            c = (o.get("message") or {}).get("content")
            if o.get("type") != "user" or o.get("isMeta") or not isinstance(c, str):
                continue
            t = c.strip()
            if t.startswith("<") or "```" in t or t in seen or cjk(t) < 150:
                continue
            seen.add(t)
            yield t


def density(docs, words):
    masked = [mask(unicodedata.normalize("NFC", t)) for t in docs]
    total = sum(cjk(t) for t in masked) or 1
    return total, {w: sum(t.count(w) for t in masked) for w in words}


def main(words) -> int:
    if not words:
        print(__doc__)
        return 0
    nc, c = density(list(claude_docs()), words)
    ne, e = density(list(eddie_prompts()), words)
    print(f"Claude 交付物 {nc / 1e4:.0f} 万字 | 作者提示 {ne / 1e4:.0f} 万字")
    print(f"{'词':<8}{'Claude 次数':>10}{'每万字':>8}{'作者次数':>10}{'每万字':>8}")
    for w in words:
        print(f"{w:<8}{c[w]:>10}{c[w] / nc * 1e4:>8.2f}{e[w]:>10}{e[w] / ne * 1e4:>8.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
