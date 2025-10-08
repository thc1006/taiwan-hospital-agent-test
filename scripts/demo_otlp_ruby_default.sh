#!/usr/bin/env bash
set -euo pipefail
# DEMO: OpenTelemetry Ruby OTLP Exporter 預設壓縮為 none
# TODO:
# 1) 啟動一個最小 Ruby 專案（或 irb）
# 2) 設定 exporter 並檢查預設壓縮值
# 3) 覆寫為 gzip 並驗證行為差異

mkdir -p logs
echo "[TODO] Ruby exporter 測試腳本片段" | tee -a logs/otel_ruby_default_$(date +%F).log
