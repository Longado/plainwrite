#!/usr/bin/env python3
"""人话 · 避免词检查。读同目录的 避免词.md,查文件或标准输入里的避免词。只报不改,零模型调用。

用法:
    check.py 文件...          查交付物(「全部」场合的词)
    check.py --conv 文件...   按对话回复查(再加「对话」场合的词)
    check.py --strict ...     有命中时退出码为 1,否则恒为 0
    echo 文字 | check.py -    读标准输入
"""
import re
import sys
import unicodedata
from pathlib import Path

TABLE = Path(__file__).resolve().parent.parent / "避免词.md"

# 这些地方的词是名字或在提这个词,用等长空格抹掉再匹配,行号不变。
# 顺序有讲究:先抹代码,行内代码里落单的「才不会和后文配成一段假引用(v1 2026-08-29 实证)。
MASKS = [
    re.compile(r"```.*?```", re.S),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"https?://[!-~]+"),  # 只吃 ASCII:中文习惯 URL 后不空格,\S+ 会吞掉后面整句
    # 路径只认 ASCII 段;单斜杠要带扩展名,否则「session/这轮」「fire/hire」会被当路径吞掉
    re.compile(r"(?:[A-Za-z0-9_.-]*/){2,}[A-Za-z0-9_.-]+"),
    re.compile(r"[A-Za-z0-9_-]+/[A-Za-z0-9_-]+\.[A-Za-z0-9]{1,8}"),
    re.compile(r"「[^」\n]+」"),
    re.compile(r"《[^》\n]+》"),
]


def mask(text: str) -> str:
    # 换行留着,只把别的字抹成空格:代码块跨行,连换行一起抹掉后面的行号就全错了
    for pat in MASKS:
        text = pat.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), text)
    return text


def one_line_break(text: str) -> str:
    """各种换行符(\r、\u2028 等)统一成 \n,行号才和 splitlines 显示的行对得上。"""
    return "\n".join(text.splitlines())


def load_terms(conv: bool = False):
    """[(词, 类别, 改用, 正则)]。表格行的第一格是词;表头和分隔行跳过。"""
    terms = []
    for line in TABLE.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] in ("词", "") or set(cells[0]) <= set("-: "):
            continue
        word, cat, fix, where, _ = cells
        if where == "对话" and not conv:
            continue
        word = unicodedata.normalize("NFC", word)
        if word.isascii():
            # 写成小写的只认小写:大写开头是专名(Fire TV、Track 2);本来就大写的(DOM)照原样认
            flags = 0 if word == word.lower() else re.I
            pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(word)}(?![A-Za-z0-9_])", flags)
        else:
            pat = re.compile(re.escape(word))
        terms.append((word, cat, fix, pat))
    return terms


def scan(text: str, terms):
    """[(行号, 类别, 词, 改用)],按行号排。"""
    text = one_line_break(unicodedata.normalize("NFC", text))
    masked = mask(text)
    hits = []
    for word, cat, fix, pat in terms:
        for m in pat.finditer(masked):
            hits.append((masked.count("\n", 0, m.start()) + 1, cat, word, fix))
    return sorted(hits)


def main(argv) -> int:
    conv, strict = "--conv" in argv, "--strict" in argv
    paths = [a for a in argv if not a.startswith("--") or a == "-"]
    if not paths:
        print(__doc__)
        return 0
    terms = load_terms(conv)
    total = 0
    for p in paths:
        try:
            text = sys.stdin.read() if p == "-" else Path(p).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"跳过 {p}:{e}", file=sys.stderr)
            continue
        lines = one_line_break(unicodedata.normalize("NFC", text)).split("\n")
        hits = scan(text, terms)
        total += len(hits)
        name = "(标准输入)" if p == "-" else p
        if not hits:
            print(f"{name}:没有避免词")
            continue
        print(f"{name}:{len(hits)} 处")
        for line_no, cat, word, fix in hits:
            print(f"  第 {line_no} 行 [{cat}]「{word}」→ {fix}")
            print(f"    {lines[line_no - 1].strip()[:70]}")
    if total:
        print("命中只是提醒,不是判决:看上下文再决定改不改。")
    return 1 if strict and total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
