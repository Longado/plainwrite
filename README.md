<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" width="112" alt="plainwrite">
  </picture>
</p>

<h1 align="center">plainwrite · 人话</h1>
<p align="center"><strong>让 AI 写的中文，读的人一遍就懂、照着就能做。</strong></p>
<p align="center">给 Claude Code 用的中文写作规范：写报告、接力文件、规则、回复之前读一下。</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue" alt="MIT"></a>
  <img src="https://img.shields.io/badge/tested%20with-Claude%20Code-black" alt="tested with Claude Code">
  <img src="https://img.shields.io/badge/tools-Python%203-green" alt="Python 3">
  <img src="https://img.shields.io/badge/status-Alpha-orange" alt="Alpha">
</p>

<p align="center">
  <a href="README.en.md">English</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#一起做">一起做</a>
</p>

常见的做法是列一张「AI 腔」清单，让模型写完再删。plainwrite 先问读者要什么：照航空维修手册用的受控英语 ASD-STE100、ISO 24495 简明语言、GB/T 1.1 能愿动词这些现成标准，在下笔之前就把话写对。

**只是几份 Markdown** · **不挂钩子，写一遍就交** · **每条规矩都有出处**

## 是什么

一套中文写作规范，分五种文体：别人要照着做的步骤、给人看的报告说明、给模型或人定的规则、对话里的汇报回复、改别人自己写的稿子。每种文体一份 md，再加一份共用规范和一张避免词表。

每条规矩都写了出处：来自哪个标准，或者来自哪一次真实文件的试读。标准原文没读到、只看过二手资料的，也写明了。参照了哪些标准、用了哪些条目、没用的为什么不用，见 [标准/](标准/README.md)。

> **早期版本。** 每种文体只拿一到两份真实文件试过；试读的读者是 AI 扮演的，不是真人；ASD-STE100、ISO 24495、GB/T 1.1 附录 C 的原文没读到。详见 [DESIGN.md](DESIGN.md) 的「已知局限」。

## 效果

一条真实的进度汇报，原来 864 字，分「做了什么」「我看到的」「失败与局限」几个加粗小标题，满是 `comp.yoff`、「复现闸」「R1 到 R3」这类代号。按「回复」文体改写后剩 411 字，开头是这样：

> 阶段成果 3 做完了：高远、深远、平远各配石质和土质两种，共 6 个配方，都能出图；另加了一个控制山体上方留白的旋钮，默认不变，旧结果不受影响。哪张像水墨、好不好，没有外部判据，只是我目测。

让一个没背景的读者来读，看不懂的地方从 11 处降到 7 处。更多对照见 [样例/看这里.md](样例/看这里.md)。

## 它管什么

| 你要写 | 它会让模型 |
|---|---|
| 接力文件、装机说明、复现流程 | 一步一个动作，条件写在动作前面，每步写清做完的样子，要你决定的事单列一节 |
| 给领导、客户、同事的报告说明 | 第一段就是读者最需要的那句；写清要读者做什么，包括「什么都不用做」；名词在第一次出现的地方解释 |
| 规则：CLAUDE.md、规则文件、验收条件 | 文件开头放一句图例，说明「应 / 宜 / 可」各有多硬；触发条件写在前面；一条只写一件事 |
| 对话里的进度汇报 | 先删再翻译：只留做了什么、往哪改、结论；代号翻成白话或不用；钱、时间、风险这类数留着 |
| 改你自己写的稿子 | 只做减法；口语、夹的英文、语气词保留，那是你说话的样子 |

## 可以试试

装好以后，在 Claude Code 里说：

| 试试 | 你会看到 |
|---|---|
| 「用人话的规范，把这段汇报改写一下」，贴一段带代号和加粗小标题的汇报 | 代号翻成白话，加粗小标题去掉；原文缺的信息单独列出来，不替你编 |
| 「按人话的规范，把这条规则改写一下：NEVER push without asking.」 | 改成「当要执行 git push 时，应先问……」，并说明为什么用「应」这一档 |
| 「用人话写一份 HANDOFF.md 给下一个 agent」 | 要你决定的事单列一节；「现在到哪了」写的是它实际运行出来的结果，每一步都写了期望输出 |
| 「用人话把这段打磨一下」，贴一段你随手写的口语 | 只动一两处断句，「basically」「吧」「hold 住」这类原样保留，并说明改了哪里 |

## 快速开始

### 方式 A：让你的 AI 帮你装

把下面这段贴进 Claude Code：

```text
帮我安装 plainwrite 这个写作规范 skill:
1. 先读 https://github.com/Longado/plainwrite 的 README。
2. 把仓库克隆到 ~/plainwrite。
3. 建一个链接:ln -s ~/plainwrite ~/.claude/skills/plainwrite(如果 ~/.claude/skills 不存在就先建目录)。
4. 确认 ~/.claude/skills/plainwrite/SKILL.md 能读到。
5. 告诉我:新开一个会话以后,说「用人话写……」或者输入 /plainwrite 就能用。
```

### 方式 B：自己装

```bash
git clone https://github.com/Longado/plainwrite.git ~/plainwrite
mkdir -p ~/.claude/skills
ln -s ~/plainwrite ~/.claude/skills/plainwrite
```

新开一个 Claude Code 会话，说「用人话写……」或者输入 `/plainwrite`。

不用 Claude Code 的话，这几份 md 本身就是一份写作指南，可以直接看，也可以贴给别的模型当上下文。目前只在 Claude Code 上测过。

## 文件

| 文件 | 干什么 |
|---|---|
| `SKILL.md` | 入口：先读什么、哪种文体读哪份 |
| `规范.md` | 五种文体共用：先想读者、用词、句子段落、能愿动词、标点数字 |
| `文体/` | 五种文体各一份 |
| `避免词.md` | 不该用的词和改用什么，每条都有出处 |
| `标准/` | 参照的每个写作标准：要点、来源可信度、用了哪些、没用的为什么不用 |
| `样例/` | 真实文件改写前后的对照 |
| `DESIGN.md` | 为什么这样设计、每部分的依据、不做什么 |
| `工具/` | 维护避免词表的脚本，写东西时用不到 |

## 隐私

规范本身只是文本。`工具/` 里的脚本只读本机文件，不联网：`backtest.py` 会读本机 Claude Code 的对话记录，用来数某个词你自己用过几次，结果只打印在终端里。

## 已知问题

- 样本小：五种文体各只拿一到两份真实文件试过。
- 试读的读者是 AI 扮演的，它不认识你自己的项目名，「看不懂」的数会偏高。
- 只照规矩改一遍不一定变好。写接力文件时实测过，只改一遍、不试读，要猜的步数反而从 4 步变成 8 步。规矩已经吸收了那次的结论，但不保证每次都对。
- 避免词表只收作者自己实际犯过的词，换一个人用，词表未必合适。

## 一起做

**中文里怎样写，读的人一遍就懂？**

| 你喜欢…… | 可以贡献 |
|---|---|
| 读标准原文 | 核对 ASD-STE100、ISO 24495、GB/T 1.1 附录 C 的原文，把 `标准/` 里标着「二手」的条目改成原文 |
| 写作、编辑 | 拿你自己的稿子跑 `工具/backtest.py`，看哪些词是模型写得多、你写得少，补进避免词表 |
| 做评测 | 用真人读者代替 AI 读者重做试读，看结论还站不站得住 |
| 用别的 agent 工具 | 测这套 md 在 Codex 等工具里能不能用，怎么接最省事 |
| 有新的文体需求 | 比如邮件、PR 描述：先拿真实文件证明现在写得有问题，再提新文体 |

欢迎提 issue 或 pull request。

## 开发

```bash
cd 工具
python3 test_check.py && python3 test_diff.py   # 脚本自检
python3 check.py 文件.md                         # 查避免词(对话回复加 --conv)
python3 diff.py 原文.txt 改稿.txt                # 改稿对照
python3 backtest.py 词1 词2                      # 回测:模型和你各用了多少次
```

`backtest.py` 读两份材料：`~/.claude/plainwrite-dirs` 里列的目录下模型写的交付物，以及 `~/.claude/projects/` 下你自己打的提示。

## 许可证

[MIT](LICENSE) © Yutai Lin
