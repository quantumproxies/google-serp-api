"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class SearchRow(TypedDict, total=False):
    """One row of `google-serp search` (POST /v1/serp)."""

    rank: int
    """Position on the results page, 1-based."""
    title: str
    """Result title."""
    link: str
    """Target URL."""
    display_link: str
    """Breadcrumb shown under the title."""
    source: str
    """Domain of the result."""
    description: str
    """Snippet shown under the title."""
    date: Optional[str]
    """Date shown in the snippet, when present."""
    rating: Optional[float]
    """Star rating shown in the snippet, when present."""
    reviews: Optional[int]
    """Review count shown with the rating."""

class NewsRow(TypedDict, total=False):
    """One row of `google-serp news` (POST /v1/serp)."""

    rank: int
    """Position in the news results."""
    title: str
    """Headline."""
    link: str
    """Article URL."""
    source: str
    """Publisher."""
    date: str
    """Age or date as shown ("20 hours ago")."""
    description: str
    """Snippet, when Google shows one."""

class ImagesRow(TypedDict, total=False):
    """One row of `google-serp images` (POST /v1/serp)."""

    rank: int
    """Position in the image grid."""
    title: str
    """Caption as shown in the grid."""
    thumbnail: str
    """Thumbnail URL."""
    source: str
    """Host of the page that uses the image."""
    source_url: str
    """Page that uses the image."""

class PlacesRow(TypedDict, total=False):
    """One row of `google-serp places` (POST /v1/serp)."""

    rank: int
    """Position in the local results."""
    name: str
    """Business name."""
    rating: float
    """Star rating."""
    reviews: int
    """Review count."""
    category: str
    """Main category."""
    address: str
    """Address as shown."""
    website: str
    """Website host, when listed."""
    link: str
    """Google Maps link."""
    gps_coordinates: Dict[str, Any]
    """{ latitude, longitude }."""
    place_id: str
    """Place id, the input of place details and reviews."""
    data_id: str
    """Same id in the form the reviews call takes."""
    weekly_hours: Dict[str, Any]
    """Opening hours per weekday."""
    open_state: str
    """Open or closed now, as shown."""
    phone: Optional[str]
    """Phone number, when listed."""
    description: Optional[str]
    """Short description, when Google has one."""

class AutocompleteRow(TypedDict, total=False):
    """One row of `google-serp autocomplete` (POST /v1/serp)."""

    rank: int
    """Order in the suggestion list."""
    value: str
    """The suggested query."""
    relevance: int
    """Google's relevance score for the suggestion."""
    type: str
    """Suggestion kind (QUERY for a plain query)."""

class TrendsRow(TypedDict, total=False):
    """One row of `google-serp trends` (POST /v1/serp)."""

    date: str
    """Week as shown by Google Trends."""
    timestamp: int
    """Start of the week, Unix seconds."""
    value: int
    """Interest, 0 to 100 relative to the peak of the period."""
    partial: Optional[bool]
    """True for the current, incomplete week."""
