# Git 与 GitHub

项目规则以根目录 `AGENTS.md` 和 `coummucation.md` 为准。本参考将这些规则整理为任务工作流程。

## 修改前检查

```powershell
git status --short --branch
git pull --rebase origin main
gh pr list --state open --base main
```

还应检查是否有未关闭的 PR 或其他任务认领涉及相同任务/文件。如果工作树有改动导致 pull 失败，不要 stash、reset、覆盖 checkout，也不要将现有改动纳入提交。通过向 `coummucation.md` 追加记录协调；需要隔离任务时，可使用基于当前 `origin/main` 的干净工作树。仅在本地 fetch 不能替代发布前与 `main` 同步的要求。

实现前向日志追加 `CLAIMED` 记录，包含任务编号、日期、角色、基准提交、范围/路径、预期复现检查、已知限制和下一责任方。硬件工作应使用已分配的任务编号，并确认没有重叠的未关闭 PR；不要仅凭分支名推断任务所有权。

## 每轮单独提交

使用 `agent/<github-account>/<task-id>` 分支。每次提交只包含一轮方案或测试，并以任务编号作为提交信息开头：

```powershell
git switch -c agent/<github-account>/<task-id> origin/main
git add <only-files-for-this-round>
git diff --cached --check
git diff --cached --stat
git status --short
git commit -m "<task-id>: <result>"
```

工作树可能包含无关文件时，应显式暂存指定路径，不要使用 `git add -A`。每轮实现/测试/报告都要相应更新 `coummucation.md`，包括被否决的轮次，并记录准确条件、提交、测量结果、证据链接、限制和下一责任方。保留已有证据；共享记录应追加或做最小修改，不要改写既有结论。

发布前应先同步分支，并再次检查暂存差异：

```powershell
git fetch origin
git rebase origin/main
git diff --check origin/main...HEAD
git status --short --branch
git push -u origin agent/<github-account>/<task-id>
gh pr create --base main --head agent/<github-account>/<task-id> --title "<task-id>: <result>" --body-file <review-notes.md>
```

适用时运行仓库策略检查器。CI 要求每个非合并提交都以任务编号开头；代码、测试、板卡、方案或报告文件发生变化时，提交还必须包含 `coummucation.md` 修改。使用常规 push/rebase；绝不能强推覆盖其他写作者的工作。如果 GitHub 身份验证、分支保护或冲突阻止发布，应记录阻塞原因并停止发布，不得声称该轮已发布。

## 制品管理边界

源码、脚本、小型结构化证据和报告应放在仓库规定目录。遵守 `.gitignore`：不要将 Vivado 缓存、生成的位流、编译产物、模型权重或未经授权的人声写入 Git 历史。经批准的跨电脑模型交付应使用项目 Release 流程，提供每个文件的 SHA-256，并在干净目录重新下载运行；仅提供本地路径或 PR 不算完成交付。
