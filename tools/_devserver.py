import http.server, socketserver, base64, pathlib, urllib.parse
ROOT = pathlib.Path.cwd()
ALLOW = {"world-eaters-classic-blood/images", "slaves-to-darkness-paint-guide/images"}
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml; charset=utf-8'}
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel = (q.get("path") or [""])[0]
        target = (ROOT / rel).resolve()
        if not str(target).startswith(str(ROOT)) or str(target.parent.relative_to(ROOT)) not in ALLOW:
            self.send_error(403, "path not allowed"); return
        body = self.rfile.read(int(self.headers["Content-Length"]))
        s = body.decode()
        if "," in s[:64]:
            s = s.split(",", 1)[1]
        target.write_bytes(base64.b64decode(s))
        self.send_response(200); self.send_header("Content-Type", "text/plain")
        self.end_headers(); self.wfile.write(f"saved {rel} {target.stat().st_size}B".encode())
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
print("dev server on 8768")
socketserver.TCPServer(("127.0.0.1", 8768), H).serve_forever()
