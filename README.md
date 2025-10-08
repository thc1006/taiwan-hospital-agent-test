# GHW Open Source Week Scaffold

一鍵取得「每日任務清單＋PR 模板＋REPRO/DEMO 腳本樣板」。  
目標：在 10/11–10/15（台北時間，每日 17:00 後）穩定產出 **2–3 個高價值 PR**。

## 包含內容
- `tasks/`：Day 2 → Day 6 勾選清單（可直接逐項打勾）。
- `scripts/`：重現／展示腳本樣板（free5gc、Nephio、Prometheus、OpenTelemetry Ruby）。
- `.github/`：PR 模板與 Issue 模板。
- `docs/`：提交流程、分支策略、指令速查。

## 快速開始
```bash
# 初始化 git 與分支（會自動建立多條工作分支與初始提交）
bash scripts/bootstrap_git.sh

# （可選）推到 GitHub（請先在 GitHub 建立空倉庫，替換 YOUR-REPO-URL）
git remote add origin YOUR-REPO-URL
git push -u origin main
git push -u origin feat/free5gc-oauth2-fix
git push -u origin docs/nephio-filename
git push -u origin feat/prometheus-yaml-multidoc
git push -u origin feat/otel-ruby-default-none
```

## 目標議題（可自訂替換）
- free5gc `#682` OAuth2 × OpenBao 憑證相容性
- Nephio `#966` Backstage UI 不渲染／`#955` 文檔檔名不一致
- Prometheus `#15834` YAML 規則檔多文件警告
- OpenTelemetry Ruby `#1798` OTLP Exporter 壓縮預設值

> **Commit 規範**：預設採用 Conventional Commits，提交一律 `git commit -s`（DCO）。
