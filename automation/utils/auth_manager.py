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
import os
from playwright.sync_api import sync_playwright
from utils.logger import get_logger

logger = get_logger(__name__)

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


def ensure_logged_in(config: dict, force_relogin: bool = False) -> str:
    """
    Ensures a valid storage_state file exists for this environment.
    Returns the path to the storage_state JSON file.
    """
    state_path = config["storage_state_path"]

    if os.path.exists(state_path) and not force_relogin:
        logger.info(f"Reusing existing session/storage state: {state_path}")
        return state_path

    logger.info("No saved session found - logging in once via the UI...")
    os.makedirs(os.path.dirname(state_path), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.get("headless", True))
        context = browser.new_context()
        page = context.new_page()

        page.goto(config["base_url"])
        page.locator("#user-name").fill(VALID_USER)
        page.locator("#password").fill(VALID_PASSWORD)
        page.locator("#login-button").click()

        # Confirm login succeeded before saving state
        page.wait_for_selector(".inventory_list", timeout=config.get("timeout_ms", 30000))

        # This is the key step: dump cookies + localStorage to disk
        context.storage_state(path=state_path)
        logger.info(f"Session saved to: {state_path}")

        browser.close()

    return state_path


def clear_saved_session(config: dict):
    """Deletes the saved storage_state file, forcing a fresh login next run."""
    state_path = config["storage_state_path"]
    if os.path.exists(state_path):
        os.remove(state_path)
        logger.info(f"Cleared saved session: {state_path}")
