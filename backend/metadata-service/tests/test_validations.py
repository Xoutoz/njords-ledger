"""Test all input validations"""


from tests.constants import (
    CATEGORY_INPUT_JSON,
    CATEGORY_NAME,
    SUBSCRIPTION_ID,
    SUBSCRIPTION_JSON,
    SUBSCRIPTION_ALL_REQUIRED_JSON,
    INVALID_CATEGORY,
    INVALID_CATEGORY_JSON,
    INVALID_SUBSCRIPTION,
    INVALID_SUBSCRIPTION_JSON
)
from metadata.validations import (
    is_category_valid,
    is_subscription_valid
)


def test_is_category_string_valid():
    assert is_category_valid(CATEGORY_NAME)


def test_is_category_json_valid():
    assert is_category_valid(CATEGORY_INPUT_JSON)


def test_is_category_string_invalid():
    assert not is_category_valid(INVALID_CATEGORY)


def test_is_category_json_invalid():
    assert not is_category_valid(INVALID_CATEGORY_JSON)


def test_is_subscription_string_valid():
    assert is_subscription_valid(SUBSCRIPTION_ID)


def test_is_subscription_all_required_json_valid():
    assert is_subscription_valid(SUBSCRIPTION_ALL_REQUIRED_JSON, is_all_required=True)


def test_is_subscription_all_required_json_invalid():
    assert not is_subscription_valid(SUBSCRIPTION_JSON, is_all_required=True)


def test_is_subscription_json_valid():
    for json in SUBSCRIPTION_JSON:
        assert is_subscription_valid(json, is_all_required=False)


def test_is_subscription_json_invalid():
    assert not is_subscription_valid(INVALID_SUBSCRIPTION_JSON, is_all_required=False)


def test_is_subscription_string_invalid():
    assert not is_subscription_valid(INVALID_SUBSCRIPTION)
