import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

HOST = os.getenv('HOST')
NAVBAR = ['Английский язык', 'Математика', 'Регистрация', 'Войти']


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    page.goto(HOST)
    yield


def test_contains(page: Page) -> None:
    navbar = page.locator('.navbar-nav li')
    expect(navbar).to_have_count(4)
    expect(navbar).to_contain_text(NAVBAR)
