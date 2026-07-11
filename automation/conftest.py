# -*- coding: utf-8 -*-
"""
conftest.py

Shared pytest fixtures for the whole framework.

Key fixtures:
  config              -> loads config/environments.yaml for the active ENV
  browser             -> one browser instance for the whole test session
  context              -> fresh, ISOLATED context per test (no login)
  page                 -> a page inside that fresh context
  authenticated_context -> context pre-loaded with a saved login session
  authenticated_page    -> a page inside the authenticated context
                           (this is what "Login Once, Reuse Login" tests use)
"""
# -*- coding: utf-8 -*-

import os
import pytest
from playwright.sync_api import sync_playwright

from utils.config_reader import get_config
from utils.auth_manager import ensure_logged_in
from utils.logger import get_logger

logger = get_logger(__name__)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

@pytest.fixture(scope="session")
def config():
    cfg = get_config()
    return cfg


# --------------------------------------------------
# Playwright
# --------------------------------------------------

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    browser_type = getattr(playwright_instance, config["browser"])

    browser = browser_type.launch(
        headless=config.get("headless", True)
    )

    yield browser

    browser.close()


# --------------------------------------------------
# Fresh Context
# --------------------------------------------------

@pytest.fixture
def context(browser, config):
    context = browser.new_context(
        viewport=config.get("viewport"),
        base_url=config["base_url"]
    )

    context.set_default_timeout(config["timeout_ms"])

    yield context

    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page


# --------------------------------------------------
# Login Once
# --------------------------------------------------

@pytest.fixture(scope="session")
def storage_state_path(browser, config):
    return ensure_logged_in(browser, config)


@pytest.fixture
def authenticated_context(browser, config, storage_state_path):

    context = browser.new_context(
        viewport=config.get("viewport"),
        base_url=config["base_url"],
        storage_state=storage_state_path
    )

    context.set_default_timeout(config["timeout_ms"])

    yield context

    context.close()


@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    yield page


# --------------------------------------------------
# Screenshot on failure
# --------------------------------------------------

@pytest.fixture(autouse=True)
def screenshot_on_failure(request):

    yield

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:

        page_fixture = None

        for fixture in ("page", "authenticated_page"):

            if fixture in request.fixturenames:
                page_fixture = request.getfixturevalue(fixture)
                break

        if page_fixture:

            os.makedirs("reports/screenshots", exist_ok=True)

            screenshot = f"reports/screenshots/{request.node.name}.png"

            page_fixture.screenshot(path=screenshot)

            logger.info(f"Screenshot saved: {screenshot}")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)
