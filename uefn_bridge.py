"""
UEFN MCP Bridge - single-threaded, ticked from Slate pre-tick callback.
Run via: exec(open(r"C:/Users/Admin/uefn_mcp/uefn_bridge.py").read())
"""
import unreal
import select
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8765

# Unregister any tick callbacks from previous exec() runs
for _old in getattr(unreal, "_bridge_tick_handles", []):
    try:
        unreal.unregister_slate_pre_tick_callback(_old)
    except Exception:
        pass
unreal._bridge_tick_handles = []

# Close previous server if any
_prev = getattr(unreal, "_bridge_server", None)
if _prev:
    try:
        _prev.server_close()
    except Exception:
        pass


def _sub():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


class UEFNHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == "/ping":
                self._ok({"status": "ok", "version": unreal.SystemLibrary.get_engine_version()})
            elif self.path == "/actors":
                self._ok([self._info(a) for a in _sub().get_all_level_actors()])
            elif self.path == "/selected":
                self._ok([self._info(a) for a in _sub().get_selected_level_actors()])
            else:
                self._err(404, "Unknown endpoint")
        except Exception as e:
            self._err(500, str(e))

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if length:
                self.connection.setblocking(True)
                try:
                    raw = b""
                    while len(raw) < length:
                        chunk = self.connection.recv(length - len(raw))
                        if not chunk:
                            break
                        raw += chunk
                finally:
                    self.connection.setblocking(False)
                body = json.loads(raw.decode("utf-8")) if raw else {}
            else:
                body = {}

            if self.path == "/place_actor":
                loc = body.get("location", [0, 0, 0])
                loaded = unreal.EditorAssetLibrary.load_asset(body["asset_path"])
                if not loaded:
                    return self._err(400, f"Asset not found: {body['asset_path']}")
                actor = _sub().spawn_actor_from_object(loaded, unreal.Vector(*loc))
                if not actor:
                    return self._err(500, "Failed to spawn actor")
                if body.get("label"):
                    actor.set_actor_label(body["label"])
                self._ok({"spawned": actor.get_name(), "label": actor.get_actor_label()})

            elif self.path == "/move_actor":
                actor = self._find(body["name"])
                if not actor:
                    return self._err(404, f"Actor not found: {body['name']}")
                actor.set_actor_location(unreal.Vector(*body["location"]), False, False)
                self._ok({"moved": body["name"]})

            elif self.path == "/delete_actor":
                actor = self._find(body["name"])
                if not actor:
                    return self._err(404, f"Actor not found: {body['name']}")
                actor.destroy_actor()
                self._ok({"deleted": body["name"]})

            elif self.path == "/select_actor":
                actor = self._find(body["name"])
                if not actor:
                    return self._err(404, f"Actor not found: {body['name']}")
                sub = _sub()
                sub.select_nothing()
                sub.set_actor_selection_state(actor, True)
                self._ok({"selected": body["name"]})

            elif self.path == "/run_python":
                lines = []
                def _print(*args, **kwargs):
                    lines.append(" ".join(str(a) for a in args))
                code = body.get("code", "")
                globs = {"unreal": unreal, "print": _print, "__builtins__": __builtins__, "open": open}
                try:
                    exec(code, globs)
                except Exception as ex:
                    lines.append("ERROR: " + str(ex))
                self._ok({"output": "\n".join(lines)})

            else:
                self._err(404, "Unknown endpoint")
        except Exception as e:
            self._err(500, str(e))

    def _find(self, name):
        return next((a for a in _sub().get_all_level_actors()
                     if a.get_name() == name or a.get_actor_label() == name), None)

    def _info(self, a):
        loc = a.get_actor_location()
        return {
            "name": a.get_name(),
            "label": a.get_actor_label(),
            "class": a.get_class().get_name(),
            "location": {"x": round(loc.x, 1), "y": round(loc.y, 1), "z": round(loc.z, 1)},
        }

    def _ok(self, data):   self._respond(200, data)
    def _err(self, code, msg): self._respond(code, {"error": msg})

    def _respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a): pass


# Start fresh server
_srv = HTTPServer(("localhost", PORT), UEFNHandler)
_srv.socket.setblocking(False)
unreal._bridge_server = _srv


def _tick(delta):
    try:
        if select.select([_srv.socket], [], [], 0)[0]:
            _srv._handle_request_noblock()
    except Exception as e:
        unreal.log_error(f"[MCP Bridge] {e}")


_handle = unreal.register_slate_pre_tick_callback(_tick)
unreal._bridge_tick_handles.append(_handle)

unreal.log(f"[MCP Bridge] Started on http://localhost:{PORT}")
