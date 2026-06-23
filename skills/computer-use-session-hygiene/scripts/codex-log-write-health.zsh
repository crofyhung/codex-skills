#!/bin/zsh
set -euo pipefail

codex_home="${CODEX_HOME:-$HOME/.codex}"
sample_seconds="${CODEX_LOG_SAMPLE_SECONDS:-10}"
warn_mb_per_min="${CODEX_LOG_WARN_MB_PER_MIN:-10}"
danger_mb_per_min="${CODEX_LOG_DANGER_MB_PER_MIN:-50}"
warn_rows_per_min="${CODEX_LOG_WARN_ROWS_PER_MIN:-2000}"
danger_rows_per_min="${CODEX_LOG_DANGER_ROWS_PER_MIN:-10000}"

bytes() {
  local file="$1"
  stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0
}

mtime() {
  local file="$1"
  stat -f%m "$file" 2>/dev/null || stat -c%Y "$file" 2>/dev/null || echo 0
}

mb() {
  awk -v b="$1" 'BEGIN { printf "%.1f", b / 1024 / 1024 }'
}

rows() {
  local db="$1"
  [[ -f "$db" ]] || { echo 0; return; }
  sqlite3 -readonly "$db" 'SELECT COUNT(*) FROM logs;' 2>/dev/null || echo 0
}

levels() {
  local db="$1"
  [[ -f "$db" ]] || return
  sqlite3 -readonly "$db" 'SELECT level || ":" || COUNT(*) FROM logs GROUP BY level ORDER BY COUNT(*) DESC;' 2>/dev/null || true
}

score() {
  local mb_per_min="$1"
  local rows_per_min="$2"
  awk -v x="$mb_per_min" -v y="$rows_per_min" -v dm="$danger_mb_per_min" -v dr="$danger_rows_per_min" 'BEGIN { exit !((x >= dm) || (y >= dr)) }' && { echo "DANGER"; return; }
  awk -v x="$mb_per_min" -v y="$rows_per_min" -v wm="$warn_mb_per_min" -v wr="$warn_rows_per_min" 'BEGIN { exit !((x >= wm) || (y >= wr)) }' && { echo "WARN"; return; }
  echo "OK"
}

dbs=(
  "$codex_home/logs_2.sqlite"
  "$codex_home/sqlite/logs_2.sqlite"
)

echo "Codex log write health"
echo "CODEX_HOME: $codex_home"
echo "Sample: ${sample_seconds}s"
echo

for db in "${dbs[@]}"; do
  wal="${db}-wal"
  if [[ ! -f "$db" && ! -f "$wal" ]]; then
    continue
  fi

  db_before="$(bytes "$db")"
  wal_before="$(bytes "$wal")"
  rows_before="$(rows "$db")"
  db_mtime_before="$(mtime "$db")"
  wal_mtime_before="$(mtime "$wal")"

  sleep "$sample_seconds"

  db_after="$(bytes "$db")"
  wal_after="$(bytes "$wal")"
  rows_after="$(rows "$db")"
  db_mtime_after="$(mtime "$db")"
  wal_mtime_after="$(mtime "$wal")"

  byte_delta=$(( (db_after + wal_after) - (db_before + wal_before) ))
  row_delta=$(( rows_after - rows_before ))
  [[ "$byte_delta" -lt 0 ]] && byte_delta=0
  [[ "$row_delta" -lt 0 ]] && row_delta=0

  mb_per_min="$(awk -v b="$byte_delta" -v s="$sample_seconds" 'BEGIN { printf "%.2f", (b / 1024 / 1024) * 60 / s }')"
  rows_per_min="$(awk -v r="$row_delta" -v s="$sample_seconds" 'BEGIN { printf "%.0f", r * 60 / s }')"
  health_status="$(score "$mb_per_min" "$rows_per_min")"

  printf "%-6s db=%s MB wal=%s MB growth=%s MB/min rows=%s/min path=%s\n" \
    "$health_status" "$(mb "$db_after")" "$(mb "$wal_after")" "$mb_per_min" "$rows_per_min" "$db"

  if [[ "$db_mtime_before" != "$db_mtime_after" || "$wal_mtime_before" != "$wal_mtime_after" ]]; then
    echo "       file changed during sample"
  fi

  level_summary="$(levels "$db" | tr '\n' ' ')"
  [[ -n "$level_summary" ]] && echo "       levels: $level_summary"
done

