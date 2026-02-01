from bcfeed.gmail import scrape_info_from_email, EmailReleaseInfo


def create_bandcamp_email(
    page_name: str,
    release_title: str,
    release_url: str,
    release_type: str,
    artist_name: str | None = None,
    img_url: str = "https://example.com/img/cover.jpg",
):
    """
    Create a mock Bandcamp release notification email.

    Args:
        page_name: The Bandcamp page name (e.g., "testartist")
        release_title: The title of the release
        release_url: The Bandcamp URL for the release
        release_type: Either "album" or "track"
        artist_name: Optional artist name (for "by Artist" syntax)
        img_url: URL of the cover art
    """
    username = "testuser"
    band_id = "1234567890"
    fan_id = "9876543"
    sig = "abcdef1234567890"
    email_address = "user%40example.com"

    release_phrase = (
        f'just released <span style="font-style: italic;">{release_title}</span>'
    )
    if artist_name:
        release_phrase += f" by {artist_name}"

    from_param = "fanpub_fnb_trk" if release_type == "track" else "fanpub_fnb"
    utm_content = from_param
    utm_campaign = (
        f"{page_name}+{release_type}+{release_title.lower().replace(' ', '-')}"
    )

    release_link = f"{release_url}?from={from_param}&amp;utm_source={release_type}_release&amp;utm_medium=email&amp;utm_content={utm_content}&amp;utm_campaign={utm_campaign}"

    return f"""Delivered-To: user@example.com
Received: by example.server.com with SMTP id test123;
        Sat, 01 Feb 2026 12:00:00 -0800 (PST)
From: Bandcamp <noreply@bandcamp.com>
Subject: New release from {page_name}
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="it_was_only_a_kiss"
Message-ID: <test@example.com>
Reply-To: noreply@bandcamp.com
Date: Sat, 01 Feb 2026 12:00:00 +0000 (UTC)
To: {username} <user@example.com>

--it_was_only_a_kiss
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit


Greetings {username},

{page_name} just released "{release_title}"{f" by {artist_name}" if artist_name else ""}, check it out at:

{release_url}?from={from_param}







Enjoy!




Unfollow {page_name} by visiting:

https://{page_name}.bandcamp.com/fan_unsubscribe?band_id={band_id}&email={email_address}&fan_id={fan_id}&sig={sig}





--it_was_only_a_kiss
Content-Type: text/html; charset=us-ascii
Content-Transfer-Encoding: 7bit

<div id="msg" style="color:#595959;font-family: 'Helvetica Neue',arial,verdana,sans-serif;line-height:150%;padding:0;font-size:14px">

<div style="width:210px;min-height:210px;margin-bottom: 20px;">
    <a href="{release_link}">
        <img style="width:210px;min-height:210px;" src="{img_url}" alt="{release_title} Cover Art">
    </a>
</div>

Greetings {username},
<br>
{page_name} {release_phrase}, <a href="{release_link}" style="color:#0687f5;text-decoration:none;" >check it out here</a>.



    <br><br>
    Enjoy!

<br><br>
<a href="https://bandcamp.com"><img src="https://bandcamp.com/img/email/bc-logo-small-2.gif" width="105" height="19" border="0" alt="bandcamp logo"></a><br/>

<br>
<span style="font-size:11px;border-top:1px dotted #ccc;width:95%;display:block;padding:1em 0;margin:1em 0 0;"><a style="color:#999;text-decoration:none;font-size:11px;" href="https://{page_name}.bandcamp.com/fan_unsubscribe?band_id={band_id}&amp;email={email_address}&amp;fan_id={fan_id}&amp;sig={sig}">Unfollow {page_name}</a></span>
<br>&nbsp;

</div>


--it_was_only_a_kiss--
"""


album_email = create_bandcamp_email(
    page_name="testartist",
    release_title="Test Album",
    release_url="https://testartist.bandcamp.com/album/test-album",
    release_type="album",
)

track_email = create_bandcamp_email(
    page_name="testpage",
    release_title="Test Track",
    release_url="https://testpage.bandcamp.com/track/test-track",
    release_type="track",
    artist_name="Test Artist",
)


def test_scrape_info_from_email_album():
    res = scrape_info_from_email(album_email)
    assert isinstance(res, EmailReleaseInfo)
    assert res.is_track is False


def test_scrape_info_from_email_track():
    res = scrape_info_from_email(track_email)
    assert isinstance(res, EmailReleaseInfo)
    assert res.is_track is True
