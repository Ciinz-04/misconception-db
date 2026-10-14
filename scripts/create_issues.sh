#!/usr/bin/env bash
# 把 scripts/issues.tsv 的每一列建成 Issue，貼上 P0–P8 標籤；已存在的標題會略過。
set -euo pipefail
cd "$(dirname "$0")/.."

for p in P0 P1 P2 P3 P4 P5 P6 P7 P8; do
  gh label create "$p" --color "1F6FEB" --force >/dev/null </dev/null
done

existing=$(gh issue list --state all --limit 500 --json title --jq '.[].title' </dev/null)

while IFS=$'\t' read -r label title body <&3; do
  [ -z "$title" ] && continue
  if grep -Fxq -- "$title" <<< "$existing"; then
    echo "略過（已存在）：$title"; continue
  fi
  url=""
  for try in 1 2 3; do
    if url=$(gh issue create --title "$title" --body "${body//<br>/$'\n'}" --label "$label" </dev/null); then break; fi
    echo "GitHub 暫時拒絕（多半是建立太快），60 秒後重試……"; sleep 60
  done
  [ -z "$url" ] && { echo "建立失敗：$title，請稍後再跑一次本腳本"; exit 1; }
  echo "建立：$url"
  sleep 3
  if [ -n "${PROJECT_NUMBER:-}" ]; then
    gh project item-add "$PROJECT_NUMBER" --owner "@me" --url "$url" >/dev/null </dev/null
  fi
done 3< scripts/issues.tsv
echo "完成。"
