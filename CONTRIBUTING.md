# 貢獻指南（CONTRIBUTING）

## 簽署方式（DCO）
本倉庫採 **DCO**。請在每次提交時附上 `Signed-off-by:`，建議輸入：

```bash
git commit -s -m "feat: your change"
```

> 說明：DCO 的簽署行會附在 commit 訊息末行，格式為 `Signed-off-by: Full Name <email>`。

## Commit 風格
採 **Conventional Commits**：

```
<type>(optional scope): <description>

[optional body]
[optional footer(s)]
```

常用 type：`feat`、`fix`、`docs`、`refactor`、`test`、`chore`。

## PR 提交流程
1. 由 `tasks/` 完成對應日程勾選。
2. 建分支（或使用本倉庫預建的功能分支）。
3. 填 `.github/PULL_REQUEST_TEMPLATE.md` 所需欄位。
4. 本地或 CI 跑測試／腳本驗證。
5. 送出 PR，等審查回覆後迭代。

## 目錄與腳本
- `examples/`：最小重現與展示案例。
- `scripts/`：重現與 Demo 腳本，請先閱讀檔頭 TODO。
