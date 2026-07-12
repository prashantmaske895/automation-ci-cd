# -*- coding: utf-8 -*-
"""
utils/auth_manager.py

Implements the "Login Once, Reuse Login" pattern using Playwright's
storage_state feature.

Flow:
  1. ensure_logged_in() checks whether a valid storage_state file already
     exists for the current environment.
  2. If not, it launches a real (temporary) browser, logs in through the
     UI exactly once, and saves the resulting cookies + local storage
     (the session) to a JSON file.
  3. Every test after that creates its browser context with
     storage_state=<that file>, which restores the cookies/session
     instantly - no UI login step needed.

This is what "Login Once, Reuse Login, Storage State, Cookies, Session"
means in practice.
"""
# -*- coding: utf-8 -*-

"""
Creates storage_state once and reuses it.
No nested sync_playwright() calls.
"""

import os
from utils.logger import get_logger

logger = get_logger(__name__)

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


def ensure_logged_in(browser, config, force_relogin=False):
    state_path = config["storage_state_path"]

    if os.path.exists(state_path) and not force_relogin:
        logger.info(f"Using existing storage state: {state_path}")
        return state_path

    logger.info("No session found. Logging in once...")

    os.makedirs(os.path.dirname(state_path), exist_ok=True)

    context = browser.new_context()
    page = context.new_page()

    page.goto(config["base_url"])

    page.locator("#user-name").fill(VALID_USER)
    page.locator("#password").fill(VALID_PASSWORD)
    page.locator("#login-button").click()

    page.wait_for_selector(".inventory_list")

    context.storage_state(path=state_path)

    logger.info(f"Storage state created at {state_path}")

    context.close()

    return state_path


def clear_saved_session(config):
    state_path = config["storage_state_path"]

    if os.path.exists(state_path):
        os.remove(state_path)
        logger.info("Old session removed")
