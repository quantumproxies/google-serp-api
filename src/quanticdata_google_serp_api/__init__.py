"""Google SERP API: Google SERP API for Python and the command line: organic results with the AI Overview, news, images, local places, autocomplete and Google Trends as JSON or CSV. Free and open source; sign in with your QuanticData account, no Google API key or proxies needed.

    from quanticdata_google_serp_api import GoogleSERP

    scraper = GoogleSERP()   # saved login (`google-serp login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # Google organic results, AI Overview and related searches
    run = scraper.news(...)   # Google News articles for a topic
    run = scraper.images(...)   # Google Images results for a query
    run = scraper.places(...)   # local businesses from Google's local results
    run = scraper.autocomplete(...)   # Google autocomplete suggestions for a seed
    run = scraper.trends(...)   # Google Trends interest over time and related queries
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["GoogleSERP", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class GoogleSERP:
    """Google SERP API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="google-serp/0.1.0 (+https://github.com/quantumproxies/google-serp-api)", timeout=timeout)

    def search(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        location: Optional[str] = None,
        device: Optional[str] = None,
        num: Optional[int] = None,
        page: Optional[int] = None,
        safe: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """Google web results for a query: organic results with rank, title, link, snippet and date, plus the AI Overview, related searches and pagination when Google shows them.

        Args:
            query: What to search, e.g. "best usb c hub for macbook".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            location: Search from this place, e.g. "Milan, Italy": the results a searcher there sees.
            device: Desktop or mobile results page. One of: desktop, mobile.
            num: How many organic results to collect, 1 to 100; Google serves about 10 per page and the pages are merged.
            page: Result page, 1-based.
            safe: SafeSearch. One of: active, off.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``organic`` list (see ``types.SearchRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
            "location": location,
            "device": device,
            "num": num,
            "page": page,
            "safe": safe,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'search'}, **payload}, rows_key='organic', row_field='value', timeout=timeout)

    def news(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        location: Optional[str] = None,
        num: Optional[int] = None,
        page: Optional[int] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """Google News results for a query: title, publisher, how long ago, snippet and link.

        Args:
            query: Topic to search in Google News, e.g. "electric vehicles".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            location: Search from this place, e.g. "Milan, Italy": the results a searcher there sees.
            num: Results to request (clamped to 1–100 by the service; Google serves ~10 per page and merges pages — see `search_metadata.paging`).
            page: Result page, 1-based.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``news`` list (see ``types.NewsRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
            "location": location,
            "num": num,
            "page": page,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'news'}, **payload}, rows_key='news', row_field='value', timeout=timeout)

    def images(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        num: Optional[int] = None,
        page: Optional[int] = None,
        safe: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """Google Images results for a query: thumbnail, the page that uses the image and its host.

        Args:
            query: What to search in Google Images.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            num: Results to request (clamped to 1–100 by the service; Google serves ~10 per page and merges pages — see `search_metadata.paging`).
            page: Result page, 1-based.
            safe: SafeSearch. One of: active, off.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``images`` list (see ``types.ImagesRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
            "num": num,
            "page": page,
            "safe": safe,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'images'}, **payload}, rows_key='images', row_field='value', timeout=timeout)

    def places(
        self, query: str,
        *,
        location: Optional[str] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        num: Optional[int] = None,
        page: Optional[int] = None,
        gps_coordinates: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """Local results for a query in a place: name, rating, review count, category, address, phone, website, coordinates, opening hours and the place id.

        Args:
            query: Business type or name, e.g. "coffee shop"; set the place with --location.
            location: Where to search, as a place name, e.g. "Austin, Texas, United States".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            num: Results to request (clamped to 1–100 by the service; Google serves ~10 per page and merges pages — see `search_metadata.paging`).
            page: Result page, 1-based.
            gps_coordinates: `maps`/`places`: map center `lat,lon[,zoom]`. Wins over `uule` and `location`.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``places`` list (see ``types.PlacesRow``).
        """
        payload = {
            "query": query,
            "location": location,
            "country": country,
            "lang": lang,
            "num": num,
            "page": page,
            "gps_coordinates": gps_coordinates,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'places'}, **payload}, rows_key='places', row_field='value', timeout=timeout)

    def autocomplete(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """The suggestions Google offers while typing a seed query, with Google's own relevance score: real searches people make, for keyword research.

        Args:
            query: Seed query whose suggestions you want, e.g. "google serp".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``suggestions`` list (see ``types.AutocompleteRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'autocomplete'}, **payload}, rows_key='suggestions', row_field='value', timeout=timeout)

    def trends(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """Google Trends for a keyword: interest over time for the last 12 months (0 to 100), plus the top and rising related queries in the full response.

        Args:
            query: Keyword to read in Google Trends, e.g. "air fryer".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``trends.interest_over_time`` list (see ``types.TrendsRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'trends'}, **payload}, rows_key='trends.interest_over_time', row_field='value', timeout=timeout)
