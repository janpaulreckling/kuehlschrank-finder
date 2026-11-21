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
