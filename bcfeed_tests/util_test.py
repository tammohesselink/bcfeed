from bcfeed.util import parse_text_date
import datetime
import pytest


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("released January 16, 2026", datetime.date(2026, 1, 16)),
        ("January 16, 2026", datetime.date(2026, 1, 16)),
        ("released December 31, 2025", datetime.date(2025, 12, 31)),
        ("December 31, 2025", datetime.date(2025, 12, 31)),
        ("released March 5, 2024", datetime.date(2024, 3, 5)),
        ("  released January 16, 2026  ", datetime.date(2026, 1, 16)),
        ("  January 16, 2026  ", datetime.date(2026, 1, 16)),
        ("released February 29, 2024", datetime.date(2024, 2, 29)),
        ("", None),
        ("invalid date", None),
        ("released invalid", None),
        ("January 32, 2026", None),
        ("released February 30, 2025", None),
    ],
)
def test_parse_text_date(input_text, expected):
    assert parse_text_date(input_text) == expected