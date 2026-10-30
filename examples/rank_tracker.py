"""Daily Google rank tracking for one domain.

    python rank_tracker.py example.com --keywords keywords.txt --country us

For each keyword (one per line in keywords.txt) it reads the top 100 Google
results and appends the best position of the domain, or nothing when it is not
in the top 100, to ranks.csv with today's date. Run it once a day from cron.
"""

import argparse
import csv
import os
from datetime import date

from quanticdata_google_serp_api import GoogleSERP


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domain", help="e.g. example.com (subdomains count too)")
    parser.add_argument("--keywords", default="keywords.txt")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--out", default="ranks.csv")
    args = parser.parse_args()

    with open(args.keywords, encoding="utf-8") as fh:
        keywords = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    serp = GoogleSERP()
    domain = args.domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    new_file = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(["date", "country", "keyword", "position", "url"])
        for keyword in keywords:
            result = serp.search(keyword, country=args.country, lang=args.lang, num=100)
            hit = next((r for r in result if (r.get("source") or "").lower().endswith(domain)), None)
            writer.writerow([date.today().isoformat(), args.country, keyword,
                             hit["rank"] if hit else "", hit["link"] if hit else ""])
            print(f"{keyword!r}: {hit['rank'] if hit else 'not in top 100'}")


if __name__ == "__main__":
    main()
