#!/usr/bin/env python3
"""Render the Awesome DeepSeek Integrations list as a small web app.

This lets the repository run as a Hugging Face Docker Space with Spaces Dev
Mode support. The English README is rendered to HTML at ``/`` and the other
translations are available under their own routes. Static files in ``docs/``
(images, etc.) are served directly.

Edit ``README*.md`` and hit Refresh in the Dev Mode panel to see changes.
"""

import http.server
import os
import re

import markdown

PORT = int(os.environ.get("PORT", "7860"))
HERE = os.path.dirname(os.path.abspath(__file__))

# Route -> markdown file. The first entry is the homepage.
LANGUAGES = [
    ("/", "README.md", "English"),
    ("/cn", "README_cn.md", "简体中文"),
    ("/zh_tw", "README_zh_tw.md", "繁體中文"),
    ("/ja", "README_ja.md", "日本語"),
    ("/es", "README_es.md", "Español"),
]
ROUTES = {route: filename for route, filename, _ in LANGUAGES}

NAV = " · ".join(
    f'<a href="{route}">{label}</a>' for route, _, label in LANGUAGES
)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome DeepSeek Integrations</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica,
         Arial, sans-serif; line-height: 1.6; color: #1f2328;
         max-width: 980px; margin: 0 auto; padding: 24px; }}
  nav {{ position: sticky; top: 0; background: #fff; padding: 12px 0;
         border-bottom: 1px solid #d0d7de; margin-bottom: 24px; }}
  nav a {{ margin-right: 4px; text-decoration: none; color: #0969da; }}
  img {{ max-width: 100%; }}
  pre {{ background: #f6f8fa; padding: 16px; overflow: auto; border-radius: 6px; }}
  code {{ background: #f6f8fa; padding: .2em .4em; border-radius: 6px; }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; }}
  th, td {{ border: 1px solid #d0d7de; padding: 6px 13px; }}
  a {{ color: #0969da; }}
</style>
</head>
<body>
<nav>{nav}</nav>
<main class="markdown-body">
{body}
</main>
</body>
</html>
"""

# Strips a leading Hugging Face Space YAML front-matter block so it is not
# rendered into the page body.
_FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def render(md_filename: str) -> bytes:
    with open(os.path.join(HERE, md_filename), encoding="utf-8") as fh:
        text = fh.read()
    text = _FRONT_MATTER.sub("", text, count=1)
    body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "toc", "sane_lists"]
    )
    return PAGE_TEMPLATE.format(nav=NAV, body=body).encode("utf-8")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (http.server API)
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path in ROUTES:
            try:
                data = render(ROUTES[path])
            except OSError:
                self.send_error(404, "Document not found")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        # Fall back to serving static files (e.g. docs/ images).
        super().do_GET()


def main() -> None:
    handler = lambda *a, **k: Handler(*a, directory=HERE, **k)
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), handler)
    print(f"Serving Awesome DeepSeek Integrations on http://0.0.0.0:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
