#!/bin/zsh
set -euo pipefail

project="${1:-$PWD}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
script_dir="${0:A:h}"

current_warn_kb="${CURRENT_WARN_KB:-10}"
brief_warn_kb="${BRIEF_WARN_KB:-20}"
memory_file_warn_kb="${MEMORY_FILE_WARN_KB:-100}"

bytes() {
  local file="$1"
  stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0
}

kb() {
  awk -v b="$1" 'BEGIN { printf "%.1f", b / 1024 }'
}

label_size() {
  local file="$1"
  local limit_kb="$2"
  local b k
  b="$(bytes "$file")"
  k="$(kb "$b")"
  awk -v k="$k" -v limit="$limit_kb" 'BEGIN { exit !(k > limit) }' && \
    printf "WARN  %8s KB  %s\n" "$k" "$file" || \
    printf "OK    %8s KB  %s\n" "$k" "$file"
}

echo "Computer Use session hygiene"
echo "Project: $project"
echo

if [[ -d "$project/.codex-memory" ]]; then
  echo "Project memory entry files:"
  [[ -f "$project/.codex-memory/current.md" ]] && label_size "$project/.codex-memory/current.md" "$current_warn_kb"
  if [[ -d "$project/.codex-memory/tasks/active" ]]; then
    find "$project/.codex-memory/tasks/active" -name brief.md -type f -print | while read -r brief; do
      label_size "$brief" "$brief_warn_kb"
    done
  fi
  echo
  echo "Large memory files:"
  find "$project/.codex-memory" -type f -size +"${memory_file_warn_kb}"k -print 2>/dev/null | while read -r file; do
    label_size "$file" "$memory_file_warn_kb"
  done
else
  echo "WARN  No .codex-memory directory found. Create one before long Computer Use work."
fi

echo
echo "Codex session health:"
if [[ -f "$codex_home/skills/codex-session-continuity/scripts/session-health.zsh" ]]; then
  zsh "$codex_home/skills/codex-session-continuity/scripts/session-health.zsh"
else
  echo "WARN  session-health.zsh not found under $codex_home"
fi

echo
echo "Codex log write health:"
if [[ -f "$script_dir/codex-log-write-health.zsh" ]]; then
  zsh "$script_dir/codex-log-write-health.zsh"
else
  echo "WARN  codex-log-write-health.zsh not found next to project-session-hygiene.zsh"
fi

