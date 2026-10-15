#!/usr/bin/env python3
"""Tells Bing, Yandex, Seznam and other IndexNow engines that every sitemap URL changed. Run after deploy."""
import json
import pathlib
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import INDEXNOW_KEY, OUT, SITE  # noqa: E402

urls = (OUT / "indexnow-urls.txt").read_text().split()
body = json.dumps({"host": SITE.split("//")[1], "key": INDEXNOW_KEY,
                   "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow:", r.status, f"{len(urls)} urls")
