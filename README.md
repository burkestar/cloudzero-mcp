# Cloudzero Model Context Protocol (MCP) server

Talk to your cloud cost data in Cloudzero from a Large Language Model (LLM).

Uses [CloudZero v2 API](https://docs.cloudzero.com/reference/introduction).

## Setup

Install [uv](https://docs.astral.sh/uv/)

```bash
uv init
uv add "mcp[cli]"
```

## Run

Generate your [CloudZero API key](https://app.cloudzero.com/organization/api-keys).

```bash
export CLOUDZERO_API_KEY=YOUR_SECRET_KEY
```

Run the server:

```bash
uv run mcp
```

Install in Claude Desktop:

```bash
uv run mcp install server.py
```

Check your `claude_desktop_config.json` looks like:

```json
    "Demo": {
      "command": "/Users/USERNAME/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/Users/USERNAME/workspace/open_source/cloudzero-mcp/server.py"
      ]
    }
```

Restart Claude Desktop and ask "what tools are available?".

## Debug

Run the MCP development server with an interactive GUI to inspect:

```bash
uv run mcp dev server.py
```
