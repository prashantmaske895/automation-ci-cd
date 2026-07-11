# -*- coding: utf-8 -*-
"""
tests/test_inventory.py

These tests use the `authenticated_page` fixture, which is backed by a
SAVED session (storage_state) instead of logging in through the UI.

The very first test in the run that needs authentication triggers exactly
ONE real UI login (see utils/auth_manager.ensure_logged_in), and every
test after that - in this file and any other file - reuses the same
saved cookies/local storage instantly.

Run tests/test_session_reuse.py alongside this file to see proof that
no second login happens.
"""
from pages.inventory_page import InventoryPage


def test_inventory_page_loads_without_login(authenticated_page, config):
    """
    Navigates straight to /inventory.html - if the saved session did NOT
    work, saucedemo would redirect back to the login page and this
    assertion would fail.
    """
    inventory_page = InventoryPage(authenticated_page, config["base_url"]).open_directly()
    inventory_page.expect_page_loaded()


def test_add_product_to_cart_with_reused_session(authenticated_page, config):
    inventory_page = InventoryPage(authenticated_page, config["base_url"]).open_directly()
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    assert inventory_page.get_cart_count() == "1"


def test_multiple_products_can_be_added(authenticated_page, config):
    inventory_page = InventoryPage(authenticated_page, config["base_url"]).open_directly()
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    assert inventory_page.get_cart_count() == "2"
