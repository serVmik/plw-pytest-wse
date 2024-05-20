import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page, expect

load_dotenv()

HOST = os.getenv('HOST')
URL_PATH = 'task/math-calculate-choice/'
STATE_PATH = os.getenv('STATE_PATH')


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


def test_page_date(page: Page) -> None:
    expect(page).to_have_title('Условия задания')
    expect(page.get_by_test_id('headline')).to_have_text('Условия задания')


# TODO: check selected
def test_calculation_type_choice(page: Page) -> None:
    choices = ['Сложение', 'Вычитание', 'Умножение']
    choice_locator = page.locator('#div_id_calculation_type')

    expect(choice_locator.locator('label')).to_have_text('Вид вычисления*')
    expect(choice_locator.locator('option')).to_have_text(choices)


def test_timeout_choice(page: Page) -> None:
    choice_locator = page.get_by_text('Время на ответ (сек)*')
    expect(choice_locator).to_have_value('2')


def test_min_and_max_number_choice(page: Page) -> None:
    min_locator = page.get_by_text('Минимальное число*')
    max_locator = page.get_by_text('Максимальное число*')
    expect(min_locator).to_have_value('2')
    expect(max_locator).to_have_value('9')


def test_set_is_task_with_solution(page: Page) -> None:
    solution_locator = page.locator('#div_id_with_solution')
    expect(solution_locator.locator('label')).to_have_text('С вводом ответа')
    expect(solution_locator.locator('input')).not_to_be_checked()


def test_has_submit(page: Page) -> None:
    expect(page.locator('input[name="submit"]')).to_be_visible()
