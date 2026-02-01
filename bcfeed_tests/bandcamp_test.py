from bcfeed.bandcamp import build_embed_url, extract_bc_meta

def test_embed_url_for_album_():
    res = build_embed_url(445172539, False)
    assert res is not None
    assert res == "https://bandcamp.com/EmbeddedPlayer/album=1234567890/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=true/artwork=small/transparent=true/"


def test_embed_url_for_track():
    res = build_embed_url(3972831481, True)
    assert res is not None
    assert res == "https://bandcamp.com/EmbeddedPlayer/track=1234567890/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=true/artwork=small/transparent=true/"