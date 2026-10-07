<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" width="112" alt="plainwrite">
  </picture>
</p>

<h1 align="center">plainwrite</h1>
<p align="center"><strong>Chinese that readers get on the first pass and can act on.</strong></p>
<p align="center">A Chinese writing standard for Claude Code. Load it before writing reports, handoffs, rules or replies.</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue" alt="MIT"></a>
  <img src="https://img.shields.io/badge/tested%20with-Claude%20Code-black" alt="tested with Claude Code">
  <img src="https://img.shields.io/badge/tools-Python%203-green" alt="Python 3">
  <img src="https://img.shields.io/badge/status-Alpha-orange" alt="Alpha">
</p>

<p align="center">
  <a href="README.md">中文</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#build-with-us">Build with us</a>
</p>

The usual approach is a list of "AI tells" that the model deletes after writing. plainwrite starts from what the reader needs. It borrows from existing standards (ASD-STE100 Simplified Technical English from aircraft maintenance manuals, ISO 24495 plain language, the GB/T 1.1 modal verbs used in Chinese national standards) so the text comes out right the first time.

**Just a few Markdown files** · **No hooks, one pass and done** · **Every rule cites its source**

The rules themselves are written in Chinese, because they are about writing Chinese. The Chinese name 人话 means "human talk", as in "say it like a person would".

## What it is

A Chinese writing standard split into five document types: steps someone will follow, reports for people to read, rules for models or people, progress replies in a chat, and edits to someone's own draft. Each type is one Markdown file, plus a shared core standard and a list of words to avoid.

Every rule cites where it came from: a named standard, or a reader test on a real file. Where we only saw secondhand material and not the standard itself, the file says so. See [标准/](标准/README.md) for each standard, what we took from it, and what we left out and why.

> **Early version.** Each document type was tried on only one or two real files. The test readers were AI models playing the reader, not people. We did not get hold of the original text of ASD-STE100, ISO 24495 or GB/T 1.1 Annex C. See "已知局限" (known limits) in [DESIGN.md](DESIGN.md).

## What it does

One real progress report was 864 characters, split into bold subheadings and full of internal codes like `comp.yoff` and "R1 to R3". Rewritten with the reply rules it came to 411 characters and opened with what was done, what it means, and what is still unknown. A reader with no context flagged 7 unclear spots instead of 11. More before-and-after pairs are in [样例/看这里.md](样例/看这里.md).

| You are writing | It has the model |
|---|---|
| Handoffs, install notes, reproduction steps | One action per step, conditions before actions, what "done" looks like for each step, decisions for you in their own section |
| Reports for a manager, client or colleague | Put the sentence the reader most needs first; say what the reader should do, including "nothing"; explain terms where they first appear |
| Rules: CLAUDE.md, rule files, acceptance criteria | Open with a legend for how strict "应 / 宜 / 可" (must / should / may) are; put the trigger first; one requirement per rule |
| Progress replies in chat | Cut first, then translate: keep what was done, where to go next, and the conclusion; turn codes into plain words; keep numbers about money, time and risk |
| Edits to your own draft | Only remove; keep your slang, the English you mix in, and your sentence-final particles, because that is how you talk |

## Try these

After installing, say in Claude Code:

| Try | You will see |
|---|---|
| "用人话的规范，把这段汇报改写一下" (rewrite this report the plainwrite way), then paste a report with codes and bold subheadings | Codes turned into plain words, bold subheadings gone; missing facts listed separately instead of made up |
| "按人话的规范，把这条规则改写一下：NEVER push without asking." | Rewritten as "when about to run git push, (you) 应 (must) ask first…", with a note on why it chose the must level |
| "用人话写一份 HANDOFF.md 给下一个 agent" (write a handoff for the next agent) | Decisions for you in their own section; the current state is what it actually ran; every step lists its expected output |
| "用人话把这段打磨一下" (polish this), then paste something you wrote casually | One or two sentence breaks changed; "basically", "吧", "hold 住" kept as they were, with a note on what changed |

## Quick start

### Option A: let your AI install it

Paste this into Claude Code:

```text
Install the plainwrite writing skill for me:
1. Read the README at https://github.com/Longado/plainwrite.
2. Clone the repo to ~/plainwrite.
3. Create a link: ln -s ~/plainwrite ~/.claude/skills/plainwrite (create ~/.claude/skills first if it does not exist).
4. Check that ~/.claude/skills/plainwrite/SKILL.md can be read.
5. Tell me that in a new session I can say "用人话写……" or type /plainwrite to use it.
```

### Option B: install it yourself

```bash
git clone https://github.com/Longado/plainwrite.git ~/plainwrite
mkdir -p ~/.claude/skills
ln -s ~/plainwrite ~/.claude/skills/plainwrite
```

Open a new Claude Code session and say "用人话写……" or type `/plainwrite`.

Without Claude Code, the Markdown files are a writing guide on their own. Read them directly or paste them into another model as context. Only Claude Code has been tested.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Entry point: what to read first, and which file for which document type |
| `规范.md` | Shared core: think of the reader, word choice, sentences and paragraphs, modal verbs, punctuation and numbers |
| `文体/` | One file per document type |
| `避免词.md` | Words to avoid and what to use instead, each with a source |
| `标准/` | Each standard we referenced: key points, how reliable our source was, what we used, what we left out and why |
| `样例/` | Before-and-after pairs from real files |
| `DESIGN.md` | Why it is designed this way, the evidence for each part, what it does not do |
| `工具/` | Scripts for maintaining the avoid list; not needed for writing |

## Privacy

The standard is plain text. The scripts in `工具/` only read local files and make no network calls. `backtest.py` reads your local Claude Code transcripts to count how often you yourself use a word, and prints the result to the terminal.

## Known issues

- Small samples: each document type was tried on one or two real files.
- The test readers were AI models. They do not know your own project names, so their "unclear" counts run high.
- One pass of the rules does not always make things better. In one handoff test, a single rewrite without a reader test made the guessed steps go from 4 to 8. The rules now include what that test taught, but there is no guarantee every time.
- The avoid list only holds words the author actually got wrong. It may not fit someone else.

## Build with us

**How do you write Chinese that readers get on the first pass?**

| If you like… | You could |
|---|---|
| Reading standards | Check the original ASD-STE100, ISO 24495 and GB/T 1.1 Annex C, and replace the entries in `标准/` marked secondhand |
| Writing and editing | Run `工具/backtest.py` on your own writing, find words the model uses much more than you do, and add them to the avoid list |
| Evaluation | Redo the reader tests with real people instead of AI readers and see whether the findings hold |
| Other agent tools | Test whether these files work in Codex and similar tools, and the simplest way to hook them up |
| A new document type | Such as emails or PR descriptions: first show with real files that current writing has a problem, then propose the type |

Issues and pull requests are welcome.

## Development

```bash
cd 工具
python3 test_check.py && python3 test_diff.py   # self-test
python3 check.py file.md                         # check for avoid-list words (--conv for chat replies)
python3 diff.py original.txt edited.txt          # edit comparison
python3 backtest.py word1 word2                  # how often the model and you each use a word
```

`backtest.py` reads two sets of text: deliverables the model wrote, in the folders listed in `~/.claude/plainwrite-dirs`, and prompts you typed yourself, under `~/.claude/projects/`.

## License

[MIT](LICENSE) © Yutai Lin
