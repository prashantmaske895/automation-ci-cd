# -*- coding: utf-8 -*-
"""
tests/test_session_reuse.py

A focused test that makes the "Login Once, Reuse Login" behavior
explicit and easy to point to in an interview: it inspects the actual
cookies restored from storage_state and confirms the session cookie
saucedemo relies on ("session-username") is present WITHOUT this test
ever calling login() itself.
"""
from pages.inventory_page import InventoryPage


def test_session_cookie_is_restored_from_storage_state(authenticated_context, authenticated_page, config):
    # Prove we never logged in during this test - just navigate directly.
    inventory_page = InventoryPage(authenticated_page, config["base_url"]).open_directly()
    inventory_page.expect_page_loaded()

    cookies = authenticated_context.cookies()
    cookie_names = [c["name"] for c in cookies]

    assert "session-username" in cookie_names, (
        "Expected the session cookie to already be present from the saved "
        "storage_state - this proves the login step was skipped entirely."
    )
