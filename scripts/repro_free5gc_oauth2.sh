#!/usr/bin/env bash
set -euo pipefail
# REPRO: free5gc OAuth2 x OpenBao 憑證相容性
# TODO:
# 1) 生成或導入測試鏈（root -> intermediate -> leaf）
# 2) 啟動最小化 OAuth2/OIDC 流程
# 3) 使用 openssl/curl 驗證握手與鏈順序
# 4) 將輸出寫入 logs/free5gc_oauth2_$(date +%F).log

mkdir -p logs
echo "[TODO] 生成憑證與重現指令寫在這裡" | tee -a logs/free5gc_oauth2_$(date +%F).log
