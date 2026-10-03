import os
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer

count = 0
CONFIG_KEYS = ["APP_MESSAGE", "APP_ENV", "LOG_LEVEL", "PORT", "DATABASE_HOST"]
SECRET_KEYS = ["DB_USERNAME", "DB_PASSWORD", "API_KEY", "JWT_SECRET", "TLS_PRIVATE_KEY"]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global count
        if self.path == "/favicon.ico":
            self.send_response(204); self.end_headers(); return
        if self.path != "/":
            self.send_response(404); self.end_headers(); return

        count += 1
        message = os.getenv("APP_MESSAGE", "this is 1st deployment")

        def rows(keys):
            return "".join(
                f"<tr><td>{escape(k)}</td><td>{escape(os.getenv(k, ''))}</td></tr>"
                for k in keys
            )

        html = f"""<!doctype html>
<html><head><title>ConfigMap & Secret Demo</title>
<style>
body{{margin:0;background:#f5f7fa;font-family:Arial,sans-serif;color:#222}}
.container{{max-width:1100px;margin:auto;padding:40px 24px}}
.deployment{{text-align:center;font-family:"Comic Sans MS",cursive;font-size:20px;margin-bottom:35px}}
.tables{{display:flex;gap:24px;align-items:flex-start}}
.card{{flex:1;background:white;border-radius:10px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,.08)}}
h2{{margin-top:0;font-size:20px}} table{{width:100%;border-collapse:collapse}}
th,td{{border:1px solid #ddd;padding:10px;text-align:left;word-break:break-word}}
th{{background:#eee}} .refresh{{position:fixed;top:15px;right:20px;color:#555;font-size:14px}}
@media(max-width:800px){{.tables{{flex-direction:column}}.card{{width:100%;box-sizing:border-box}}}}
</style></head>
<body>
<div class="refresh">Refresh Count: {count}</div>
<div class="container">
<div class="deployment">{escape(message)}</div>
<div class="tables">
<div class="card"><h2>ConfigMaps</h2>
<table><tr><th>Key</th><th>Value</th></tr>{rows(CONFIG_KEYS)}</table></div>
<div class="card"><h2>Secrets</h2>
<table><tr><th>Key</th><th>Value</th></tr>{rows(SECRET_KEYS)}</table></div>
</div></div></body></html>"""
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting app on port {port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
