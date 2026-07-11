# -*- coding: utf-8 -*-
"""
pages/login_page.py

Page Object for https://www.saucedemo.com login page.
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator('[data-test="error"]')

    def open(self):
        self.goto("/")
        return self

    def login(self, username: str, password: str):
        # Fields are cleared first so this method is safe to call
        # multiple times in the same test (e.g. retry scenarios).
        self.username_input.fill(username or "")
        self.password_input.fill(password or "")
        self.login_button.click()
        return self

    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def expect_login_error(self, expected_text: str):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(expected_text)
