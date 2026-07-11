# -*- coding: utf-8 -*-
"""
tests/test_login.py

Data-driven login tests. Test data comes from data/login_data.csv
(and the same data also exists in data/login_data.xlsx to demonstrate
reading from Excel too - see test_login_from_excel below).

These tests intentionally use the plain `page` fixture (NOT
`authenticated_page`) because they are testing the login flow itself.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data_reader import read_csv_data, read_excel_data, as_parametrize_tuples

KEYS = ["username", "password", "expected_result"]

csv_rows = read_csv_data("data/login_data.csv")
csv_cases = as_parametrize_tuples(csv_rows, KEYS)


@pytest.mark.parametrize("username,password,expected_result", csv_cases)
def test_login_scenarios_from_csv(page, config, username, password, expected_result):
    login_page = LoginPage(page, config["base_url"]).open()
    login_page.login(username, password)

    if expected_result == "success":
        inventory_page = InventoryPage(page, config["base_url"])
        inventory_page.expect_page_loaded()
    else:
        login_page.expect_login_error(expected_result)


# ---------------------------------------------------------------------
# Same scenarios, this time sourced from the Excel file - proves the
# framework is not tied to one data format.
# ---------------------------------------------------------------------
excel_rows = read_excel_data("data/login_data.xlsx")
excel_cases = as_parametrize_tuples(excel_rows, KEYS)


@pytest.mark.parametrize("username,password,expected_result", excel_cases)
def test_login_scenarios_from_excel(page, config, username, password, expected_result):
    login_page = LoginPage(page, config["base_url"]).open()
    login_page.login(username, password)

    if expected_result == "success":
        inventory_page = InventoryPage(page, config["base_url"])
        inventory_page.expect_page_loaded()
    else:
        login_page.expect_login_error(expected_result)
