"""Embed data/fridges.json into src/template.html -> index.html."""
import json, pathlib
root = pathlib.Path(__file__).parent
data = json.loads((root / "data/fridges.json").read_text())
gal = json.loads((root / "data/gallery.json").read_text())
for m in data["models"]:
    if m["id"] in gal:
        m["gallery"] = gal[m["id"]]
    if (root / "img" / f"{m['id']}.jpg").exists():
        m["image"] = f"img/{m['id']}.jpg"
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = (root / "src/template.html").read_text().replace("__DATA__", blob)
(root / "index.html").write_text(html)
print(f"index.html: {len(data['models'])} Modelle, {len(html)//1024} KB")

# Eigenständige Version für GitHub Pages (docs/), ohne claude.ai-Hülle
import shutil
docs = root / "docs"
if docs.exists(): shutil.rmtree(docs)
(docs / "img").mkdir(parents=True)
head = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="robots" content="noindex,nofollow">'
        '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>')
(docs / "index.html").write_text(head + html + "</body></html>")
shutil.copytree(root / "img", docs / "img", dirs_exist_ok=True)
(docs / ".nojekyll").write_text("")
print("docs/ für GitHub Pages geschrieben")
