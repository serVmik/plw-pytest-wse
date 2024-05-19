# English task conditions page test.

import os
from typing import Generator
from unittest import skip
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, BrowserContext, expect

load_dotenv()

HOST = os.getenv('HOST')
URL_PATH = 'task/english-translate-choice/'
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


def test_page_status(page: Page) -> None:
    assert page.goto(page.url).ok


def test_page_title(page: Page) -> None:
    expect(page).to_have_title('Упражнение "Изучаем слова"')


def test_english_headline(page: Page) -> None:
    headline = page.get_by_test_id('headline')
    expect(headline).to_have_text('Упражнение "Изучаем слова"')


@skip('TODO: add assertions')
def test_choice_favorite_words_for_english_task(page: Page) -> None:
    page.get_by_test_id('favorites').check()
    page.get_by_test_id('submit').click()


def test_choice_contains_language_order(page: Page) -> None:
    order_locator = page.get_by_test_id('language_order').locator('option')
    expect(order_locator).to_have_text(
        [
            'Перевод в случайном порядке',
            'Перевод с английского языка',
            'Перевод на английский язык',
        ]
    )


def test_choice_word_addition_period(page: Page) -> None:
    # Star period has choices.
    choices_start = [
        'Сегодня', 'Три дня назад', 'Неделя назад', 'Две недели назад',
        'Три недели назад', 'Четыре недели назад', 'Семь недель назад',
        'Три месяца назад', 'Шесть месяцев назад', 'Девять месяцев назад',
        'Добавлено'
    ]
    start_date_locator = page.locator("select[name='period_start_date']")
    expect(start_date_locator.locator('option')).to_have_text(choices_start)
    # Default selected "Добавлено".
    expect(start_date_locator).to_have_value('NC')
    expect(start_date_locator).not_to_have_value('DT')

    # End period has choices.
    choices_end = choices_start[:-1]
    end_date_locator = page.locator("select[name='period_end_date']")
    expect(end_date_locator.locator('option')).to_have_text(choices_end)
    # Default selected "Сегодня".
    expect(end_date_locator).to_have_value('DT')
    expect(end_date_locator).not_to_have_value('NC')


def test_choice_word_knowledge_assessment(page: Page) -> None:
    assessments = ['Изучаю', 'Повторяю', 'Проверяю', 'Знаю']

    checkbox = page.get_by_test_id('knowledge_assessment').locator('label')
    expect(checkbox).to_have_text(assessments)

    expect(checkbox.nth(0)).to_be_checked()
    expect(checkbox.nth(1)).not_to_be_checked()
    expect(checkbox.nth(2)).not_to_be_checked()
    expect(checkbox.nth(3)).not_to_be_checked()


def test_choice_timeout_default(page: Page):
    timeout_locator = page.get_by_text('Время на ответ (сек)')
    expect(timeout_locator).to_have_value('5')


def test_choice_word_count(page: Page):
    word_count = ['Слово', 'Словосочетание', 'Часть предложения', 'Предложение']

    legend = page.locator('#div_id_word_count legend')
    expect(legend).to_have_text('Слово, длина выражения')

    checkbox = page.get_by_test_id('word_count')
    expect(checkbox.locator('.form-check')).to_have_text(word_count)

    locator = checkbox.locator('input')
    expect(locator.nth(0)).to_be_checked()
    expect(locator.nth(1)).to_be_checked()
    expect(locator.nth(2)).not_to_be_checked()
    expect(locator.nth(3)).not_to_be_checked()
