import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

HOST = os.getenv('HOST')
URL_PATH = 'task/english-translate-choice/'
STATE_PATH = os.getenv('STATE_PATH')


@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'storage_state': STATE_PATH,
    }


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    # First, visit the task conditions page, the transition from which
    # sets the task conditions. Otherwise, there will be a redirect
    page.goto(urljoin(HOST, URL_PATH))
    page.get_by_test_id('submit').click()
    yield


def test_page_data(page: Page) -> None:
    expect(page).to_have_title('Упражнение "Изучаем слова"')
    headline = page.get_by_test_id('headline')
    expect(headline).to_have_text('Упражнение "Изучаем слова"')
