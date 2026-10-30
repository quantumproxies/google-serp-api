"""Google Trends interest over time for several keywords, in one CSV.

    python trends_to_csv.py "air fryer" "slow cooker" "rice cooker" --country us

Each keyword is read separately (values are 0 to 100 relative to that
keyword's own peak), and the rows are written in long format: keyword, week,
value. Open it in a spreadsheet and pivot, or plot it with pandas.
"""

import argparse

from quanticdata_google_serp_api import GoogleSERP, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--out", default="trends.csv")
    args = parser.parse_args()

    serp = GoogleSERP()
    rows = []
    for keyword in args.keywords:
        series = serp.trends(keyword, country=args.country)
        rows.extend({"keyword": keyword, "week": p["date"], "value": p["value"],
                     "partial": bool(p.get("partial"))} for p in series)
        rising = (series.meta.get("trends") or {}).get("related_queries", {}).get("rising", [])
        print(f"{keyword!r}: {len(series)} weeks, rising: {', '.join(q['query'] for q in rising[:3])}")

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()
