import datetime
from email.utils import parsedate_to_datetime


def parse_date(val, *, allow_none: bool = False) -> datetime.date | None:
    """Parse an ISO (YYYY-MM-DD) or RFC 2822 date string into a date."""
    if val is None:
        if allow_none:
            return None
        raise ValueError("Missing date")
    if isinstance(val, datetime.datetime):
        return val.date()
    if isinstance(val, datetime.date):
        return val
    if isinstance(val, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.datetime.strptime(val, fmt).date()
            except ValueError:
                continue
        try:
            parsed = parsedate_to_datetime(val)
            if parsed is not None:
                return parsed.date()
        except (TypeError, ValueError, IndexError):
            pass
    if allow_none:
        return None
    raise ValueError("Incorrect date format, should be YYYY-MM-DD or RFC 2822 date")


def construct_release(is_track=None, release_url=None, date=None, img_url=None, artist_name=None, release_title=None, page_name=None, release_id=None):
    release = {}
    release['img_url'] = img_url
    release['date'] = date
    release['artist'] = artist_name
    release['title'] = release_title
    release['page_name'] = page_name
    release['url'] = release_url
    release['release_id'] = release_id
    release['is_track'] = is_track
    return release
