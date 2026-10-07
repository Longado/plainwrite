# Testing Requirements

## 覆盖率不设数字

写测试,但不追百分比 —— 80% 这类数字是行业惯例不是你的实证,而且覆盖率工具本来就该在 CI 里管,不该由模型记着。
与 coding-style.md 减法阶梯冲突时以阶梯为准:非平凡逻辑留一个能跑的检查,平凡一行不强配测试。

Test Types (for projects that warrant them):
1. **Unit Tests** - Individual functions, utilities, components
2. **Integration Tests** - API endpoints, database operations
3. **E2E Tests** - Critical user flows (framework chosen per language)

## Test-Driven Development

For new non-trivial logic:
- RED-GREEN-REFACTOR cycle: failing test → minimal code to pass → refactor
- Iron Law: no production code without a failing test first
- Don't reuse the same value in test and implementation (假绿 risk — see feedback_fix_contract_not_example)

**修 bug 时把测试锁住(2026-08-27 增补)**。顺序:让 agent 先把 bug 复现成一个失败测试 → 确认它失败的原因跟你预期一致 → **先提交这个测试** → 再让它改代码改到通过,期间不准动测试文件。一个"修复之前就存在、且改不了"的测试才算 bug 没了的证据。

载体必须在代码层。**闸已建并实测**:`~/.claude/hooks/guardrail-test-edit.sh`(PreToolUse / Write|Edit)—— 改动**已存在**的测试文件返回 `deny` 硬拦,新建测试文件放行(TDD 的 RED 步不受影响)。正当修改先 `touch ~/.claude/.allow-test-edit` 再重试,标记一次性、用掉即删。

**9-05 实测踩到的坑,比规则本身更重要**:第一版返回 `permissionDecision:"ask"`,插桩证明 hook 确实被调用、确实返回了 ask,但编辑照样通过 —— **`ask` 在 bypassPermissions 模式下被自动接受,闸等于不存在**(源码里该模式的定义就是 auto-accept all)。只有 `deny` 穿透。推论:任何写在 hook 里、指望靠 `ask` 拦人的红线,在 bypass 模式下全是空的,包括 `guardrail-artifact.sh`。

**这道闸覆盖不到的地方**:它只挂在 Write/Edit 工具上,用 Bash 改文件(`sed -i`、heredoc、`>` 重定向)完全绕过 —— 而 bypassPermissions 模式下 Bash 恰是改文件的主路径。工具层要堵死得枚举无数写法,不现实;真正可靠的层是 git pre-commit(提交本就是本节流程的节点)。**提交层 9-05 已补**:`config/git-hooks/pre-commit`(全局 `core.hooksPath`),同一 commit 里「修改已存在的测试代码 + 改非测试文件」即拦,新增测试或只改测试放行,逃生口 `git commit --no-verify`。链式执行仓库自带 hook。临时仓真提交端到端验过 3 场景。两层合起来才算闸:工具层挡 Write/Edit,提交层兜住 Bash。

8-27 立规到 9-04 建闸之间 8 天靠自觉,9-04 到 9-05 又有一天靠的是个假闸 —— 两次都是「prompt 不算闸」的自证,第二次还多附赠一条:**代码闸也要实测,不测就不知道它是不是假的**(见 [[learn_3repos_study]])。

## Verification Before Completion

NO completion claims without fresh verification evidence (full rule: development-workflow.md #5).

## Troubleshooting Test Failures

4-phase debugging: Evidence → Pattern → Hypothesis → Fix (see development-workflow.md). 3+ failed fixes = stop and question the architecture.

## Agent Support

- **tdd-guide** agent — use proactively for new features
