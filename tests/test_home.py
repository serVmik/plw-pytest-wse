import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

HOST = os.getenv('HOST')


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    page.goto(HOST)
    yield


def test_title(page: Page) -> None:
    expect(page).to_have_title('Домашняя страница')
