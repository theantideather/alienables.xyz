#!/usr/bin/env python3
"""Builds the static site into site/public. Standard library only, no JavaScript shipped.

Each file in site/pages/ starts with one line of JSON metadata inside an HTML comment:
<!--{"slug": "/about", "title": "About", "description": "...", "schema": ["profile"]}-->
"""
import datetime
import html
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / "pages"
STATIC = ROOT / "static"
OUT = ROOT / "public"

SITE = "https://dromgurram.com"
NAME = "Dr. Om Gurram"
ONE_LINE = ("Dr. Om Gurram is a dentist and health tech founder from Solapur and Pune, "
            "co-founder of OroCare AI and founder of the CastleBlock tech community.")
INDEXNOW_KEY = "2f0599b5823ecf0ee9ff0acaff92259f"
CONTACT_EMAIL = None  # set once hello@dromgurram.com forwarding works (see DEPLOY.md)
HEADSHOT = None       # set to "/img/dr-om-gurram-headshot.jpg" once the real photo is added

# Every profile that should point back here. Order is the order shown in the footer.
PROFILES = [
    ("LinkedIn", "https://www.linkedin.com/in/om-gurram-071a81334/"),
    ("X", "https://x.com/omg14doteth"),
    ("Instagram", "https://www.instagram.com/theantideather/"),
    ("GitHub", "https://github.com/theantideather"),
    ("Medium", "https://medium.com/@om.g"),
    ("Linktree", "https://linktr.ee/om.g"),
    ("Telegram", "https://t.me/theantideather"),
]

NAV = [("/about", "About"), ("/work", "Work"), ("/community", "Community"),
       ("/speaking", "Speaking"), ("/writing", "Writing"), ("/press", "Press"), ("/contact", "Contact")]

PERSON_ID = SITE + "/#person"
OROCARE_ID = SITE + "/work#orocare"
RESQ_ID = SITE + "/work#resq"
CASTLEBLOCK_ID = SITE + "/community#castleblock"


def person():
    p = {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": NAME,
        "honorificPrefix": "Dr.",
        "givenName": "Om",
        "additionalName": "Jayant",
        "familyName": "Gurram",
        "alternateName": ["Om Gurram", "Om Jayant Gurram", "Dr. Gurram", "Dr. Om Jayant Gurram"],
        "jobTitle": ["Dentist", "Co-founder and Technical Director, OroCare AI"],
        "description": ONE_LINE,
        "url": SITE + "/",
        "homeLocation": [
            {"@type": "Place", "name": "Solapur, Maharashtra, India"},
            {"@type": "Place", "name": "Pune, Maharashtra, India"},
        ],
        "address": [
            {"@type": "PostalAddress", "addressLocality": "Solapur", "addressRegion": "Maharashtra", "addressCountry": "IN"},
            {"@type": "PostalAddress", "addressLocality": "Pune", "addressRegion": "Maharashtra", "addressCountry": "IN"},
        ],
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Sinhgad Dental College and Hospital, Pune"},
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree",
                          "name": "Bachelor of Dental Surgery (BDS)",
                          "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Maharashtra University of Health Sciences"}},
        "worksFor": [{"@id": OROCARE_ID}, {"@id": RESQ_ID}],
        "knowsAbout": ["Dentistry", "Oral diagnostics", "Dental radiology", "Medical AI",
                       "Multi-agent systems", "Community building", "Web3"],
        "sameAs": [u for _, u in PROFILES],
    }
    if HEADSHOT:
        p["image"] = SITE + HEADSHOT
    return p


def orgs():
    """Short references so worksFor and founder resolve on every page. Full detail lives on /work and /community."""
    return [
        {"@type": "Organization", "@id": OROCARE_ID, "name": "OroCare AI", "url": "https://orocare.live/",
         "sameAs": ["https://instagram.com/orocare.ai"]},
        {"@type": "Organization", "@id": RESQ_ID, "name": "ResQ", "legalName": "Life ResQ Healthcare Systems LLP",
         "url": "https://resq.gitbook.io/resq-whitepaper"},
        {"@type": "Organization", "@id": CASTLEBLOCK_ID, "name": "CastleBlock",
         "url": "https://linktr.ee/castlexblock", "founder": {"@id": PERSON_ID}},
    ]


def org_detail(kind):
    if kind == "orocare":
        return {"@type": "Organization", "@id": OROCARE_ID, "name": "OroCare AI", "url": "https://orocare.live/",
                "description": "Dental diagnostic AI: imaging analysis for X-rays, OPGs and cephalograms, VR clinical training, and a multilingual voice interface for rural patients.",
                "founder": {"@id": PERSON_ID}, "sameAs": ["https://instagram.com/orocare.ai"],
                "areaServed": "IN", "knowsAbout": ["Dental radiology", "Medical AI", "Virtual reality"]}
    if kind == "resq":
        return {"@type": "Organization", "@id": RESQ_ID, "name": "ResQ", "legalName": "Life ResQ Healthcare Systems LLP",
                "description": "AI emergency response for clinics: a desk unit with a talking avatar that guides the doctor through a medical emergency, backed by specialist AI agents, with ambulance and hospital alerts.",
                "url": "https://resq.gitbook.io/resq-whitepaper",
                "founder": [{"@id": PERSON_ID}, {"@type": "Person", "name": "Dr. Sameer Patil"}],
                "sameAs": ["https://youtu.be/W8I0IFj6fjA"]}
    if kind == "castleblock":
        return {"@type": "Organization", "@id": CASTLEBLOCK_ID, "name": "CastleBlock",
                "alternateName": "CastleBlock tech community",
                "description": "A developer community founded by Dr. Om Gurram in March 2022, with city chapters including Solapur.",
                "url": "https://linktr.ee/castlexblock", "foundingDate": "2022-03",
                "founder": {"@id": PERSON_ID},
                "location": [{"@type": "Place", "name": "Solapur, Maharashtra, India"},
                             {"@type": "Place", "name": "Pune, Maharashtra, India"}],
                "sameAs": ["https://instagram.com/castlexblock", "https://linktr.ee/castlexblock"]}
    raise ValueError(kind)


def jsonld(meta, url):
    page_type = "ProfilePage" if "profile" in meta.get("schema", []) else "WebPage"
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
         "publisher": {"@id": PERSON_ID}, "inLanguage": "en-IN"},
        {"@type": page_type, "@id": url + "#page", "url": url, "name": page_title(meta),
         "isPartOf": {"@id": SITE + "/#website"},
         ("mainEntity" if page_type == "ProfilePage" else "about"): {"@id": PERSON_ID},
         "inLanguage": "en-IN"},
        person(),
    ]
    detailed = {k for k in meta.get("schema", []) if k in ("orocare", "resq", "castleblock")}
    for o in orgs():
        key = {OROCARE_ID: "orocare", RESQ_ID: "resq", CASTLEBLOCK_ID: "castleblock"}[o["@id"]]
        graph.append(org_detail(key) if key in detailed else o)
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")


def page_title(meta):
    return NAME if meta["slug"] == "/" else f"{NAME} | {meta['title']}"


def og_name(slug):
    return "home" if slug == "/" else slug.strip("/").replace("/", "-")


def render(meta, body):
    slug = meta["slug"]
    url = SITE + ("/" if slug == "/" else slug)
    title = page_title(meta)
    if meta.get("htmltitle"):
        title = meta["htmltitle"]
    desc = html.escape(meta["description"], quote=True)
    og = f"{SITE}/og/{og_name(slug)}.png"
    robots = '<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    current = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{current if h == slug else ""}>{t}</a>' for h, t in NAV)
    profiles = "".join(f'<li><a href="{u}" rel="me">{n}</a></li>' for n, u in PROFILES)
    year = datetime.date.today().year
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{NAME}">
{robots}
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/newsreader-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<meta name="theme-color" content="#F5F0E6">
<meta property="og:type" content="{'profile' if 'profile' in meta.get('schema', []) else 'website'}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(title)}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@omg14doteth">
<meta name="twitter:creator" content="@omg14doteth">
<script type="application/ld+json">
{jsonld(meta, url)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
<a class="wordmark" href="/">{NAME}</a>
<nav aria-label="Main">{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="site">
<p>{ONE_LINE}</p>
<ul class="profiles">{profiles}</ul>
<p class="small">&copy; {year} {NAME}. Solapur and Pune, Maharashtra, India.</p>
</footer>
</body>
</html>
"""


def read_pages():
    pages = []
    for f in sorted(PAGES.glob("*.html")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"<!--(\{.*?\})-->\n", text)
        if not m:
            raise SystemExit(f"{f.name}: missing metadata comment on line 1")
        pages.append((json.loads(m.group(1)), text[m.end():]))
    return pages


def out_path(slug):
    if slug == "/":
        return OUT / "index.html"
    if slug == "/404":
        return OUT / "404.html"
    return OUT / slug.strip("/") / "index.html"


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    pages = read_pages()
    today = datetime.date.today().isoformat()
    urls = []
    for meta, body in pages:
        p = out_path(meta["slug"])
        p.parent.mkdir(parents=True, exist_ok=True)
        email = (f'<p>Email: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>'
                 if CONTACT_EMAIL else "")
        p.write_text(render(meta, body.replace("<!--EMAIL-->", email)), encoding="utf-8")
        if not meta.get("noindex"):
            urls.append(SITE + ("/" if meta["slug"] == "/" else meta["slug"]))

    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")

    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]
    (OUT / "robots.txt").write_text(
        "# Search engines and AI assistants are welcome here.\n"
        + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
        + "User-agent: *\nAllow: /\n\n"
        + f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    (OUT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (OUT / "indexnow-urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"built {len(pages)} pages, {len(urls)} in sitemap -> {OUT}")
    if not CONTACT_EMAIL:
        print("note: CONTACT_EMAIL not set, /contact and /press show profile links only")
    if not HEADSHOT:
        print("note: HEADSHOT not set, Person JSON-LD has no image yet")


if __name__ == "__main__":
    main()
