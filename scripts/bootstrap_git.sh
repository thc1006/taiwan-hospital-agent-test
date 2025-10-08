#!/usr/bin/env bash
set -euo pipefail

# 初始化 git 與主要分支
if [ ! -d .git ]; then
  git init
  git checkout -b main
  git add .
  git commit -s -m "chore: bootstrap scaffold repo"
fi

# 建立工作分支
git branch feat/free5gc-oauth2-fix || true
git branch docs/nephio-filename || true
git branch feat/prometheus-yaml-multidoc || true
git branch feat/otel-ruby-default-none || true

echo "✅ Done. Branches:"
git branch -v
