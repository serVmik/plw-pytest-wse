import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

HOST = os.getenv('HOST')
STATE_PATH = os.getenv('STATE_PATH')


@pytest.fixture(autouse=True)
def browser_context_args(browser_context_args) -> dict:
    """Reuse the signed-in state."""
    return {
        **browser_context_args,
        'storage_state': STATE_PATH,
    }


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    page.goto(HOST)
    yield


def test_title(page: Page) -> None:
    expect(page).to_have_title('Домашняя страница')


def test_home_page_links_to_site_pages(page: Page) -> None:
    links = {
        'Упражнение "Изучаем слова"': 'task/english-translate-choice/',
        'Добавить слово в словарь': 'english/word/create/',
    }
    for link_name, link_href in links.items():
        link = page.locator('a', has_text=link_name)
        expect(link).to_have_text(link_name)

        link.click()
        expect(page).to_have_title(link_name)
        expect(page.get_by_test_id('headline')).to_have_text(link_name)
        page.goto(HOST)
