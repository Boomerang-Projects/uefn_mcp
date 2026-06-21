"""
UEFN MCP Server - run this separately, then add it to Claude Code's MCP config.
Requires: pip install mcp requests
"""
import requests
from mcp.server.fastmcp import FastMCP

BASE = "http://localhost:8765"
mcp = FastMCP("uefn")


def _get(path):
    r = requests.get(BASE + path, timeout=10)
    return r.json()


def _post(path, data):
    r = requests.post(BASE + path, json=data, timeout=10)
    return r.json()


@mcp.tool()
def ping() -> dict:
    """Check if UEFN bridge is running and get engine version."""
    return _get("/ping")


@mcp.tool()
def get_actors() -> list:
    """List all actors in the current UEFN level with their names, classes, and locations."""
    return _get("/actors")


@mcp.tool()
def get_selected_actors() -> list:
    """Get the currently selected actors in the UEFN editor."""
    return _get("/selected")


@mcp.tool()
def place_actor(asset_path: str, x: float, y: float, z: float, label: str = "") -> dict:
    """
    Place an actor in the UEFN level.
    asset_path: Unreal asset path e.g. /Game/Devices/ItemSpawner
    x, y, z: World location in Unreal units (cm)
    label: Optional display name for the actor
    """
    return _post("/place_actor", {"asset_path": asset_path, "location": [x, y, z], "label": label})


@mcp.tool()
def move_actor(name: str, x: float, y: float, z: float) -> dict:
    """Move an actor to a new world location. Use the actor's internal name from get_actors()."""
    return _post("/move_actor", {"name": name, "location": [x, y, z]})


@mcp.tool()
def delete_actor(name: str) -> dict:
    """Delete an actor from the level by its internal name."""
    return _post("/delete_actor", {"name": name})


@mcp.tool()
def select_actor(name: str) -> dict:
    """Select an actor in the UEFN editor viewport by its internal name."""
    return _post("/select_actor", {"name": name})


@mcp.tool()
def run_python(code: str) -> dict:
    """
    Execute arbitrary Python code inside UEFN (has access to the unreal module).
    Use for advanced operations not covered by other tools.
    Example: code='import unreal; unreal.log("hello")'
    """
    return _post("/run_python", {"code": code})


if __name__ == "__main__":
    mcp.run()
