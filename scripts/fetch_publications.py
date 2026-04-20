#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and write publications.json.
Runs as a GitHub Action (see .github/workflows/fetch-publications.yml).
"""

import json
import sys
import time
from pathlib import Path

SCHOLAR_ID = "30e95fEAAAAJ"
OUTPUT = Path(__file__).parent.parent / "publications.json"


def fetch(scholar_id: str) -> list[dict]:
    from scholarly import scholarly

    print(f"Fetching author profile: {scholar_id}")
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["publications"])

    pubs = []
    total = len(author["publications"])
    print(f"Found {total} publications. Fetching details...")

    for i, pub in enumerate(author["publications"], 1):
        try:
            filled = scholarly.fill(pub)
            bib = filled.get("bib", {})

            title   = bib.get("title", "").strip()
            authors = bib.get("author", "").strip()
            year    = str(bib.get("pub_year", "")).strip()
            venue   = (bib.get("journal") or bib.get("booktitle") or "").strip()
            url     = filled.get("pub_url", "") or ""
            cites   = filled.get("num_citations", 0) or 0

            if title:
                pubs.append({
                    "title":   title,
                    "authors": authors,
                    "year":    year,
                    "venue":   venue,
                    "url":     url,
                    "citations": cites,
                })
            print(f"  [{i}/{total}] {title[:60]}...")

            # polite delay to avoid rate-limiting
            time.sleep(1.5)

        except Exception as e:
            print(f"  [{i}/{total}] WARNING: could not fill pub – {e}", file=sys.stderr)
            # still include what we have from the stub
            bib = pub.get("bib", {})
            title = bib.get("title", "").strip()
            if title:
                pubs.append({
                    "title":   title,
                    "authors": bib.get("author", "").strip(),
                    "year":    str(bib.get("pub_year", "")),
                    "venue":   (bib.get("journal") or bib.get("booktitle") or "").strip(),
                    "url":     "",
                    "citations": pub.get("num_citations", 0) or 0,
                })

    # Sort newest first; unknown year goes to bottom
    pubs.sort(key=lambda p: p["year"] or "0", reverse=True)
    return pubs


if __name__ == "__main__":
    try:
        pubs = fetch(SCHOLAR_ID)
        OUTPUT.write_text(json.dumps(pubs, ensure_ascii=False, indent=2))
        print(f"\nWrote {len(pubs)} publications → {OUTPUT}")
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
