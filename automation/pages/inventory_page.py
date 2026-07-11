# -*- coding: utf-8 -*-
"""
pages/inventory_page.py

Page Object for the post-login product listing page on saucedemo.com.
Used to prove that a reused/stored session lands the user straight here
without going through the login form again.
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.inventory_list = page.locator(".inventory_list")
        self.page_title = page.locator(".title")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.product_names = page.locator(".inventory_item_name")

    def open_directly(self):
        """Navigate straight to the inventory URL - only works if already logged in."""
        self.goto("/inventory.html")
        return self

    def is_loaded(self) -> bool:
        return self.inventory_list.is_visible()

    def add_product_to_cart(self, product_name: str):
        card = self.page.locator(".inventory_item", has_text=product_name)
        card.get_by_role("button", name="Add to cart").click()
        return self

    def get_cart_count(self) -> str:
        return self.cart_badge.inner_text() if self.cart_badge.is_visible() else "0"

    def expect_page_loaded(self):
        expect(self.page_title).to_have_text("Products")
        expect(self.inventory_list).to_be_visible()
