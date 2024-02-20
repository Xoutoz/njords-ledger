"""Functions to validate request inputs."""

import re

from cerberus import Validator

from metadata.config import (
    BUDGET_DOCUMENT_SCHEMA,
    CATEGORY_DOCUMENT_SCHEMA,
    CATEGORY_REGEX,
    PREFERENCES_DOCUMENT_SCHEMA,
    SUBSCRIPTION_ID_REGEX,
    SUBSCRIPTION_SCHEMAS,
)


def is_category_valid(category: str | dict) -> bool:
    """Check whether the provided category is valid.

    Args:
        category: The category to validate.

    Returns
    -------
        bool: Whether the category is valid.
    """
    match category:
        case str():
            return re.match(CATEGORY_REGEX, category)
        case dict():
            validator = Validator(CATEGORY_DOCUMENT_SCHEMA)
            return validator.validate(category)
        case _:
            return False


def is_subscription_valid(
    subscription: str | dict, is_all_required: bool = False
) -> bool:
    """Verify whether the provided subscription is valid.

    Args:
        subscription (str | dict): Subscription to validate.
            If a string, it is assumed to be a subscription ID.
            If a dictionary, it is assumed to be a subscription object.

        is_all_required (bool): Whether all fields in the subscription object
            are required to be present and valid. Defaults to False.

    Returns
    -------
        bool: Whether the subscription is valid.
    """
    match subscription:
        case str():
            return re.match(SUBSCRIPTION_ID_REGEX, subscription)
        case dict():
            validator = Validator(SUBSCRIPTION_SCHEMAS)
            if is_all_required:
                validator.require_all = True
            return validator.validate(subscription) and any(
                key for key in subscription.keys()
            )
        case _:
            return False


def is_budget_valid(budget: dict) -> bool:
    """Validate a budget input.

    Args:
        budget (dict): The budget to validate.

    Returns
    -------
        bool: True if the budget is valid, False otherwise.
    """
    validator = Validator(BUDGET_DOCUMENT_SCHEMA)
    return validator.validate(budget)


def are_preferences_valid(preferences: dict) -> bool:
    """Validate the given preferences.

    Args:
        preferences (dict): The preferences dictionary to validate.

    Returns
    -------
        bool: True if the preferences are valid, False otherwise.
    """
    validator = Validator(PREFERENCES_DOCUMENT_SCHEMA)
    return validator.validate(preferences) and any(key for key in preferences.keys())
