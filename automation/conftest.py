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
import os
import pytest
from playwright.sync_api import sync_playwright

from utils.config_reader import get_config
from utils.auth_manager import ensure_logged_in
from utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Config - loaded once per test session
# ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def config():
    cfg = get_config()
    logger.info(f"Running against environment: {cfg['env_name']} ({cfg['base_url']})")
    return cfg


# ---------------------------------------------------------------------
# Browser - launched once, reused by every test (contexts give isolation)
# ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    browser_type = getattr(playwright_instance, config["browser"])
    browser = browser_type.launch(headless=config.get("headless", True))
    yield browser
    browser.close()


# ---------------------------------------------------------------------
# Plain (unauthenticated) context/page - use for login tests themselves,
# since those tests need to start at the login screen every time.
# ---------------------------------------------------------------------
@pytest.fixture
def context(browser, config):
    context = browser.new_context(
        viewport=config.get("viewport"),
        base_url=config["base_url"],
    )
    context.set_default_timeout(config.get("timeout_ms", 30000))
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page


# ---------------------------------------------------------------------
# Authenticated context/page - THIS is the "Login Once, Reuse Login" fixture.
# The first test in the session that needs it triggers a real UI login
# (via utils/auth_manager.ensure_logged_in), and the resulting storage_state
# file is then reused by every other test - no repeated UI logins.
# ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def storage_state_path(config):
    return ensure_logged_in(config)


@pytest.fixture
def authenticated_context(browser, config, storage_state_path):
    context = browser.new_context(
        viewport=config.get("viewport"),
        base_url=config["base_url"],
        storage_state=storage_state_path,   # <-- session restored here
    )
    context.set_default_timeout(config.get("timeout_ms", 30000))
    yield context
    context.close()


@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    yield page


# ---------------------------------------------------------------------
# Auto screenshot-on-failure - saved to reports/ for debugging CI runs
# ---------------------------------------------------------------------
@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        page_fixture = None
        for fixture_name in ("page", "authenticated_page"):
            if fixture_name in request.fixturenames:
                page_fixture = request.getfixturevalue(fixture_name)
                break
        if page_fixture:
            os.makedirs("reports/screenshots", exist_ok=True)
            path = f"reports/screenshots/{request.node.name}.png"
            page_fixture.screenshot(path=path, full_page=True)
            logger.info(f"Failure screenshot saved: {path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Makes the test result available to the screenshot_on_failure fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
