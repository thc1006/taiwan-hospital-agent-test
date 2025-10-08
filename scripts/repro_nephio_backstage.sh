#!/usr/bin/env bash
set -euo pipefail
# REPRO: Nephio Backstage UI 不渲染
# TODO:
# 1) 啟動 Backstage（或 docker compose 版本）
# 2) 收集 browser console 與後端 API 日誌
# 3) 將輸出寫入 logs/nephio_backstage_$(date +%F).log

mkdir -p logs
echo "[TODO] 啟動與收集日誌指令寫在這裡" | tee -a logs/nephio_backstage_$(date +%F).log
