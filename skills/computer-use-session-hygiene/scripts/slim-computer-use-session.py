#!/usr/bin/env python3
"""Safely slim Codex JSONL sessions by replacing Computer Use screenshots only.

Default behavior is conservative:
- preserve original file
- write to a new output path
- replace screenshots from Computer Use tool outputs and MCP event logs
- preserve user/assistant text, project state, decisions, output paths, and non-Computer Use images
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TRANSPARENT_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)
TRANSPARENT_PNG_DATA_URL = f"data:image/png;base64,{TRANSPARENT_PNG_BASE64}"

COMPUTER_USE_TOOLS = {
    "get_app_state",
    "click",
    "press_key",
    "type_text",
    "scroll",
    "set_value",
    "drag",
    "perform_secondary_action",
    "select_text",
}

DATA_IMAGE_RE = re.compile(r"^data:image/(png|jpeg|jpg|webp);base64,", re.I)
RAW_IMAGE_PREFIXES = ("/9j/", "iVBOR", "UklGR")


def is_data_url_image(value: Any) -> bool:
    return isinstance(value, str) and bool(DATA_IMAGE_RE.match(value))


def is_raw_image_base64(value: Any) -> bool:
    return isinstance(value, str) and len(value) > 256 and value.startswith(RAW_IMAGE_PREFIXES)


def maybe_computer_use_tool_name(name: str | None) -> bool:
    if not name:
        return False
    short = name.rsplit(".", 1)[-1]
    short = short.rsplit("__", 1)[-1]
    return short in COMPUTER_USE_TOOLS


def replace_images_in_computer_use_output(payload: dict[str, Any], stats: Counter) -> None:
    output = payload.get("output")
    if not isinstance(output, list):
        return
    for item in output:
        if not isinstance(item, dict):
            continue
        if is_data_url_image(item.get("image_url")):
            original_len = len(item["image_url"])
            item["image_url"] = TRANSPARENT_PNG_DATA_URL
            item["detail"] = "low"
            stats["response_images_replaced"] += 1
            stats["bytes_removed_estimate"] += max(0, original_len - len(TRANSPARENT_PNG_DATA_URL))


def replace_images_in_computer_use_event(payload: dict[str, Any], stats: Counter) -> None:
    invocation = payload.get("invocation")
    if not isinstance(invocation, dict):
        return
    if invocation.get("server") != "computer-use":
        return
    if not maybe_computer_use_tool_name(invocation.get("tool")):
        return

    result = payload.get("result")
    if not isinstance(result, dict):
        return
    ok = result.get("Ok")
    if not isinstance(ok, dict):
        return
    content = ok.get("content")
    if not isinstance(content, list):
        return

    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "image" and is_raw_image_base64(item.get("data")):
            original_len = len(item["data"])
            item["data"] = TRANSPARENT_PNG_BASE64
            item["mimeType"] = "image/png"
            stats["event_images_replaced"] += 1
            stats["bytes_removed_estimate"] += max(0, original_len - len(TRANSPARENT_PNG_BASE64))


def slim_file(input_path: Path, output_path: Path | None, dry_run: bool) -> Counter:
    call_names: dict[str, str] = {}
    stats: Counter = Counter()

    out_fh = None
    if not dry_run:
        if output_path is None:
            raise SystemExit("--output is required unless --dry-run is used")
        if output_path.exists():
            raise SystemExit(f"Refusing to overwrite existing output: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        out_fh = output_path.open("w", encoding="utf-8")

    try:
        with input_path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                stats["lines"] += 1
                stats["input_bytes"] += len(line.encode("utf-8", "replace"))
                try:
                    obj = json.loads(line)
                except Exception:
                    stats["json_parse_errors"] += 1
                    if out_fh:
                        out_fh.write(line)
                    continue

                obj_type = obj.get("type")
                payload = obj.get("payload")
                if isinstance(payload, dict):
                    payload_type = payload.get("type")

                    if obj_type == "response_item" and payload_type in {"function_call", "custom_tool_call"}:
                        call_id = payload.get("call_id") or payload.get("id")
                        name = payload.get("name") or payload.get("recipient_name")
                        if isinstance(call_id, str) and isinstance(name, str):
                            call_names[call_id] = name

                    elif obj_type == "response_item" and payload_type == "function_call_output":
                        call_id = payload.get("call_id")
                        name = call_names.get(call_id, "")
                        if maybe_computer_use_tool_name(name):
                            replace_images_in_computer_use_output(payload, stats)
                        elif "data:image/" in line:
                            stats["non_computer_use_images_preserved"] += line.count("data:image/")

                    elif obj_type == "event_msg" and payload_type == "mcp_tool_call_end":
                        replace_images_in_computer_use_event(payload, stats)

                if out_fh:
                    out_line = json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
                    stats["output_bytes"] += len(out_line.encode("utf-8", "replace"))
                    out_fh.write(out_line)
                elif dry_run:
                    out_line = json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
                    stats["estimated_output_bytes"] += len(out_line.encode("utf-8", "replace"))
    finally:
        if out_fh:
            out_fh.close()

    return stats


def validate_jsonl(path: Path) -> int:
    errors = 0
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                json.loads(line)
            except Exception:
                errors += 1
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Slim Computer Use screenshots from a Codex JSONL session.")
    parser.add_argument("input", type=Path, help="Input Codex JSONL session file")
    parser.add_argument("--output", type=Path, help="Output slim JSONL path")
    parser.add_argument("--dry-run", action="store_true", help="Report what would be replaced without writing output")
    parser.add_argument("--validate", action="store_true", help="Validate output JSONL after writing")
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    if not args.dry_run and not args.output:
        raise SystemExit("--output is required unless --dry-run is used")

    stats = slim_file(args.input, args.output, args.dry_run)

    print("Computer Use session slim report")
    print(f"input={args.input}")
    if args.output:
        print(f"output={args.output}")
    print(f"dry_run={args.dry_run}")
    print(f"lines={stats['lines']}")
    print(f"input_mb={stats['input_bytes'] / 1024 / 1024:.1f}")
    key = "estimated_output_bytes" if args.dry_run else "output_bytes"
    if stats[key]:
        print(f"output_mb={stats[key] / 1024 / 1024:.1f}")
    print(f"response_images_replaced={stats['response_images_replaced']}")
    print(f"event_images_replaced={stats['event_images_replaced']}")
    print(f"non_computer_use_images_preserved={stats['non_computer_use_images_preserved']}")
    print(f"bytes_removed_estimate_mb={stats['bytes_removed_estimate'] / 1024 / 1024:.1f}")
    print(f"json_parse_errors={stats['json_parse_errors']}")

    if args.validate and args.output:
        errors = validate_jsonl(args.output)
        print(f"output_json_parse_errors={errors}")
        if errors:
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

