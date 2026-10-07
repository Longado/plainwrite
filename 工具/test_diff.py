#!/usr/bin/env python3
"""diff.py 的可跑检查,用例沿用 v1(2026-09-09 改稿翻车那批)。"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))

def run(src, dst):
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.txt"), os.path.join(d, "b.txt")
        open(a, "w", encoding="utf-8").write(src); open(b, "w", encoding="utf-8").write(dst)
        return subprocess.run([sys.executable, HERE + "/diff.py", a, b], capture_output=True, text=True)

# 1) 保留率 + 逐句列出改动
r = run("韵文王宇负责时间,hold这个点。价格一概不给回应。", "韵文、王宇负责时间,守住这个点。价格一概不回应。")
assert "保留率" in r.stdout and "hold这个点" in r.stdout and "守住这个点" in r.stdout, r.stdout
# 2) 被换掉的英文口语、被删的语气词单独点名
assert "hold" in r.stdout.split("保留率")[-1], r.stdout
r = run("我们要拿什么来拯救自己的前额叶呢?", "我们拿什么拯救它?")
assert "呢" in r.stdout and "语气词" in r.stdout, r.stdout
# 3) 一字未动
r = run("原样。", "原样。")
assert "100%" in r.stdout and "没有改动" in r.stdout, r.stdout
# 4) 缺文件不崩
r = subprocess.run([sys.executable, HERE + "/diff.py", "/nonexistent/a", "/nonexistent/b"], capture_output=True, text=True)
assert r.returncode == 0 and "跳过" in r.stderr, r.stderr
# 5) 只动标点的句子不列
r = run("第一句，没动。第二句hold住。第三句也没动。", "第一句,没动。 第二句守住。 第三句也没动。")
items = [l for l in r.stdout.splitlines() if l[:1].isdigit()]
assert len(items) == 1 and "第二句" in items[0], r.stdout
# 6) 口述稿重新断句后仍按原句归组
r = run("甲句在这。乙句hold住。丙句收尾。", "甲句在这,乙句守住,丙句收尾。")
items = [l for l in r.stdout.splitlines() if l[:1].isdigit()]
assert len(items) == 1 and "乙句" in items[0] and "甲句" not in items[0], r.stdout
# 7) 改稿在原文末尾续写,改动清单要列出来(2026-10-06 审查发现:末尾插入被漏掉)
r = run("甲句。", "甲句。乙句是新加的。")
assert "乙句是新加的" in r.stdout, r.stdout
# 8) 长文只改一处,保留率接近 100%(审查发现:没关 autojunk,长文报成 2%)
a = "今天天气不错我们去公园玩。" * 30
r = run(a, a.replace("公园", "海边", 1))
assert "保留率 99%" in r.stdout or "保留率 100%" in r.stdout, r.stdout.splitlines()[0]
# 9) 「了解」里的「了」不是语气词
r = run("我了解这个。", "我理解这个。")
assert "语气词" not in r.stdout, r.stdout
print("diff.py 9 组全过")
