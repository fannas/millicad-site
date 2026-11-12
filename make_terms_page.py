"""Builds terms.html from the panel's terms.md so the website and the app always show the same text."""
import html, pathlib, re

here = pathlib.Path(__file__).parent
src = (here.parent / "App" / "madcad" / "ui" / "terms.md").read_text(encoding="utf-8")

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s

out, lines, i = [], src.splitlines(), 0
while i < len(lines):
    l = lines[i]
    m = re.match(r"^(#{1,4})\s+(.*)", l)
    if m:
        out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>"); i += 1; continue
    if re.match(r"^\s*[-*]\s+", l):
        items = []
        while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
            items.append(re.sub(r"^\s*[-*]\s+", "", lines[i])); i += 1
        out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"); continue
    if not l.strip():
        i += 1; continue
    para = []
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4})\s+|^\s*[-*]\s+", lines[i]):
        para.append(lines[i]); i += 1
    out.append("<p>" + inline(" ".join(para)) + "</p>")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Milli Cad: terms of use, privacy and refunds</title>
<style>
:root{{--bg:#14161a;--text:#e8eaf0;--muted:#9aa3b2;--accent:#f0a500;--line:#2a2f3a}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:28px 20px 60px}}
a{{color:#ffcb47}} h1{{font-size:28px;margin:10px 0 6px}} h2{{font-size:19px;margin:26px 0 6px;color:var(--accent)}}
p,li{{color:var(--text)}} .back{{display:inline-block;margin-bottom:10px;color:var(--muted);text-decoration:none}}
hr{{border:0;border-top:1px solid var(--line);margin:30px 0}} .foot{{color:var(--muted);font-size:14px}}
</style></head><body><div class="wrap">
<a class="back" href="index.html">&larr; Milli Cad</a>
{chr(10).join(out)}
<hr><p class="foot">Milli Cad is made by Polytimos, Midrand, South Africa. Contact: <a href="mailto:info@fanna.org">info@fanna.org</a>.</p>
</div></body></html>
"""
(here / "terms.html").write_text(page, encoding="utf-8")
print("terms.html written,", len(out), "blocks")
