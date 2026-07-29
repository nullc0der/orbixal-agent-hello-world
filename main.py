from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_INPUT_PATH = Path("/orbixal/input/input.json")
DEFAULT_OUTPUT_PATH = Path("/orbixal/output/result.json")


def _runtime_path(environment_name: str, default: Path) -> Path:
    value = os.environ.get(environment_name, "").strip()
    return Path(value) if value else default


def _read_input(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")

    name = value.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("input field 'name' must be a non-empty string")

    return value


def _write_output(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.tmp")
    temporary_path.write_text(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def main() -> None:
    input_path = _runtime_path("ORBIXAL_INPUT_PATH", DEFAULT_INPUT_PATH)
    output_path = _runtime_path("ORBIXAL_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
    input_value = _read_input(input_path)
    name = input_value["name"].strip()

    _write_output(output_path, {"greeting": f"Hello, {name}!"})
    print("Hello-world job completed successfully.")


if __name__ == "__main__":
    main()
