import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

HOST = os.getenv('HOST')
STATE_PATH = os.getenv('STATE_PATH')
NAVBAR = ['Личный кабинет: user3', 'Английский язык', 'Выйти']
NAVIGATION = {
    'Личный кабинет: user3': 'users/3/account/',
    'Английский язык': 'english/',
    'Выйти': 'users/logout/',
}


@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'storage_state': STATE_PATH,
    }


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    page.goto(HOST)
    yield


def test_contains(page: Page) -> None:
    """Test navbar contain."""
    navbar = page.locator('.navbar-nav li')
    expect(navbar).to_have_count(3)
    expect(navbar).to_contain_text(NAVBAR)


def test_navigation_links(page: Page) -> None:
    """Test navigation links."""
    for link_name in NAVBAR[:-2]:
        url = urljoin(HOST, NAVIGATION[link_name])
        page.goto(url)
        expect(page).to_have_url(url)
