#!/usr/bin/env python3
"""人话 · 改稿对照。diff.py 原文 改稿:给保留率、逐句列改动,点名被换掉的英文口语和被删的语气词。只报不判。"""
import re
import sys
import unicodedata
from pathlib import Path

from check import mask

# 改稿对照:2026-09-09 实证,我改作者的口述笔记把「hold 这个点」写成「守住这个点」,词表看不见 ——
# 不是词的病,是把人改没了。改动清单交给代码列,模型自己交代会漏会编。只报不判。
SENT_SPLIT = re.compile(r"(?<=[。!?!?;;\n])")
TONE_WORDS = ("呢", "吧", "啊", "嘛", "呀", "了")


def diff_report(src: str, dst: str) -> str:
    import difflib
    src, dst = unicodedata.normalize("NFC", src), unicodedata.normalize("NFC", dst)
    # autojunk 关掉:默认会把长文里的高频字当噪音丢掉,200 字以上的稿子保留率会错报成个位数
    ratio = difflib.SequenceMatcher(None, src, dst, autojunk=False).ratio()
    out = [f"保留率 {ratio:.0%}(1 字没动 = 100%)"]
    if src == dst:
        out.append("没有改动。")
        return "\n".join(out)
    # 按字比,按原文的句子归组:口述稿常常没句号全靠逗号,改稿一重新断句,句子级怎么配都对不上。
    # 每个原句下面给它在改稿里对应的片段(用字级对齐把原句首尾映射过去),只动标点/空白的不算改动。
    PUNCT = re.compile(r"^[\s,，。.!!??;;::、\"“”'‘’()()《》「」]*$")
    ops = difflib.SequenceMatcher(None, src, dst, autojunk=False).get_opcodes()
    real = [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in ops
            if t != "equal" and not (PUNCT.match(src[i1:i2]) and PUNCT.match(dst[j1:j2]))]
    def to_dst(i):  # 原文下标 → 改稿下标
        for t, i1, i2, j1, j2 in ops:
            if i1 <= i < i2 or (i == i2 and i2 == len(src)):
                return j1 + (i - i1) if t == "equal" else (j1 if i == i1 else j2)
        return len(dst)
    bounds, pos = [], 0
    for sent in SENT_SPLIT.split(src):
        if sent.strip():
            bounds.append((pos, pos + len(sent)))
        pos += len(sent)
    items = []
    for s0, s1 in bounds:
        # 插入算在它后面那句;插在原文末尾的(续写)算在最后一句
        last = s1 == bounds[-1][1]
        if not any(i1 < s1 and i2 > s0 or (i1 == i2 == s0) or (last and i1 == i2 >= s1)
                   for _, i1, i2, _, _ in real):
            continue
        before = src[s0:s1].strip()
        after = dst[to_dst(s0):(len(dst) if last else to_dst(s1))].strip()
        items.append((before, after))
    for n, (before, after) in enumerate(items, 1):
        out.append(f"{n}. 原:{before}\n   改:{after or '(删了)'}")
    # 两类最常被当瑕疵删掉的手迹,单独点名
    eng_src = set(w.lower() for w in re.findall(r"[A-Za-z]{2,}", mask(src)))
    eng_dst = set(w.lower() for w in re.findall(r"[A-Za-z]{2,}", mask(dst)))
    gone = sorted(eng_src - eng_dst)
    if gone:
        out.append(f"原文里的英文口语被换掉:{'、'.join(gone)} —— 那是他说话的样子,默认还原")
    # 只数句末或停顿前的语气词:「了解」「吧台」里的字不算
    def tone(text, w):
        return len(re.findall(re.escape(w) + r"(?=[\s,，。.!！?？;；…~]|$)", text))
    tone_gone = [w for w in TONE_WORDS if tone(src, w) > tone(dst, w)]
    if tone_gone:
        out.append(f"语气词被删了:{'、'.join(tone_gone)} —— 里面有叹气和犹豫,默认还原")
    return "\n".join(out)


def main(argv) -> int:
    paths = [a for a in argv if not a.startswith("--")]
    if len(paths) != 2:
        print("用法:diff.py 原文 改稿", file=sys.stderr)
        return 0
    try:
        src, dst = (Path(p).read_text(encoding="utf-8") for p in paths)
    except (OSError, UnicodeDecodeError) as e:
        print(f"跳过:{e}", file=sys.stderr)
        return 0
    print(diff_report(src, dst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
