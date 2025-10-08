# 提交流程與分支策略

## 分支命名
- `feat/free5gc-oauth2-fix`
- `docs/nephio-filename`
- `feat/prometheus-yaml-multidoc`
- `feat/otel-ruby-default-none`

## 提交流程
1. 以 `tasks/` 勾選完成狀態。
2. 本地驗證：`make demo_*` 或手動跑 `scripts/`。
3. 撰寫 PR（見模板）。
4. 提交後追蹤 reviewer 回覆並迭代。

## DCO 與 Conventional Commits
- 每次 `git commit -s`。
- 提交訊息遵循 Conventional Commits；重大變更於 footer 註記。