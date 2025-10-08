#!/usr/bin/env bash
set -euo pipefail
# DEMO: Prometheus 規則檔包含多個 YAML 文件時警告
# TODO:
# 1) 建立多文件規則檔（含 '---' 分隔）
# 2) 執行驗證邏輯或單元測試
# 3) 收斂為最小重現供 PR 使用

mkdir -p logs examples/prometheus-multidoc-rule
echo "[TODO] 產生多文件規則與檢測流程" | tee -a logs/prometheus_multidoc_$(date +%F).log
