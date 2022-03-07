#!/usr/bin/env python
"""Tests for `super_iterables` package."""
# pylint: disable=redefined-outer-name

import pytest
from super_iterables import superlist


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    del response


def test_superlist():
    assert superlist([1, 2, 3]).sort_by(lambda x: -x) == [3, 2, 1]
