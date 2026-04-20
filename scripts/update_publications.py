#!/usr/bin/env python3
"""
Update publications.json from Google Scholar.

Usage:
    pip install scholarly
    python scripts/update_publications.py

Outputs publications.json in the repo root.
Each entry: { title, authors, year, venue, venue_abbr, url }

Run this locally whenever you want to refresh the publication list.
"""

import json
import re
import sys
import time
from pathlib import Path

SCHOLAR_ID = "30e95fEAAAAJ"
OUTPUT = Path(__file__).parent.parent / "publications.json"

# ── Venue abbreviation map ────────────────────────────────────────────────────
# Keys are substrings to match (case-insensitive) in the venue string.
# First match wins, so put more specific entries first.
VENUE_MAP = [
    # Conferences
    ("CVPR",        "CVPR"),
    ("ICCV",        "ICCV"),
    ("ECCV",        "ECCV"),
    ("NeurIPS",     "NeurIPS"),
    ("NIPS",        "NeurIPS"),
    ("ICLR",        "ICLR"),
    ("AAAI",        "AAAI"),
    ("MICCAI",      "MICCAI"),
    ("ISBI",        "ISBI"),
    ("MIDL",        "MIDL"),
    ("IPMI",        "IPMI"),
    ("ACMMM",       "ACM MM"),
    ("ACM Multimedia", "ACM MM"),
    # NLP
    ("ACL",         "ACL"),
    ("EMNLP",       "EMNLP"),
    ("NAACL",       "NAACL"),
    ("COLING",      "COLING"),
    # Journals
    ("Medical Image Analysis",                  "MedIA"),
    ("IEEE Transactions on Medical Imaging",    "TMI"),
    ("Journal of Biomedical and Health Informatics", "JBHI"),
    ("JMIR",        "JMIR"),
    ("Pattern Recognition",  "PR"),
    ("Neurocomputing",       "Neurocomputing"),
    ("arXiv",       "arXiv"),
]

# ── URL-based venue inference (fallback when venue string is empty) ───────────
def infer_venue_from_url(url: str) -> str:
    if not url:
        return ""
    u = url.lower()
    if "arxiv.org" in u:
        return "arXiv"
    if "openaccess.thecvf.com" in u or "cvf.com" in u:
        if "iccv" in u:
            return "ICCV"
        if "eccv" in u:
            return "ECCV"
        return "CVPR"
    if "aclanthology.org" in u or "aclweb.org" in u:
        path = u
        if "naacl" in path:
            return "NAACL"
        if "emnlp" in path:
            return "EMNLP"
        if "coling" in path:
            return "COLING"
        return "ACL"
    if "link.springer.com" in u:
        if "978-3-030" in u or "978-3-031" in u:
            return "MICCAI"
    if "ieeexplore.ieee.org" in u:
        # ISBI paper IDs roughly 8500000–9098000 (2018-2021 era)
        m = re.search(r"document/(\d+)", u)
        if m:
            pid = int(m.group(1))
            if 8_500_000 <= pid <= 9_100_000:
                return "ISBI"
        return "IEEE"
    if "proceedings.mlr.press" in u:
        return "MIDL" if "midl" in u else "PMLR"
    if "openreview.net" in u:
        return "ICLR"
    return ""


def venue_abbr(venue_str: str, url: str) -> str:
    if venue_str:
        v = venue_str
        for keyword, abbr in VENUE_MAP:
            if keyword.lower() in v.lower():
                return abbr
    # Fall back to URL inference
    return infer_venue_from_url(url)


# ── Fetch from Google Scholar ─────────────────────────────────────────────────
def fetch(scholar_id: str) -> list[dict]:
    from scholarly import scholarly

    print(f"Fetching author profile: {scholar_id}")
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["publications"])

    pubs = []
    total = len(author["publications"])
    print(f"Found {total} publications. Fetching details (this takes ~{total*1.5//60:.0f} min)…")

    for i, pub in enumerate(author["publications"], 1):
        try:
            filled = scholarly.fill(pub)
            bib = filled.get("bib", {})

            title   = bib.get("title", "").strip()
            authors = bib.get("author", "").strip()
            year    = str(bib.get("pub_year", "")).strip()
            venue   = (bib.get("journal") or bib.get("booktitle") or "").strip()
            url     = filled.get("pub_url", "") or ""

            if title:
                abbr = venue_abbr(venue, url)
                pubs.append({
                    "title":      title,
                    "authors":    authors,
                    "year":       year,
                    "venue":      venue,
                    "venue_abbr": abbr,
                    "url":        url,
                })
            print(f"  [{i}/{total}] {title[:70]}")
            time.sleep(1.5)  # polite delay

        except Exception as e:
            print(f"  [{i}/{total}] WARNING: {e}", file=sys.stderr)
            bib = pub.get("bib", {})
            title = bib.get("title", "").strip()
            if title:
                venue = (bib.get("journal") or bib.get("booktitle") or "").strip()
                pubs.append({
                    "title":      title,
                    "authors":    bib.get("author", "").strip(),
                    "year":       str(bib.get("pub_year", "")),
                    "venue":      venue,
                    "venue_abbr": venue_abbr(venue, ""),
                    "url":        "",
                })

    pubs.sort(key=lambda p: p.get("year") or "0", reverse=True)
    return pubs


# ── Manual overrides (applied after fetch) ────────────────────────────────────
# Add entries here if scholarly mis-classifies a paper's venue.
OVERRIDES: dict[str, dict] = {
    # "Exact paper title": {"venue_abbr": "TMI"},
}

def apply_overrides(pubs: list[dict]) -> list[dict]:
    for p in pubs:
        fix = OVERRIDES.get(p["title"])
        if fix:
            p.update(fix)
    return pubs


if __name__ == "__main__":
    try:
        pubs = fetch(SCHOLAR_ID)
        pubs = apply_overrides(pubs)
        OUTPUT.write_text(json.dumps(pubs, ensure_ascii=False, indent=2))
        print(f"\nWrote {len(pubs)} publications → {OUTPUT}")
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
