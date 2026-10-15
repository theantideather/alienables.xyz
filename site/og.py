#!/usr/bin/env python3
"""Draws the 1200x630 Open Graph card for each page into static/og/. Needs Pillow. Run after editing og text."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "static" / "fonts"
OUT = ROOT / "static" / "og"
PAPER, INK, MUTED, RULE, ACCENT = "#F5F0E6", "#1E1A16", "#5B5248", "#D8CDBB", "#8A3A1E"

CARDS = {
    "home": ("Dentist and health tech founder", "Co-founder of OroCare AI. Founder of the CastleBlock tech community. Solapur and Pune."),
    "about": ("About", "Om Jayant Gurram. Dentist from Solapur and Pune who builds health tech."),
    "work": ("Work", "OroCare AI, dental diagnostic AI. ResQ, AI emergency response for clinics."),
    "community": ("CastleBlock", "The tech community I started in 2022. Solapur chapter led by Aksha Gurram."),
    "speaking": ("Speaking", "World Health Conference, Jio World Centre. Indian Dental Association. More."),
    "writing": ("Writing", "Dental AI, clinic emergencies and building tech communities."),
    "press": ("Press kit", "Approved bios, facts and photos. Copy freely."),
    "contact": ("Contact", "Press, talks, OroCare AI, ResQ and CastleBlock."),
    "404": ("Page not found", "dromgurram.com"),
}


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(draw, text, f, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=f) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


def card(slug, kicker, line):
    im = Image.new("RGB", (1200, 630), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1200, 14], fill=ACCENT)
    d.text((80, 92), kicker.upper(), font=font("source-sans-3-latin-600-normal.woff2", 30), fill=ACCENT)
    d.text((80, 150), "Dr. Om Gurram", font=font("newsreader-latin-600-normal.woff2", 124), fill=INK)
    d.line([80, 330, 1120, 330], fill=RULE, width=2)
    y = 362
    body = font("newsreader-latin-400-normal.woff2", 44)
    for ln in wrap(d, line, body, 1000)[:3]:
        d.text((80, y), ln, font=body, fill=INK)
        y += 60
    d.text((80, 548), "dromgurram.com", font=font("source-sans-3-latin-400-normal.woff2", 30), fill=MUTED)
    im.save(OUT / f"{slug}.png", optimize=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (k, l) in CARDS.items():
        card(slug, k, l)
    icon = Image.new("RGB", (180, 180), ACCENT)
    d = ImageDraw.Draw(icon)
    f = font("newsreader-latin-600-normal.woff2", 92)
    w = d.textlength("OG", font=f)
    d.text(((180 - w) / 2, 30), "OG", font=f, fill=PAPER)
    icon.save(ROOT / "static" / "apple-touch-icon.png", optimize=True)
    print("og cards:", len(CARDS))
