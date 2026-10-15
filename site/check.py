#!/usr/bin/env python3
"""Checks the built site against the brief. Run after build.py. Exits non-zero on any failure."""
import json
import pathlib
import re
import sys

OUT = pathlib.Path(__file__).resolve().parent / "public"
BANNED = re.compile(r"—|revolutioni[sz]e|leverag|unlock|seamless|delve|game[- ]changer|"
                    r"at the intersection of|fast-paced world|it.s not .{1,40}, it.s", re.I)
REQUIRED = ["name", "alternateName", "jobTitle", "description", "url", "homeLocation", "address",
            "alumniOf", "worksFor", "knowsAbout", "sameAs"]
errors = []

for page in sorted(OUT.rglob("*.html")):
    rel = page.relative_to(OUT)
    s = page.read_text(encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    if not title.startswith("Dr. Om Gurram"):
        errors.append(f"{rel}: title does not start with Dr. Om Gurram: {title}")
    if 'rel="canonical"' not in s:
        errors.append(f"{rel}: no canonical")
    if re.search(r"<script(?![^>]*application/ld\+json)", s):
        errors.append(f"{rel}: ships JavaScript")
    og = re.search(r'og:image" content="https://dromgurram.com(/og/[^"]+)"', s)
    if not og or not (OUT / og.group(1).lstrip("/")).exists():
        errors.append(f"{rel}: og image missing")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    try:
        graph = json.loads(blocks[0])["@graph"]
    except Exception as e:  # noqa: BLE001
        errors.append(f"{rel}: JSON-LD invalid: {e}")
        continue
    person = next((n for n in graph if n.get("@type") == "Person"), None)
    if not person:
        errors.append(f"{rel}: no Person")
    else:
        missing = [k for k in REQUIRED if k not in person]
        if missing:
            errors.append(f"{rel}: Person missing {missing}")
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", s, flags=re.S))
    for m in BANNED.finditer(text):
        errors.append(f"{rel}: banned copy: {m.group(0)!r}")

for f in ["robots.txt", "sitemap.xml", "llms.txt", "favicon.svg"]:
    if not (OUT / f).exists():
        errors.append(f"missing {f}")
robots = (OUT / "robots.txt").read_text()
for bot in ["GPTBot", "OAI-SearchBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]:
    if f"User-agent: {bot}\nAllow: /" not in robots:
        errors.append(f"robots.txt does not allow {bot}")
if BANNED.search((OUT / "llms.txt").read_text()):
    errors.append("llms.txt: banned copy")

print("\n".join(errors) or "check: all pages pass")
sys.exit(1 if errors else 0)
