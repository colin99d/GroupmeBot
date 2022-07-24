import pytest
from bot import bible


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_get_books():
    books = bible.get_books()
    assert len(books) == 66


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_get_chapters():
    chapters = bible.get_chapters("JHN")
    assert len(chapters) == 22


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_get_verse():
    verse = bible.get_verse("JHN", "3", "16")
    assert "¶ For God so loved the world, that he gave his only" in verse


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_get_text_to_verse():
    verse = bible.text_to_verse(text="@sportsbot john 3:16")
    assert "¶ For God so loved the world, that he gave his only" in verse


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_get_text_to_verse_error():
    verse = bible.text_to_verse(text="@sportsbot jonah 3:16")
    assert verse == "Could not find verse"
