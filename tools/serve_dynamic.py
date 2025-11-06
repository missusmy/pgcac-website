import os
import json
import mimetypes
import sys
import importlib
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import jinja2

ROOT = os.path.abspath(os.getcwd())
SRC = ROOT
TEMPLATES_DIR = os.path.join(SRC, "templates")
PAGES_PREFIX = "pages"
STATIC_DIR = os.path.join(SRC, "static")
PORT = 8000
HOST = "localhost"  # bind to localhost so assets referenced by hostname resolve

# Try to import deploystatic helpers (filters/context) to match static build
ds = None
global_filters = {}
_external_load_context = None
try:
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    ds = importlib.import_module("tools.deploystatic")
    global_filters = getattr(ds, "global_filters", {}) or {}
    _external_load_context = getattr(ds, "load_context", None)
except Exception:
    ds = None
    global_filters = {}
    _external_load_context = None

# Use sandboxed environment when available to mirror deploystatic
EnvClass = getattr(jinja2.sandbox, "SandboxedEnvironment", jinja2.Environment)
env = EnvClass(
    loader=jinja2.FileSystemLoader([TEMPLATES_DIR]),
    autoescape=True,
    auto_reload=True
)
env.filters.update(global_filters)


def _local_load_context():
    ctx = {}
    try:
        path = os.path.join(TEMPLATES_DIR, "context.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf8") as f:
                ctx.update(json.load(f))
        override = os.path.join(TEMPLATES_DIR, "context.override.json")
        if os.path.exists(override):
            with open(override, "r", encoding="utf8") as f:
                ctx.update(json.load(f))
    except Exception:
        pass
    return ctx


def load_context():
    # Prefer the deploystatic loader if present, fall back to local loader
    if _external_load_context:
        try:
            return _external_load_context()
        except TypeError:
            try:
                return _external_load_context(None)
            except Exception:
                return _local_load_context()
        except Exception:
            return _local_load_context()
    return _local_load_context()


class Handler(BaseHTTPRequestHandler):
    def _send_common_no_cache(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def do_GET(self):
        # strip query
        path = self.path.split("?", 1)[0]

        # If request targets /static/... serve from STATIC_DIR directly
        if path.startswith("/static/"):
            rel = path[len("/static/"):]
            fs_path = os.path.join(STATIC_DIR, rel)
            if os.path.isdir(fs_path):
                fs_path = os.path.join(fs_path, "index.html")
            if os.path.exists(fs_path) and os.path.isfile(fs_path):
                ctype, _ = mimetypes.guess_type(fs_path)
                if not ctype:
                    ctype = "application/octet-stream"
                try:
                    with open(fs_path, "rb") as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", ctype)
                    self._send_common_no_cache()
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                except Exception:
                    pass
            # fall through to 404 if not found

        # Normalize to template candidates under templates/pages/
        if path.endswith("/"):
            candidates = [
                os.path.join(PAGES_PREFIX, path.lstrip("/") + "index.html"),
                os.path.join(PAGES_PREFIX, path.lstrip("/") + "index")
            ]
        else:
            candidates = [
                os.path.join(PAGES_PREFIX, path.lstrip("/") + ".html"),
                os.path.join(PAGES_PREFIX, path.lstrip("/"))
            ]

        for cand in candidates:
            try:
                tmpl = env.get_template(cand)
                context = load_context()
                rendered = tmpl.render(**context)
                body = rendered.encode("utf8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self._send_common_no_cache()
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            except jinja2.exceptions.TemplateNotFound:
                continue
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._send_common_no_cache()
                self.end_headers()
                self.wfile.write(f"Template render error: {e}".encode("utf8"))
                return

        # Not found
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self._send_common_no_cache()
        self.end_headers()
        self.wfile.write(b"Not found")


if __name__ == "__main__":
    print(f"Serving dynamic site on http://{HOST}:{PORT} (templates from {TEMPLATES_DIR})")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("Stopped.")