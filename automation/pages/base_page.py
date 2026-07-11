# -*- coding: utf-8 -*-
"""
pages/base_page.py

Common functionality shared by every Page Object. Real page classes
(LoginPage, InventoryPage, CartPage, ...) inherit from this.
"""
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = "/"):
        self.page.goto(self.base_url.rstrip("/") + path)

    def title(self) -> str:
        return self.page.title()

    def current_url(self) -> str:
        return self.page.url

    def screenshot(self, path: str):
        self.page.screenshot(path=path, full_page=True)
