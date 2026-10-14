#!/usr/bin/env bash
# 用 GitHub CLI 把 issues.tsv 的每一列建成一個 Issue，並貼上 P0–P8 標籤。
# 用法：在 repo 資料夾裡執行  bash scripts/create_issues.sh
# 想同時加進看板：PROJECT_NUMBER=1 bash scripts/create_issues.sh
set -euo pipefail
cd "$(dirname "$0")/.."

for p in P0 P1 P2 P3 P4 P5 P6 P7 P8; do
  gh label create "$p" --color "1F6FEB" --force >/dev/null
done

while IFS=$'\t' read -r label title body; do
  [ -z "$title" ] && continue
  url=$(gh issue create --title "$title" --body "${body//<br>/$'\n'}" --label "$label")
  echo "建立：$url"
  if [ -n "${PROJECT_NUMBER:-}" ]; then
    gh project item-add "$PROJECT_NUMBER" --owner "@me" --url "$url" >/dev/null
  fi
done < scripts/issues.tsv
echo "完成。"
