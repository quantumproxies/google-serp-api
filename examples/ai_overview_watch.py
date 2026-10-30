"""Which keywords show a Google AI Overview, and what it says.

    python ai_overview_watch.py "best usb c hub" "what is a serp" --country us

Appends one JSON line per keyword to ai_overviews.jsonl: date, keyword,
whether an AI Overview was shown, its text, and the top 3 organic domains
under it. Run it weekly to see how Google answers your topics over time.
"""

import argparse
import json
from datetime import date

from quanticdata_google_serp_api import GoogleSERP


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--out", default="ai_overviews.jsonl")
    args = parser.parse_args()

    serp = GoogleSERP()
    with open(args.out, "a", encoding="utf-8") as fh:
        for keyword in args.keywords:
            result = serp.search(keyword, country=args.country, lang=args.lang)
            overview = result.meta.get("ai_overview")
            record = {
                "date": date.today().isoformat(),
                "keyword": keyword,
                "country": args.country,
                "ai_overview": bool(overview),
                "text": overview,
                "top_domains": [r.get("source") for r in result.rows[:3]],
            }
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"{keyword!r}: {'AI Overview' if overview else 'no AI Overview'}")


if __name__ == "__main__":
    main()
