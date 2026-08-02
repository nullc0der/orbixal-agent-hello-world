from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_INPUT_PATH = Path("/orbixal/input/input.json")
DEFAULT_OUTPUT_PATH = Path("/orbixal/output/result.json")
SAMPLE_SECRET_NAMES = (
    "HELLO_WORLD_API_KEY",
    "HELLO_WORLD_SIGNING_KEY",
    "HELLO_WORLD_WEBHOOK_TOKEN",
)
RUNTIME_IDENTITY_NAMES = (
    "ORBIXAL_LISTING_ID",
    "ORBIXAL_ARTIFACT_ID",
    "ORBIXAL_MANIFEST_VERSION_ID",
    "ORBIXAL_CONTAINER_VERSION",
    "ORBIXAL_IMAGE_DIGEST",
    "ORBIXAL_WORKLOAD_SLUG",
)
SAMPLE_ENVIRONMENT_DEFAULTS = {
    "HELLO_WORLD_GREETING_PREFIX": "Hello",
    "HELLO_WORLD_GREETING_SUFFIX": "!",
    "HELLO_WORLD_UPPERCASE": "false",
}
TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
FALSE_VALUES = frozenset({"0", "false", "no", "off"})


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


def _sample_runtime_environment() -> dict[str, str]:
    return {
        variable_name: os.environ.get(variable_name, default)
        for variable_name, default in SAMPLE_ENVIRONMENT_DEFAULTS.items()
    }


def _environment_flag(variable_name: str, value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise ValueError(
        f"environment variable '{variable_name}' must be one of: "
        "true, false, 1, 0, yes, no, on, off"
    )


def _log_sample_runtime_environment(environment: dict[str, str]) -> None:
    print(
        json.dumps(
            {
                "event": "sample_runtime_environment",
                "environment": environment,
            },
            separators=(",", ":"),
        )
    )


def _log_sample_runtime_secrets() -> None:
    print(
        json.dumps(
            {
                "event": "sample_runtime_secrets",
                "secrets": {
                    secret_name: os.environ.get(secret_name)
                    for secret_name in SAMPLE_SECRET_NAMES
                },
            },
            separators=(",", ":"),
        )
    )


def _log_runtime_identity() -> None:
    print(
        json.dumps(
            {
                "event": "sample_runtime_identity",
                "runtime": {
                    variable_name: os.environ.get(variable_name)
                    for variable_name in RUNTIME_IDENTITY_NAMES
                },
            },
            separators=(",", ":"),
        )
    )


def main() -> None:
    input_path = _runtime_path("ORBIXAL_INPUT_PATH", DEFAULT_INPUT_PATH)
    output_path = _runtime_path("ORBIXAL_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
    input_value = _read_input(input_path)
    name = input_value["name"].strip()
    environment = _sample_runtime_environment()
    greeting = (
        f"{environment['HELLO_WORLD_GREETING_PREFIX']}, "
        f"{name}{environment['HELLO_WORLD_GREETING_SUFFIX']}"
    )
    if _environment_flag(
        "HELLO_WORLD_UPPERCASE",
        environment["HELLO_WORLD_UPPERCASE"],
    ):
        greeting = greeting.upper()

    _log_runtime_identity()
    _log_sample_runtime_environment(environment)
    _log_sample_runtime_secrets()
    _write_output(output_path, {"greeting": greeting})
    print("Hello-world job completed successfully.")


if __name__ == "__main__":
    main()
