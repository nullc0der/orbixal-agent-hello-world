# Orbixal Hello World Agent

A minimal Orbixal agent intended to be scheduled as a runner `job`. It prints a message and exits with status code `0`.

## Run Locally

```bash
./main.sh
```

## Run With Docker

```bash
docker build -t orbixal-hello-world-agent .
docker run --rm orbixal-hello-world-agent
```

To customize the output:

```bash
docker run --rm -e ORBIXAL_HELLO_MESSAGE="Hello from a runner job" orbixal-hello-world-agent
```
