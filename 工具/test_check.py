#!/usr/bin/env python3
"""check.py 的可跑检查。python3 test_check.py,全过打印一行。用例沿用 v1 踩过的坑。"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
from check import load_terms, scan

def hit(text, conv=False):
    return {t for _, _, t, _ in scan(text, load_terms(conv))}

# 1) 表里的词抓得到;「对话」场合的词只在 conv 下抓
assert {"摩擦", "幌子", "fire"} <= hit("最大的摩擦是作者的说法是个幌子,建议 fire 一个任务。")
assert "session" not in hit("这个 session 先放一放") and "session" in hit("这个 session 先放一放", conv=True)
assert "闸" not in hit("两层合起来才算闸") and "闸" in hit("两层合起来才算闸", conv=True)
# 2) 代码块、行内代码、链接、路径、「」《》里的不算
assert hit("看 `track_id`,脚本在 tools/track/run.sh,见 https://x.com/tab/1,「fire」这个词\n```\nfire()\n```") == set()
# 3) 英文按词边界:firewall、tablet 不算
assert hit("firewall 挡住了 tablet") == set()
# 4) 小写词不认大写开头的专名;表里本来大写的照认
assert hit("在 Fire TV 上试,Track 2 的规则,Sprint 结束", conv=True) == set()
assert {"track", "DOM"} <= hit("这条 track 的 DOM 不对")
# 5) 斜杠挨着中文不当路径吞掉(v1 2026-08-28 实证)
assert "session" in hit("别写 session/这轮", conv=True)
# 6) 命令行:有命中退出码仍是 0,--strict 才是 1;读不到文件不崩
r = subprocess.run([sys.executable, HERE + "/check.py", "-"], input="这是个幌子", capture_output=True, text=True)
assert r.returncode == 0 and "幌子" in r.stdout and "改成说材料" in r.stdout, r.stdout
r = subprocess.run([sys.executable, HERE + "/check.py", "--strict", "-"], input="这是个幌子", capture_output=True, text=True)
assert r.returncode == 1, r.returncode
r = subprocess.run([sys.executable, HERE + "/check.py", "/nonexistent.md"], capture_output=True, text=True)
assert r.returncode == 0 and "跳过" in r.stderr, r.stderr
# 7) 代码块之后的命中,行号要对得上原文(2026-10-06 审查发现:抹代码块时连换行一起抹了)
assert [h[0] for h in scan("```\na\nb\n```\n这是幌子\n", load_terms())] == [5]
# 8) 特殊换行符(\u2028)也按一行算,行号与显示的行一致
assert [h[0] for h in scan("a\u2028这是幌子\n", load_terms())] == [2]
print("check.py 8 组全过")
