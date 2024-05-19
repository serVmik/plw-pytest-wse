import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect, BrowserContext

load_dotenv()

HOST = os.getenv('HOST')
URL_PATH = 'english/'
STATE_PATH = '/home/dev/projects/plw-pytest-wse/tests/.auth/state.json'
ENGLISH_CHAPTER_PATHS = {
    'Добавить слово в словарь': 'english/word/create/',
    'Список слов': 'english/word/list/',
    'Категории': 'english/categories/list/',
    'Источники': 'english/sources/list/',
}


@pytest.fixture()
def browser_context_args(browser_context_args: BrowserContext) -> dict:
    """Reuse the signed-in state."""
    return {
        **browser_context_args,
        'storage_state': STATE_PATH,
    }


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    """New browser page pytest-playwright fixture for a test."""
    page.goto(urljoin(HOST, URL_PATH))
    yield


def test_english_page_status(page: Page) -> None:
    assert page.goto(page.url).ok


def test_english_title(page: Page) -> None:
    expect(page).to_have_title('Английский язык')


def test_english_headline(page: Page) -> None:
    headline = page.get_by_test_id('headline')
    expect(headline).to_have_text('Английский язык')


def test_chapter_links(page: Page) -> None:
    chapters = page.locator('.list-unstyled li')
    expect(chapters).to_have_text(list(ENGLISH_CHAPTER_PATHS))
    assert chapters.count() == len(ENGLISH_CHAPTER_PATHS)


def test_goto_chapter_links(page: Page) -> None:
    for link_name, path in ENGLISH_CHAPTER_PATHS.items():
        url = urljoin(HOST, path)
        page.goto(url)
        expect(page).to_have_title(link_name)
        expect(page).to_have_url(url)
