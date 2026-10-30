# Google SERP API

[![ci](https://github.com/quantumproxies/google-serp-api/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/google-serp-api/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Google search results as structured JSON, from Python or the command line: organic results with the AI Overview and related searches, Google News, Google Images, local places, autocomplete suggestions and Google Trends. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no Google API key to request and no proxy pool to maintain: sign in once and run a query.

```bash
pip install git+https://github.com/quantumproxies/google-serp-api
google-serp login
google-serp search "best usb c hub for macbook" --country us --num 20 -o serp.json
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `google-serp search` | query | Rank, title, link, snippet, date, sitelinks, 9 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api)) | up to 100 |
| `google-serp news` | topic | Title, publisher, date, snippet, link, 6 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api)) | up to 100 |
| `google-serp images` | query | Title, thumbnail, source page, host, 5 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api)) | up to 100 |
| `google-serp places` | business type + --location | Name, rating, reviews, category, address, phone, website, coordinates, hours, 15 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api)) | 20 per page, more with --page |
| `google-serp autocomplete` | seed query | Suggestion, relevance score, type, 4 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api)) | the whole suggestion list |
| `google-serp trends` | keyword | Date, interest value (0 to 100), 4 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api)) | one year of weekly values |

Any country and language: `--country us --lang en`, `--country de --lang de`. `--location "Milan, Italy"` returns the page a searcher in that city sees.

## Sample output

A real row from `google-serp search "best usb c hub for macbook" --country us --lang en --num 10` (2026-10-22):

```json
{
  "rank": 1,
  "title": "Best USB-C hubs and dongles: Add ports to your laptop or tablet",
  "link": "https://www.pcworld.com/article/402858/the-best-usb-c-hubs-for-your-laptop-tablet-or-2-in-1.html",
  "display_link": "www.pcworld.com › Accessories › Computer Accessories",
  "source": "pcworld.com",
  "description": "Anker 555 8-in-1 USB-C Hub Best overall USB-C hub. Excellent build quality Supplies 85W of power Good mix of ports. USB-C is common among Macs, ...",
  "date": "Oct 7, 2026"
}
```

That is one entry of `organic`. With `-o results.json` you get the whole response, which also carries `search_metadata`, `search_parameters`, `related_searches`, `ai_overview`, `pagination`.

## Python

```python
from quanticdata_google_serp_api import GoogleSERP

serp = GoogleSERP()  # saved login, or QUANTICDATA_API_KEY

result = serp.search("best usb c hub for macbook", country="us", num=20)
for r in result:
    print(r["rank"], r["source"], r["title"])
print(result.meta.get("ai_overview"))
print([q["query"] for q in result.meta.get("related_searches", [])])

news = serp.news("electric vehicles", country="us")
shops = serp.places("coffee shop", location="Austin, Texas, United States")
ideas = serp.autocomplete("google serp")
interest = serp.trends("air fryer", country="us")
interest.to_csv("air_fryer_trend.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Rank tracking**: Record where a domain ranks for a list of keywords, per country, and append the positions to a CSV every day. See [`examples/rank_tracker.py`](examples/rank_tracker.py).
- **AI Overview monitoring**: See which of your keywords trigger an AI Overview and keep its text, to follow how Google answers your topics. See [`examples/ai_overview_watch.py`](examples/ai_overview_watch.py).
- **Trend research**: Weekly Google Trends interest for a list of keywords in one long-format CSV, ready for a chart. See [`examples/trends_to_csv.py`](examples/trends_to_csv.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). With `-o results.json` you get the whole API response; the table, CSV and JSONL views hold its main list.

### `google-serp search`

Google web results for a query: organic results with rank, title, link, snippet and date, plus the AI Overview, related searches and pagination when Google shows them.

```
google-serp search QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search, e.g. "best usb c hub for macbook". |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |
| `--location` | string |  | Search from this place, e.g. "Milan, Italy": the results a searcher there sees. |
| `--device` | desktop / mobile | `desktop` | Desktop or mobile results page. |
| `--num` | integer |  | How many organic results to collect, 1 to 100; Google serves about 10 per page and the pages are merged. |
| `--page` | integer |  | Result page, 1-based. |
| `--safe` | active / off |  | SafeSearch. |

Sent with every call: `engine=google`, `search_type=search`.

### `google-serp news`

Google News results for a query: title, publisher, how long ago, snippet and link.

```
google-serp news QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Topic to search in Google News, e.g. "electric vehicles". |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |
| `--location` | string |  | Search from this place, e.g. "Milan, Italy": the results a searcher there sees. |
| `--num` | integer |  | Results to request (clamped to 1–100 by the service; Google serves ~10 per page and merges pages — see `search_metadata.paging`). |
| `--page` | integer |  | Result page, 1-based. |

Sent with every call: `engine=google`, `search_type=news`.

### `google-serp images`

Google Images results for a query: thumbnail, the page that uses the image and its host.

```
google-serp images QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search in Google Images. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |
| `--num` | integer |  | Results to request (clamped to 1–100 by the service; Google serves ~10 per page and merges pages — see `search_metadata.paging`). |
| `--page` | integer |  | Result page, 1-based. |
| `--safe` | active / off |  | SafeSearch. |

Sent with every call: `engine=google`, `search_type=images`.

### `google-serp places`

Local results for a query in a place: name, rating, review count, category, address, phone, website, coordinates, opening hours and the place id.

```
google-serp places QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Business type or name, e.g. "coffee shop"; set the place with --location. |
| `--location` | string |  | Where to search, as a place name, e.g. "Austin, Texas, United States". |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |
| `--num` | integer |  | Results to request (clamped to 1–100 by the service; Google serves ~10 per page and merges pages — see `search_metadata.paging`). |
| `--page` | integer |  | Result page, 1-based. |
| `--gps-coordinates` | string |  | `maps`/`places`: map center `lat,lon[,zoom]`. Wins over `uule` and `location`. |

Sent with every call: `engine=google`, `search_type=places`.

### `google-serp autocomplete`

The suggestions Google offers while typing a seed query, with Google's own relevance score: real searches people make, for keyword research.

```
google-serp autocomplete QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Seed query whose suggestions you want, e.g. "google serp". |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |

Sent with every call: `engine=google`, `search_type=autocomplete`.

### `google-serp trends`

Google Trends for a keyword: interest over time for the last 12 months (0 to 100), plus the top and rising related queries in the full response.

```
google-serp trends QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Keyword to read in Google Trends, e.g. "air fryer". |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |

Sent with every call: `engine=google`, `search_type=trends`.

## Output fields

<details><summary><code>google-serp search</code>: 9 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position on the results page, 1-based. |
| `title` | string | Result title. |
| `link` | string | Target URL. |
| `display_link` | string | Breadcrumb shown under the title. |
| `source` | string | Domain of the result. |
| `description` | string | Snippet shown under the title. |
| `date` | string or null | Date shown in the snippet, when present. |
| `rating` | number or null | Star rating shown in the snippet, when present. |
| `reviews` | integer or null | Review count shown with the rating. |

</details>

<details><summary><code>google-serp news</code>: 6 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in the news results. |
| `title` | string | Headline. |
| `link` | string | Article URL. |
| `source` | string | Publisher. |
| `date` | string | Age or date as shown ("20 hours ago"). |
| `description` | string | Snippet, when Google shows one. |

</details>

<details><summary><code>google-serp images</code>: 5 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in the image grid. |
| `title` | string | Caption as shown in the grid. |
| `thumbnail` | string | Thumbnail URL. |
| `source` | string | Host of the page that uses the image. |
| `source_url` | string | Page that uses the image. |

</details>

<details><summary><code>google-serp places</code>: 15 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in the local results. |
| `name` | string | Business name. |
| `rating` | number | Star rating. |
| `reviews` | integer | Review count. |
| `category` | string | Main category. |
| `address` | string | Address as shown. |
| `website` | string | Website host, when listed. |
| `link` | string | Google Maps link. |
| `gps_coordinates` | object | { latitude, longitude }. |
| `place_id` | string | Place id, the input of place details and reviews. |
| `data_id` | string | Same id in the form the reviews call takes. |
| `weekly_hours` | object or null | Opening hours per weekday. |
| `open_state` | string | Open or closed now, as shown. |
| `phone` | string or null | Phone number, when listed. |
| `description` | string or null | Short description, when Google has one. |

</details>

<details><summary><code>google-serp autocomplete</code>: 4 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Order in the suggestion list. |
| `value` | string | The suggested query. |
| `relevance` | integer | Google's relevance score for the suggestion. |
| `type` | string | Suggestion kind (QUERY for a plain query). |

</details>

<details><summary><code>google-serp trends</code>: 4 fields</summary>

| Field | Type | Description |
|---|---|---|
| `date` | string | Week as shown by Google Trends. |
| `timestamp` | integer | Start of the week, Unix seconds. |
| `value` | integer | Interest, 0 to 100 relative to the peak of the period. |
| `partial` | boolean or null | True for the current, incomplete week. |

</details>

## Sign-in and API keys

- `google-serp login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `google-serp login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `google-serp login --api-key`.
- `google-serp logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Searches are billed to your QuanticData account per call, at the price shown on the SERP API page linked above; $2 of usage is free every month and failed calls are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/serp \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"engine": "google", "search_type": "search", "query": "best usb c hub for macbook", "country": "us", "lang": "en", "num": 10}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Google SERP API free?**

The code is free and MIT-licensed. Searches run on your QuanticData account: $2 of usage is free every month with no card, then you pay per search at the price on the SERP API page. Failed calls are never billed.

**Do I need a Google API key or proxies?**

No. There is no Google Cloud project, no Custom Search key and no proxy to configure: you send a query and get the parsed results page back.

**Does it return the AI Overview?**

Yes, when Google shows one for the query: it is in the ai_overview field of the full response (-o results.json in the CLI, result.meta in Python).

**How many results can one search return?**

Up to 100 organic results with --num; Google serves about 10 per page and the pages are fetched and merged for you. Use --page to address one specific page.

**Can I search from a specific country or city?**

Yes: --country and --lang set the Google market and language, and --location "Milan, Italy" returns the results a searcher in that city sees.

**Can I export to CSV?**

Add -o results.csv for the main list (organic results, news, images, places, suggestions or the Trends series); -o results.json keeps the whole response.

## Related scrapers

- [Google Maps Scraper](https://github.com/quantumproxies/google-maps-scraper): Google Maps scraper for Python and the command line.
- [YouTube Scraper](https://github.com/quantumproxies/youtube-scraper): YouTube scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=google-serp-api).
