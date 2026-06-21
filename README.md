# UEFN MCP

Control Unreal Editor for Fortnite (UEFN) with Claude via the Model Context Protocol.

Claude can place actors, move things around, run Python inside UEFN, and more — all from chat.

---

## How it works

```
Claude <--> mcp_server.py (MCP) <--> uefn_bridge.py (HTTP inside UEFN)
```

- **`uefn_bridge.py`** runs inside UEFN's Python console. It hosts a tiny HTTP server on `localhost:8765` ticked from Unreal's Slate pre-tick callback, so it can safely call Unreal APIs.
- **`mcp_server.py`** is the MCP server Claude connects to. It forwards tool calls to the bridge over HTTP.

---

## Setup

### 1. Prerequisites

- [Unreal Editor for Fortnite (UEFN)](https://dev.epicgames.com/documentation/en-us/uefn/get-started-in-uefn) installed
- Python 3.9+
- [Claude Code](https://claude.ai/code) (CLI or desktop app)

### 2. Install Python dependencies

```bash
pip install mcp requests
```

### 3. Clone this repo

```bash
git clone https://github.com/ceeano/uefn_mcp.git
cd uefn_mcp
```

### 4. Start the MCP server

```bash
python mcp_server.py
```

Leave this running in the background.

### 5. Load the bridge inside UEFN

Open your UEFN project, then open the **Python Console** (Window → Developer Tools → Python Console) and run:

```python
exec(open(r"C:\path\to\uefn_mcp\uefn_bridge.py").read())
```

Replace `C:\path\to\uefn_mcp` with where you cloned the repo. You should see:

```
[MCP Bridge] Started on http://localhost:8765
```

> **Note:** You need to re-run this every time you reopen UEFN. If you re-run it in the same session, it automatically cleans up the previous instance first.

### 6. Add the MCP to Claude Code

In your Claude Code settings (`~/.claude/settings.json` or via the app), add:

```json
{
  "mcpServers": {
    "uefn": {
      "command": "python",
      "args": ["C:\\path\\to\\uefn_mcp\\mcp_server.py"]
    }
  }
}
```

### 7. Test it

Ask Claude: *"ping UEFN"* — it should return the engine version.

---

## Available tools

| Tool | Description |
|------|-------------|
| `ping` | Check bridge is running, get engine version |
| `get_actors` | List all actors in the level |
| `get_selected_actors` | Get currently selected actors |
| `place_actor` | Spawn an actor by asset path at a location |
| `move_actor` | Move an actor to a new location |
| `delete_actor` | Delete an actor |
| `select_actor` | Select an actor in the viewport |
| `run_python` | Execute arbitrary Python inside UEFN |

---

## Troubleshooting

**Bridge not responding:** Restart UEFN and re-run the bridge script. Old background threads from previous sessions can block port 8765.

**`unreal` module not found:** Make sure you're running the bridge inside UEFN's Python console, not a regular Python shell.

**Port already in use:** The bridge script automatically unregisters old tick callbacks and closes the previous server when re-run. If problems persist, restart UEFN.
