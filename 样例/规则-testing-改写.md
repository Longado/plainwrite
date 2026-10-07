# Testing Requirements

> 本文件的义务词照 GB/T 1.1-2020:「应 / 不应」= 必须做到,任何情况都不能违反;「宜 / 不宜」= 默认这样做,有理由可以不做,但要说出理由;「可 / 不必」= 做不做都行。

## 覆盖率不设数字

- 宜写测试,不宜追百分比〔强度待作者定〕。理由:80% 这类数字是行业惯例,不是你的实证;覆盖率工具本来就该在 CI 里管,不该由模型记着。
- 本节与 coding-style.md 减法阶梯冲突时,应以阶梯为准。
- 写非平凡逻辑时,宜留一个能跑的检查〔强度待作者定〕;平凡的一行不宜强配测试〔强度待作者定〕。

Test Types(适用于值得做的项目):
1. **Unit Tests**:单个函数、工具、组件
2. **Integration Tests**:API 接口、数据库操作
3. **E2E Tests**:关键用户流程(框架按语言选)

上面三类宜按项目需要选用〔强度待作者定〕。

## Test-Driven Development

针对新写的非平凡逻辑:

- 宜走 RED-GREEN-REFACTOR 循环:先写失败的测试,再写刚好能通过的代码,最后重构〔强度待作者定〕。
- 写生产代码之前,宜先有一个失败的测试(原文称 Iron Law)〔强度待作者定〕。
- 测试与实现里不宜用同一个值(有假绿风险,见 feedback_fix_contract_not_example)〔强度待作者定〕。

**修 bug 时把测试锁住(2026-08-27 增补)**。顺序如下:

1. 修 bug 时,宜先让 agent 把 bug 复现成一个失败的测试〔强度待作者定〕。
2. 宜确认它失败的原因与你预期的一致〔强度待作者定〕。
3. 宜先提交这个测试,再让 agent 改代码〔强度待作者定〕。
4. 改代码到测试通过期间,不应动测试文件。
5. 判据:一个在修复之前就存在、且改不了的测试,才算 bug 没了的证据。

锁测试的手段应落在代码层。**闸已建并实测**:`~/.claude/hooks/guardrail-test-edit.sh`(PreToolUse / Write|Edit)——改动**已存在**的测试文件时返回 `deny` 硬拦,新建测试文件放行(TDD 的 RED 步不受影响)。需要正当修改时,宜先 `touch ~/.claude/.allow-test-edit` 再重试;标记一次性,用掉即删〔强度待作者定〕。

**9-05 实测踩到的坑,比规则本身更重要**:第一版返回 `permissionDecision:"ask"`。插桩证明 hook 确实被调用、确实返回了 ask,但编辑照样通过——**`ask` 在 bypassPermissions 模式下被自动接受,闸等于不存在**(源码里该模式的定义就是自动接受全部)。只有 `deny` 能穿透。推论:任何写在 hook 里、指望靠 `ask` 拦人的红线,在 bypass 模式下全是空的,包括 `guardrail-artifact.sh`〔强度待作者定:原文只给事实与推论,没写该怎么做〕。

**这道闸覆盖不到的地方**:它只挂在 Write/Edit 工具上,用 Bash 改文件(`sed -i`、heredoc、`>` 重定向)完全绕过——而 bypassPermissions 模式下,Bash 恰是改文件的主路径。工具层要堵死,得枚举无数种写法,不现实;真正可靠的层是 git pre-commit(提交本就是本节流程的节点)。**提交层 9-05 已补**:`config/git-hooks/pre-commit`(全局 `core.hooksPath`),同一个 commit 里「修改已存在的测试代码 + 改非测试文件」即拦,新增测试或只改测试放行。逃生口 `git commit --no-verify` 可用。链式执行仓库自带的 hook。临时仓里真提交,端到端验过 3 个场景。两层合起来才算闸:工具层挡 Write/Edit,提交层兜住 Bash。

8-27 立规到 9-04 建闸之间,8 天靠自觉;9-04 到 9-05 又有一天靠的是个假闸。两次都是「prompt 不算闸」的自证,第二次还多一条:**代码闸也宜实测,不测就不知道它是不是假的**〔强度待作者定〕(见 [[learn_3repos_study]])。

## Verification Before Completion

没有新鲜的验证证据,不应声称完成(全文见 development-workflow.md #5)。

## Troubleshooting Test Failures

- 宜按四个阶段排查:Evidence → Pattern → Hypothesis → Fix(见 development-workflow.md)〔强度待作者定〕。
- 同一个问题修了 3 次以上还没好时,宜停下来重新看架构〔强度待作者定〕。

## Agent Support

- **tdd-guide** agent:做新功能时宜主动使用〔强度待作者定〕。
