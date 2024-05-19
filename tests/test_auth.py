import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, Page

load_dotenv()

HOST = os.getenv('HOST')
LOGIN_PATH = 'users/login/'
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')


@pytest.fixture(autouse=True)
def ruan_around_test(page: Page) -> Generator[None, None, None]:
    page.goto(HOST)
    yield


def test_user_authentication_page(page: Page):
    """Test user authentication page."""
    page.goto(urljoin(HOST, LOGIN_PATH))

    expect(page).to_have_title('Вход в приложение')

    page.locator('#id_username').fill(TEST_USERNAME)
    page.locator('#id_password').fill(TEST_USER_PASSWORD)
    page.get_by_role('button', name='Войти').click()

    expect(page).to_have_title('Домашняя страница')
