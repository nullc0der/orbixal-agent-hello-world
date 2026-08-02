# Orbixal Hello World Agent

A minimal Orbixal agent intended to be scheduled as a runner `job`. It reads a JSON object from the Runner-provided input path and writes its JSON result to the Runner-provided output path.

## Runtime Secrets

The manifest declares three sample runtime secrets:

- `HELLO_WORLD_API_KEY` — required
- `HELLO_WORLD_SIGNING_KEY` — required
- `HELLO_WORLD_WEBHOOK_TOKEN` — optional

Orbixal injects selected secret values into the matching environment variables at runtime. For manual end-to-end testing, this sample writes one `sample_runtime_secrets` JSON event containing all three raw values to standard output. A missing optional value is logged as `null`.

Do not copy this logging behavior into a real workload. Runtime logs are not a safe place for production secrets.

The sample also writes a `sample_runtime_identity` event showing the canonical runtime identity injected by Runner: listing ID, artifact ID, manifest version ID, container version, image digest, and workload slug.

## Run Locally

```bash
work_dir="$(mktemp -d)"
cp -R examples "$work_dir"
mkdir "$work_dir/output"
ORBIXAL_INPUT_PATH="$work_dir/examples/input.json" \
ORBIXAL_OUTPUT_PATH="$work_dir/output/result.json" \
python main.py
cat "$work_dir/output/result.json"
```

## Run With Docker

```bash
docker build -t orbixal-hello-world-agent .
work_dir="$(mktemp -d)"
mkdir "$work_dir/input" "$work_dir/output"
cp examples/input.json "$work_dir/input/input.json"
docker run --rm \
  -v "$work_dir/input:/orbixal/input:ro" \
  -v "$work_dir/output:/orbixal/output" \
  orbixal-hello-world-agent
cat "$work_dir/output/result.json"
```

The Runner injects `ORBIXAL_INPUT_PATH` and `ORBIXAL_OUTPUT_PATH`. The workload falls back to the JSON v1 contract paths `/orbixal/input/input.json` and `/orbixal/output/result.json`.

Standard output and standard error are logs only. The job result is the single JSON document written to the output path.
