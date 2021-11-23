"""Bible"""
__docformat__ = "numpy"
import os

import requests
from bs4 import BeautifulSoup

base = "https://api.scripture.api.bible/v1/bibles/"
version = "de4e12af7f28f599-02"
BIBLE_API_KEY = os.getenv("BIBLE_API_KEY")


def get_books():
    end = "/books"
    headers = {"api-key": BIBLE_API_KEY}
    data = requests.get(base + version + end, headers=headers)
    return data.json()["data"]


def get_chapters(book):
    end = f"/books/{book}/chapters"
    headers = {"api-key": BIBLE_API_KEY}
    data = requests.get(base + version + end, headers=headers)
    return data.json()["data"]


def get_verse(bookID, chapter, verse):
    end = f"/verses/{f'{bookID}.{chapter}.{verse}'}"
    headers = {"api-key": BIBLE_API_KEY}
    data = requests.get(base + version + end, headers=headers)
    soup = BeautifulSoup(data.json()["data"]["content"], "html.parser")
    return soup.text[len(verse) :]


def text_to_verse(text, *args):
    try:
        if "@sportsbot " in text:
            text = text.replace("@sportsbot ", "")
        text = text.replace("bible", "")
        books = get_books()
        book_list = [x["name"].lower() for x in books]
        book = " ".join(text.split()[:-1]).strip()
        index = book_list.index(book)
        nums = text.split()[-1].split(":")
        bid = books[index]["id"]
        return get_verse(bid, nums[0], nums[1])
    except BaseException:
        return "Could not find verse"
