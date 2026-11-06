"""Inline vendor/three.min.js into src/app.html and write index.html (single self-contained file)."""
from pathlib import Path
root = Path(__file__).parent
app = (root / "src" / "app.html").read_text(encoding="utf-8")
three = (root / "vendor" / "three.min.js").read_text(encoding="utf-8")
assert "/*THREE*/" in app, "placeholder missing"
(root / "index.html").write_text(app.replace("/*THREE*/", three), encoding="utf-8")
print("wrote index.html")
